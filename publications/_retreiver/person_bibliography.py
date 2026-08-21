"""Mantém a seção "## Publications" no perfil de uma pessoa (people/<username>.qmd)
como um único listing NATIVO do Quarto (cards, igual ::: {#teaching} ::: da
home), apontando pra publications/<username>/ — uma pasta cheia de links
simbólicos que generate_person_bibliographies.py mantém (ver aquele módulo
para o que entra nela: oficiais + externas).

Como o `contents:` só precisa apontar pra essa pasta (o conteúdo dela é que
muda a cada render, não o caminho), o bloco `listing:` no front matter é
praticamente estático — só aparece ou desaparece conforme a pessoa tem ou
não pelo menos uma publicação.

Front matter da pessoa (bloco marcado por comentário YAML, seguro de
atualizar de novo sem mexer no resto do front matter escrito à mão):

    ---
    title: "..."
    group: "..."
    # publications-listing:start (gerado por generate_person_bibliographies.py — não editar)
    listing:
      id: publications
      contents: ../publications/username
      type: default
      sort: "date desc"
      fields: [title, description]
    # publications-listing:end
    filters:
      - ../band-sections.lua
    ---

Corpo da pessoa (heading + div que o Quarto preenche com o listing acima):

    ## Publications

    ::: {#publications}
    :::

Se a pessoa não tem nenhuma publicação, a seção inteira — incluindo o bloco
`listing:` no front matter — é removida.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
PEOPLE_DIR = ROOT / "people"

LISTING_START = "# publications-listing:start (gerado por generate_person_bibliographies.py — não editar)"
LISTING_END = "# publications-listing:end"

LISTING_BLOCK_RE = re.compile(
    re.escape(LISTING_START) + r"\n.*?\n" + re.escape(LISTING_END) + r"\n",
    re.DOTALL,
)

FRONTMATTER_RE = re.compile(r"\A(---\n.*?\n---\n)", re.DOTALL)

SECTION_RE = re.compile(r"\n## Publications\n.*?(?=\n## |\Z)", re.DOTALL)

SECTION_BODY = "## Publications\n\n::: {#publications}\n:::\n"


def _listing_yaml(person_slug: str) -> str:
    return (
        f"{LISTING_START}\n"
        "listing:\n"
        "  id: publications\n"
        f'  contents: "../publications/{person_slug}/*.qmd"\n'
        "  type: default\n"
        '  sort: "date desc"\n'
        "  fields: [title, description]\n"
        f"{LISTING_END}\n"
    )


def _set_listing_block(text: str, person_slug: str, has_publications: bool) -> str:
    """Front matter é YAML, não o corpo — tratado à parte, sempre dentro do
    trecho isolado por FRONTMATTER_RE, pra nunca arriscar mexer num "---"
    que seja na verdade um separador horizontal escrito à mão no corpo."""
    fm_match = FRONTMATTER_RE.match(text)
    if not fm_match:
        return text
    frontmatter = fm_match.group(1)
    rest = text[fm_match.end():]

    has_block = bool(LISTING_BLOCK_RE.search(frontmatter))

    if not has_publications:
        new_frontmatter = LISTING_BLOCK_RE.sub("", frontmatter) if has_block else frontmatter
    else:
        block = _listing_yaml(person_slug)
        if has_block:
            new_frontmatter = LISTING_BLOCK_RE.sub(lambda _m: block, frontmatter)
        else:
            # frontmatter termina em "---\n" (4 caracteres) — insere o bloco
            # logo antes desse fechamento
            new_frontmatter = frontmatter[:-4] + block + "---\n"

    return new_frontmatter + rest


def set_person_publications(person_slug: str, has_publications: bool) -> Path:
    """has_publications: se publications/<person_slug>/ (mantida por
    generate_person_bibliographies.py) tem pelo menos um link simbólico."""
    path = PEOPLE_DIR / f"{person_slug}.qmd"
    if not path.exists():
        raise FileNotFoundError(f"Perfil não encontrado: {path}")

    text = path.read_text(encoding="utf-8")

    if not has_publications:
        text = SECTION_RE.sub("", text) if SECTION_RE.search(text) else text
        text = _set_listing_block(text, person_slug, False)
        path.write_text(text, encoding="utf-8")
        return path

    section = "\n" + SECTION_BODY
    if SECTION_RE.search(text):
        text = SECTION_RE.sub(lambda _m: section.rstrip("\n"), text, count=1)
    else:
        text = text.rstrip("\n") + "\n" + section

    text = _set_listing_block(text, person_slug, True)
    path.write_text(text, encoding="utf-8")
    return path
