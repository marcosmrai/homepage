"""Varre o perfil de TODA pessoa da equipe com Google Scholar cadastrado
(ver extract_scholar_links.py) e junta a caixa "Coautores" de cada uma num
cache só (coauthors/coauthors.json), retroalimentando scholar-id em
people/ pra quem a gente descobrir no caminho.

Bem mais leve que sync_from_google_scholar.py: só visita a página de
perfil de cada pessoa (que já traz a caixa "Coautores" de graça), sem
abrir a página de detalhes de publicação nenhuma nem buscar coautores
desconhecidos no Scholar. Pensado pra rodar de vez em quando e deixar o
cache de fotos/IDs de coautores frequentes sempre atualizado, mesmo pra
pessoas que você não sincronizou publicações ainda.

Uso:
    python3 refresh_coauthors.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from extract_scholar_links import extract_scholar_links  # noqa: E402
from google_scholar_scraper import human_delay, scrape_author_profile  # noqa: E402
from resolve_authors import ingest_coauthors_sidebar  # noqa: E402


def main() -> None:
    links = extract_scholar_links()
    if not links:
        print("[i] Ninguém em people/ tem Google Scholar cadastrado ainda.")
        return

    print(f"[i] {len(links)} pessoa(s) com Google Scholar cadastrado: {', '.join(sorted(links))}")

    from playwright.sync_api import sync_playwright

    total_new = 0
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

        for username, info in sorted(links.items()):
            profile = scrape_author_profile(page, info["scholar_url"])
            if not profile:
                print(f"[-] {username}: não consegui ler o perfil, pulando.")
                human_delay(20, 40)
                continue

            coauthor_map = ingest_coauthors_sidebar(profile["coauthors"])
            print(f"[✔] {username}: {len(coauthor_map)} coautor(es) na caixa \"Coautores\".")
            total_new += len(coauthor_map)

            human_delay(20, 40)

        browser.close()

    print(f"\n[✔] Cache de coautores atualizado a partir de {len(links)} perfil(is).")


if __name__ == "__main__":
    main()
