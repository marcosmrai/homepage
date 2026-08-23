"""Front matter no Quarto só aceita UMA chave `listing:` por página — para
uma pessoa ter tanto "## Publications" quanto "## Projects" (cada um o seu
próprio listing nativo), os dois precisam ser itens de uma mesma lista sob
`listing:`, não duas chaves `listing:` separadas (isso é um
`YAMLException: duplicated mapping key`, erro real de render).

Este módulo gerencia essa chave compartilhada: cada script "dono" de um
item (generate_person_bibliographies.py para "publications",
generate_project_pages.py para "projects") só sabe sobre o próprio bloco,
delimitado por um marcador — este módulo garante que a chave `listing:`
exista com exatamente os itens presentes, na ordem em que cada script foi
chamado, e desapareça de vez quando o último item for removido.

Uso:
    item = (
        f"  {MARKER_START}\n"
        "  - id: publications\n"
        '    contents: "../publications/gvaldrighi/*.qmd"\n'
        f"  {MARKER_END}\n"
    )
    new_frontmatter = set_listing_item(frontmatter, MARKER_START, MARKER_END, item)
    new_frontmatter = set_listing_item(frontmatter, MARKER_START, MARKER_END, None)  # remove
"""

import re

LISTING_KEY_RE = re.compile(r"^listing:\n((?:[ \t].*\n)*)", re.MULTILINE)


def set_listing_item(frontmatter: str, marker_start: str, marker_end: str, item_yaml: str | None) -> str:
    """frontmatter: o front matter inteiro (com os "---" de abertura/fechamento).
    item_yaml: bloco já indentado (2 espaços) com os marcadores nas
    extremidades, pronto para colar dentro de `listing:` — ou None para
    remover esse item. Nunca mexe em outros itens da lista."""
    block_re = re.compile(
        r"[ \t]*" + re.escape(marker_start) + r"\n.*?[ \t]*" + re.escape(marker_end) + r"\n",
        re.DOTALL,
    )

    listing_match = LISTING_KEY_RE.search(frontmatter)
    if listing_match:
        items_block = listing_match.group(1)
        has_item = bool(block_re.search(items_block))

        if item_yaml is None:
            new_items_block = block_re.sub("", items_block) if has_item else items_block
        elif has_item:
            new_items_block = block_re.sub(lambda _m: item_yaml, items_block, count=1)
        else:
            new_items_block = items_block + item_yaml

        if new_items_block.strip() == "":
            return frontmatter[:listing_match.start()] + frontmatter[listing_match.end():]
        return frontmatter[:listing_match.start()] + "listing:\n" + new_items_block + frontmatter[listing_match.end():]

    if item_yaml is None:
        return frontmatter
    # frontmatter termina em "---\n" (4 caracteres) — insere a chave nova
    # logo antes desse fechamento
    return frontmatter[:-4] + "listing:\n" + item_yaml + "---\n"
