"""Funções de raspagem do Google Scholar (Playwright + BeautifulSoup),
usadas por sync_from_google_scholar.py. Nada aqui decide pra onde os dados
vão (publications/, publications/_external/, coauthors/, people/) — isso é
render_publication.py/resolve_authors.py; este módulo só sabe ler páginas
do Scholar e devolver dados estruturados.
"""

import random
import re
import sys
import time
import urllib.parse
from pathlib import Path
from typing import Any, Dict, List, Optional
from bs4 import BeautifulSoup
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

sys.path.insert(0, str(Path(__file__).parent))
from resolve_authors import _name_key, _query_name  # noqa: E402


def human_delay(min_sec: float = 12.0, max_sec: float = 35.0) -> None:
    """Gera pausas aleatórias simulando o tempo de navegação humano."""
    wait_time = random.uniform(min_sec, max_sec)
    print(f"[...] Aguardando {wait_time:.1f} segundos para evitar detecção...")
    time.sleep(wait_time)


def scrape_author_profile(page: Any, scholar_url: str, max_papers: int = 5) -> Optional[Dict[str, Any]]:
    """Extrai os metadados do perfil do autor, a lista dos `max_papers`
    artigos mais recentes, e a caixa "Coautores" da barra lateral.

    A ordenação padrão do Scholar num perfil é por número de citações, não
    por data — sem "&sortby=pubdate" na URL, os `max_papers` primeiros da
    tabela seriam os mais citados, não os mais recentes, e um artigo novo
    ainda sem citações nunca apareceria (visto na prática: dois papers
    recentes de M. M. Raimundo ficavam de fora mesmo com --max-papers
    maior, porque o corte de linhas acontecia ANTES do parâmetro de
    quantidade sequer ser aplicado — o slice era fixo em 5, ignorando o
    valor pedido)."""
    if "sortby=pubdate" not in scholar_url:
        separator = "&" if "?" in scholar_url else "?"
        scholar_url = f"{scholar_url}{separator}sortby=pubdate"

    print(f"\n[+] Acessando perfil do autor: {scholar_url}")
    try:
        page.goto(scholar_url, wait_until="networkidle")
        human_delay(5, 10)

        # Verificação básica de bloqueio
        if "sorry/index" in page.url or "recaptcha" in page.url:
            print("[-] CAPTCHA ou bloqueio temporário detectado pelo Google!")
            return None

        # O perfil só mostra 20 publicações por página — clica em "Show
        # more" (id="gsc_bpf_more") até ter linhas suficientes pra
        # max_papers, ou até o botão sumir/desabilitar (acabaram as
        # publicações da pessoa).
        while len(page.query_selector_all("tr.gsc_a_tr")) < max_papers:
            more_button = page.query_selector("#gsc_bpf_more")
            if not more_button or more_button.is_disabled():
                break
            more_button.click()
            human_delay(3, 6)

        soup = BeautifulSoup(page.content(), "html.parser")

        # Nome
        name_elem = soup.find("div", id="gsc_prf_in")
        name = name_elem.text.strip() if name_elem else "Autor Desconhecido"

        # Foto do autor
        img_elem = soup.find("img", id="gsc_prf_pup-img")
        photo_url = img_elem.get("src") if img_elem else None
        if photo_url and photo_url.startswith("/"):
            photo_url = f"https://scholar.google.com{photo_url}"

        # Afiliação
        aff_elem = soup.find("div", class_="gsc_prf_il")
        affiliation = aff_elem.text.strip() if aff_elem else "Afiliação não informada"

        # Captura as `max_papers` primeiras publicações (perfil ordenado
        # por data via sortby=pubdate acima, não por citações)
        pub_rows = soup.find_all("tr", class_="gsc_a_tr")[:max_papers]
        publications: List[Dict[str, str]] = []

        for row in pub_rows:
            link_elem = row.find("a", class_="gsc_a_at")
            if link_elem:
                pub_title = link_elem.text.strip()
                pub_href = link_elem.get("href")
                full_pub_url = f"https://scholar.google.com{pub_href}"
                publications.append(
                    {"title": pub_title, "scholar_url": full_pub_url}
                )

        # Caixa "Coautores" da barra lateral (id="gsc_rsb_co") — só quem o
        # próprio Google Scholar já reconhece como colaborador frequente
        # (não é a lista completa de coautores de todos os artigos), mas é
        # a ÚNICA parte do site do Scholar que liga um nome a um ID de
        # perfil + foto de verdade, já que a lista de autores de uma
        # citação (ver scrape_paper_details) é só texto puro.
        coauthors: List[Dict[str, Optional[str]]] = []
        co_block = soup.find(id="gsc_rsb_co")
        if co_block:
            for item in co_block.find_all("div", class_="gsc_rsb_aa"):
                link = item.find("a")
                img = item.find("img")
                if not link or not link.get("href"):
                    continue
                id_match = re.search(r"user=([^&]+)", link["href"])
                if not id_match:
                    continue
                coauthors.append({
                    "name": link.text.strip(),
                    "scholar_id": id_match.group(1),
                    "photo_url": (img["src"].replace("view_op=small_photo", "view_op=view_photo")
                                  if img and img.get("src") else None),
                })

        return {
            "name": name,
            "photo_url": photo_url,
            "affiliation": affiliation,
            "publications": publications,
            "coauthors": coauthors,
        }

    except Exception as e:
        print(f"[-] Erro ao raspar perfil do autor: {e}")
        return None


# Rótulos conhecidos na tabela de detalhes da página de citação (gsc_oci_field
# / gsc_oci_value) — cobre pt-BR e en, já que o idioma segue o "hl=" da URL
# do perfil da pessoa (cada perfil pode estar num idioma diferente).
_KNOWN_FIELD_LABELS = {
    "autores": "authors", "authors": "authors",
    "data de publicação": "date", "publication date": "date",
    "volume": "volume",
    "edição": "issue", "issue": "issue",
    "páginas": "pages", "pages": "pages",
    "editora": "publisher", "publisher": "publisher",
    "descrição": "abstract", "description": "abstract",
    "total de citações": "citations", "total citations": "citations",
    "artigos do google acadêmico": "related", "scholar articles": "related",
}


def _parse_scholar_date(raw: str) -> tuple[str, str]:
    """"2023/3/1" ou "2023/3" ou "2023" -> ("2023-03-01", "2023"). Falha
    graciosamente devolvendo o texto cru como ano se não conseguir parsear."""
    parts = raw.strip().split("/")
    year = parts[0]
    month = parts[1].zfill(2) if len(parts) > 1 else "01"
    day = parts[2].zfill(2) if len(parts) > 2 else "01"
    if not year.isdigit():
        return raw, raw
    return f"{year}-{month}-{day}", year


def scrape_paper_details(page: Any, paper_url: str) -> Dict[str, Any]:
    """Abre a página individual do artigo e extrai tudo que dá: resumo,
    autores, data (convertida pra ISO), veículo (periódico/conferência —
    o rótulo exato desse campo varia, então tratamos o primeiro campo "não
    reconhecido" da tabela como sendo ele). Autores/data/veículo aqui saem
    bem mais completos do que na lista de publicações do perfil (que só
    tem título + link)."""
    print(f"[+] Coletando detalhes do artigo: {paper_url}")
    result: Dict[str, Any] = {
        "abstract": None, "authors": [], "date_iso": None, "year": None, "venue": None,
    }
    try:
        page.goto(paper_url, wait_until="networkidle")
        human_delay(15, 30)  # Pausa longa necessária ao acessar cada publicação

        if "sorry/index" in page.url:
            print("[-] Bloqueio temporário detectado na página do artigo.")
            return result

        soup = BeautifulSoup(page.content(), "html.parser")

        for row in soup.find_all("div", class_="gs_scl"):
            field = row.find("div", class_="gsc_oci_field")
            value = row.find("div", class_="gsc_oci_value")
            if not field or not value:
                continue
            label = field.text.strip().lower()
            text = value.text.strip()
            key = _KNOWN_FIELD_LABELS.get(label)

            if key == "authors":
                result["authors"] = [a.strip() for a in text.split(",") if a.strip()]
            elif key == "date":
                result["date_iso"], result["year"] = _parse_scholar_date(text)
            elif key == "abstract":
                result["abstract"] = text
            elif key is None and result["venue"] is None:
                # primeiro campo fora da lista conhecida = provavelmente o
                # periódico/conferência (o rótulo varia bastante: "Revista",
                # "Conferência", "Fonte", "Publicações"...)
                result["venue"] = text

        return result

    except PlaywrightTimeoutError:
        print("[-] Tempo limite excedido ao carregar a publicação.")
        return result
    except Exception as e:
        print(f"[-] Erro ao extrair detalhes: {e}")
        return result


def _get_profile_photo(page: Any, scholar_id: str) -> Optional[str]:
    """Visita o perfil de scholar_id só pra pegar a foto (usado depois de
    achar alguém por search_coauthor, que não tem foto no resultado da
    busca — só a página do perfil dela tem)."""
    try:
        page.goto(f"https://scholar.google.com/citations?user={scholar_id}&hl=pt-BR", wait_until="networkidle")
        human_delay(5, 10)
        if "sorry/index" in page.url or "accounts.google.com" in page.url:
            return None
        soup = BeautifulSoup(page.content(), "html.parser")
        img_elem = soup.find("img", id="gsc_prf_pup-img")
        photo_url = img_elem.get("src") if img_elem else None
        if photo_url and photo_url.startswith("/"):
            photo_url = f"https://scholar.google.com{photo_url}"
        return photo_url
    except Exception:
        return None


def search_coauthor(page: Any, target_name: str, anchor_name: str) -> Optional[Dict[str, Optional[str]]]:
    """Busca no Scholar por um paper que tenha target_name E anchor_name
    como autores, e devolve o perfil de target_name se achar
    {"scholar_id", "photo_url"} — ou None se não achar nada.

    NÃO usa a busca de autor do próprio Scholar (view_op=search_authors) —
    essa trava numa tela de login mesmo com sessão normal. Usa a busca
    geral de artigos (/scholar?q=...), que não trava, e cujos resultados
    linkam nomes de autor abreviados ("J Poco") pro perfil deles quando
    a pessoa tem um.

    anchor_name é essencial pra não achar a pessoa errada: um nome comum
    sozinho pode ter várias pessoas com perfil no Scholar (testado com
    "Jorge Poco" — a busca sem âncora achou um homônimo). anchor_name deve
    ser alguém já confirmado como coautor de verdade — normalmente a
    pessoa cujo perfil está sendo sincronizado nesta rodada, já que ela
    literalmente escreveu o artigo com target_name."""
    query = f'author:"{_query_name(target_name)}" author:"{_query_name(anchor_name)}"'
    url = f"https://scholar.google.com/scholar?q={urllib.parse.quote(query)}"
    target_key = _name_key(target_name)
    if target_key is None:
        return None

    print(f"[+] Buscando coautor no Scholar: {target_name} (com {anchor_name})")
    try:
        page.goto(url, wait_until="networkidle")
        human_delay(8, 15)
        if "sorry/index" in page.url or "accounts.google.com" in page.url:
            print("[-] Bloqueio/tela de login detectado na busca.")
            return None

        soup = BeautifulSoup(page.content(), "html.parser")
        for byline in soup.find_all("div", class_="gs_a"):
            for link in byline.find_all("a", href=True):
                if "/citations?user=" not in link["href"]:
                    continue
                if _name_key(link.text.strip()) != target_key:
                    continue
                id_match = re.search(r"user=([^&]+)", link["href"])
                if not id_match:
                    continue
                scholar_id = id_match.group(1)
                photo_url = _get_profile_photo(page, scholar_id)
                return {"scholar_id": scholar_id, "photo_url": photo_url}

        print(f"[i] Nenhum perfil encontrado pra {target_name} nessa busca.")
        return None
    except Exception as e:
        print(f"[-] Erro ao buscar coautor: {e}")
        return None
