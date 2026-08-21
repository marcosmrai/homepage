"""Extrai os IDs/links de Google Scholar já cadastrados em people/*.qmd.

Não faz nenhuma requisição de rede — só lê arquivos locais. Serve para
alimentar a lista `author_urls` do google-scholar.py com os perfis reais do
site, em vez de mantê-la hardcoded manualmente.

Uso:
    python3 extract_scholar_links.py

Saída: um dict {slug_da_pessoa: {name, scholar_id, scholar_url}}, impresso
como JSON. Rode isso à vontade — é seguro, não toca o Google Scholar. O que
NÃO deve ser rodado sem revisão é o google-scholar.py (esse sim acessa a
rede e pode levar a um bloqueio temporário do Scholar).
"""

import json
import re
from pathlib import Path

PEOPLE_DIR = Path(__file__).resolve().parent.parent.parent / "people"

# Fonte preferida: campo de front matter próprio, ex. scholar-id: "iQXEldcAAAAJ"
# — mais robusto que ler o ID de dentro do href de um <a> escrito à mão no
# corpo do perfil (ver SCHOLAR_LINK_RE abaixo, mantido só como fallback para
# perfis antigos que ainda não têm o campo).
SCHOLAR_ID_FIELD_RE = re.compile(r'^scholar-id:\s*"?([A-Za-z0-9_-]+)"?', re.MULTILINE)

# Fallback: o mesmo padrão usado no bloco ::: {.profile-links} de
# people/*.qmd — um <a> com ícone "bi-mortarboard-fill" e texto "Google
# Scholar", de onde extraímos o ID via o parâmetro user= da URL.
SCHOLAR_LINK_RE = re.compile(
    r'<a href="[^"]*[?&]user=([A-Za-z0-9_-]+)[^"]*"[^>]*>\s*'
    r'<i class="bi bi-mortarboard-fill"></i>\s*'
    r'<span class="about-link-text">Google Scholar</span>',
)

TITLE_RE = re.compile(r'^title:\s*"([^"]+)"', re.MULTILINE)


def extract_scholar_links(people_dir: Path = PEOPLE_DIR) -> dict[str, dict[str, str]]:
    """Varre people/*.qmd (pasta plana, sem subpastas) e retorna, para cada
    pessoa com Google Scholar cadastrado, {slug: {name, scholar_id, scholar_url}}.

    Pessoas sem scholar-id nem link no profile-links simplesmente não
    aparecem no resultado — não há nada para o google-scholar.py buscar
    para elas ainda.
    """
    results: dict[str, dict[str, str]] = {}

    for qmd_path in sorted(people_dir.glob("*.qmd")):
        if qmd_path.name == "index.qmd":
            continue

        text = qmd_path.read_text(encoding="utf-8")

        id_match = SCHOLAR_ID_FIELD_RE.search(text)
        if id_match:
            scholar_id = id_match.group(1)
        else:
            link_match = SCHOLAR_LINK_RE.search(text)
            if not link_match:
                continue
            scholar_id = link_match.group(1)

        title_match = TITLE_RE.search(text)
        name = title_match.group(1) if title_match else qmd_path.stem

        results[qmd_path.stem] = {
            "name": name,
            "scholar_id": scholar_id,
            "scholar_url": f"https://scholar.google.com/citations?user={scholar_id}&hl=pt-BR",
        }

    return results


if __name__ == "__main__":
    links = extract_scholar_links()
    print(json.dumps(links, indent=2, ensure_ascii=False))
    print(f"\n{len(links)} pessoa(s) com Google Scholar cadastrado.")
