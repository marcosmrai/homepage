"""Busca as publicações de uma pessoa no Google Scholar de verdade.

Duas listas diferentes, por pedido explícito:
  - publications/ (nível superior, sem estágio de rascunho — vai direto)
    recebe os artigos em que o dono do site (Marcos) também é autor — é a
    lista "oficial" do site, usada na página de Publications, na home e no
    perfil do próprio Marcos.
  - publications/_external/<username>/ recebe os demais artigos dela (sem
    Marcos) — página de verdade também (título, resumo, link pro Scholar),
    só que sem author-ids/fotos, e fora de publications/, então nunca
    aparece na lista oficial do site nem na home.

O perfil da pessoa (people/<slug>.qmd) combina as duas num único listing
nativo do Quarto — isso é feito por ../generate_person_bibliographies.py
(não por este script), toda vez que o site é renderizado (ver
project.pre-render em _quarto.yml).

NÃO fiz nada para esconder de onde a requisição parte (sem proxy, sem VPN,
sem rotação de IP) — só o essencial pra não parecer um robô agressivo:
uma única sessão de navegador, pausas humanas entre páginas
(google_scholar_scraper.human_delay), user-agent de navegador real. O
Google Scholar não tem API pública como o Semantic Scholar, então acessar
os dados aqui significa abrir as páginas HTML como um usuário normal
abriria — e aceitar o risco real de bloqueio/CAPTCHA temporário que isso
sempre carrega.

Uso:
    python3 sync_from_google_scholar.py --person gvaldrighi

--person é o username (slug do arquivo em people/, ex.: gvaldrighi para
people/gvaldrighi.qmd) — o link de Google Scholar é lido de lá via
extract_scholar_links.py, não precisa colar a URL na mão.
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from extract_scholar_links import extract_scholar_links  # noqa: E402
from google_scholar_scraper import human_delay, scrape_author_profile, scrape_paper_details, search_coauthor  # noqa: E402
from resolve_authors import (  # noqa: E402
    PEOPLE_DIR,
    _find_coauthor_by_name,
    _index_by_name,
    _name_key,
    ingest_coauthors_sidebar,
    is_known_not_found,
    load_coauthors_registry,
    mark_not_found,
)
from render_publication import (  # noqa: E402
    ROOT,
    backfill_scholar_ids,
    existing_external_titles,
    existing_titles,
    find_existing_publication,
    looks_like_preprint,
    render_publication,
    slugify,
    update_venue_if_published,
    write_external_publication,
    write_publication,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--person", required=True, help="username (slug do arquivo em people/, ex.: gvaldrighi)")
    parser.add_argument("--owner-name", default="M. M. Raimundo", help="dono do site, usado tanto pra decidir fotos quanto pra decidir quais papers viram oficiais")
    parser.add_argument("--max-papers", type=int, default=5, help="quantas publicações recentes olhar (padrão do rascunho original: 5)")
    args = parser.parse_args()

    links = extract_scholar_links()
    if args.person not in links:
        print(f"[-] '{args.person}' não tem link de Google Scholar cadastrado em people/.")
        print(f"    Pessoas disponíveis: {', '.join(sorted(links)) or '(nenhuma)'}")
        return

    scholar_url = links[args.person]["scholar_url"]
    name = links[args.person]["name"]
    print(f"[i] Sincronizando {name} <- {scholar_url}")

    # import local: só carrega playwright se o script for realmente executado,
    # não só importado (ex.: por outro script que só queira as funções acima)
    from playwright.sync_api import sync_playwright

    known_titles = existing_titles() | existing_external_titles(args.person)
    staged, externalized, skipped_existing = 0, 0, 0

    with sync_playwright() as p:
        # headless=False é a mesma escolha do rascunho original — sem isso
        # o Google costuma desconfiar mais rápido de ser um robô.
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

        profile = scrape_author_profile(page, scholar_url, max_papers=args.max_papers)
        if not profile:
            print("[-] Não consegui ler o perfil (bloqueio/CAPTCHA ou erro de rede). Parando.")
            browser.close()
            return

        owner_key = _name_key(args.owner_name)
        people_index = _index_by_name(PEOPLE_DIR)

        # {_name_key(nome): {"scholar_id", "photo_url"}} — caixa "Coautores"
        # da barra lateral do perfil (só quem o próprio Scholar já confirma
        # como colaborador frequente, não todo mundo de todo artigo). Já
        # registra em coauthors.json e retroalimenta people/ nesse passo.
        coauthor_scholar_map = ingest_coauthors_sidebar(profile["coauthors"])
        print(f"[i] {len(coauthor_scholar_map)} coautor(es) com Scholar conhecido pelo próprio perfil.")

        for pub in profile["publications"]:  # já vem limitado a max_papers, ordenado por data
            title_key = pub["title"].strip().lower()

            # já cadastrado (oficial ou externo): nem vale a pena abrir a
            # página de detalhes (menos uma requisição, menos risco de
            # bloqueio) — só atualiza scholar-ids com o que já sabemos
            # agora, sem rebaixar nada do artigo em si.
            if title_key in known_titles:
                print(f"[=] Já cadastrado: {pub['title']}")
                skipped_existing += 1
                existing_path = find_existing_publication(title_key, args.person)
                if existing_path:
                    if backfill_scholar_ids(existing_path, coauthor_scholar_map):
                        print(f"    [i] scholar-ids atualizado em {existing_path.relative_to(ROOT)}")
                    # só reabre a página de citação se o arquivo ainda
                    # parecer um preprint — depois de publicado de verdade
                    # (veículo != preprint/arXiv), nunca mais confere de novo
                    if looks_like_preprint(existing_path):
                        details = scrape_paper_details(page, pub["scholar_url"])
                        if update_venue_if_published(existing_path, details):
                            print(f"    [✔] publicado! veículo atualizado em {existing_path.relative_to(ROOT)}: {details['venue']}")
                        human_delay(15, 30)
                continue

            details = scrape_paper_details(page, pub["scholar_url"])
            authors = details["authors"] or [name]
            venue = details["venue"] or "Preprint"

            # autores que não são da equipe, não vieram na caixa
            # "Coautores" desta rodada, e ainda não estão no registro nem
            # marcados como "sem resultado" — vale tentar achar o perfil
            # deles buscando no Scholar ancorado em quem estamos
            # sincronizando (ela é uma coautora confirmada de verdade
            # desse artigo, então serve de âncora segura pra desambiguar
            # nomes comuns — ver google_scholar_scraper.search_coauthor).
            registry = load_coauthors_registry()
            for author_name in authors:
                key = _name_key(author_name)
                if key is None or key == owner_key or key in people_index:
                    continue
                if key in coauthor_scholar_map or _find_coauthor_by_name(author_name, registry):
                    continue
                if is_known_not_found(author_name):
                    continue
                found = search_coauthor(page, author_name, name)
                if found:
                    coauthor_scholar_map[key] = found
                else:
                    mark_not_found(author_name)
                human_delay(10, 20)

            rendered = render_publication(
                title=pub["title"],
                authors=authors,
                date_iso=details["date_iso"] or "YYYY-MM-DD",
                year=details["year"] or "YYYY",
                venue=venue,
                abstract=details["abstract"],
                source_url=pub["scholar_url"],
                owner_name=args.owner_name,
                coauthor_scholar_map=coauthor_scholar_map,
            )

            involves_owner = any(_name_key(a) == owner_key for a in authors)
            if involves_owner:
                out_path = write_publication(slugify(pub["title"]), rendered)
                print(f"[+] Gerado em publications/ (envolve {args.owner_name}): {out_path.relative_to(ROOT)}")
                staged += 1
            else:
                out_path = write_external_publication(args.person, slugify(pub["title"]), rendered)
                print(f"[+] Gerado em publications/_external/ (sem {args.owner_name}): {out_path.relative_to(ROOT)}")
                externalized += 1

            human_delay(20, 40)

        browser.close()

    print(f"\n[✔] {staged} arquivo(s) novo(s) em publications/ (envolvem {args.owner_name} — já oficiais, sem "
          f"revisão), {externalized} novo(s) em publications/_external/{args.person}/ (sem {args.owner_name} — já "
          f"entram direto no listing do perfil dela), {skipped_existing} já existente(s) ignorado(s).")


if __name__ == "__main__":
    main()
