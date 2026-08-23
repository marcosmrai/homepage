# Fontes usadas — Aula 1

> Trechos literais extraídos em 2026-08-10 de `../fontes/prml.pdf` (Bishop,
> 2006). Offset confirmado entre página impressa e página do PDF: **+20**
> (ex.: p. 78 impressa = página 98 do PDF), mesmo offset já usado em
> `supervised`.
>
> **DLFC não foi localizado para os tópicos desta aula dentro do esforço
> desta sessão** — não encontrei rapidamente a seção equivalente sobre a
> Gaussiana multivariada (a estrutura de capítulos do DLFC não espelha a do
> PRML aqui). Fica como pendência caso se queira o par PRML+DLFC completo,
> como em `supervised`; por ora só o PRML está citado.

### Fonte 1: Bishop (2006, PRML), §2.3, eq. 2.42–2.43, p. 78
**Uso pretendido:** definição formal da Gaussiana univariada e multivariada (Bloco 3).

**Trecho:**
> "In the case of a single variable x, the Gaussian distribution can be
> written in the form N(x|μ,σ²) = ... For a D-dimensional vector x, the
> multivariate Gaussian distribution takes the form
> N(x|μ,Σ) = 1/(2π)^(D/2) · 1/|Σ|^(1/2) · exp{-1/2 (x-μ)ᵀΣ⁻¹(x-μ)}
> where μ is a D-dimensional mean vector, Σ is a D×D covariance matrix, and
> |Σ| denotes the determinant of Σ."

---

### Fonte 2: Bishop (2006, PRML), §2.3, p. 78
**Uso pretendido:** por que a Gaussiana é a escolha natural — máxima entropia e Teorema Central do Limite (Bloco 3).

**Trecho:**
> "we have already seen that for a single real variable, the distribution
> that maximizes the entropy is the Gaussian. This property applies also
> to the multivariate Gaussian. [...] the central limit theorem (due to
> Laplace) tells us that, subject to certain mild conditions, the sum of a
> set of random variables, which is of course itself a random variable,
> has a distribution that becomes increasingly Gaussian as the number of
> terms in the sum increases."

---

### Fonte 3: Bishop (2006, PRML), §2.3, eq. 2.44, p. 80
**Uso pretendido:** definição da distância de Mahalanobis (Bloco 5) — citação central da aula.

**Trecho:**
> "Δ² = (x − μ)ᵀΣ⁻¹(x − μ) [...] which appears in the exponent. The
> quantity Δ is called the Mahalanobis distance from μ to x and reduces to
> the Euclidean distance when Σ is the identity matrix."

---

### Fonte 4: Bishop (2006, PRML), §2.3, pp. 80–81
**Uso pretendido:** interpretação geométrica de $\Sigma$ via autovetores/autovalores — as elipses de densidade constante (Bloco 3).

**Trecho:**
> "The quadratic form, and hence the Gaussian density, will be constant on
> surfaces for which (2.51) is constant. If all of the eigenvalues λᵢ are
> positive, then these surfaces represent ellipsoids, with their centres
> at μ and their axes oriented along uᵢ, and with scaling factors in the
> directions of the axes given by λᵢ^(1/2), as illustrated in Figure 2.7."

---

### Fonte 5: Bishop (2006, PRML), §2.3, p. 84
**Uso pretendido:** restringir $\Sigma$ à diagonal = supor independência entre dimensões; o preço dessa restrição (Bloco 6, item c).

**Trecho:**
> "If we consider restricted forms of the covariance matrix. If we
> consider covariance matrices that are diagonal, so that Σ = diag(σᵢ²),
> then we have a total of 2D independent parameters in the density model.
> The corresponding contours of constant density are given by axis-aligned
> ellipsoids. [...] Unfortunately, whereas such approaches limit the number
> of degrees of freedom in the distribution and make inversion of the
> covariance matrix a much faster operation, they also greatly restrict the
> form of the probability density and limit its ability to capture
> interesting correlations in the data."

---

### Fonte 6: Bishop (2006, PRML), §2.3.4, eqs. 2.118–2.122, pp. 93–94
**Uso pretendido:** derivação da máxima verossimilhança para $\hat{\boldsymbol\mu}$ e $\hat\Sigma$ (Bloco 4).

**Trecho:**
> "Given a data set X = (x1,...,xN)ᵀ in which the observations {xn} are
> assumed to be drawn independently from a multivariate Gaussian
> distribution, we can estimate the parameters of the distribution by
> maximum likelihood. [...] μ_ML = (1/N)∑ₙ xₙ [...] Σ_ML = (1/N)∑ₙ(xₙ −
> μ_ML)(xₙ − μ_ML)ᵀ"

---

### Fonte 7 *(bônus, não usada no plano original — ver nota)*: Bishop (2006, PRML), §2.3.4, eqs. 2.123–2.125, p. 94
**Uso pretendido:** viés do estimador de máxima verossimilhança da covariância, e a correção $N-1$ — relevante para o Bloco 4 (armadilha do $N>d$), ainda não incorporada ao `00-plano-aula.md`.

**Trecho:**
> "We see that the expectation of the maximum likelihood estimate for the
> mean is equal to the true mean. However, the maximum likelihood estimate
> for the covariance has an expectation that is less than the true value,
> and hence it is biased. We can correct for this bias by defining a
> different estimator Σ̃ given by Σ̃ = 1/(N−1) ∑ₙ(xₙ−μ_ML)(xₙ−μ_ML)ᵀ."

---

## Pendências e itens sem citação nos livros

- **Distribuição qui-quadrado da distância de Mahalanobis** ($D_M(\mathbf{x})^2\sim\chi^2_d$ quando $\mathbf{x}\sim\mathcal{N}(\boldsymbol\mu,\Sigma)$, usada no Bloco 6): **não localizada no PRML nem no DLFC.** É um resultado padrão de estatística multivariada clássica (não um tópico de ML per se), derivado diretamente na sessão de planejamento — não copiado de fonte alguma. Verificação feita: $Y=\Sigma^{-1/2}(\mathbf{X}-\boldsymbol\mu)\sim\mathcal{N}(0,I_d)$, e $Y^TY=\sum_i Y_i^2$ é soma de $d$ quadrados de normais padrão independentes, que é a definição de $\chi^2_d$.
- **Teste combinado de Fisher** ($-2\sum_i\ln p_i \sim \chi^2_{2d}$, Bloco 6, item c): mesmo caso — resultado padrão de estatística clássica, não localizado no PRML/DLFC, não copiado.
- **Distribuição empírica vs. teórica** (Bloco 2): framing conceitual, sem citação de página específica ainda — considerar buscar em PRML §2.5 (Nonparametric Methods) se quiser lastro bibliográfico aqui também.
- **DLFC**: não localizado para os tópicos desta aula (ver aviso no topo). Considerar se vale o esforço de procurar, dado que o PRML já cobre tudo com solidez.
- `esl.pdf` (Elements of Statistical Learning) foi linkado mas não usado nesta aula — não verifiquei se cobre Mahalanobis/anomaly detection; pode ser fonte para o qui-quadrado se alguém quiser lastro bibliográfico para esse ponto.
