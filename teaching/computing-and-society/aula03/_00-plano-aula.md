## Resumo — Aula 3: Computing, Its Domains, and Professional Responsibility

As duas primeiras aulas construíram o vocabulário conceitual (sistema
sociotécnico, mapa de atores, teorias éticas normativas, Ciclo Ético) —
mas nenhuma delas tratou de como a **profissão de computação**, como
instituição concreta, tenta traduzir esse vocabulário em regras
praticáveis do dia a dia. Esta aula faz essa ponte: parte de um caso
real (BART) em que engenheiros foram demitidos por seguirem o código de
ética profissional que os protegia só no papel; usa isso para
desenvolver o que são códigos de conduta (profissionais vs.
corporativos; aspiracionais, consultivos, disciplinares), seus limites
conhecidos (vagueza, autointeresse/*window-dressing*, o problema de
"viver pelo código"); e fecha com uma particularidade brasileira pouco
óbvia e rica para discussão: a Informática **não é uma profissão
regulamentada** no Brasil (ao contrário de engenharia, medicina, direito)
— o que significa, na prática, que não existe um conselho fiscalizador
nem um código de ética profissional oficial único para quem atua na
área, só códigos voluntários de entidades como ACM e IEEE-CS.

**Pré-requisitos:** Aula 1 (mapa de atores, responsabilidade
compartilhada) e Aula 2 (teorias éticas, Ciclo Ético — retomado ao final
desta aula em comparação com um processo análogo de 5 passos proposto
por Maciel & Viterbo, Cap. 7).

**Objetivos de aprendizagem** (do `index.md`, Lesson 3):
- **Objectives:** Mapear o campo da computação, discutir a relevância e
  aplicação de códigos de ética profissionais (ACM, SBC, IEEE), e
  examinar o escopo das responsabilidades profissionais ativas e
  passivas perante a sociedade.
- **Expected Competencies:** Capacidade de alinhar práticas técnicas a
  códigos de ética profissionais estabelecidos e avaliar responsabilidade
  individual em cenários de falha de software ou dano social.

**Leitura recomendada** (`index.md`, corrigida nesta sessão — ver nota
abaixo): Maciel & Viterbo (2020), Vol. 1, Cap. 1 "A Formação em
Computação", Cap. 5 "Regulamentação da Profissão", e Cap. 7 "Ética
Profissional em Computação"; Van de Poel & Royakkers (2011), Cap. 2
"Codes of Conduct".

> **Nota sobre a correção de fontes:** a leitura recomendada original
> citava "Capítulo 1: Panorama do Ensino Superior em Computação no
> Brasil" e "Capítulo 5: O Exercício da Profissão em Computação e os
> Aspectos Regulatórios no Brasil" — **nenhum dos dois títulos existe**
> no livro. Confirmado pelo sumário real do Vol. 1: Cap. 1 é "A formação
> em computação", Cap. 5 é "Regulamentação da profissão". Corrigidos, e
> adicionado o Cap. 7 "Ética profissional em computação" — ausente da
> leitura original, mas o capítulo mais diretamente relevante ao
> objetivo de códigos de ética profissionais (ACM, IEEE-CS).

## Plano de aula — Aula 3 (carga horária nominal: ~50min)

> Mesma ressalva das aulas anteriores: o conteúdo em texto/slides é mais
> profundo do que cabe em 50 min falados — o professor escolhe, ao vivo,
> quanto detalhar.

1.  **Abertura: um código que não protegeu quem o seguiu** (~5–8 min) —
    O caso **BART** (Van de Poel & Royakkers, Cap. 2, pp. 32–33): três
    engenheiros do Bay Area Rapid Transport Project, demitidos em 1972
    depois de alertar a diretoria (contornando a hierarquia) sobre falhas
    de segurança no sistema de trem automatizado. O IEEE interveio com
    uma carta *amicus curiae* argumentando que o código profissional
    obriga o engenheiro a zelar pela segurança pública — mas isso não
    impediu a demissão. Três semanas depois, um acidente do sistema
    confirmou o alerta. **Pergunta de abertura:** se seguir o código
    profissional não protege quem o segue, para que serve um código de
    conduta?

2.  **O que é (e não é) um código de conduta** (~12–15 min) — Van de Poel
    & Royakkers, §2.2: distinção entre **códigos profissionais**
    (formulados por associações, ex. IEEE, NSPE) e **códigos
    corporativos** (formulados por empresas); os três objetivos possíveis
    de um código — **aspiracional** (expressar valores), **consultivo**
    (ajudar no julgamento moral cotidiano), **disciplinar** (garantir
    conformidade). Concretizar com os códigos de computação específicos
    do Brasil e do mundo (Maciel & Viterbo, Cap. 7): os **Dez
    Mandamentos da Ética na Computação** (Computer Ethics Institute) como
    exemplo de código consultivo memorável e simples; os códigos da
    **ACM** e do **IEEE-CS/ACM** (este último voltado especificamente à
    engenharia de software) como os dois códigos formais mais citados
    hoje na área. Nota: nenhum dos dois é vinculado a um conselho
    fiscalizador brasileiro — ambos são adesão voluntária.

3.  **Os limites conhecidos dos códigos** (~10–12 min) — Van de Poel &
    Royakkers, §2.3: **autointeresse e *window-dressing*** (caso Google
    na China — a "Grande Firewall" e a tensão entre a missão declarada e
    a prática real); **vagueza e contradições potenciais** (o problema da
    "lealdade" ao empregador — lealdade crítica vs. acrítica —, e a
    inconsistência entre códigos quanto a confidencialidade vs. dever de
    informar o público, reconectando com o dilema do *whistleblower* já
    visto nas Aulas 1 e 2); **pode-se viver pelo código?** (o próprio
    caso BART reaberto — seguir o código pode entrar em conflito direto
    com a sobrevivência no emprego). Fechar com a observação de que
    nenhuma dessas críticas invalida os códigos — só mostra que eles são
    ponto de partida, não substituto, para o julgamento moral (ecoando o
    fechamento da Aula 2: nenhuma teoria/código decide por você).

4.  **Mapeando a profissão no Brasil: por que a Informática não é
    regulamentada** (~12–15 min, núcleo brasileiro da aula) — Maciel &
    Viterbo, Cap. 5: contexto de como funcionam os **conselhos de
    profissão** no Brasil (CREA para engenharia, CRM para medicina, OAB
    para direito) — autarquias que registram profissionais e podem impedir
    o exercício ilegal da profissão; o fato de que, de mais de 2400
    ocupações reconhecidas no país, apenas ~68 são regulamentadas, e a
    Informática **não está entre elas**, apesar de décadas de tentativas
    desde 1978. Uma lista rica de vantagens/desvantagens já argumentadas
    no próprio livro para regulamentar a profissão (custo de anuidades,
    redução da flexibilidade multidisciplinar histórica da área — citada
    também no Cap. 1 —, mas também falta de garantia de qualidade e de
    proteção contra profissionais de baixa competência). Conectar
    diretamente com o Bloco 2: é exatamente por essa ausência de
    regulamentação que **não existe um código de ética profissional
    oficial único** para computação no Brasil — só a adesão voluntária a
    códigos como o da ACM.

5.  **Fechamento: um caso para aplicar, e ponte** (~8–10 min) — Usar o
    caso **Edward Snowden** (Maciel & Viterbo, Cap. 7, §7.5) —
    vigilância em massa da NSA revelada por um ex-prestador de serviços —
    como provocação final, sem resolver: quais códigos profissionais
    (ACM? Nenhum formal aplicável, já que Snowden não era necessariamente
    "engenheiro" registrado em conselho algum) se aplicariam, e como? O
    livro-fonte propõe seu próprio processo de 5 passos para deliberação
    ética (identificar fatos → definir dilema/valores → identificar
    interessados → identificar alternativas → identificar consequências)
    — comparar brevemente com o Ciclo Ético da Aula 2 (mesma lógica,
    formulação mais enxuta, sem fase de reflexão final explícita) para
    mostrar que a estrutura de deliberação ética se repete em fontes
    independentes. Fechar com a ponte para a Aula 4 (Parte 2 do curso:
    impactos ambientais e materiais da computação).
