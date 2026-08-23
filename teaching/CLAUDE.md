# Fluxo de trabalho — geração de aulas

Esta pasta (`teaching/`) contém MÚLTIPLAS disciplinas, cada uma em sua
própria subpasta (ex.: `supervised-learning/`,
`optimization-linear-algebra/`, `computing-and-society/`,
`unsupervised-learning/`). Este `CLAUDE.md` vale para todas elas.

Este projeto segue um processo de checkpoints POR AULA, com aprovação
humana obrigatória em cada etapa. NUNCA pule uma etapa, NUNCA gere a
etapa seguinte sem que o usuário tenha sinalizado aprovação explícita
(ex: "pode seguir", "próxima etapa", "ok").

O `index.qmd` de cada disciplina é a página pública do curso no site
(lista de aulas, objetivos, competências esperadas) e também a
referência de planejamento do semestre — use-o para identificar tema,
objetivos de aprendizagem e a sequência das aulas. Não proponha
alterações nele além de acrescentar/atualizar a entrada da aula em
questão, a não ser que explicitamente dito ou aprovado pelo usuário.

---

## Estrutura de pastas

```
teaching/
├── CLAUDE.md
├── lesson-theme.scss          # paleta azul/laranja/vermelho, só das aulas
├── logos-footer.html          # rodapé com os logos UNICAMP/IC nos slides
├── UNICAMP.png, IC.png
├── supervised-learning/
│   ├── index.qmd              # página pública do curso + planejamento
│   ├── _fontes/                # PDFs de referência (normalmente links simbólicos)
│   ├── _progresso.md           # registro de estado, não publicado
│   ├── aula01/
│   │   ├── index.qmd           # a aula em si (saída HTML + RevealJS)
│   │   ├── _00-plano-aula.md   # plano de aula, não publicado
│   │   └── _01-fontes.md       # fontes citadas, não publicado
│   ├── aula02/
│   └── ...
├── optimization-linear-algebra/
│   ├── index.qmd
│   ├── src/                   # módulo Python compartilhado entre aulas
│   ├── _fontes/
│   ├── _progresso.md
│   └── aula01/, aula02/, ...
└── ...
```

Cada disciplina é autocontida na sua subpasta. Cada aula é uma subpasta
própria dentro da disciplina, nomeada `aulaNN` (`aula01`, `aula02`, ...).

**Por que os nomes com `_` na frente:** o Quarto ignora por convenção
qualquer arquivo ou pasta cujo nome comece com `_` — nunca é renderizado
nem copiado para o site publicado. `_fontes/`, `_progresso.md`,
`_00-plano-aula.md` e `_01-fontes.md` usam esse prefixo de propósito:
são material de apoio/planejamento (e, no caso de `_fontes/`, PDFs de
livros com direitos autorais) que nunca deve aparecer no site ao vivo —
só o `index.qmd` de cada aula (e o `index.qmd` da disciplina) é
público.

---

## Etapa 0 — Identificar a disciplina (OBRIGATÓRIA, toda sessão)

Antes de ler, editar ou gerar qualquer arquivo, é preciso saber em qual
subpasta de disciplina trabalhar nesta sessão.

- Se o usuário já declarou a disciplina na mensagem (ex: "Disciplina:
  supervised-learning" ou "trabalhando em optimization-linear-algebra"),
  usar essa subpasta e confirmar em uma linha antes de prosseguir.
- Se não declarou e houver mais de uma subpasta de disciplina em
  `teaching/`, **perguntar qual é a disciplina da sessão** antes de
  qualquer outra ação. Não adivinhar pela última disciplina usada em
  sessões anteriores — o estado pode ter mudado.
- Se o workspace aberto já é a subpasta de uma única disciplina, essa é
  a disciplina — não perguntar.

Todos os caminhos de arquivo nas etapas abaixo (`index.qmd`,
`_fontes/`, `aulaNN/`, `_progresso.md`) são relativos à subpasta da
disciplina identificada nesta etapa, não à raiz `teaching/`.

---

## Estrutura da aula

### Estrutura macro (o "esqueleto" da aula)

A espinha dorsal mais robusta é a de três movimentos:

**1. Abertura (5–10 min)** — o objetivo é criar o "gancho" cognitivo:
- **Organizador prévio** (Ausubel): uma ideia-ponte que conecta o novo conteúdo ao que já se sabe. Ex.: antes de modelos generativos, retomar "estimar densidade" como algo já visto em detecção de anomalias.
- **Roteiro explícito**: dizer as 3–4 perguntas que a aula vai responder. Isso reduz carga cognitiva extrínseca porque o aluno para de gastar memória de trabalho tentando adivinhar para onde vai.
- **Problema motivador** antes do formalismo, não depois.

**2. Desenvolvimento (segmentado)** — o ponto crítico: não é um bloco contínuo.
- **Segmentação em blocos de 10–15 min**, cada um com um único "ponto de aterrissagem". A atenção sustentada em exposição passiva degrada rapidamente; o corte periódico reinicia o ciclo.
- **Pausas ativas**: crie um slide `Pergunta` entre blocos: peça para o aluno escrever a ideia central com suas palavras, comparar com o colega, ou responder uma pergunta de checagem. É o intervalo que consolida, não a exposição. Apresentar como uma **pergunta direta**, sem rótulo genérico tipo "Pausa ativa" antes dela — o título do `callout-tip` é a própria pergunta:
  ```
  ::: {.callout-tip}
  ## Por que o corte "no cruzamento das curvas" está errado, e o que falta entrar na conta?
  :::
  ```
  **Atenção — no RevealJS isso precisa de um heading real por fora da
  caixa.** Um `##` usado como título de um `callout-tip` não gera um
  heading de verdade (vira um `<div class="callout-title">`), e por
  isso o Reveal.js sozinho não reconhece ali um novo slide — o
  conteúdo gruda no slide anterior. É por isso que o slide `Pergunta`
  citado acima precisa de um heading real `## Pergunta`, genérico,
  ANTES da caixa (fora dela) — só esse heading real garante o corte de
  slide certo. A pergunta específica continua sendo o título do
  `callout-tip`, dentro da caixa:
  ```
  ::: {.content-visible when-format="revealjs"}
  ## Pergunta

  ::: {.callout-tip}
  ## Por que o corte "no cruzamento das curvas" está errado, e o que falta entrar na conta?
  :::
  :::
  ```
  Nas notas HTML não há esse problema de corte de slide (não é
  necessário o heading genérico `## Pergunta` por fora) — mas usar o
  mesmo padrão nos dois formatos não atrapalha.

  Neste slide também coloque uma pergunta de V/F que auxilie a pensar nesse conceito.

  Crie um slide seguinte chamando `Resposta` onde a pergunta direta é repetida e a resposta do VF é dada.
- **Sinalização verbal**: "isto é o resultado central", "esta hipótese é a que vamos relaxar depois". Marcadores explícitos de hierarquia evitam que tudo pareça igualmente importante.

**3. Fechamento (5 min)** — quase sempre o mais sacrificado e o mais valioso:
- Retomar as perguntas da abertura e responder cada uma em uma frase.
- Nomear explicitamente o que ficou em aberto e o que vem na próxima aula.

### Técnicas de nível micro

| Técnica | Para que serve |
|---|---|
| **Exemplo resolvido (worked example)** antes de exercício | Reduz carga cognitiva em conteúdo novo; a ordem inversa só funciona com alunos já proficientes |
| **Contraexemplo deliberado** | Delimita a fronteira do conceito. "Onde este método falha?" ensina mais que três casos de sucesso |
| **Duplo registro** (intuição → formalismo → volta à intuição) | Evita que a derivação matemática se torne um fim em si |
| **Perguntas de diagnóstico** com alternativas plausíveis erradas | Revela concepções equivocadas; funciona melhor que "alguma dúvida?", que quase nunca produz resposta |
| **Princípio da redundância** (Mayer) | Não ler o slide em voz alta — texto e narração idênticos competem pelo mesmo canal. Slide com pouco texto + fala elaborando |
| **Explicitar a estrutura argumentativa** | "Vou fazer três suposições; a terceira é frágil e vou atacá-la no fim" |

---

## Formato do arquivo de aula

Cada aula é um **único arquivo `index.qmd`** dentro da sua pasta
`aulaNN/`, não um par separado de slides e notas. O mesmo arquivo
produz duas saídas (HTML e RevealJS) via blocos
`::: {.content-visible when-format="..."}`:

- **HTML** (`unless-format="revealjs"`): prosa corrida, completa,
  com as provas/derivações por extenso, citações de página do livro,
  avisos de leitura e notas de rodapé pedagógicas. Sai como `notas.html`
  (algumas aulas ainda saem como `index.html`, o nome padrão do Quarto —
  ver "Nomes de arquivo de saída" abaixo).
- **RevealJS**: densa e completa, não um resumo de tópicos — os slides
  precisam sustentar a aula sozinhos em sala, não só sinalizar
  *highlights* ("só highlights é complicado para trabalhar", feedback
  explícito do usuário). Usar bullets/fragmentos (`. . .`,
  `::: {.fragment}`) para revelar progressivamente e organizar uma ideia
  por slide, mas sem cortar explicações, derivações e nuances
  essenciais — o corte em relação à versão HTML é de ritmo e organização
  visual, não de profundidade de conteúdo. Conceitos não-triviais
  (ex: teoria kantiana, normas *prima facie*) precisam do mesmo cuidado
  explicativo nos slides que têm nas notas — não vale simplificar a
  ponto de distorcer. Sai como `slides.html`.

## Dados: prefira exemplos reais a sintéticos

Feedback explícito do usuário: as aulas têm ficado teóricas demais para
quem está aprendendo Aprendizado de Máquina/Otimização pela primeira
vez — sem um dado real e palpável por trás, a matemática fica abstrata
demais. Ao escolher o dataset que ilustra o fio condutor de uma aula (o
"problema-fio" que atravessa os blocos), **prefira um dataset real a um
dataset sintético**, e **prefira ambos a um dataset de brinquedo como
Iris** — interessante para ensinar sintaxe, mas pouco palpável (poucos
alunos têm intuição sobre pétalas de flor).

**De onde puxar o dataset: Hugging Face Hub, não pedir arquivo ao
usuário a cada aula.** Em vez de esperar o usuário trazer um CSV para
cada aula nova, use a lista curada abaixo — todos os itens foram
testados com `datasets.load_dataset(repo_id)`, sem token/chave
(datasets públicos do Hub não exigem autenticação; só datasets
*gated*/privados exigiriam, via `HF_TOKEN`, o que não é o caso de
nenhum item desta lista). O kernel Jupyter usado nas aulas
(`sensibleml-moo`) já tem `datasets` e `huggingface_hub` instalados. Ao
carregar, aparece um aviso de "unauthenticated requests" — é só um
aviso de limite de taxa, não um bloqueio; pode ignorar.

| Dataset (repo Hugging Face) | Linhas | Uso recomendado | Observações |
|---|---|---|---|
| **Adult / Census Income** — `scikit-learn/adult-census-income` | 32.561 | Classificação binária (renda >50k), atributos mistos (contínuos + categóricos) — bom para Naive Bayes, árvores, regressão logística | Sem colunas problemáticas |
| **Breast Cancer Wisconsin** — `scikit-learn/breast-cancer-wisconsin` | 569 | Classificação binária médica (diagnóstico M/B), todos os atributos contínuos | Descartar `id` e `Unnamed: 32` (coluna vazia, artefato do CSV original) |
| **Pima Indians Diabetes** — `khoaguin/pima-indians-diabetes-database` | 768 | Médico, multivariado contínuo (Glicose, IMC, pressão, etc.), alvo binário — bom para Aula 1 de `supervised-learning` (Beta 1D, usando só `Glucose`) **e** Aula 1 de `unsupervised-learning` (Gaussiana multivariada/Mahalanobis, no lugar dos sensores sintéticos) | Coluna alvo já vem nomeada `y` |
| **California Housing** — `gvlassis/california_housing` | 20.640 (já dividido train/val/test) | Regressão — preço de imóvel a partir de 8 atributos contínuos; bom para regressão linear, regularização, e para `optimization-linear-algebra` (escalas bem diferentes entre atributos, motiva *feature scaling*) | Substitui o antigo Boston Housing (removido do scikit-learn por um problema ético numa variável) |
| **Default of Credit Card Clients (UCI)** — `Lancer73/uci-credit-card-default` | 30.000 (já dividido train/val/test) | Risco de crédito, classificação binária, atributos de histórico de pagamento — bom para árvores, ensembles | — |
| **German Credit Data (Statlog)** — `AiresPucrs/german-credit-data` | 1.000 | Risco de crédito, mistura explícita de categóricos (Sexo, Moradia, Propósito) e numéricos (Idade, Valor, Duração) — bom encaixe para Naive Bayes com atributos de tipos diferentes | Dataset pequeno, bom para uma aula que não quer um treino pesado |
| **Credit Card Transactions Fraud Detection** — `dazzle-nu/CIS435-CreditCardFraudDetection` | ~1.048.575 | Fraude/anomalia com atributos interpretáveis (valor, categoria, localização) — melhor para a lógica de detecção de anomalia da Aula 1 de `unsupervised-learning` do que o dataset clássico da ULB, cujos atributos são componentes de PCA anônimos, não interpretáveis | Grande: **subamostrar** para uso em aula; descartar colunas `Unnamed: 0`, `Unnamed: 23`, `6006` (artefatos); classe muito desbalanceada (avisar antes de usar) |

Isso não bane dados sintéticos por completo: eles seguem úteis para
isolar um ponto matemático específico (ex.: um contraexemplo
controlado, ou uma verificação numérica de uma propriedade, como o
contraexemplo de Gini/entropia da Aula 3 de `supervised-learning`). Mas
o **exemplo-fio** que atravessa os blocos de uma aula — o problema que
dá contexto para tudo o resto — deve, sempre que possível, vir de um
dataset real, preferencialmente um da tabela acima.

**Como usar no `.qmd`:** carregar no bloco de setup global, junto com
os outros imports:

```python
from huggingface_hub.utils import logging as hf_logging
hf_logging.set_verbosity_error()  # evita o aviso "unauthenticated requests" vazando no chunk

from datasets import disable_progress_bar
disable_progress_bar()  # evita barra de progresso poluindo a saída do chunk

from datasets import load_dataset
ds = load_dataset("scikit-learn/adult-census-income")["train"].to_pandas()
```

Sem as duas primeiras linhas, tanto o aviso de "unauthenticated
requests" quanto a barra de progresso do download vazam para a saída do
chunk renderizado (mesmo com `echo: false`, que só esconde o código,
não a saída/stderr) — com elas, a saída fica limpa.

O download é armazenado em cache local (`~/.cache/huggingface/`) —
renderizações seguintes na mesma máquina não baixam de novo. Se, algum
dia, um dataset novo (fora desta lista) for necessário, teste o
`load_dataset(repo_id)` antes de incorporar à aula (confirmar que
carrega sem token e checar as colunas), e considere adicionar à tabela
acima se for reutilizável em outras aulas.

## Citações e trechos de fontes: sempre traduzidos no `index.qmd`

Fontes bibliográficas em inglês (comum neste projeto) devem ter seus
trechos **traduzidos para português** no `index.qmd` da aula — tanto
nas notas quanto nos slides. Deixar a citação em inglês tem um custo
alto de troca de idioma para quem lê ou apresenta em português
(feedback explícito do usuário). Evite "copiar e colar" trechos dos
livros.

- Em `_01-fontes.md`, o "Trecho" deve ser um overview dos conceitos, a
  citação literal deve sempre ser traduzida para evitar travas de
  direitos autorais — a intenção é ter um registro de verificação
  direta contra o PDF (Etapa 3, não mexer nisso).
- No `index.qmd` da aula, usar a tradução para português do trecho,
  deixando claro que é tradução nossa (ex.: "tradução livre"), não uma
  citação literal de outra fonte. Termos técnicos sem tradução direta e
  estável (ex.: *prima facie*, em latim) podem ficar no original, com
  uma explicação ao lado na primeira aparição.

Código Python é embutido nos mesmos chunks, gerando as figuras que
ilustram tanto a versão HTML quanto a RevealJS.

- Um único bloco de **setup global** no topo (imports, seed do RNG,
  paleta de cores fixa reutilizada em toda a aula, funções auxiliares).
  **Cores preferenciais, nesta ordem:** as cores do IC —
  `#0085CA` (RGB 0,133,202), `#FF5E00` (RGB 255,94,0) e `#E03C31`
  (RGB 224,60,49). Use essas três primeiro (ex.: `COR_A`, `COR_B`,
  `COR_LIM`) antes de introduzir qualquer outra cor na paleta da aula;
  cores adicionais (`COR_NEU`, `COR_ALT`, etc.), se precisar de mais de
  três, ficam livres, mas as três do IC vêm sempre primeiro. (Essa é a
  mesma paleta de `../lesson-theme.scss`, que estiliza a própria
  página — headings/links em azul, código/destaque em laranja, callouts
  de atenção em vermelho.)
- Chunks com `#| echo: false` e `#| fig-align: center` para as figuras.
- Numeração de blocos/seções consistente com a numeração usada no
  planejamento do semestre.
- Avisos de leitura (`::: {.callout-warning}`, `::: {.callout-note}`,
  `::: {.callout-important}`) quando a interpretação do curso diverge
  da referência bibliográfica, ou quando há uma armadilha prática
  conhecida (ex: zeros exatos quebrando uma verossimilhança).

**Nomes de arquivo de saída:** definir explicitamente no YAML do
`index.qmd`, já que o padrão do Quarto usaria o nome do próprio arquivo
(`index`) para ambos os formatos:

```yaml
format:
  html:
    output-file: notas.html
  revealjs:
    output-file: slides.html
```

Além disso, cada aula soma o tema visual e as configurações
compartilhadas de slide (footer, logos, dimensões) por cima — ver um
`index.qmd` de aula já existente para o bloco `format:` completo,
copiando-o em vez de reescrever do zero. **Essas configurações
compartilhadas vivem no front matter de CADA aula, não no `_quarto.yml`
do projeto** — um `format: revealjs:` global já quebrou o build do
site inteiro de forma silenciosa (nem toda página some do render, e o
erro reportado não aponta pra causa real), então não promova essas
configurações pro `_quarto.yml`, mesmo que pareça redundante repeti-las
em cada aula.

## Sugestão de fluxogramas e diagramas

Ao montar o bloco, se o conteúdo tiver estrutura sequencial, uma árvore de decisão, um processo com ramificações, ou uma comparação de caminhos alternativos (ex: "três saídas honestas para um problema"), **proponha um diagrama TikZ** (` ```{.tikz} ` , com `%%| fig-align: center`), sem esperar o usuário pedir. O site já está configurado (`_quarto.yml` da raiz do projeto) com o filtro `pandoc-ext/diagram` e o *engine* TikZ (via `pdflatex`), renderizando nativamente nos dois formatos de saída (HTML e RevealJS). Use as cores preferenciais do IC (ver seção acima) nos elementos do diagrama quando fizer sentido. Só pergunte se não estiver claro que o diagrama ajuda mais do que texto.

## Exercícios (obrigatório em toda aula)

Toda aula precisa de exercícios — em dois formatos distintos, um por saída, que não devem ser confundidos entre si:

- **Notas (HTML):** terminar o arquivo com uma seção de **Exercícios** (dentro do bloco `content-visible` exclusivo de HTML), com **exatamente 3 questões discursivas/conceituais** e **12 questões de V/F** (não 12 itens — **12 blocos de 4 itens cada**, ou seja, 48 itens ao todo, cada bloco num tema diferente da aula, cobrindo o conteúdo da aula de ponta a ponta) — quotas fixas, por aula. Pode reaproveitar questões de fim de capítulo das próprias fontes bibliográficas (citando de onde vieram, como já se faz com trechos citados) ou propor questões originais — nesse caso, sinalizar que são originais, não da fonte. Ficam sem solução no arquivo (é trabalho para o aluno resolver por conta, fora da aula). Cada questão de V/F tem 4 itens do mesmo tema, e só é considerada correta se todos os 4 forem acertados (na avaliação, o aluno pode deixar a questão em branco com punição de 20% da nota da questão). Cada uma das 12 questões (os 4 itens de um mesmo tema) fica dentro de um `::: {.callout-tip}` cujo título é o **tema** daquela questão (não um rótulo genérico) — deixa explícito que aquilo é uma unidade de questão.

- **Slides (RevealJS):** intercalar, **no meio** da sequência de slides (não só ao final), pequenos exercícios de checagem/acompanhamento — uma pergunta objetiva e rápida sobre o que acabou de ser apresentado, para o aluno testar se acompanhou o conteúdo em tempo real. **No mínimo 3 desses exercícios de checagem por aula**, espalhados ao longo dos slides (não concentrados num só bloco). Cada um é um V/F de 4 itens (mesmo tema, mesma lógica das notas), com os 4 itens juntos em **um único slide**, dentro de um `::: {.callout-tip}` cujo título é o **tema** do bloco — seguido **imediatamente** (no slide seguinte) por **um único slide de resposta**, com a solução dos 4 itens junta, também em caixa (`::: {.callout-tip}`, título "*tema* — Resposta"). Não deixar nenhum desses três para o fim da aula.

---

## Para cada aula (repetir o ciclo)

### 1. Identificar a aula no planejamento
Consultar `index.qmd` da disciplina e confirmar com o usuário o tema,
objetivos e carga horária da aula NN. Não seguir sem confirmação.

### 2. Plano de aula (resumo + estrutura)
Gerar `aulaNN/_00-plano-aula.md`, contendo:

- **Resumo** (5-10 linhas): o que a aula cobre, objetivos de
  aprendizagem, pré-requisitos (conferindo com o que já foi dado nas
  aulas anteriores aprovadas).
- **Plano de aula**: sequência de blocos/tópicos na ordem em que serão
  apresentados, com tempo estimado por bloco (somando à carga horária
  da aula) e a lógica de transição entre eles (ex: "Bloco 1 termina
  com uma pergunta sem resposta, que o Bloco 2 resolve").

Formato:

```markdown
## Resumo — Aula N

[5-10 linhas: cobertura, objetivos, pré-requisitos]

## Plano de aula — Aula N (carga horária: XXmin)

1. **[Nome do bloco]** (~XX min) — [o que cobre, por que vem aqui]
2. **[Nome do bloco]** (~XX min) — [o que cobre, como conecta com o anterior]
...
```

**PARAR** e esperar aprovação/edição do usuário.

### 3. Fontes — com trecho citado literalmente
Gerar `aulaNN/_01-fontes.md` listando cada fonte usada, com:
- referência (livro, capítulo, seção, páginas);
- **o uso pretendido** daquele trecho na aula;
- **o trecho citado literalmente**, extraído do PDF/slide antigo,
  **na língua original da fonte** — nunca reescrito de memória, nunca
  paraphraseado, nunca traduzido nesta etapa, para que a checagem do
  usuário seja direta contra o PDF. A tradução para português (ver seção
  "Citações e trechos de fontes" acima) é feita depois, só no
  `index.qmd` da aula (Etapa 4).

Formato:

```markdown
## Fontes usadas — Aula N

### Fonte 1: PRML, §1.5.1, pp. 39-41
**Uso pretendido:** prova de que o cruzamento das conjuntas minimiza
o erro esperado.

**Trecho:**
> "the smallest probability of misclassification is achieved if
> each value of x is assigned to the class for which the joint
> probability p(x, Ck) is largest..."

---

### Fonte 2: DLFC, §2.1.1, pp. 25-26
**Uso pretendido:** exemplo de triagem médica (Bayes discreto).

**Trecho:**
> [trecho copiado literalmente do PDF]
```

**PARAR** e esperar aprovação/edição do usuário.

**Fontes como link simbólico:** os arquivos em `_fontes/` podem ser
links simbólicos apontando para os PDFs/slides originais em outro
lugar do disco (ex: `ln -s ../../../livros/prml.pdf _fontes/prml.pdf`).
Leia-os normalmente pelo caminho dentro de `_fontes/` — não há
tratamento especial necessário. Prefira links relativos, para o
projeto continuar funcionando se a pasta for movida. **Nunca copie o
PDF de verdade para dentro do projeto** — o prefixo `_` só garante que
o Quarto ignore a pasta; um link simbólico garante também que o
arquivo de direitos autorais nunca é versionado como blob do git.

### 4. Montar a aula completa
Gerar `aulaNN/index.qmd`: arquivo único com saída dupla HTML/RevealJS,
código Python embutido, seguindo o estilo descrito acima e o tom das
aulas já publicadas em outras disciplinas (comece a partir de uma
delas como referência de formato, já que o antigo diretório de
exemplos de estilo não foi trazido para este projeto), e a estrutura
de blocos definida em `_00-plano-aula.md`. Incluir diagramas TikZ onde
fizer sentido (ver seção acima), e os exercícios obrigatórios (ver
seção "Exercícios" acima: seção de exercícios ao fim das notas HTML;
exercícios de checagem intercalados nos slides, cada um seguido da
solução no slide seguinte). **PARAR.**

### 5. Atualizar o `index.qmd` da disciplina
Após o usuário aprovar `index.qmd` da aula (fim da Etapa 4), propor a
atualização do `index.qmd` da disciplina — a listagem de aulas do
curso.

Adicionar (ou atualizar, se a aula já tinha uma entrada anterior) o
link da aula, no mesmo formato das demais entradas dessa disciplina
(ver as lições já linkadas no mesmo arquivo para o formato exato —
título, conceito de ML, conceito teórico, objetivos, competências
esperadas), apontando para `./aulaNN/index.qmd`.

**Esta é uma edição de um arquivo já existente, não a criação de um
arquivo novo — por isso o mesmo cuidado das etapas anteriores não
basta.** Antes de escrever no `index.qmd`:

1. Mostrar no chat o trecho exato que será alterado/adicionado (a
   linha nova ou o antes/depois, se for uma atualização).
2. Esperar confirmação explícita do usuário.
3. Só então aplicar a edição no arquivo.

Se o usuário pedir para regenerar `index.qmd` da aula depois de já ter
uma entrada no `index.qmd` da disciplina (ex: reaprovação de uma
versão revisada), tratar a atualização do link/título da mesma forma —
propor, mostrar, esperar aprovação.

### 6. Avançar
Só gerar a aula N+1 quando o usuário disser algo como "próxima aula"
ou "continuar".

---

## Continuidade entre aulas

Antes de gerar uma aula nova, reler os planos de aula e os `index.qmd`
das aulas anteriores já aprovadas, para manter notação, nível de
formalismo e progressão consistentes — e para não repetir conteúdo já
coberto.

## Precisão de conteúdo técnico

Ao lidar com conteúdo matemático/estatístico, sinalizar explicitamente
quando algo estiver sendo inferido ou generalizado a partir do livro,
em vez de copiado fielmente — especialmente em provas, propriedades
estatísticas, e afirmações sobre otimalidade.

## Registro de estado

Sempre atualizar `_progresso.md` marcando a aula atual e o que já foi
aprovado nela (plano de aula / fontes / aula completa).
