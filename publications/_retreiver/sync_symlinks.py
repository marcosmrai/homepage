"""Varre as publicações do site e cria/atualiza publications/<username>/
com um link simbólico para cada uma — só isso, nada de front matter ou
listing. É a única fonte da verdade de "quais publicações são dessa
pessoa", usada tanto pelo pre-render (generate_person_bibliographies.py)
quanto por quem quiser depurar sem rodar `quarto render` inteiro:

    python3 sync_symlinks.py

Duas fontes por pessoa:
  - oficiais: publications/<slug>.qmd (nível superior) cujo author-ids
    inclui o username dela.
  - externas: publications/_external/<username>/*.qmd (ver
    sync_from_google_scholar.py) — sempre dela, a pasta já é a chave.

publications/_papers/ (rascunho ainda não revisado) NUNCA entra aqui de
propósito — só author-ids de arquivos já promovidos para publications/
contam como "oficial". Uma pessoa citada num rascunho não aparece no
listing dela até você promover o arquivo.
"""

import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
PEOPLE_DIR = ROOT / "people"
PUBLICATIONS_DIR = ROOT / "publications"
EXTERNAL_DIR = PUBLICATIONS_DIR / "_external"

AUTHOR_IDS_RE = re.compile(r"^author-ids:\s*\[(.*?)\]", re.MULTILINE)


def official_files() -> list[Path]:
    """publications/*.qmd de nível superior — a lista oficial do site."""
    return sorted(p for p in PUBLICATIONS_DIR.glob("*.qmd") if p.name != "index.qmd")


def official_by_person(files: list[Path]) -> dict[str, list[Path]]:
    """{username: [caminho_do_arquivo_oficial, ...]} a partir de author-ids: [...]."""
    by_person: dict[str, list[Path]] = {}
    for path in files:
        ids_match = AUTHOR_IDS_RE.search(path.read_text(encoding="utf-8"))
        if not ids_match:
            continue
        for person_id in (i.strip() for i in ids_match.group(1).split(",")):
            if person_id and (PEOPLE_DIR / f"{person_id}.qmd").exists():
                by_person.setdefault(person_id, []).append(path)
    return by_person


def sync_person_folder(username: str, targets: list[Path]) -> bool:
    """Cria/atualiza publications/<username>/ com um link simbólico para
    cada arquivo em `targets` (caminhos absolutos), removendo links que não
    correspondem mais a nada. Retorna True se a pasta ficou com pelo menos
    um link (então a pessoa tem alguma publicação pra mostrar)."""
    person_dir = PUBLICATIONS_DIR / username
    wanted = {target.name: target for target in targets}

    if not wanted:
        if person_dir.exists():
            for existing in person_dir.iterdir():
                existing.unlink()
            person_dir.rmdir()
        return False

    person_dir.mkdir(exist_ok=True)
    for existing in person_dir.iterdir():
        if existing.name not in wanted:
            existing.unlink()

    for name, target in wanted.items():
        link = person_dir / name
        relative_target = Path("..") / target.relative_to(PUBLICATIONS_DIR)
        if link.is_symlink() and Path(os.readlink(link)) == relative_target:
            continue
        if link.exists() or link.is_symlink():
            link.unlink()
        link.symlink_to(relative_target)

    return True


def sync_all_symlinks() -> dict[str, bool]:
    """Roda pra todo mundo em people/. Retorna {username: tem_publicacao}."""
    files = official_files()
    official = official_by_person(files)

    result: dict[str, bool] = {}
    for path in PEOPLE_DIR.glob("*.qmd"):
        username = path.stem
        targets = list(official.get(username, []))
        external_dir = EXTERNAL_DIR / username
        if external_dir.exists():
            targets += sorted(external_dir.glob("*.qmd"))
        result[username] = sync_person_folder(username, targets)

    return result


if __name__ == "__main__":
    result = sync_all_symlinks()
    for username, has_publications in sorted(result.items()):
        if has_publications:
            n = len(list((PUBLICATIONS_DIR / username).glob("*.qmd")))
            print(f"[✔] {username}: {n} link(s) simbólico(s) em publications/{username}/")
    total = sum(1 for v in result.values() if v)
    print(f"\n[✔] {total} pessoa(s) com pelo menos uma publicação vinculada.")
