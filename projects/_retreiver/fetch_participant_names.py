"""Resolve nome+foto de participantes de projetos que são um scholar-id
puro (sem perfil em people/) e ainda não estão em coauthors/coauthors.json.

Acessa a rede (Google Scholar) — ao contrário de ../../participants.lua
(o filtro que desenha os cartões em tempo de render), que só lê o disco.
Rode isso manualmente depois de adicionar um scholar-id novo em
`participants:`, e então rode `quarto render` (o filtro vai reler
coauthors.json e desenhar o cartão certo).

Uso:
    python3 fetch_participant_names.py
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
PROJECTS_DIR = ROOT / "projects"
PEOPLE_DIR = ROOT / "people"

sys.path.insert(0, str(ROOT / "publications" / "_retreiver"))
from resolve_authors import _register_coauthor, _save_coauthors_registry, load_coauthors_registry  # noqa: E402

PARTICIPANTS_RE = re.compile(r"^participants:\s*\[(.*?)\]", re.MULTILINE)


def missing_scholar_ids() -> list[str]:
    registry = load_coauthors_registry()
    missing: list[str] = []
    for path in PROJECTS_DIR.glob("*.qmd"):
        if path.name == "index.qmd":
            continue
        match = PARTICIPANTS_RE.search(path.read_text(encoding="utf-8"))
        if not match:
            continue
        for participant_id in (i.strip() for i in match.group(1).split(",")):
            if not participant_id:
                continue
            if (PEOPLE_DIR / f"{participant_id}.qmd").exists():
                continue
            if participant_id in registry:
                continue
            if participant_id not in missing:
                missing.append(participant_id)
    return missing


def main() -> None:
    ids = missing_scholar_ids()
    if not ids:
        print("[i] Todo participante-scholar-id já está em coauthors.json.")
        return

    print(f"[i] {len(ids)} scholar-id(s) sem nome/foto: {', '.join(ids)}")

    from playwright.sync_api import sync_playwright
    from google_scholar_scraper import scrape_author_profile

    registry = load_coauthors_registry()
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

        for scholar_id in ids:
            url = f"https://scholar.google.com/citations?user={scholar_id}&hl=pt-BR"
            profile = scrape_author_profile(page, url)
            if not profile:
                print(f"[-] {scholar_id}: não consegui ler o perfil.")
                continue
            _register_coauthor(scholar_id, profile["name"], profile.get("photo_url"), registry)
            _save_coauthors_registry(registry)
            print(f"[+] {scholar_id} -> {profile['name']}")

        browser.close()


if __name__ == "__main__":
    main()
