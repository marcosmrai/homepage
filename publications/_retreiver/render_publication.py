"""Lógica compartilhada para gerar um .qmd de publicação a partir de
TEMPLATE.qmd, usada tanto por fetch_semantic_scholar.py quanto por
sync_from_google_scholar.py — a fonte dos dados muda, o formato de saída
(e a regra de quando incluir fotos de autores) é sempre o mesmo.
"""

import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from resolve_authors import _name_key, render_authors_block, resolve_author_ids  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent.parent
PUBLICATIONS_DIR = ROOT / "publications"
# "_papers"/"_external" com underscore: convenção do próprio Quarto pra
# ignorar arquivos/pastas inteiramente (nunca renderizados, nunca aparecem
# em nenhum listing) — exatamente o que se quer pra rascunho ainda não
# revisado (_papers) e pro estoque bruto de publicações sem o dono do site
# (_external, ver render_publication(), ramo involves_owner=False). O
# listing de cada pessoa não lê daqui diretamente — ver
# generate_person_bibliographies.py, que cria links simbólicos em
# publications/<username>/ apontando pra cá (_external) ou para
# publications/<slug>.qmd promovido (oficial), já que só um arquivo dentro
# de uma pasta SEM underscore é de fato renderizado pelo Quarto.
PAPERS_DIR = PUBLICATIONS_DIR / "_papers"
EXTERNAL_DIR = PUBLICATIONS_DIR / "_external"

TEMPLATE = (Path(__file__).parent / "TEMPLATE.qmd").read_text(encoding="utf-8")


def slugify(text: str) -> str:
    n = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    n = n.lower().replace(".", "").replace("'", "")
    n = re.sub(r"[^a-z0-9]+", "-", n)
    return n.strip("-")[:60].rstrip("-")


def existing_titles() -> set[str]:
    """Títulos (minúsculos) já presentes em publications/*.qmd — usado
    para não recriar um artigo que já foi migrado/cadastrado manualmente."""
    titles = set()
    for path in PUBLICATIONS_DIR.glob("*.qmd"):
        if path.name == "index.qmd":
            continue
        match = re.search(r'^title:\s*"([^"]+)"', path.read_text(encoding="utf-8"), re.MULTILINE)
        if match:
            titles.add(match.group(1).strip().lower())
    return titles


def render_publication(
    title: str,
    authors: list[str],
    date_iso: str,
    year: str,
    venue: str,
    abstract: str | None,
    source_url: str | None,
    source_label: str = "Semantic Scholar",
    owner_name: str | None = "M. M. Raimundo",
) -> str:
    """Preenche TEMPLATE.qmd com os dados de um artigo, independente da
    fonte (Semantic Scholar, Google Scholar, ou preenchido manualmente).

    owner_name: só decide se a seção "## Authors" (com fotos) é incluída —
    por pedido explícito, fotos só para papers em que o dono do site
    (Marcos) está envolvido, pra não explodir o número de perfis em
    authors/ com o círculo de coautoria de terceiros.
    """
    authors_str = ", ".join(authors)

    text = TEMPLATE
    text = text.replace('title: "{{TITLE}}"', f'title: "{title}"')
    text = text.replace('date: "{{DATE_ISO}}"', f'date: "{date_iso}"')
    text = text.replace("{{AUTHORS_COMMA_SEPARATED}}", authors_str)
    text = text.replace("{{YEAR}}", year)
    text = text.replace("{{VENUE}}", venue)
    # categorias não vêm de nenhuma das fontes automáticas — omitir a linha
    # inteira em vez de adivinhar
    text = re.sub(r"\ncategories: \[.*?\]\n", "\n", text)

    # Comparação por sobrenome+iniciais (_name_key), não substring exata —
    # citações abreviam nomes de formas diferentes por fonte ("M. M.
    # Raimundo" no Semantic Scholar, "Marcos Medeiros Raimundo" no Google
    # Scholar), e substring simples deixa passar praticamente todo mundo.
    owner_key = _name_key(owner_name) if owner_name else None
    involves_owner = owner_key is not None and any(_name_key(a) == owner_key for a in authors)

    if involves_owner:
        resolved = resolve_author_ids([(name, None) for name in authors], create_missing=True)
        author_ids = ", ".join(p["id"] for p in resolved)
        authors_block = render_authors_block(resolved)
        text = text.replace("{{AUTHOR_ID_1}}, {{AUTHOR_ID_2}}", author_ids)
        text = text.replace("{{AUTHORS_WITH_PHOTOS}}", authors_block)
    else:
        # sem o dono do site no paper: nada de author-ids/fotos, pra não
        # criar um perfil em authors/ pra cada coautor de terceiros
        text = re.sub(r"\nauthor-ids: \[.*?\]\n", "\n", text)
        text = re.sub(r"\n## Authors\n\n\{\{AUTHORS_WITH_PHOTOS\}\}\n", "\n", text)

    abstract = (abstract or "").strip()
    if abstract:
        text = text.replace("{{ABSTRACT}}", abstract)
    else:
        text = re.sub(r"\n## Abstract\n\n\{\{ABSTRACT\}\}\n", "\n", text)

    if source_url:
        text = text.replace("{{SOURCE_LABEL}}", source_label)
        text = text.replace("{{SOURCE_URL}}", source_url)
    else:
        text = re.sub(r"\n\[\{\{SOURCE_LABEL\}\}\]\(\{\{SOURCE_URL\}\}\)\n", "\n", text)

    return text


def write_publication(slug: str, rendered_text: str) -> Path:
    PAPERS_DIR.mkdir(exist_ok=True)
    out_path = PAPERS_DIR / f"{slug}.qmd"
    out_path.write_text(rendered_text, encoding="utf-8")
    return out_path


def existing_external_titles(person_slug: str) -> set[str]:
    """Títulos já presentes em publications/_external/<person_slug>/*.qmd —
    usado pra não reprocessar/reescrever um artigo sem o dono do site que já
    foi encontrado numa rodada anterior do scraper para essa pessoa."""
    titles = set()
    directory = EXTERNAL_DIR / person_slug
    if not directory.exists():
        return titles
    for path in directory.glob("*.qmd"):
        match = re.search(r'^title:\s*"([^"]+)"', path.read_text(encoding="utf-8"), re.MULTILINE)
        if match:
            titles.add(match.group(1).strip().lower())
    return titles


def write_external_publication(person_slug: str, slug: str, rendered_text: str) -> Path:
    directory = EXTERNAL_DIR / person_slug
    directory.mkdir(parents=True, exist_ok=True)
    out_path = directory / f"{slug}.qmd"
    out_path.write_text(rendered_text, encoding="utf-8")
    return out_path
