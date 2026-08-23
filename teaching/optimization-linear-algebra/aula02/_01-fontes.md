# Fontes usadas — Aula 2

> Trechos literais extraídos em 2026-08-21 lendo diretamente as páginas do
> PDF nesta sessão (não reescritos de memória). Offset confirmado entre
> página impressa e página do PDF: **+6** (ex.: p. 19 impressa = página 25
> do PDF), o mesmo já usado na Aula 1 desta disciplina — verificado de novo
> aqui, não assumido.

---

### Fonte 1: MathML, §2.1 "Systems of Linear Equations", pp. 19–20
**Uso pretendido:** definição formal de sistema de equações lineares, e a
afirmação central do Bloco 3 — um sistema real tem nenhuma, exatamente uma,
ou infinitas soluções, com a conexão explícita à regressão linear feita
pelo próprio livro.

**Trecho:**
> "Equation (2.3) is the general form of a system of linear equations, and
> x1, . . . , xn are the unknowns of this system. Every n-tuple
> (x1, . . . , xn) ∈ Rn that satisfies (2.3) is a solution of the linear
> equation system."
>
> "In general, for a real-valued system of linear equations we obtain
> either no, exactly one, or infinitely many solutions. Linear regression
> (Chapter 9) solves a version of Example 2.1 when we cannot solve the
> system of linear equations."

---

### Fonte 2: MathML, §2.2 "Matrices", Definition 2.1 and Eq. 2.13, pp. 22–23
**Uso pretendido:** definição formal de matriz, e a fórmula do produto
matriz-matriz (da qual o produto matriz-vetor é caso particular) — base do
Bloco 2.

**Trecho:**
> "Definition 2.1 (Matrix). With m, n ∈ N a real-valued (m, n) matrix A is
> an m·n-tuple of elements aij, i = 1, . . . , m, j = 1, . . . , n, which
> is ordered according to a rectangular scheme consisting of m rows and n
> columns."
>
> "For matrices A ∈ Rm×n, B ∈ Rn×k, the elements cij of the product
> C = AB ∈ Rm×k are computed as
> cij = Σ(l=1 to n) ail blj, i = 1, . . . , m, j = 1, . . . , k.
> This means, to compute element cij we multiply the elements of the ith
> row of A with the jth column of B and sum them up."

**Nota:** a leitura de $A\mathbf{x}$ como combinação linear das colunas de
$A$ (usada no Bloco 2 desta aula) não está enunciada nesses termos no
MathML — é uma releitura direta e imediata da própria Eq. 2.13 (fixando
$k=1$), exposição nossa, não citação separada.

---

### Fonte 3: MathML, §2.4, Remark, p. 40
**Uso pretendido:** ponte explícita com a Aula 1 — o resultado "solução de
$A\mathbf{x}=\mathbf{0}$ é subespaço", já usado como exemplo na Aula 1,
citado aqui em sua forma geral (todo subespaço é solução de algum sistema
homogêneo), abrindo a generalização desta aula para $A\mathbf{x}=\mathbf{b}$.

**Trecho:**
> "Every subspace U ⊆ (Rn, +, ·) is the solution space of a homogeneous
> system of linear equations Ax = 0 for x ∈ Rn."

---

### Fonte 4: MathML, §2.5 "Linear Independence", Definitions 2.11–2.12, p. 40
**Uso pretendido:** definição formal de combinação linear e de independência
linear — base do Bloco 4.

**Trecho:**
> "Definition 2.11 (Linear Combination). Consider a vector space V and a
> finite number of vectors x1, . . . , xk ∈ V. Then, every v ∈ V of the
> form v = λ1x1 + · · · + λkxk = Σ(i=1 to k) λixi ∈ V with
> λ1, . . . , λk ∈ R is a linear combination of the vectors x1, . . . , xk."
>
> "Definition 2.12 (Linear (In)dependence). [...] If there is a non-trivial
> linear combination, such that 0 = Σ(i=1 to k) λixi with at least one
> λi ≠ 0, the vectors x1, . . . , xk are linearly dependent. If only the
> trivial solution exists, i.e., λ1 = . . . = λk = 0 the vectors
> x1, . . . , xk are linearly independent."
>
> "Intuitively, a set of linearly independent vectors consists of vectors
> that have no redundancy, i.e., if we remove any of those vectors from
> the set, we will lose something."

---

### Fonte 5: MathML, §2.6.2 "Rank", p. 47
**Uso pretendido:** definição formal de posto (*rank*), e suas duas
propriedades centrais para o Bloco 5 — posto completo/deficiente, e a
condição de solvabilidade de $A\mathbf{x}=\mathbf{b}$ via posto.

**Trecho:**
> "The number of linearly independent columns of a matrix A ∈ Rm×n equals
> the number of linearly independent rows and is called the rank of A and
> is denoted by rk(A)."
>
> "For all A ∈ Rm×n and all b ∈ Rm it holds that the linear equation
> system Ax = b can be solved if and only if rk(A) = rk(A|b), where A|b
> denotes the augmented system."
>
> "A matrix A ∈ Rm×n has full rank if its rank equals the largest possible
> rank for a matrix of the same dimensions. This means that the rank of a
> full-rank matrix is the lesser of the number of rows and columns, i.e.,
> rk(A) = min(m, n). A matrix is said to be rank deficient if it does not
> have full rank."

---

## Pendências e notas

- Produto interno/vetores como caso particular de matrizes ($n=1$) já foi
  citado na Aula 1 (Fonte 1 daquela aula) — não repetido aqui.
- `copt.pdf` e `optml.pdf` seguem reservados para a Parte 2/3 do curso
  (Aulas 6+), não usados nesta aula.
- Por pedido geral do projeto (ver `CLAUDE.md`), este arquivo mantém só o
  essencial factual/formal (5 fontes); a exposição pedagógica, os
  exemplos com dados reais (California Housing) e as conexões entre
  blocos no `02-aula.qmd` são construção nossa, não citação.
