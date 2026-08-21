import os
import random
import re
import time
from typing import Any, Dict, List, Optional, Set
from bs4 import BeautifulSoup
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError, sync_playwright


def human_delay(min_sec: float = 12.0, max_sec: float = 35.0) -> None:
    """Gera pausas aleatórias simulando o tempo de navegação humano."""
    wait_time = random.uniform(min_sec, max_sec)
    print(f"[...] Aguardando {wait_time:.1f} segundos para evitar detecção...")
    time.sleep(wait_time)


def sanitize_filename(name: str) -> str:
    """Sanitiza strings para uso seguro como nome de arquivo."""
    return re.sub(r"[^\w\-_]", "_", name.lower())


def get_existing_paper_titles(file_path: str) -> Set[str]:
    """Lê o arquivo Markdown existente e extrai os títulos dos artigos já cadastrados."""
    if not os.path.exists(file_path):
        return set()

    existing_titles: Set[str] = set()
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        # Captura os títulos nos cabeçalhos '### Título do Artigo'
        matches = re.findall(r"^###\s+(.+)$", content, re.MULTILINE)
        for title in matches:
            existing_titles.add(title.strip().lower())

    return existing_titles


def scrape_author_profile(
    page: Any, scholar_url: str
) -> Optional[Dict[str, Any]]:
    """Extrai os metadados do perfil do autor e a lista dos 5 artigos mais recentes."""
    print(f"\n[+] Acessando perfil do autor: {scholar_url}")
    try:
        page.goto(scholar_url, wait_until="networkidle")
        human_delay(5, 10)

        # Verificação básica de bloqueio
        if "sorry/index" in page.url or "recaptcha" in page.url:
            print("[-] CAPTCHA ou bloqueio temporário detectado pelo Google!")
            return None

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

        # Captura as 5 primeiras publicações
        pub_rows = soup.find_all("tr", class_="gsc_a_tr")[:5]
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

        return {
            "name": name,
            "photo_url": photo_url,
            "affiliation": affiliation,
            "publications": publications,
        }

    except Exception as e:
        print(f"[-] Erro ao raspar perfil do autor: {e}")
        return None


def scrape_paper_abstract(page: Any, paper_url: str) -> str:
    """Abre a página individual do artigo no Scholar para extrair o resumo.

    Mantida por compatibilidade — scrape_paper_details() abaixo faz o mesmo
    e também traz autores/data/veículo, então é o que sync_from_google_scholar.py
    usa de fato."""
    print(f"[+] Coletando resumo do artigo: {paper_url}")
    try:
        page.goto(paper_url, wait_until="networkidle")
        human_delay(15, 30)  # Pausa longa necessária ao acessar cada publicação

        if "sorry/index" in page.url:
            print("[-] Bloqueio temporário detectado na página do artigo.")
            return "Resumo indisponível devido a limitação de taxa do Scholar."

        soup = BeautifulSoup(page.content(), "html.parser")

        # Elemento onde fica o resumo na citação do Scholar
        abstract_elem = soup.find("div", id="gsc_oci_descr")
        if abstract_elem:
            return abstract_elem.text.strip()

        return "Resumo não encontrado na página da citação."

    except PlaywrightTimeoutError:
        return "Tempo limite excedido ao carregar a publicação."
    except Exception as e:
        print(f"[-] Erro ao extrair resumo: {e}")
        return "Erro durante a extração do resumo."


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


def process_author_markdown(
    page: Any,
    scholar_url: str,
    output_dir: str = "authors_md",
    default_avatar: str = "https://via.placeholder.com/150?text=Avatar",
) -> None:
    """Gerencia a extração incremental e atualização do arquivo Markdown do autor."""
    author_data = scrape_author_profile(page, scholar_url)
    if not author_data:
        return

    os.makedirs(output_dir, exist_ok=True)
    name: str = author_data["name"]
    filename: str = f"{sanitize_filename(name)}.md"
    file_path: str = os.path.join(output_dir, filename)

    # 1. Carrega os artigos que já constam no Markdown existente
    saved_titles: Set[str] = get_existing_paper_titles(file_path)
    print(f"[i] Artigos já existentes no Markdown local: {len(saved_titles)}")

    # 2. Varre os artigos mais recentes do perfil
    new_publications_count: int = 0
    for pub in author_data["publications"]:
        title_lower = pub["title"].strip().lower()

        if title_lower in saved_titles:
            print(f"[=] Artigo já cadastrado: '{pub['title']}' (Ignorando requisição de resumo)")
            pub["abstract"] = "JA_EXISTE"
        else:
            print(f"[+] Novo artigo detectado: '{pub['title']}'")
            pub["abstract"] = scrape_paper_abstract(page, pub["scholar_url"])
            new_publications_count += 1

    # 3. Reescreve ou cria o Markdown apenas se for arquivo novo ou se houver novos artigos
    if not os.path.exists(file_path) or new_publications_count > 0:
        photo_url = author_data.get("photo_url") or default_avatar
        affiliation = author_data["affiliation"]

        md_content = f"# {name}\n\n"
        md_content += f"![{name}]({photo_url})\n\n"
        md_content += f"**Afiliação:** {affiliation}\n\n"
        md_content += f"[Perfil no Google Scholar]({scholar_url})\n\n"
        md_content += "## Publicações Recentes\n\n"

        for pub in author_data["publications"]:
            # Preserva o aviso caso o resumo já existisse ou aplica o novo resumo baixado
            abstract_text = (
                "(Resumo mantido da versão anterior)"
                if pub["abstract"] == "JA_EXISTE"
                else pub["abstract"]
            )

            md_content += f"### {pub['title']}\n"
            md_content += f"- **Link no Scholar:** [{pub['title']}]({pub['scholar_url']})\n"
            md_content += f"- **Resumo:** {abstract_text}\n\n"

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(md_content)

        print(f"[✔] Arquivo atualizado ({file_path}) com {new_publications_count} nova(s) publicação(ões)!")
    else:
        print(f"[i] O arquivo de {name} já está atualizado. Nenhuma ação necessária.")


def main() -> None:
    # Lista dos perfis que deseja monitorar
    author_urls: List[str] = [
        "https://scholar.google.com/citations?user=Jic3Y38AAAAJ",  # Exemplo: Yoshua Bengio
    ]

    # Busto genérico caso o autor não tenha foto no perfil
    DEFAULT_SILHOUETTE: str = (
        "https://upload.wikimedia.org/wikipedia/commons/7/7c/Profile_avatar_placeholder_large.png"
    )

    with sync_playwright() as p:
        # headless=False é crucial para evitar detecção de bots pelo Google
        browser = p.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled"],
        )

        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800},
        )

        page = context.new_page()

        for scholar_url in author_urls:
            process_author_markdown(
                page=page,
                scholar_url=scholar_url,
                output_dir="authors_md",
                default_avatar=DEFAULT_SILHOUETTE,
            )
            # Intervalo seguro entre perfis de autores diferentes
            human_delay(30, 60)

        browser.close()


if __name__ == "__main__":
    main()