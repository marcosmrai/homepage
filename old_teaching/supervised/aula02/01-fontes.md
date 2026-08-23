# Fontes usadas — Aula 2

> Trechos literais preenchidos em 2026-08-09 a partir dos PDFs em
> `../fontes/prml.pdf` (Bishop, 2006) e `../fontes/dlfc.pdf` (Bishop &
> Bishop, 2024), agora linkados. **Atenção:** o offset entre página
> impressa e página do arquivo PDF é +20 para os dois livros na maior
> parte do texto (confirmado nos capítulos 1–5), mas cai para +18 no DLFC
> por volta do capítulo 6 (provavelmente uma página de abertura de parte
> não numerada) — as páginas abaixo foram confirmadas lendo o número
> impresso em cada página, não assumidas por offset fixo.
>
> Numeração de blocos conforme `00-plano-aula.md` (Blocos 0–6, já com o
> Bloco 1 encurtado e os antigos Blocos 5+6 fundidos).

### Fonte 1: Bishop (2006, PRML), §1.4, pp. 33–38
**Uso pretendido:** a maldição da dimensionalidade — $M^d$ células, intuição geométrica do volume concentrado na casca (Bloco 1).

**Trecho:**
> "The problem with an exponentially large number of cells is that we
> would need an exponentially large quantity of training data in order to
> ensure that the cells are not empty." (p. 35)
>
> "we arrive at the remarkable result that, in spaces of high
> dimensionality, most of the volume of a sphere is concentrated in a thin
> shell near the surface!" (p. 36)
>
> "The severe difficulty that can arise in spaces of many dimensions is
> sometimes called the curse of dimensionality (Bellman, 1961)." (p. 36)

---

### Fonte 2: Bishop & Bishop (2024, DLFC), §6.1.1, pp. 172–174
**Uso pretendido:** tratamento moderno da maldição da dimensionalidade (Bloco 1).

**Trecho:**
> "The challenge with an exponentially large number of cells is that we
> would need an exponentially large quantity of training data to ensure
> that the cells are not empty." (p. 174 impressa — ver aviso de offset no
> topo deste arquivo)

---

### Fonte 3: Bishop (2006, PRML), §1.2, pp. 14–24
**Uso pretendido:** regra da soma e do produto — mesma fonte da Aula 1 (Fonte 9), agora generalizada para $K$ classes (Bloco 2).

**Trecho:**
> "sum rule  p(X) = ∑Y p(X, Y)  (1.10)
> product rule  p(X, Y) = p(Y|X)p(X).  (1.11)" (p. 14)
>
> "p(Y|X) = p(X|Y)p(Y) / p(X)  (1.12)
>
> which is called Bayes' theorem and which plays a central role in pattern
> recognition and machine learning." (p. 15)

---

### Fonte 4: Bishop & Bishop (2024, DLFC), §2.1.5–2.1.6, pp. 31–32
**Uso pretendido:** priori, posteriori, variáveis independentes — extensão a $K$ classes (Bloco 2).

**Trecho:**
> "In this example, the prior probability of having cancer is 1%. However,
> once we have observed that the test result is positive, we find that
> the posterior probability of cancer is now 23%, which is a substantially
> higher probability of cancer, as we would intuitively expect." (p. 31)
>
> "Finally, if the joint distribution of two variables factorizes into the
> product of the marginals, so that p(X, Y) = p(X)p(Y), then X and Y are
> said to be independent." (p. 31)

---

### Fonte 5: Bishop (2006, PRML), §1.5.4, eqs. 1.84–1.85, p. 46
**Uso pretendido:** independência condicional e o modelo Naive Bayes — definição formal (Bloco 3). Mesmo exemplo do diagnóstico por radiografia + sangue que a Aula 1 poderia ter usado; aqui é a primeira aparição de fato.

**Trecho:**
> "p(xI, xB|Ck) = p(xI|Ck)p(xB|Ck).  (1.84)
>
> This is an example of conditional independence property, because the
> independence holds when the distribution is conditioned on the class
> Ck." (p. 46)
>
> "The particular conditional independence assumption (1.84) is an example
> of the naive Bayes model." (p. 46)

---

### Fonte 6: Bishop & Bishop (2024, DLFC), §5.3, §5.3.1–5.3.2, pp. 150–156
**Uso pretendido:** classificadores generativos, tratamento moderno (Bloco 3).

**Trecho:**
> "We turn next to a probabilistic view of classification and show how
> models with linear decision boundaries arise from simple assumptions
> about the distribution of the data." (p. 150)
>
> "We see that the quadratic terms in x from the exponents of the Gaussian
> densities have cancelled (due to the assumption of common covariance
> matrices), leading to a linear function of x in the argument of the
> logistic sigmoid." (p. 152)

---

### Fonte 7: Bishop (2006, PRML), §4.2.1, pp. 198–200
**Uso pretendido:** entradas contínuas com covariância compartilhada → fronteira linear (Bloco 4 e Bloco 5, item 3 — a mesma matemática serve às duas perguntas: "o que a suposição custa" e "quando a razão é linear").

**Trecho:**
> "Let us assume that the class-conditional densities are Gaussian and
> then explore the resulting form for the posterior probabilities. To
> start with, we shall assume that all classes share the same covariance
> matrix." (p. 198)
>
> "We see that the quadratic terms in x from the exponents of the Gaussian
> densities have cancelled (due to the assumption of common covariance
> matrices) leading to a linear function of x in the argument of the
> logistic sigmoid." (p. 198)

---

### Fonte 8: Bishop (2006, PRML), §4.2.3, eqs. 4.81–4.82, p. 202
**Uso pretendido:** atributos discretos/binários sob Naive Bayes → fronteira linear (Bloco 4 e Bloco 5, item 3, mesmo motivo da Fonte 7).

**Trecho:**
> "Here we will make the naive Bayes assumption in which the feature
> values are treated as independent, conditioned on the class Ck. Thus we
> have class-conditional distributions of the form
>
> p(x|Ck) = ∏(i=1 to D) μki^xi (1 − μki)^(1−xi)  (4.81)
>
> which contain D independent parameters for each class." (p. 202)
>
> "ak(x) = ∑(i=1 to D) {xi ln μki + (1 − xi) ln(1 − μki)} + ln p(Ck)  (4.82)
>
> which again are linear functions of the input values xi." (p. 202)

---

### Fonte 9: Bishop (2006, PRML), §4.2, eqs. 4.57–4.63, pp. 196–198
**Uso pretendido:** modelos generativos probabilísticos; a posteriori como softmax de funções lineares das ativações — liga a linearidade do Bloco 5 ao caso $K$-classes (Bloco 5).

**Trecho:**
> "For the case of K > 2 classes we have
>
> p(Ck|x) = exp(ak) / ∑j exp(aj),  (4.62)
>
> which is known as the normalized exponential and can be regarded as a
> multiclass generalization of the logistic sigmoid." (p. 198)
>
> "The normalized exponential is also known as the softmax function, as it
> represents a smoothed version of the 'max' function." (p. 198)

---

### Fonte 10: Bishop (2006, PRML), §1.5, §1.5.2–1.5.3, pp. 38–42
**Uso pretendido:** teoria da decisão geral — espaço de decisões, perda esperada, opção de rejeição — generalizada aqui para $K$ classes e espaço de ações arbitrário (Bloco 5, itens 1, 2 e 4). Mesma seção já citada na Aula 1 (Fontes 4 e 5), agora usada na sua forma geral, não só no caso binário.

**Trecho:**
> "Here we turn to a discussion of decision theory that, when combined
> with probability theory, allows us to make optimal decisions in
> situations involving uncertainty such as those encountered in pattern
> recognition." (p. 38)
>
> "We can formalize such issues through the introduction of a loss
> function, also called a cost function, which is a single, overall
> measure of loss incurred in taking any of the available decisions or
> actions." (p. 41)
>
> "We can achieve this by introducing a threshold θ and rejecting those
> inputs x for which the largest of the posterior probabilities p(Ck|x) is
> less than or equal to θ." (p. 42)

---

### Fonte 11 *(opcional — ver pendência abaixo)*: Bishop (2006, PRML), §8.2.2, Figura 8.24, pp. 380–381
**Uso pretendido:** Naive Bayes como grafo probabilístico — mencionado no fechamento do Bloco 3, se houver tempo (não é essencial ao argumento).

**Trecho:**
> "Figure 8.24 A graphical representation of the 'naive Bayes' model for
> classification. Conditioned on the class label z, the components of the
> observed vector x = (x1,...,xD)^T are assumed to be independent." (p. 380)

**Bônus não planejado, mas relevante para o Bloco 4:** a mesma seção (p. 381)
contém a frase que resolve a pendência da fonte externa abaixo — ver nota.

---

## Resolvido: "classifica bem, estima mal" (Bloco 4) — sem fonte externa

Decisão anterior (usuário): demonstrar o fenômeno só com simulação, sem
citar Domingos & Pazzani (1997) formalmente. Ao ler PRML §8.2.2 para a
Fonte 11 (acima), apareceu — sem que eu tivesse procurado por isso — uma
frase do próprio PRML que sustenta exatamente esse argumento, na mesma
página da figura do grafo Naive Bayes:

> "Nevertheless, even if this assumption is not precisely satisfied, the
> model may still give good classification performance in practice because
> the decision boundaries can be insensitive to some of the details in the
> class-conditional densities, as illustrated in Figure 1.27." (p. 381)

Isso é melhor do que a solução planejada: em vez de "sem citação formal",
o Bloco 4 agora tem uma citação literal do PRML que diz precisamente a
mesma coisa que a simulação demonstra. Não precisa do artigo de Domingos &
Pazzani. Adicionar esta fonte como uma **Fonte 12** informal (mesma
localização da Fonte 11, §8.2.2, p. 381) se o bloco citar isso
explicitamente no `02-aula.qmd`.

## Notas sobre as fontes

Naive Bayes não é um tópico de primeira classe em nenhum dos dois livros.
No PRML ele aparece de passagem: como exemplo em §1.5.4 (p. 46), como caso
particular de modelo generativo com atributos discretos em §4.2.3 (p. 202),
e como exemplo de grafo em §8.2.2 (p. 380, Fonte 11, opcional). O livro de
2024 segue a mesma estrutura em §5.3. Isso é tratado como vantagem para o
desenho da aula: o Bishop nunca trata Naive Bayes como algoritmo, e sim como
suposição estrutural aplicada a um modelo generativo — exatamente o
enquadramento do curso.
