# Progresso — Computing and Society

Estrutura conforme `CLAUDE.md`: `index.md` é o planejamento do semestre;
cada aula é `aulaNN/` com `00-plano-aula.md`, `01-fontes.md`, `02-aula.qmd`.
Fontes em `fontes/`: `CSV1.pdf`, `CSV2.pdf`, `CSV3.pdf` (Maciel & Viterbo,
2020, 3 volumes), `EthEng.pdf` (Van de Poel & Royakkers, 2011), `EthTech.pdf`
(Steen, 2022).

**Diferença estrutural desta disciplina:** é humanidades/ética, não STEM.
Por decisão do usuário, o `.qmd` não usa chunks de código Python/simulação
— só prosa (HTML/RevealJS via `content-visible`) e diagramas Mermaid para
modelos conceituais. Sem `exemplos-estilo/` ainda (as outras disciplinas
são todas STEM; não fazem sentido como referência de tom aqui — considerar
usar a própria Aula 1 como exemplo depois de aprovada, como já feito nas
outras disciplinas).

## Achado importante: citação quebrada no `index.md`

A leitura recomendada original de **três aulas** (1, 7, 13) citava "Maciel
& Viterbo (2020), Vol. 2, Capítulo 2: Análise Cultural de Sistemas
Computacionais" — **capítulo que não existe**. Confirmado pelo sumário
real dos dois volumes: o Vol. 2 não tem Capítulo 2 (a numeração continua
do Vol. 1, começa no Cap. 9); o Capítulo 2 do Vol. 1 é sobre pós-graduação,
sem relação com o tema.

- **Corrigido no `index.md`** (a pedido explícito do usuário, que também
  autorizou usar `EthTech.pdf` como suporte adicional): substituído pelo
  Cap. 10 real do Vol. 2 ("Cultura na Prática da Computação", Salgado &
  Leitão, pp. 46–80) — mais próximo tematicamente — e adicionado Steen
  (2022), Cap. 3 "Is Technology a Neutral Tool?" como leitura
  complementar à Aula 1.
- **Aulas 7 e 13:** mesma citação quebrada, corrigida também (mesmo
  substituto), mas **sem verificar se o Cap. 10 de fato serve para essas
  aulas** — só resolvido o erro factual, não a adequação de conteúdo.
- **Achado extra, ainda não corrigido:** a leitura de Steen citada na
  Aula 7 ("Chapter 2: Ethics of Consequences") também parece errada — o
  Cap. 2 real do EthTech é "What do we mean with ethics?"; o mais próximo
  do título citado é o Cap. 9 "Consequences and outcomes" (p. 67).
  Sinalizado no `index.md`, não resolvido — assunto de quando chegarmos
  na Aula 7.

## Aula 1 — Computing as a Socio-Technical System

- [x] `00-plano-aula.md` — 5 blocos, **50 min** (não ~105 min como no
      rascunho inicial — correção de orçamento de tempo feita pelo
      usuário na segunda rodada). Núcleo: o mapa de atores (Van de Poel &
      Royakkers §1.6) recebeu o maior bloco (15 min) por ser o que a
      competência esperada do `index.md` pede de fato.
- [x] `01-fontes.md` — 8 fontes (Van de Poel & Royakkers Cap. 1 + Steen
      Cap. 3), todas com trecho literal extraído e verificado (offset de
      página confirmado por leitura direta, não assumido: +14 no EthEng,
      +9 no EthTech a partir do Cap. 3 — **atenção**, o offset do EthTech
      não é constante no livro inteiro, há uma página de abertura de
      parte não numerada que desloca o offset em 4 páginas em algum ponto
      antes do Cap. 3). Maciel & Viterbo Cap. 10 está na leitura
      recomendada mas **não foi lido** — o plano se sustentou inteiramente
      nas outras duas fontes.
- [x] `02-aula.qmd` — escrito nesta sessão, sem código Python (só prosa +
      2 diagramas Mermaid: mapa de atores recriando a Figura 1.6 de Van
      de Poel & Royakkers, e o *feedback loop* de algoritmos de redes
      sociais). Validado com `quarto render --to html` e `--to revealjs`,
      sem erro.

## Etapa 5 — index.md

Link da Aula 1 adicionado (não existia nenhum antes). Mesmo padrão das
outras disciplinas: `../../society/aula01/notas.html` (+ Slides).

## Aula 2 — What is Ethics, and The Ethical Cycle

- [x] `00-plano-aula.md` — 5 blocos, ~50 min nominais (nota explícita no
      próprio plano: conteúdo de texto/slides é mais profundo do que cabe
      em 50 min falados, igual à Aula 1).
- [x] `01-fontes.md` — 29 fontes (Van de Poel & Royakkers Caps. 3 e 5,
      Steen Cap. 16), passou por **duas rodadas**: a segunda incorporou
      feedback do usuário — trocou o exemplo de conflito de normas
      kantiano (trabalho infantil/IKEA, considerado ruim) pelo exemplo já
      do livro (provas de alunos vs. amigo) + o assassino à porta de Kant
      (sinalizado como externo ao livro-base); aprofundou ética do
      cuidado; usou o Ford Pinto como caso central atravessando três das
      quatro teorias, mostrando profundidade revertendo conclusões dentro
      de cada teoria (não só entre teorias); adicionou provocações de
      fim de subseção (nos slides) usando Study/Discussion Questions do
      próprio livro (pp. 107–108); expandiu "quando voltar" no Ciclo
      Ético em três mecanismos nomeados, com honestidade explícita sobre
      quais são citação literal do livro (Seta 2) vs. reconstrução nossa
      (Setas 1 e 3).
- [x] `02-aula.qmd` — sem código Python, só prosa + Mermaid. Passou por
      **duas rodadas completas**: a primeira gerou o conteúdo inicial; a
      segunda (pedido explícito do usuário: "recomece desde
      planejamento, mas não precisa das minhas intervenções") reescreveu
      substancialmente os Blocos 2, 3 e 5 incorporando todo o feedback
      listado acima, sem parar para aprovação intermediária. Corrigido
      também um bug de numeração de seções (`###` pulando `##`, gerando
      "3.0.1" em vez de "3.1" no sumário). Validado com
      `quarto render --to html` e `--to revealjs`, sem erro, div-balance
      verificado por script Python a cada rodada.
- [x] Etapa 5 (`index.md`) — **ainda não feita**, pendente aprovação do
      usuário sobre o conteúdo final desta segunda rodada.

### Nota de infraestrutura: `output-dir` do `_quarto.yml`

Durante esta rodada, `content/teaching/_quarto.yml` foi encontrado com
uma alteração não commitada: `output-dir` mudou de `"../../static/"`
para `"../../teaching/static/"`. Perguntado ao usuário, que confirmou
**manter** o novo valor. Efeito prático: a partir desta rodada, os
HTMLs renderizados da Aula 2 foram gravados em
`mraimundo/teaching/static/society/aula02/` (novo local), não mais em
`mraimundo/static/society/aula02/` (local antigo, usado pela Aula 1 e
pelas primeiras renderizações da própria Aula 2 nesta sessão — ficou
com uma cópia desatualizada, não removida). Se o Hugo do site espera os
HTMLs em `mraimundo/static/`, os links do `index.md` (Etapa 5) e a
publicação real do site podem quebrar até que a Aula 1 e as outras
disciplinas também migrem para o novo caminho, ou até o `_quarto.yml`
volte ao valor antigo — vale confirmar com o usuário antes de publicar.

## Aulas 3–15

Não iniciadas.
