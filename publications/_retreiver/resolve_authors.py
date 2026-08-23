"""Resolve nomes de autores de um artigo para um destino (perfil da equipe,
foto de coautor confirmado, ou ícone genérico), e monta o bloco "lista de
participantes com foto" para colar no template da publicação.

Não existe mais um perfil (.qmd) por coautor externo — Marcos decidiu que
isso gerava perfil demais pra gente que só apareceu numa citação. Em vez
disso:

  1. Já existe em people/*.qmd (equipe do laboratório)? Link pro perfil da
     pessoa no site. Se a gente já sabe o scholar_id dela por esta rodada
     e o perfil ainda não tem `scholar-id:` no front matter, adiciona (ver
     `_ensure_scholar_id`).
  2. Não é da equipe, mas o Google Scholar já confirma ela como coautora
     conhecida de alguém que a gente sincronizou (a caixa "Coautores" da
     barra lateral do perfil — ver google_scholar_scraper.scrape_author_profile,
     chave "coauthors")? Link direto pro Scholar dela, com a foto real
     baixada uma vez e guardada em coauthors/<scholar_id>.<ext>, indexada
     em coauthors/coauthors.json (scholar_id -> arquivo da foto). NÃO
     fazemos busca por nome no Scholar/Google pra tentar adivinhar quem é
     alguém sem essa confirmação — testado e descartado: o primeiro
     resultado de uma busca por nome pode ser a pessoa errada (mesmo nome,
     pessoa diferente), então só confiamos na confirmação que o próprio
     Scholar já dá.
  3. Nenhum dos dois: ícone de pessoa genérico (mesmo pra todo mundo nesse
     caso, sem tentar adivinhar avatar) e link pra uma busca no Google
     pelo nome — não temos identidade nenhuma confirmada pra essa pessoa.

Uso típico (depois que o google-scholar.py já rodou e te deu os nomes dos
coautores de um paper, e opcionalmente o scholar_id/foto de cada um a
partir da caixa "Coautores" do perfil sincronizado):

    from resolve_authors import resolve_author_ids, render_authors_block

    authors = [
        ("Marcos M. Raimundo", None, None),   # já existe em people/, ignorado
        ("Jorge Poco", "S_88vX4AAAAJ", "https://.../foto.jpg"),  # confirmado
        ("Alguém Desconhecido", None, None),  # cai no ícone genérico
    ]
    resolved = resolve_author_ids(authors)
    print(render_authors_block(resolved))
"""

import json
import re
import unicodedata
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
PEOPLE_DIR = ROOT / "people"
COAUTHORS_DIR = ROOT / "coauthors"
COAUTHORS_JSON = COAUTHORS_DIR / "coauthors.json"

TITLE_RE = re.compile(r'^title:\s*"([^"]+)"', re.MULTILINE)
IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".webp")


def slugify(name: str) -> str:
    n = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    n = n.lower().replace(".", "").replace("'", "")
    n = re.sub(r"[^a-z0-9]+", "-", n)
    return n.strip("-")


# Partículas comuns que aparecem ou somem entre a forma abreviada e a forma
# completa de um nome ("Jansen S. B. Pereira" vs. "Jansen Silva de Brito
# Pereira" — o "de" nem sempre vira uma inicial própria). Ignoradas ao
# montar as iniciais, senão contam como uma inicial a mais numa forma e não
# na outra, quebrando o casamento.
_NAME_PARTICLES = {"de", "da", "do", "dos", "das", "e", "van", "von", "der", "y"}


def _name_key(name: str) -> tuple[str, frozenset[str]] | None:
    """Normaliza um nome para (sobrenome, iniciais) — ex.: tanto "Marcos M.
    Raimundo" quanto "M. M. Raimundo" (forma abreviada comum em citações)
    viram ("raimundo", {"m"}). Usado para casar nomes de autor vindos do
    Semantic Scholar/Google Scholar (que citam de formas diferentes) com os
    perfis reais do site (que usam o nome completo).

    Limitação conhecida: dois sobrenomes iguais com as mesmas iniciais
    seriam tratados como a mesma pessoa. Para o tamanho do site (equipe +
    coautores conhecidos) o risco é baixo, mas revise author-ids gerados
    automaticamente antes de publicar."""
    parts = [p.strip(".,") for p in name.split() if p.strip(".,")]
    if not parts:
        return None
    last = parts[-1].lower()
    initial_tokens = []
    for p in parts[:-1]:
        if p.lower() in _NAME_PARTICLES:
            continue
        # "SB" (sem pontos/espaços separando as iniciais, como o Google
        # Scholar às vezes cita) precisa virar duas iniciais {"s", "b"}, não
        # uma só ("s") — senão "Jansen SB Pereira" não bate com "Jansen S.
        # B. Pereira" (perfil real, escrito por extenso com pontuação).
        if p.isupper() and len(p) > 1:
            initial_tokens.extend(p.lower())
        else:
            initial_tokens.append(p[0].lower())
    initials = frozenset(initial_tokens)
    return last, initials


def _query_name(name: str) -> str:
    """Simplifica um nome pra uso em `author:"..."` numa busca do Scholar:
    só primeiro e último token, sem iniciais do meio nem partículas. O
    operador author: do Scholar casa mal contra pontuação (testado ao
    vivo: 'author:"Jansen S. B. Pereira"' não achou nada, mesmo a pessoa
    tendo papers indexados) e fica exigente demais com nomes de muitos
    tokens combinados com um segundo author: — 'author:"Jansen Pereira"
    author:"Marcos Raimundo"' encontrou o paper certo, mas as formas com
    iniciais do meio (com ou sem pontuação) não encontraram nada. Mesma
    simplificação de sobrenome já usada por _name_key (só a última palavra
    conta como sobrenome)."""
    parts = [p.strip(".,") for p in name.split() if p.strip(".,") and p.strip(".,").lower() not in _NAME_PARTICLES]
    if not parts:
        return name
    if len(parts) == 1:
        return parts[0]
    return f"{parts[0]} {parts[-1]}"


# Nomes de citação que a heurística sobrenome+iniciais (_name_key) não
# consegue casar porque o Google Scholar cita a pessoa com o sobrenome
# truncado (falta um pedaço do nome do perfil) ou expandido (sobrenome
# materno a mais que o perfil não usa) — nesses casos o último token do
# nome citado nem aparece no perfil real, então nenhuma heurística de
# sobrenome ajuda. Mapeamento manual, confirmado à mão por Marcos; só entra
# aqui alguém já verificado como a mesma pessoa, pra não arriscar juntar
# duas pessoas diferentes por engano.
_KNOWN_ALIASES = {
    "arthur hendricks": "ahmoliveira",
    "juan david nieto garcia": "jdnieto",
}


def _index_by_name(directory: Path) -> dict[str, str]:
    """{nome_normalizado: slug} para cada *.qmd de nível único em directory,
    indexado por _name_key() (ver docstring) em vez do nome exato — assim
    "M. M. Raimundo" (citação) casa com "Marcos M. Raimundo" (perfil)."""
    index: dict[tuple[str, frozenset[str]], str] = {}
    if not directory.exists():
        return index
    for path in directory.glob("*.qmd"):
        if path.name == "index.qmd":
            continue
        match = TITLE_RE.search(path.read_text(encoding="utf-8"))
        if match:
            key = _name_key(match.group(1).strip())
            if key:
                index[key] = path.stem
    return index


def _find_image(directory: Path, slug: str) -> str | None:
    for ext in IMAGE_EXTS:
        if (directory / f"{slug}{ext}").exists():
            return f"{slug}{ext}"
    return None


def _download_photo(url: str, path: Path) -> bool:
    """Baixa a foto real de um coautor confirmado. Retorna False sem
    travar nada se der qualquer erro de rede — quem chama cai pro ícone
    genérico nesse caso."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            path.write_bytes(resp.read())
        return True
    except Exception:
        return False


SCHOLAR_ID_FIELD_RE = re.compile(r'^\s*-?\s*scholar-id:\s*"?([A-Za-z0-9_-]+)"?', re.MULTILINE)
FRONTMATTER_RE = re.compile(r"\A(---\n.*?\n---\n)", re.DOTALL)


def _read_scholar_id(path: Path) -> str | None:
    if not path.exists():
        return None
    match = SCHOLAR_ID_FIELD_RE.search(path.read_text(encoding="utf-8"))
    return match.group(1) if match else None


def _ensure_scholar_id(path: Path, scholar_id: str) -> bool:
    """Se path (people/<slug>.qmd) ainda não tem scholar-id: no front
    matter, adiciona como o primeiro item da lista "links:" (criando a
    lista se a pessoa ainda não tiver nenhum link). Retorna True se
    escreveu algo. Nunca sobrescreve um valor já existente (mesmo que
    diferente do que veio agora)."""
    text = path.read_text(encoding="utf-8")
    fm_match = FRONTMATTER_RE.match(text)
    if not fm_match or SCHOLAR_ID_FIELD_RE.search(fm_match.group(1)):
        return False

    frontmatter = fm_match.group(1)
    entry = f'  - scholar-id: "{scholar_id}"\n'
    links_key_match = re.search(r"^links:\s*\n", frontmatter, re.MULTILINE)
    if links_key_match:
        insert_at = links_key_match.end()
        new_frontmatter = frontmatter[:insert_at] + entry + frontmatter[insert_at:]
    else:
        new_frontmatter = frontmatter[:-4] + "links:\n" + entry + "---\n"

    path.write_text(new_frontmatter + text[fm_match.end():], encoding="utf-8")
    return True


def load_coauthors_registry() -> dict[str, dict]:
    """{scholar_id: {"name", "photo"}} — coautores externos (não são da
    equipe) já confirmados pelo Google Scholar (caixa "Coautores" de
    algum perfil sincronizado), com a foto real já baixada em
    coauthors/<photo>."""
    if not COAUTHORS_JSON.exists():
        return {}
    return json.loads(COAUTHORS_JSON.read_text(encoding="utf-8"))


def _save_coauthors_registry(registry: dict[str, dict]) -> None:
    COAUTHORS_DIR.mkdir(exist_ok=True)
    COAUTHORS_JSON.write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8")


def _find_coauthor_by_name(name: str, registry: dict[str, dict]) -> str | None:
    """Devolve o scholar_id já registrado pra esse nome, se algum bater
    por _name_key() (mesma heurística sobrenome+iniciais de sempre)."""
    key = _name_key(name)
    if key is None:
        return None
    for scholar_id, entry in registry.items():
        if _name_key(entry.get("name", "")) == key:
            return scholar_id
    return None


def _register_coauthor(scholar_id: str, name: str, photo_url: str | None, registry: dict[str, dict]) -> dict:
    """Garante uma entrada em coauthors.json pra esse scholar_id — baixa a
    foto se ainda não tiver e um photo_url foi dado. Retorna a entrada
    (pode não ter "photo" se o download falhar ou não tiver photo_url)."""
    entry = registry.get(scholar_id, {"name": name})
    if "photo" not in entry and photo_url:
        for ext in (".jpg",):  # fotos do Scholar vêm como JPEG independente da extensão na URL
            photo_path = COAUTHORS_DIR / f"{scholar_id}{ext}"
            if _download_photo(photo_url, photo_path):
                entry["photo"] = photo_path.name
                break
    registry[scholar_id] = entry
    return entry


NOT_FOUND_JSON = COAUTHORS_DIR / "not_found.json"


def load_not_found() -> list[str]:
    """Nomes já buscados (via search_coauthor) sem achar ninguém — evita
    buscar de novo a cada sincronização (cada busca é uma requisição a
    mais no Scholar)."""
    if not NOT_FOUND_JSON.exists():
        return []
    return json.loads(NOT_FOUND_JSON.read_text(encoding="utf-8"))


def mark_not_found(name: str) -> None:
    names = load_not_found()
    if name not in names:
        names.append(name)
        COAUTHORS_DIR.mkdir(exist_ok=True)
        NOT_FOUND_JSON.write_text(json.dumps(names, indent=2, ensure_ascii=False), encoding="utf-8")


def is_known_not_found(name: str) -> bool:
    key = _name_key(name)
    return any(_name_key(n) == key for n in load_not_found())


def ingest_coauthors_sidebar(coauthors: list[dict]) -> dict[tuple, dict]:
    """coauthors: lista de {"name", "scholar_id", "photo_url"} vinda de
    google_scholar_scraper.scrape_author_profile (a caixa "Coautores" da
    barra lateral de UM perfil). Registra cada um em coauthors.json
    (baixando foto se ainda não tiver), retroalimenta scholar-id em
    people/ pra quem a gente descobrir, e devolve
    {_name_key(nome): {"scholar_id", "photo_url"}} pronto pra usar como
    coauthor_scholar_map em render_publication()."""
    registry = load_coauthors_registry()
    result_map: dict[tuple, dict] = {}

    for co in coauthors:
        key = _name_key(co["name"])
        if key is None:
            continue
        result_map[key] = {"scholar_id": co["scholar_id"], "photo_url": co["photo_url"]}
        backfill_scholar_id_if_person(co["name"], co["scholar_id"])
        _register_coauthor(co["scholar_id"], co["name"], co["photo_url"], registry)

    _save_coauthors_registry(registry)
    return result_map


def find_known_scholar_id(name: str) -> str | None:
    """Só consulta se já sabemos o scholar_id dessa pessoa (people/ ou o
    registro de coautores confirmados), pelo nome — sem criar nada. Usado
    pelas publicações externas (sem o dono do site), que não passam por
    resolve_author_ids."""
    key = _name_key(name)
    if key is None:
        return None
    people_index = _index_by_name(PEOPLE_DIR)
    if key in people_index:
        return _read_scholar_id(PEOPLE_DIR / f"{people_index[key]}.qmd")
    return _find_coauthor_by_name(name, load_coauthors_registry())


def backfill_scholar_id_if_person(name: str, scholar_id: str) -> None:
    """Se `name` casa com um perfil em people/ que ainda não tem
    scholar-id:, adiciona. Usado por publicações externas (sem o dono do
    site), que não passam por resolve_author_ids — mas o pedido de
    "vincular quem está em people a um perfil" vale pra elas também."""
    key = _name_key(name)
    if key is None:
        return
    people_index = _index_by_name(PEOPLE_DIR)
    if key in people_index:
        _ensure_scholar_id(PEOPLE_DIR / f"{people_index[key]}.qmd", scholar_id)


def resolve_author_ids(authors: list[tuple[str, str | None, str | None]]) -> list[dict]:
    """authors: lista de (nome, scholar_id_ou_None, photo_url_ou_None) —
    scholar_id/photo_url vêm da caixa "Coautores" do perfil sincronizado
    nesta rodada (ver google_scholar_scraper.scrape_author_profile),
    quando o Scholar já confirma essa pessoa como colaboradora conhecida.

    Retorna uma lista de dicts {name, id, source, scholar_id}, na MESMA
    ordem de entrada. "source" é:
      - "people": alguém da equipe, id = slug em people/
      - "coauthor": coautor externo confirmado pelo Scholar, id = scholar_id
      - "unknown": sem identidade confirmada, id = None
    """
    people_index = _index_by_name(PEOPLE_DIR)
    registry = load_coauthors_registry()
    registry_changed = False

    results = []
    for name, scholar_id, photo_url in authors:
        alias_slug = _KNOWN_ALIASES.get(name.strip().lower())
        if alias_slug:
            results.append({"name": name, "id": alias_slug, "source": "people", "scholar_id": scholar_id})
            continue

        key = _name_key(name)

        if key in people_index:
            person_id = people_index[key]
            person_path = PEOPLE_DIR / f"{person_id}.qmd"
            if scholar_id:
                _ensure_scholar_id(person_path, scholar_id)
            else:
                scholar_id = _read_scholar_id(person_path)
            results.append({"name": name, "id": person_id, "source": "people", "scholar_id": scholar_id})
            continue

        # não é da equipe: só confia em confirmação do próprio Scholar,
        # nunca em busca por nome (ver docstring do módulo)
        known_id = scholar_id or _find_coauthor_by_name(name, registry)
        if known_id:
            _register_coauthor(known_id, name, photo_url, registry)
            registry_changed = True
            results.append({"name": name, "id": known_id, "source": "coauthor", "scholar_id": known_id})
        else:
            results.append({"name": name, "id": None, "source": "unknown", "scholar_id": None})

    if registry_changed:
        _save_coauthors_registry(registry)

    return results


def render_authors_block(resolved: list[dict]) -> str:
    """Monta o bloco ::: {.paper-authors} ... ::: para colar em
    {{AUTHORS_WITH_PHOTOS}} no corpo de TEMPLATE.qmd. Os hrefs são
    RAIZ-relativos (começam com "/"), não relativos a publications/<slug>.qmd
    — o mesmo HTML gerado aqui é reutilizado, sem alteração, nas cópias
    symlinkadas em publications/<username>/<slug>.qmd (uma pasta mais
    fundo), então um caminho relativo tipo "../people/..." resolve certo
    na página canônica mas quebra (fotos/links quebrados) nas cópias por
    pessoa. Raiz-relativo funciona em qualquer profundidade, ao custo de só
    funcionar com o site publicado na raiz do domínio (não numa subpasta) —
    ver documentação de publicação do site.
      - "people": link pro perfil da pessoa no site.
      - "coauthor": link direto pro Google Scholar dela, foto real de
        coauthors/<scholar_id>.<ext> (ou ícone genérico se não tiver foto).
      - "unknown": ícone de pessoa genérico, link pra uma busca no Google
        pelo nome — sem identidade confirmada."""
    lines = ["::: {.paper-authors}"]
    for person in resolved:
        if person["source"] == "people":
            href = f'/people/{person["id"]}.html'
            target_attrs = ""
            image = _find_image(PEOPLE_DIR, person["id"]) or f'{person["id"]}.jpg'
            img_src = f"/people/{image}"
        elif person["source"] == "coauthor":
            href = f'https://scholar.google.com/citations?user={person["id"]}&hl=pt-BR'
            target_attrs = ' target="_blank" rel="noopener"'
            registry = load_coauthors_registry()
            photo = registry.get(person["id"], {}).get("photo")
            img_src = f"/coauthors/{photo}" if photo else None
        else:
            href = f'https://www.google.com/search?q={urllib.parse.quote(person["name"])}'
            target_attrs = ' target="_blank" rel="noopener"'
            img_src = None

        img_or_icon = (
            f'<img src="{img_src}" alt="{person["name"]}">'
            if img_src else
            '<i class="bi bi-person-circle"></i>'
        )
        lines.append(f'<a href="{href}"{target_attrs}>{img_or_icon}<span>{person["name"]}</span></a>')
    lines.append(":::")
    return "\n".join(lines)
