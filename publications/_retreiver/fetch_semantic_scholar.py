"""Busca publicações de um autor via a API pública do Semantic Scholar
(api.semanticscholar.org) e gera os .qmd correspondentes em
publications/papers/ (área de rascunho — excluída do build do site em
_quarto.yml; revise antes de mover para publications/ de verdade).

Esta é a via alternativa ao Google Scholar (ver sync_from_google_scholar.py
para a via que você pediu de fato usar como fonte principal). Mantive esta
também porque não depende de navegador/Playwright e não tem risco de
bloqueio — útil pra conferir/comparar dados quando quiser.

Uso:
    python3 fetch_semantic_scholar.py --author-id 2373214840 --owner-name "M. M. Raimundo"

O --owner-name é usado só para decidir se a seção "## Authors" (com fotos)
é gerada — por pedido explícito, fotos só para papers em que o dono do
site (Marcos) está envolvido, pra não explodir o número de perfis em
authors/ com o círculo de coautoria de terceiros.
"""

import argparse
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from render_publication import (  # noqa: E402
    ROOT,
    existing_titles,
    render_publication,
    slugify,
    write_publication,
)

API_BASE = "https://api.semanticscholar.org/graph/v1"
REQUEST_DELAY_SECONDS = 1.5  # a API pública já pede um request/seg no máximo


def _api_get(path: str, params: dict) -> dict:
    url = f"{API_BASE}{path}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": "personal-site-publication-sync/1.0"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def search_author(name: str) -> list[dict]:
    """Retorna candidatos {authorId, name, paperCount} para um nome —
    útil pra desambiguar manualmente antes de rodar com --author-id."""
    data = _api_get("/author/search", {"query": name, "fields": "name,paperCount,affiliations"})
    return data.get("data", [])


def fetch_author_papers(author_id: str) -> list[dict]:
    fields = "title,abstract,year,venue,publicationDate,externalIds,authors"
    data = _api_get(f"/author/{author_id}/papers", {"fields": fields})
    return data.get("data", [])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--author-id", required=True, help="Semantic Scholar authorId (use search_author() pra achar)")
    parser.add_argument("--owner-name", default="M. M. Raimundo", help="Nome do dono do site, pra decidir quando incluir fotos")
    args = parser.parse_args()

    known_titles = existing_titles()
    papers = fetch_author_papers(args.author_id)
    print(f"[i] {len(papers)} publicação(ões) encontradas no perfil.")

    written, skipped_existing = 0, 0
    for paper in papers:
        title_key = paper["title"].strip().lower()
        if title_key in known_titles:
            print(f"[=] Já existe em publications/: {paper['title']}")
            skipped_existing += 1
            continue

        rendered = render_publication(
            title=paper["title"],
            authors=[a["name"] for a in paper["authors"]],
            date_iso=paper.get("publicationDate") or f"{paper.get('year', '')}-01-01",
            year=str(paper.get("year", "")),
            venue=paper.get("venue") or "Preprint",
            abstract=paper.get("abstract"),
            source_url=f"https://www.semanticscholar.org/paper/{paper['paperId']}",
            source_label="Semantic Scholar",
            owner_name=args.owner_name,
        )
        out_path = write_publication(slugify(paper["title"]), rendered)
        print(f"[+] Gerado: {out_path.relative_to(ROOT)}")
        written += 1

        time.sleep(REQUEST_DELAY_SECONDS)

    print(f"\n[✔] {written} arquivo(s) novo(s) em publications/papers/, "
          f"{skipped_existing} já existente(s) ignorado(s). Revise antes de mover para publications/.")


if __name__ == "__main__":
    main()
