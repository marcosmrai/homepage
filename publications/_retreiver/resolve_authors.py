"""Resolve nomes de autores de um artigo para IDs de perfil, e monta o
bloco "lista de participantes com foto" para colar no template da
publicação.

Local-only: não acessa a rede. A única coisa que este módulo ESCREVE é um
perfil mínimo em authors/<slug>.qmd (com placeholder de foto) para gente
que aparece como autora mas não é do laboratório — nunca em people/, que é
reservado para a equipe (ver people/README implícito: cada pessoa lá tem
group:, bio, Education etc., coisas que não temos para um coautor externo).

Ordem de resolução para cada nome de autor:
  1. Já existe em people/*.qmd (equipe do laboratório)?
  2. Já existe em authors/*.qmd (colaborador externo já cadastrado antes)?
  3. Nenhum dos dois -> cria um stub em authors/<slug>.qmd (nome + link do
     Google Scholar, se você já tiver essa URL à mão) e uma foto-placeholder
     (círculo colorido com iniciais, via ImageMagick — mesmo padrão usado
     para os avatares de people/ que não tinham foto real).

Uso típico (depois que o google-scholar.py já rodou e te deu os nomes dos
coautores de um paper, e opcionalmente os links de Scholar de cada um):

    from resolve_authors import resolve_author_ids, render_authors_block

    authors = [
        ("Marcos M. Raimundo", None),   # já existe em people/, URL ignorada
        ("L. G. Nonato", "https://scholar.google.com/citations?user=..."),
    ]
    resolved = resolve_author_ids(authors)
    print(render_authors_block(resolved))
"""

import re
import subprocess
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
PEOPLE_DIR = ROOT / "people"
AUTHORS_DIR = ROOT / "authors"

TITLE_RE = re.compile(r'^title:\s*"([^"]+)"', re.MULTILINE)
IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".webp")

AUTHOR_STUB_TEMPLATE = (Path(__file__).parent / "AUTHOR_TEMPLATE.qmd").read_text(encoding="utf-8")

PLACEHOLDER_COLORS = [
    "#2c3e50", "#34495e", "#3498db", "#16a085", "#8e44ad",
    "#c0392b", "#d35400", "#2980b9", "#27ae60", "#7f8c8d",
]


def slugify(name: str) -> str:
    n = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    n = n.lower().replace(".", "").replace("'", "")
    n = re.sub(r"[^a-z0-9]+", "-", n)
    return n.strip("-")


def _initials(name: str) -> str:
    parts = [p for p in re.split(r"\s+", name.strip()) if p and p[0].isupper()]
    if len(parts) >= 2:
        return (parts[0][0] + parts[-1][0]).upper()
    return name[:2].upper()


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


def _make_placeholder_avatar(path: Path, name: str, color: str) -> bool:
    """Gera um avatar-placeholder (círculo colorido + iniciais) via
    ImageMagick, igual ao usado para pessoas de people/ sem foto real.
    Retorna False (sem travar nada) se o ImageMagick não estiver disponível.
    """
    magick = "magick" if subprocess.run(["which", "magick"], capture_output=True).returncode == 0 else "convert"
    try:
        subprocess.run(
            [
                magick, "-size", "400x400", f"xc:{color}",
                "-gravity", "center", "-pointsize", "140", "-fill", "white",
                "-annotate", "0", _initials(name), str(path),
            ],
            check=True, capture_output=True,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def resolve_author_ids(authors: list[tuple[str, str | None]], create_missing: bool = True) -> list[dict]:
    """authors: lista de (nome, url_do_scholar_ou_None).

    Retorna uma lista de dicts {name, id, source, created}, na MESMA ordem
    de entrada — "source" é "people" ou "authors", "created" indica se o
    stub acabou de ser criado nesta chamada.
    """
    people_index = _index_by_name(PEOPLE_DIR)
    authors_index = _index_by_name(AUTHORS_DIR)

    results = []
    for i, (name, scholar_url) in enumerate(authors):
        alias_slug = _KNOWN_ALIASES.get(name.strip().lower())
        if alias_slug:
            source = "people" if (PEOPLE_DIR / f"{alias_slug}.qmd").exists() else "authors"
            results.append({"name": name, "id": alias_slug, "source": source, "created": False})
            continue

        key = _name_key(name)

        if key in people_index:
            results.append({"name": name, "id": people_index[key], "source": "people", "created": False})
            continue

        if key in authors_index:
            results.append({"name": name, "id": authors_index[key], "source": "authors", "created": False})
            continue

        slug = slugify(name)
        created = False

        if create_missing:
            AUTHORS_DIR.mkdir(exist_ok=True)
            stub_path = AUTHORS_DIR / f"{slug}.qmd"

            if scholar_url:
                scholar_link = (
                    f'<a href="{scholar_url}" class="about-link" target="_blank" rel="me">'
                    f'<i class="bi bi-mortarboard-fill"></i> '
                    f'<span class="about-link-text">Google Scholar</span></a>'
                )
            else:
                scholar_link = "<!-- Sem link de Google Scholar conhecido para esta pessoa ainda. -->"

            if not stub_path.exists():
                stub_path.write_text(
                    AUTHOR_STUB_TEMPLATE.replace("{{NAME}}", name)
                    .replace("{{SLUG}}", slug)
                    .replace("{{SCHOLAR_LINK_OR_COMMENT}}", scholar_link),
                    encoding="utf-8",
                )
                created = True

            if not _find_image(AUTHORS_DIR, slug):
                color = PLACEHOLDER_COLORS[i % len(PLACEHOLDER_COLORS)]
                _make_placeholder_avatar(AUTHORS_DIR / f"{slug}.jpg", name, color)

        results.append({"name": name, "id": slug, "source": "authors", "created": created})

    return results


def render_authors_block(resolved: list[dict]) -> str:
    """Monta o bloco ::: {.paper-authors} ... ::: para colar em
    {{AUTHORS_WITH_PHOTOS}} no corpo de TEMPLATE.qmd. Os hrefs são
    relativos a publications/<slug>.qmd (um nível acima de people/authors)."""
    lines = ["::: {.paper-authors}"]
    for person in resolved:
        source_dir = PEOPLE_DIR if person["source"] == "people" else AUTHORS_DIR
        image = _find_image(source_dir, person["id"]) or f"{person['id']}.jpg"
        lines.append(
            f'<a href="../{person["source"]}/{person["id"]}.html">'
            f'<img src="../{person["source"]}/{image}" alt="{person["name"]}">'
            f'<span>{person["name"]}</span></a>'
        )
    lines.append(":::")
    return "\n".join(lines)


if __name__ == "__main__":
    # Exemplo com dados fictícios só pra checar que o encadeamento funciona
    # (não escreve nada em authors/ de verdade: create_missing=False).
    example = [("Marcos M. Raimundo", None), ("Fulano de Tal Externo", None)]
    resolved = resolve_author_ids(example, create_missing=False)
    print(resolved)
    print()
    print(render_authors_block(resolved))
