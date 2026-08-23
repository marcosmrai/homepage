## Resumo — Aula 1: Computing as a Socio-Technical System

Esta é a primeira aula do curso, e estabelece a tese que sustenta as
outras 14: computação não é feita só de hardware e software — é um
**sistema sociotécnico**, no qual tecnologia, pessoas, organizações e
cultura se moldam mutuamente. A aula abre com um caso (o desastre do
Challenger) em que uma falha "técnica" (um anel de vedação) só aconteceu
por causa de pressão organizacional e comunicação falha — nenhuma
explicação puramente técnica dá conta do que houve. Disso, a aula constrói
duas ideias centrais: **tecnologia não é neutra** (ela incorpora decisões
de projeto com consequências sociais, muitas vezes não previstas) e
**desenvolvimento tecnológico tem um mapa de atores** (produtores,
usuários, reguladores, outros interessados) cujos interesses conflitam e
cuja influência sobre a tecnologia é desigual. A aula fecha discutindo o
que isso implica para a responsabilidade de quem constrói tecnologia — ao
mesmo tempo menor (você é só um dos muitos atores) e maior (você precisa
considerar interessados que não estão na sala).

**Pré-requisitos:** nenhum prévio do curso — é a Aula 1. Não exige
formação técnica avançada; o caso de abertura (Challenger) é acessível a
qualquer aluno de graduação em computação.

**Objetivos de aprendizagem** (do `index.md`, Lesson 1):
- **Objectives:** Entender que computação não é feita só de elementos
  técnicos (hardware e software), mas constitui um sistema sociotécnico
  onde tecnologia, pessoas, organizações e cultura se influenciam
  mutuamente.
- **Expected Competencies:** Analisar artefatos computacionais no
  contexto social, cultural e organizacional mais amplo, identificando
  *feedback loops* não-técnicos e impactos sistêmicos.

**Leitura recomendada** (`index.md`, já corrigida nesta sessão — ver nota
abaixo): Van de Poel & Royakkers (2011), Cap. 1 (esp. §1.6 "The Social
Context of Technological Development"); Maciel & Viterbo (2020), Vol. 2,
Cap. 10 "Cultura na Prática da Computação"; Steen (2022), Cap. 3 "Is
Technology a Neutral Tool?" (adicionado nesta sessão).

> **Nota sobre a correção de fontes:** a leitura recomendada original no
> `index.md` citava "Maciel & Viterbo (2020), Vol. 2, Capítulo 2: Análise
> Cultural de Sistemas Computacionais" — capítulo que **não existe**: o
> Vol. 2 não tem Capítulo 2 (a numeração continua do Vol. 1 e começa no
> Cap. 9), e o Capítulo 2 do Vol. 1 é sobre pós-graduação em computação,
> sem relação com o tema. Substituído pelo Cap. 10 real do Vol. 2 (Salgado
> & Leitão, "Cultura na Prática da Computação", pp. 46–80), o mais próximo
> tematicamente. O mesmo erro de citação afeta as Aulas 7 e 13 — corrigido
> lá também, embora ainda não tenhamos lido o conteúdo dessas aulas em
> detalhe (ver `progresso.md`).

## Plano de aula — Aula 1 (carga horária: ~50min)

**Ajuste (feedback do usuário sobre o rascunho anterior):** a versão
original tinha 7 blocos somando ~105 min — o dobro do real. Cortado por
prioridade, não por corte proporcional: o mapa de atores (Bloco 4) é o
que a competência esperada do `index.md` pede de fato ("analisar no
contexto social, cultural e organizacional") — é o que menos perde tempo.
O Challenger encurta para o essencial do gancho; a seção de não-
neutralidade fica com um exemplo só; o caso do Teflon vira uma frase; os
antigos Blocos 5, 6 e 7 (*feedback loop*, responsabilidade, fechamento)
foram fundidos num único bloco final rápido.

1.  **Abertura: um desastre "técnico" que não foi só técnico** (~5 min) —
    Challenger, versão rápida (Van de Poel & Royakkers, pp. 7–9): o
    engenheiro Roger Boisjoly alertou por escrito sobre a falha do anel
    de vedação em baixas temperaturas; a recomendação técnica foi não
    lançar; a decisão final foi lançar, sob pressão organizacional, com
    os gerentes votando sem os engenheiros. A comissão presidencial
    atribuiu o desastre a "inadequate communication at NASA" — não a um
    erro de engenharia isolado. **Pergunta de abertura:** se a causa raiz
    não foi técnica, em que sentido isso ainda é um problema de
    computação/engenharia?

2.  **O que é um sistema sociotécnico** (~10 min) — Definição
    operacional: tecnologia, pessoas, organizações e cultura se
    influenciam mutuamente — nenhuma determina as outras isoladamente.
    Tese de coformação mútua: "we shape our tools and thereafter they
    shape us" (Culkin sobre McLuhan, citado em Steen 2022, p. 29).
    Reconectar com o Challenger em uma frase: a cultura organizacional
    moldou a decisão técnica, e o desastre depois remoldou a cultura
    (dois anos de programa parado, mudança para encorajar
    *whistle-blowing*) — um laço, não uma linha reta.

3.  **Tecnologia não é neutra** (~10 min) — Argumento do Cap. 3 de Steen
    (2022), com **um** exemplo forte: as **pontes de Robert Moses** em
    Nova York (Winner apud Steen, p. 29) — viadutos construídos
    deliberadamente baixos para impedir que ônibus passassem por baixo,
    excluindo pessoas pobres e majoritariamente negras do acesso a
    parques e praias. Fecha com a lei de Kranzberg (Steen, p. 30):
    "Technology is neither good nor bad; nor is it neutral."

4.  **O mapa de atores do desenvolvimento tecnológico** (~15 min, o
    núcleo da aula) — Van de Poel & Royakkers, §1.6, pp. 25–26:
    **atores** (produtores/desenvolvedores, usuários, reguladores, outros
    atores) vs. **interessados/*stakeholders*** (têm interesse no
    resultado, mas não necessariamente poder de influenciá-lo) — Figura
    1.6, recriada como diagrama Mermaid. Os interesses desses atores
    frequentemente conflitam; não há acordo automático sobre a direção
    "certa". Em uma frase: o caso do Teflon (pp. 26–27) mostra que
    desenvolvimento tecnológico é imprevisível — a descoberta foi
    acidental, e décadas depois seu uso mais difundido trouxe uma
    preocupação de saúde (PFOA) que ninguém antecipou em 1938 (o dilema
    de Collingridge, só nomeado, não detalhado).

5.  ***Feedback loop* contemporâneo, responsabilidade, e ponte** (~10 min,
    fusão dos antigos Blocos 5+6+7) — Um exemplo rápido de computação:
    algoritmos de redes sociais otimizados para tempo de tela usam
    "décadas de conhecimento do domínio de jogos de azar e caça-níqueis"
    (Steen 2022, p. 32) para capturar atenção; o comportamento capturado
    gera os dados que retreinam o algoritmo — um *feedback loop* não-
    técnico, sem que nenhuma linha de código sozinha "cause" o resultado.
    Disso, a implicação quase contraintuitiva para a responsabilidade
    (Van de Poel & Royakkers, p. 28): o contexto social **diminui** a
    responsabilidade do engenheiro individual (é só um entre muitos
    atores) mas **também a amplia** (precisa considerar interessados que
    não estão na sala). Fechamento: falta uma ferramenta para raciocinar
    sistematicamente sobre o que é certo fazer dentro dessa teia — é o
    assunto da Aula 2 (ética normativa e o Ciclo Ético).
