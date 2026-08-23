## Resumo — Aula 1: Data Space, Parametric Generative Models, and Anomalies

Esta é a primeira aula do curso, e a primeira vez que os alunos veem
aprendizado **sem rótulo algum** — nem implícito. A pergunta central é: o
que significa "modelar dados" quando não há $y$ para prever? A resposta
desta aula é a mais simples possível: assumir que os dados foram gerados
por uma distribuição teórica conhecida (Gaussiana multivariada), ajustá-la
por máxima verossimilhança, e usar a verossimilhança de um ponto novo sob
esse modelo para decidir se ele é típico ou anômalo. A aula generaliza a
lógica de limiar-por-quantil (familiar de detecção de anomalias
unidimensional) para $d$ dimensões via distância de Mahalanobis, e fecha
com a identidade exata que torna o limiar rigoroso: a distância de
Mahalanobis ao quadrado de um ponto gaussiano segue qui-quadrado com $d$
graus de liberdade.

**Pré-requisitos:** probabilidade básica (vetor aleatório, média, matriz de
covariância), álgebra linear básica (inversa e determinante de matriz,
formas quadráticas). Nenhuma aula anterior do curso — é a Aula 1.

**Objetivos de aprendizagem** (do `index.md`, Lesson 1):
- **ML Concept:** O que significa "modelar dados" sem rótulos; *profiling*
  para identificar comportamentos atípicos.
- **Statistical Concept:** Distribuição empírica vs. teórica; assumir que
  os dados foram gerados por uma distribuição teórica conhecida (Gaussiana
  multivariada); usar a verossimilhança de um ponto sob o modelo ajustado
  para definir regiões de exclusão estatística.
- **Objectives:** Entender como ajustar distribuições teóricas a dados não
  rotulados e usar verossimilhança para detecção de anomalias.
- **Expected Competencies:** Ajustar uma Gaussiana multivariada a dados e
  definir limiares de anomalia robustos, baseados em probabilidade.

## Plano de aula — Aula 1 (carga horária: ~120min)

**Ajuste (feedback do usuário sobre o rascunho anterior):** o Bloco 6
original só definia um limiar fixo (dentro/fora) — faltava a pergunta mais
fundamental de detecção de anomalia não-supervisionada: "qual a
probabilidade de ver algo tão extremo quanto este ponto, se ele viesse do
modelo ajustado?" Bloco 6 reescrito para responder isso via $p$-valor, e
para contrastar a versão conjunta (Mahalanobis, cara) com a versão por
dimensão sob suposição de independência (barata, cega à correlação) — o
mesmo trade-off do Naive Bayes, agora em teste de hipótese. Tempo subiu de
~110 para ~120 min.

1.  **Abertura: modelar dados sem rótulos** (~10 min) — Contraste explícito
    com aprendizado supervisionado: não há $y$, só $\mathbf{x}_1,\dots,\mathbf{x}_N$.
    A pergunta deixa de ser "que função prever" e passa a ser "que forma
    esses dados têm". *Profiling*: descrever o comportamento típico de uma
    população para depois reconhecer o que se desvia dele (fraude, falha de
    sensor, transação suspeita).

2.  **Distribuição empírica vs. teórica** (~15 min) — O histograma/a
    distribuição empírica $\hat{p}(\mathbf{x})$ é sempre calculável, mas é
    ruidosa e não generaliza para pontos não vistos. A aposta desta aula:
    assumir que os dados vieram de uma família teórica conhecida (Gaussiana
    multivariada) troca ruído por estrutura — ao custo de a suposição poder
    estar errada. Motivar com um exemplo 2D (ex.: duas medidas de sensores
    correlacionadas) antes de formalizar.

3.  **A Gaussiana Multivariada: forma e parâmetros** (~20 min) — Definição
    $\mathcal{N}(\mathbf{x}\mid\boldsymbol\mu,\Sigma)$, papel geométrico de
    $\boldsymbol\mu$ (centro) e $\Sigma$ (forma/orientação das elipses de
    densidade constante — autovalores/autovetores de $\Sigma$). Por que é a
    escolha natural como *default*: Teorema Central do Limite, e é a
    distribuição de máxima entropia dada média e covariância fixas (citar,
    não provar em detalhe nesta aula).

4.  **Ajuste por Máxima Verossimilhança** (~15 min) — Derivar
    $\hat{\boldsymbol\mu} = \bar{\mathbf{x}}$,
    $\hat\Sigma = \frac{1}{N}\sum_n(\mathbf{x}_n-\bar{\mathbf{x}})(\mathbf{x}_n-\bar{\mathbf{x}})^T$
    maximizando a log-verossimilhança. Armadilha prática a anunciar: $\hat\Sigma$
    só é invertível se $N > d$ (mais amostras que dimensões) — antecipa a
    maldição da dimensionalidade da Aula 2.

5.  **Da Verossimilhança à Distância de Mahalanobis** (~20 min) — Mostrar
    que comparar $p(\mathbf{x})$ com um limiar é equivalente a comparar a
    forma quadrática do expoente,
    $D_M(\mathbf{x})^2 = (\mathbf{x}-\hat{\boldsymbol\mu})^T\hat\Sigma^{-1}(\mathbf{x}-\hat{\boldsymbol\mu})$,
    com um limiar — a **distância de Mahalanobis**. Diferença crucial com a
    distância Euclidiana: Mahalanobis "estica" o espaço pelas direções de
    baixa variância, então dois pontos igualmente distantes em Euclidiana
    podem ter distâncias de Mahalanobis muito diferentes se um está ao
    longo do eixo de alta correlação e outro não.

6.  **Da posição ao $p$-valor: qual a probabilidade de ver algo tão
    extremo?** (~30 min, ampliado) — O resultado que fecha a aula com
    rigor: se $\mathbf{x}\sim\mathcal{N}(\boldsymbol\mu,\Sigma)$, então
    $D_M(\mathbf{x})^2 \sim \chi^2_d$.

    a. **Do limiar fixo ao escore contínuo.** Em vez de só "dentro/fora" a
       $\alpha$ fixo, definir o **escore de anomalia como um $p$-valor**:
       $p(\mathbf{x}) = P\big(D_M(\mathbf{X}')^2 \ge D_M(\mathbf{x})^2 \mid \mathbf{X}'\sim\mathcal{N}(\hat{\boldsymbol\mu},\hat\Sigma)\big) = 1 - F_{\chi^2_d}\big(D_M(\mathbf{x})^2\big)$
       — literalmente "qual a probabilidade de um ponto do modelo ajustado
       ser tão extremo (ou mais) quanto $\mathbf{x}$". O limiar fixo é o
       caso particular $p(\mathbf{x}) < \alpha$; o $p$-valor é a versão
       graduada, que ordena os pontos por quão surpreendentes eles são, não
       só os separa em duas caixas.
    b. **Armadilha de interpretação (anunciar explicitamente):**
       $p(\mathbf{x})$ pequeno não significa "probabilidade de
       $\mathbf{x}$ pertencer à distribuição verdadeira" — significa
       "probabilidade de um ponto *do modelo ajustado* ser tão extremo
       quanto $\mathbf{x}$". É uma afirmação sobre o modelo, condicional a
       ele estar certo; não é uma afirmação sobre a origem de $\mathbf{x}$.
    c. **Conjunta vs. por dimensão — o mesmo trade-off do Naive Bayes, agora
       em teste de hipótese.** Calcular $D_M$ exige estimar e inverter
       $\hat\Sigma$ ($d(d+1)/2$ parâmetros — cara e instável quando $N$ não
       é $\gg d$, o mesmo alerta do Bloco 4). Alternativa mais barata:
       supor independência entre dimensões e calcular um $p$-valor **por
       dimensão**, $p_i(x_i) = P(|Z_i|\ge|z_i|)$, usando só a marginal
       $\mathcal{N}(\hat\mu_i,\hat\sigma_i^2)$ ($d$ parâmetros, não
       $d(d+1)/2$). Combinar os $d$ $p$-valores independentes via o teste
       de Fisher, $-2\sum_i \ln p_i(x_i) \sim \chi^2_{2d}$ — a versão
       "naive" do mesmo teste. **O preço:** um ponto que é normal em cada
       dimensão isoladamente mas quebra a relação de correlação entre elas
       (ex.: dois sensores que deveriam variar juntos, e não variam) passa
       o teste por dimensão e é pego pelo teste conjunto. Mesma lição da
       Aula 2 de "supervised" (preço da suposição de independência),
       aplicada aqui a teste de hipótese em vez de classificação.

    Visualizar: elipses de contorno em 2D nos quantis de $\chi^2_2$, um
    ponto com $p(\mathbf{x})$ baixo mas que passaria os dois testes
    marginais por dimensão — a ilustração concreta do item (c).

7.  **Armadilhas e Ponte para a Aula 2** (~10 min) — O que pode quebrar
    tudo: (a) dados genuinamente multimodais (duas populações distintas)
    não são bem descritos por uma única Gaussiana — o ajuste "funciona"
    matematicamente e mesmo assim mente; (b) outliers no próprio conjunto
    de ajuste contaminam $\hat{\boldsymbol\mu}$ e $\hat\Sigma$, then inflam
    o limiar e escondem exatamente o que se queria detectar (problema de
    robustez, não resolvido aqui). Ponte: a saída não-paramétrica — $k$-NN
    e KDE — é o assunto da Aula 2.
