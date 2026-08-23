"""Extrai os IDs/links de Google Scholar já cadastrados em people/*.qmd.

Não faz nenhuma requisição de rede — só lê arquivos locais. Serve pra
sync_from_google_scholar.py achar o perfil de uma pessoa a partir do
--person, sem precisar colar a URL na mão.

Uso:
    python3 extract_scholar_links.py

Saída: um dict {slug_da_pessoa: {name, scholar_id, scholar_url}}, impresso
como JSON. Rode isso à vontade — é seguro, não toca o Google Scholar. O que
NÃO deve ser rodado sem revisão é o sync_from_google_scholar.py (esse sim
acessa a rede e pode levar a um bloqueio temporário do Scholar).
"""

import json
import re
from pathlib import Path

PEOPLE_DIR = Path(__file__).resolve().parent.parent.parent / "people"

# scholar-id vive dentro da lista "links:" do front matter, como item de
# uma sequência YAML (ex. '  - scholar-id: "iQXEldcAAAAJ"'), renderizada em
# HTML só em tempo de build por links.lua — o corpo do .qmd nunca contém um
# <a> escrito à mão, então não há fallback em HTML para procurar aqui.
SCHOLAR_ID_FIELD_RE = re.compile(r'^\s*-?\s*scholar-id:\s*"?([A-Za-z0-9_-]+)"?', re.MULTILINE)

TITLE_RE = re.compile(r'^title:\s*"([^"]+)"', re.MULTILINE)


def extract_scholar_links(people_dir: Path = PEOPLE_DIR) -> dict[str, dict[str, str]]:
    """Varre people/*.qmd (pasta plana, sem subpastas) e retorna, para cada
    pessoa com Google Scholar cadastrado, {slug: {name, scholar_id, scholar_url}}.

    Pessoas sem scholar-id simplesmente não aparecem no resultado — não há
    nada para o sync_from_google_scholar.py buscar para elas ainda.
    """
    results: dict[str, dict[str, str]] = {}

    for qmd_path in sorted(people_dir.glob("*.qmd")):
        if qmd_path.name == "index.qmd":
            continue

        text = qmd_path.read_text(encoding="utf-8")

        id_match = SCHOLAR_ID_FIELD_RE.search(text)
        if not id_match:
            continue
        scholar_id = id_match.group(1)

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
