"""Gera automaticamente:

  1. A seção "## Publications" (listing nativo do Quarto) de cada perfil em
     people/, a partir de publications/<username>/ — pasta de links
     simbólicos mantida por publications/_retreiver/sync_symlinks.py (ver
     aquele módulo pro que entra nela: oficiais + externas). Esta etapa só
     decide SE a seção existe (a pessoa tem ou não pelo menos um link) — o
     conteúdo em si é o próprio listing lendo a pasta.

     Efeito colateral aceito: uma publicação oficial com N coautores
     cadastrados no site acaba renderizada N+1 vezes (a página "oficial"
     em publications/<slug>.html, mais uma cópia via link simbólico em
     cada publications/<username>/<slug>.html) — mesmo conteúdo, URLs
     diferentes. É o preço de ter um listing nativo por pessoa sem mexer
     em texto à mão.

  2. A lista `contents:` do listing de Publications na página de
     Publications (publications/index.qmd) e na home (index.qmd) — só os
     arquivos de publications/*.qmd de nível superior (nunca _external/
     nem as pastas por pessoa).

Sem rede, sem scraping — só lê o que já está no disco. Roda automaticamente
antes de cada `quarto render`/`quarto preview` via project.pre-render em
_quarto.yml.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "_retreiver"))
from person_bibliography import set_person_publications  # noqa: E402
from sync_symlinks import PUBLICATIONS_DIR, official_files, sync_all_symlinks  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

CONTENTS_MARKER = "# publications-contents:start (gerado por generate_person_bibliographies.py — não editar)"
CONTENTS_RE = re.compile(re.escape(CONTENTS_MARKER) + r"\n(\s*)contents:\s*\[.*?\]")


def _update_contents_line(path: Path, paths: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    contents = ", ".join(paths)
    new_text, n = CONTENTS_RE.subn(
        lambda m: f"{CONTENTS_MARKER}\n{m.group(1)}contents: [{contents}]", text, count=1,
    )
    if n == 0:
        raise RuntimeError(
            f"Marcador '{CONTENTS_MARKER}' não encontrado em {path} — "
            "adicione manualmente no front matter (ver publications/index.qmd)."
        )
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")


def main() -> None:
    has_publications = sync_all_symlinks()
    for username, has_pubs in has_publications.items():
        set_person_publications(username, has_pubs)
    updated = sum(1 for v in has_publications.values() if v)

    # listagens principais: só os arquivos de publications/ de nível
    # superior, nunca _external/ nem as pastas por pessoa.
    # "./nome.qmd" (com barra) é obrigatório aqui — um nome de arquivo sem
    # nenhuma barra é resolvido pelo Quarto como busca pelo nome em
    # qualquer lugar do projeto (achava as cópias via link simbólico
    # também!), não como caminho relativo à própria pasta.
    top_level_names = [p.name for p in official_files()]
    _update_contents_line(PUBLICATIONS_DIR / "index.qmd", [f"./{name}" for name in top_level_names])
    _update_contents_line(ROOT / "index.qmd", [f"publications/{name}" for name in top_level_names])

    print(f"[✔] Listing de publicações atualizado para {updated} pessoa(s), "
          f"{len(top_level_names)} publicação(ões) oficial(is).")


if __name__ == "__main__":
    main()
