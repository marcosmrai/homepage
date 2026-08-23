# Fontes usadas — Aula 1

> Trechos literais extraídos em 2026-08-09 de `../fontes/mathml.pdf`
> (Deisenroth, Faisal & Ong, *Mathematics for Machine Learning*, 2024,
> versão em PDF livre — mml-book.com). Offset confirmado entre página
> impressa e página do arquivo PDF: **+6** (ex.: p. 35 impressa = página 41
> do PDF) — este livro tem pouca capa/sumário antes do texto, diferente do
> offset +20 usado nos livros da disciplina `supervised`.
>
> Este livro **não cobre** $k$-NN, variedades/manifolds, nem RAG — esses
> são conceitos de ML acrescentados pela aula, sem lastro bibliográfico
> formal nesta fonte. Só a parte de álgebra linear/geometria analítica pura
> (Blocos 3–5) tem citação de página.

### Fonte 1: MathML, §2.4.2 "Vector Spaces", p. 37
**Uso pretendido:** definição formal de espaço vetorial (Bloco 3).

**Trecho:**
> "Definition 2.9 (Vector Space). A real-valued vector space
> V = (V, +, ·) is a set V with two operations
>
> +: V × V → V  (2.62)
> ·: R × V → V  (2.63)
>
> where
> 1. (V, +) is an Abelian group
> 2. Distributivity: [...]
> 3. Associativity (outer operation) [...]
> 4. Neutral element with respect to the outer operation: ∀x ∈ V: 1·x = x"

---

### Fonte 2: MathML, §2.4.3 "Vector Subspaces", p. 39
**Uso pretendido:** definição de subespaço e teste de fechamento; base para a prova de que $A\mathbf{x}=\mathbf{0}$ é subespaço (Bloco 3).

**Trecho:**
> "Definition 2.10 (Vector Subspace). Let V = (V, +, ·) be a vector space
> and U ⊆ V, U ≠ ∅. Then U = (U, +, ·) is called vector subspace of V (or
> linear subspace) if U is a vector space with the vector space operations
> + and · restricted to U × U and R × U."
>
> "To determine whether (U, +, ·) is a subspace of V we still do need to
> show
> 1. U ≠ ∅, in particular: 0 ∈ U
> 2. Closure of U:
>    a. With respect to the outer operation: ∀λ ∈ R ∀x ∈ U : λx ∈ U.
>    b. With respect to the inner operation: ∀x, y ∈ U : x + y ∈ U."
>
> "The solution set of a homogeneous system of linear equations Ax = 0
> with n unknowns x = [x1,···,xn]⊤ is a subspace of Rⁿ." (Example 2.12)

---

### Fonte 3: MathML, §3.1 "Norms", p. 71
**Uso pretendido:** definição formal de norma; normas $L_1$ e $L_2$ (Bloco 4).

**Trecho:**
> "Definition 3.1 (Norm). A norm on a vector space V is a function
> ‖·‖ : V → R, x ↦ ‖x‖, which assigns each vector x its length ‖x‖ ∈ R,
> such that for all λ ∈ R and x, y ∈ V the following hold:
> - Absolutely homogeneous: ‖λx‖ = |λ|‖x‖
> - Triangle inequality: ‖x + y‖ ⩽ ‖x‖ + ‖y‖
> - Positive definite: ‖x‖ ⩾ 0 and ‖x‖ = 0 ⟺ x = 0"
>
> "The Manhattan norm on Rⁿ is defined for x ∈ Rⁿ as ‖x‖₁ := ∑ᵢ|xᵢ| [...]
> The Manhattan norm is also called ℓ₁ norm." (Example 3.1)

---

### Fonte 4: MathML, §3.1 "Norms", Example 3.2, p. 72
**Uso pretendido:** norma Euclidiana $L_2$ (Bloco 4). **Pendência:** não
encontrei, nas páginas lidas, um exemplo nomeado para a norma $L_\infty$
(máximo/Chebyshev) — o livro pode não ter uma "Example" dedicada a ela como
tem para $L_1$/$L_2$. Verificar antes de citar página específica para
$L_\infty$; por ora, ela só tem lastro na definição geral de norma (Fonte 3),
não numa citação própria.

**Trecho:**
> "The Euclidean norm of x ∈ Rⁿ is defined as ‖x‖₂ := √(∑ᵢ xᵢ²) = √(xᵀx)
> [...] The Euclidean norm is also called ℓ₂ norm."

---

### Fonte 5: MathML, §3.2.2 "General Inner Products", p. 73
**Uso pretendido:** definição formal de produto interno — **ainda não
citada no `02-aula.qmd`** (ver pendência no Bloco 4 do `00-plano-aula.md`;
a aula usa a fórmula do cosseno sem antes definir produto interno
formalmente).

**Trecho:**
> "Definition 3.3. [...] A positive definite, symmetric bilinear mapping
> Ω : V × V → R is called an inner product on V. We typically write
> ⟨x, y⟩ instead of Ω(x, y)."

---

### Fonte 6: MathML, §3.3 "Lengths and Distances", pp. 75–76
**Uso pretendido:** desigualdade de Cauchy-Schwarz; definição formal de distância/métrica (Bloco 5).

**Trecho:**
> "Remark (Cauchy-Schwarz Inequality). For an inner product vector space
> (V, ⟨·,·⟩) the induced norm ‖·‖ satisfies the Cauchy-Schwarz inequality
> |⟨x, y⟩| ⩽ ‖x‖‖y‖." (p. 75)
>
> "Definition 3.6 (Distance and Metric). Consider an inner product space
> (V, ⟨·,·⟩). Then d(x, y) := ‖x − y‖ = √(⟨x−y, x−y⟩) is called the
> distance between x and y for x, y ∈ V." (p. 75)
>
> "A metric d satisfies the following: 1. d is positive definite [...]
> 2. d is symmetric [...] 3. Triangle inequality: d(x, z) ⩽ d(x, y) +
> d(y, z) for all x, y, z ∈ V." (p. 76)

---

### Fonte 7: MathML, §3.4 "Angles and Orthogonality", p. 76
**Uso pretendido:** definição do ângulo entre vetores via cosseno — base da similaridade do cosseno (Bloco 5).

**Trecho:**
> "We use the Cauchy-Schwarz inequality (3.17) to define angles ω in inner
> product spaces between two vectors x, y [...] cos ω = ⟨x,y⟩ / (‖x‖‖y‖).
> [...] The number ω is the angle between the vectors x and y."

---

## Nota sobre a Fonte 1 vs. o achado desta sessão

A **Fonte 6** acima (definição formal de métrica, p. 76) é exatamente o
padrão de axiomas contra o qual a prova de $d_{\cos}$ foi checada e
corrigida no `02-aula.qmd` nesta sessão — o MathML não discute
especificamente a distância do cosseno, então a correção (distância cordal
$\sqrt{2d_{\cos}}$ vs. $d_{\cos}$) foi derivada nesta sessão a partir da
Fonte 6 + Cauchy-Schwarz, não copiada de nenhum livro.

## Pendências

- Fonte 5 (produto interno) ainda não está citada no `.qmd` — a aula usa a
  fórmula do cosseno sem antes definir produto interno como objeto
  independente da norma. Decidir se vale adicionar essa definição ao
  Bloco 4.
- $L_\infty$ sem exemplo nomeado localizado no MathML — confirmar se existe
  em outra página antes de citar.
- `copt.pdf` (Boyd & Vandenberghe) e `optml.pdf` (Wright & Recht) foram
  linkados mas não são relevantes para a Aula 1 (são livros de otimização,
  não de álgebra linear) — ficam reservados para a Parte 2/3 do curso
  (Aulas 6+).
