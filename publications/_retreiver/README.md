# publications/_retreiver/

Ferramentas de apoio para *atualizar automaticamente* a lista de
publicações. Nada nesta pasta é renderizado pelo site — o `_` no nome faz
o Quarto ignorá-la inteiramente (mesma convenção usada em
`publications/_papers/` e `publications/_external/`, ver abaixo).

**Fonte de dados escolhida: Google Scholar** (`sync_from_google_scholar.py`),
via navegador comum, sem proxy/VPN/rotação de IP — só uma sessão normal com
pausas entre páginas. Isso significa aceitar o risco real de
bloqueio/CAPTCHA temporário do Google, que é inerente a acessar o Scholar
de forma automatizada (ele não tem API pública); não tentei contornar isso
escondendo de onde a requisição parte. `fetch_semantic_scholar.py` continua
disponível como alternativa sem esse risco (API oficial), caso queira
comparar ou usar como fallback.

Precisa do Playwright instalado neste ambiente (`.venv/` já criado aqui com
`playwright` + `beautifulsoup4`; `pip install playwright && playwright
install chromium` se recriar do zero).

## As três pastas de `publications/`

| Pasta | O que tem | Aparece no site? |
|---|---|---|
| `publications/*.qmd` (nível superior) | lista **oficial** — só papers em que o dono do site é coautor | Sim — página de Publications, home, e o listing de cada coautor |
| `publications/_papers/` | rascunho gerado pelos fetchers, **aguardando sua revisão** antes de virar oficial | Não (nome com `_`) |
| `publications/_external/<username>/` | papers de um membro da equipe **sem** o dono do site — nunca viram lista oficial | Não diretamente (nome com `_`), mas ver `publications/<username>/` abaixo |
| `publications/<username>/` (uma por pessoa, criada automaticamente) | links simbólicos pras publicações dessa pessoa (oficiais + as de `_external/<username>/`) | **Sim** — é isso que faz o listing nativo do perfil dela funcionar |

`username` é o padrão "estilo paper" usado em todo `people/*.qmd` e
`authors/*.qmd` — iniciais + sobrenome, minúsculo, sem separador (ex.:
Marcos M. Raimundo → `mmraimundo`, Giovani Valdrighi → `gvaldrighi`).

## As peças

1. **`extract_scholar_links.py`** — só leitura local, sem rede. Varre
   `people/*.qmd` e devolve `{username: {name, scholar_id, scholar_url}}`
   pra quem já tem Google Scholar cadastrado no perfil (campo
   `scholar-id:` no front matter, com fallback pro link em
   `.profile-links` se o campo ainda não existir). Seguro de rodar quando
   quiser.

2. **`google_scholar_scraper.py`** — as funções de raspagem de fato
   (Playwright + BeautifulSoup): `scrape_author_profile` (lista de
   publicações do perfil), `scrape_paper_details` (resumo, autores, data,
   veículo — a partir da página de citação de cada artigo), `human_delay`
   (pausas humanas entre requisições).

3. **`sync_from_google_scholar.py`** — a orquestração de ponta a ponta:

       python3 sync_from_google_scholar.py --person giovani-valdrighi-nao-existe-mais-use-o-username
       python3 sync_from_google_scholar.py --person gvaldrighi

   Abre o perfil de uma pessoa (`--person <username>`), ignora publicações
   já cadastradas (oficial **ou** externa, por título), e pra cada uma
   nova: se o dono do site está entre os autores → gera em
   `publications/_papers/<slug>.qmd` (rascunho); senão → gera direto em
   `publications/_external/<username>/<slug>.qmd` (página real, sem
   author-ids/fotos, pra não criar stub de coautor de terceiros em
   `authors/`).

4. **`resolve_authors.py`** — local, sem rede (a não ser pelo avatar
   placeholder, que usa ImageMagick localmente). Recebe a lista de autores
   de um artigo e, para cada um: acha o `id` em `people/*.qmd` se for
   alguém do laboratório; senão, acha em `authors/*.qmd` se já foi
   cadastrado antes; senão, cria um perfil mínimo em `authors/<username>.qmd`
   mais um avatar-placeholder. Nunca escreve em `people/`. A
   correspondência de nomes usa sobrenome + iniciais (`_name_key`), não
   string exata, porque citações abreviam nomes de formas diferentes —
   incluindo casos como iniciais grudadas sem ponto ("SB" → {s, b}) e
   partículas comuns ("de", "da"...) que não contam como iniciais.
   `_KNOWN_ALIASES` cobre à mão os casos que a heurística não resolve
   sozinha (sobrenome truncado/expandido entre a citação e o perfil real).

5. **`render_publication.py`** — o templating em si (preenche
   `TEMPLATE.qmd`), compartilhado pelos dois fetchers. Define
   `PAPERS_DIR` (`_papers/`) e `EXTERNAL_DIR` (`_external/`).

6. **`sync_symlinks.py`** — a única fonte da verdade de "quais
   publicações são de quem": varre `publications/*.qmd` (author-ids) e
   `publications/_external/<username>/*.qmd`, e cria/atualiza
   `publications/<username>/` com um link simbólico pra cada uma,
   removendo os que não correspondem mais a nada. Rodável sozinho pra
   depurar sem precisar de `quarto render`:

       python3 sync_symlinks.py

7. **`fetch_semantic_scholar.py`** — via alternativa, API oficial, sem
   risco de bloqueio.

8. **`TEMPLATE.qmd`** / **`AUTHOR_TEMPLATE.qmd`** — formatos preenchidos
   por `render_publication.py`/`resolve_authors.py`.

## Depois que `../generate_person_bibliographies.py` roda (automático)

Esse script (na raiz de `publications/`, chamado pelo `project.pre-render`
em `_quarto.yml`) chama `sync_symlinks.py` e depois atualiza o front matter
de cada `people/<username>.qmd` (bloco `listing:` delimitado por
comentário) e a lista `contents:` das duas listagens principais
(Publications e home) — tudo sozinho, a cada `quarto render`/`quarto
preview`. Não precisa rodar nada manualmente além dos fetchers acima.

## Depois de revisar e promover um arquivo de `_papers/`

1. Mover o `.qmd` de `publications/_papers/` para `publications/` (fora da
   pasta com `_`).
2. Conferir se `categories:` (quando presente) bate com os valores já
   usados em outras publicações em vez de inventar categorias novas.
3. Conferir os campos vindos do Google Scholar (ano, veículo, coautores) —
   ele não separa isso com a mesma limpeza da API do Semantic Scholar.
4. Rodar `quarto render` (ou `quarto preview`) uma vez — o pre-render
   recalcula sozinho o listing de cada coautor e das duas páginas
   principais a partir do arquivo promovido.
