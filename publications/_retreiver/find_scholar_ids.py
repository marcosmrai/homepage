"""Descobre o scholar-id de pessoas em people/ que ainda não têm um.

Não faz busca de nome solta (ver docstring de google_scholar_scraper.
search_coauthor) — cada nome é buscado ancorado num paper que também
tenha o dono do site como autor, já que ele é orientador/colaborador
confirmado da grande maioria da equipe. Quando o Scholar confirma o
perfil (link no byline do resultado), o scholar-id é gravado na lista
"links:" do front matter da pessoa via resolve_authors._ensure_scholar_id
— nunca sobrescreve quem já tem.

Quem não é encontrado simplesmente fica sem scholar-id (não há cache de
"não encontrado" aqui como há para coautores externos em
coauthors/not_found.json — é uma varredura pontual, não recorrente).

Uso:
    python3 find_scholar_ids.py
    python3 find_scholar_ids.py --owner-name "Marcos M. Raimundo"
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from google_scholar_scraper import human_delay, search_coauthor  # noqa: E402
from resolve_authors import PEOPLE_DIR, SCHOLAR_ID_FIELD_RE, _ensure_scholar_id  # noqa: E402

TITLE_RE = re.compile(r'^title:\s*"([^"]+)"', re.MULTILINE)


def people_missing_scholar_id() -> list[tuple[Path, str]]:
    missing = []
    for qmd_path in sorted(PEOPLE_DIR.glob("*.qmd")):
        if qmd_path.name == "index.qmd":
            continue
        text = qmd_path.read_text(encoding="utf-8")
        if SCHOLAR_ID_FIELD_RE.search(text):
            continue
        title_match = TITLE_RE.search(text)
        if not title_match:
            continue
        missing.append((qmd_path, title_match.group(1)))
    return missing


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--owner-name", default="Marcos M. Raimundo", help="nome usado como âncora na busca")
    args = parser.parse_args()

    targets = people_missing_scholar_id()
    if not targets:
        print("[i] Todo mundo em people/ já tem scholar-id.")
        return

    print(f"[i] {len(targets)} pessoa(s) sem scholar-id: {', '.join(name for _, name in targets)}")

    from playwright.sync_api import sync_playwright

    found, not_found = 0, 0
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled"],
        )
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1280, "height": 800},
        )
        page = context.new_page()

        for qmd_path, name in targets:
            result = search_coauthor(page, name, args.owner_name)
            if result and result.get("scholar_id"):
                wrote = _ensure_scholar_id(qmd_path, result["scholar_id"])
                if wrote:
                    print(f"[+] {name} -> {result['scholar_id']} (gravado em {qmd_path.name})")
                    found += 1
                else:
                    print(f"[=] {name} -> {result['scholar_id']} (já tinha scholar-id, não sobrescrevi)")
            else:
                print(f"[-] {name}: não encontrado no Scholar (ancorado em {args.owner_name}).")
                not_found += 1
            human_delay(10, 20)

        browser.close()

    print(f"\n[i] {found} encontrado(s), {not_found} não encontrado(s).")


if __name__ == "__main__":
    main()
