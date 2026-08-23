# Fontes usadas — Aula 3

> Trechos literais extraídos lendo diretamente as páginas do PDF nesta
> sessão (não reescritos de memória). Offset confirmado: PRML tem offset
> +20 (página impressa 663 = página 683 do PDF), o mesmo já usado nas
> Aulas 1 e 2 desta disciplina — verificado de novo aqui, não assumido.
>
> Por pedido explícito do usuário, esta aula usa **poucas citações**,
> reservadas ao essencial para ancorar as definições e fórmulas centrais
> — a exposição pedagógica no `02-aula.qmd` é nossa, não uma paráfrase
> encadeada do livro.

---

### Fonte 1: PRML, §14.4, p. 663
**Uso pretendido:** definição de árvores de decisão (CART) e a ideia de
particionamento recursivo do espaço de entrada (Bloco 1).

**Trecho:**
> "There are various simple, but widely used, models that work by
> partitioning the input space into cuboid regions, whose edges are
> aligned with the axes, and then assigning a simple model (for example,
> a constant) to each region. [...] Here we focus on a particular
> tree-based framework called *classification and regression trees*, or
> *CART* (Breiman *et al.*, 1984)."

---

### Fonte 2: PRML, §14.4, p. 664
**Uso pretendido:** setup do problema de regressão numa árvore — a
predição ótima por região é a média dos alvos ali contidos (Bloco 2).

**Trecho:**
> "Consider first a regression problem in which the goal is to predict a
> single target variable $t$ from a $D$-dimensional vector
> $\mathbf{x} = (x_1,\dots,x_D)^T$ of input variables. [...] If the
> partitioning of the input space is given, [...] the optimal value of
> the predictive variable within any given region is just given by the
> average of the values of $t_n$ for those data points that fall in that
> region."

---

### Fonte 3: PRML, §14.4, p. 665
**Uso pretendido:** por que o crescimento da árvore é guloso (busca
exaustiva variável-a-variável), não uma otimização conjunta da estrutura
inteira; e a fórmula da soma de quadrados residuais e do critério de
poda por custo-complexidade (Blocos 2 e 4).

**Trecho:**
> "Even for a fixed number of nodes in the tree, the problem of
> determining the optimal structure [...] to minimize the sum-of-squares
> error is usually computationally infeasible [...]. Instead, a greedy
> optimization is generally done by starting with a single root node
> [...] and then growing the tree by adding nodes one at a time." (p. 665)
>
> "Suppose the leaf nodes are indexed by $\tau = 1,\dots,|T|$, with leaf
> node $\tau$ representing a region $\mathcal{R}_\tau$ of input space
> having $N_\tau$ data points, and $|T|$ denoting the total number of
> leaf nodes. The optimal prediction for region $\mathcal{R}_\tau$ is
> then given by
> $$y_\tau = \frac{1}{N_\tau}\sum_{\mathbf{x}_n\in\mathcal{R}_\tau} t_n
> \qquad (14.29)$$
> and the corresponding contribution to the residual sum-of-squares is
> then
> $$Q_\tau(T) = \sum_{\mathbf{x}_n\in\mathcal{R}_\tau} \{t_n -
> y_\tau\}^2. \qquad (14.30)$$
> The pruning criterion is then given by
> $$C(T) = \sum_{\tau=1}^{|T|} Q_\tau(T) + \lambda|T| \qquad (14.31)$$
> The regularization parameter $\lambda$ determines the trade-off
> between the overall residual sum-of-squares error and the complexity
> of the model [...], and its value is chosen by cross-validation." (p. 665)
>
> "It is found empirically that often none of the available splits
> produces a significant reduction in error, and yet after several more
> splits a substantial error reduction is found. For this reason, it is
> common practice to grow a large tree [...] and then prune back the
> resulting tree." (p. 665)

---

### Fonte 4: PRML, §14.4, p. 666
**Uso pretendido:** os dois critérios de impureza usados para classificação —
cross-entropy e índice de Gini — e a nota de precisão sobre a
inconsistência de sinal na descrição da cross-entropy (Bloco 3).

**Trecho:**
> "For classification problems, the process of growing and pruning the
> tree is similar, except that the sum-of-squares error is replaced by a
> more appropriate measure of performance. If we define $p_{\tau k}$ to
> be the proportion of data points in region $\mathcal{R}_\tau$ assigned
> to class $k$, where $k = 1,\dots,K$, then two commonly used choices are
> the cross-entropy
> $$Q_\tau(T) = \sum_{k=1}^K p_{\tau k}\ln p_{\tau k} \qquad (14.32)$$
> and the *Gini index*
> $$Q_\tau(T) = \sum_{k=1}^K p_{\tau k}(1-p_{\tau k}). \qquad (14.33)$$
> These both vanish for $p_{\tau k}=0$ and $p_{\tau k}=1$ and have a
> maximum at $p_{\tau k}=0.5$."

**Nota de precisão:** a fórmula da cross-entropy (14.32), impressa sem o
sinal negativo padrão da entropia, não bate com a descrição em prosa
logo abaixo ("máximo em $p_{\tau k}=0{,}5$"). Verificado numericamente
(script à parte, não incluído na aula): a fórmula **como impressa** vale
$0$ nas bordas e é **mínima** (mais negativa) em $p=0{,}5$ — o oposto do
que o texto descreve. A entropia padrão $H(p) = -\sum p\ln p$ (com o
sinal) é que tem máximo em $p=0{,}5$, batendo com a prosa. Usamos a
convenção padrão na aula; o trecho acima preserva a fórmula exatamente
como impressa, sem "corrigi-la" na citação.

---

### Fonte 5: PRML, §14.4, p. 666
**Uso pretendido:** por que a taxa de erro de classificação não é usada
para crescer a árvore, mas é preferida para podar (Bloco 3).

**Trecho:**
> "The cross entropy and the Gini index are better measures than the
> misclassification rate for growing the tree because they are more
> sensitive to the node probabilities. Also, unlike misclassification
> rate, they are differentiable and hence better suited to gradient
> based optimization methods. For subsequent pruning of the tree, the
> misclassification rate is generally used."

---

### Fonte 6: PRML, §14.4, p. 666
**Uso pretendido:** as três limitações estruturais das árvores discutidas
no Bloco 5 (fechamento).

**Trecho:**
> "The human interpretability of a tree model such as CART is often seen
> as its major strength. However, in practice it is found that the
> particular tree structure that is learned is very sensitive to the
> details of the data set, so that a small change to the training data
> can result in a very different set of splits (Hastie *et al.*, 2001).
> [...] One is that the splits are aligned with the axes of the feature
> space, which may be very suboptimal. For instance, to separate two
> classes whose optimal decision boundary runs at 45 degrees to the axes
> would need a large number of axis-parallel splits [...] as compared to
> a single non-axis-aligned split. Furthermore, the splits in a decision
> tree are hard, so that each region of input space is associated with
> one, and only one, leaf node model. The last issue is particularly
> problematic in regression where we are typically aiming to model
> smooth functions, and yet the tree model produces piecewise-constant
> predictions with discontinuities at the split boundaries."

---

## Pendências e notas

- Por pedido do usuário ("não use os livros tanto assim"), esta aula
  tem propositalmente menos fontes citadas que as Aulas 1 e 2 — as 6
  acima cobrem só o essencial factual/formal (definição, fórmulas de
  regressão, poda, critérios de impureza, limitações). A exposição, os
  exemplos numéricos e as conexões pedagógicas (verossimilhança,
  contraexemplos, pontes com outras aulas) no `02-aula.qmd` são
  construção nossa, não citação.
- ESL (Hastie, Tibshirani & Friedman), Cap. 9 §9.2, permanece disponível
  como leitura de apoio/opcional (decisão já tomada), mas não foi citado
  nesta aula — o PRML já cobre o essencial.
