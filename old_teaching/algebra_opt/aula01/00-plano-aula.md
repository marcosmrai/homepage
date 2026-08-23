## Resumo — Aula 1: Espaços Vetoriais, Normas e Métricas

*(Reconstruído a partir do `index.qmd` já aprovado. O `plan.md` anterior era
uma colagem de conversa de chat, não um plano de aula — o conteúdo dele foi
absorvido aqui, reorganizado, e conferido linha a linha contra o que
realmente está no `.qmd`.)*

A aula ancora a representação vetorial de dados (a base de todo o curso) na
**Hipótese da Variedade** (*manifold hypothesis*): dados reais de alta
dimensão não preenchem $\mathbb{R}^d$ uniformemente, vivem em subespaços
curvos de dimensão intrínseca muito menor. Isso não está no `index.md` do
curso, mas dá o fio condutor da aula inteira — da definição de vetor até o
$k$-NN, normas, métricas e o fechamento com RAG como busca vetorial.

**Pré-requisitos:** nenhum prévio do curso (é a Aula 1). Álgebra do ensino
médio (vetores em $\mathbb{R}^2$/$\mathbb{R}^3$, ângulos, produto escalar
informal).

**Objetivos de aprendizagem** (do `index.md`, Lesson 1):
- **ML Concept:** Distance-based similarity and spatial modeling em $k$-NN.
- **Mathematical Concept:** Espaços vetoriais, produtos internos, e normas
  vetoriais/matriciais ($L_1$, $L_2$, $L_\infty$). Interpretação geométrica
  de similaridade via produtos internos e distância do cosseno.
- **Objectives:** Entender como dados estruturados são representados
  geometricamente e como a escolha da distância afeta algoritmos baseados
  em métrica.
- **Expected Competencies:** Implementar rotinas de busca por métrica
  customizada em Python com type hints, analisar propriedades de normas, e
  formalizar similaridade geométrica.

## Plano de aula — Aula 1 (carga horária: ~125min)

**Aviso de conta.** O `plan.md` original estimava 1h30–2h (90–120 min) para
6 blocos. O `.qmd` real inclui mais conteúdo do que esses blocos previam
(prova completa de que $d_{\cos}$ falha a desigualdade triangular, exemplo
Swiss Roll com código, exemplo de duas luas, fechamento com RAG) — a
estimativa realista sobe para **~125 min**, acima da faixa original.

1.  **Escalares, Vetores e a Máquina** (~15 min) — Por que dados do mundo
    real precisam virar vetores (pixels, atributos tabulares, embeddings de
    texto). Definição de escalar e vetor-coluna, operações elementares
    (soma, escala), interpretação geométrica (regra do paralelogramo).
    Visualização: um dataset de imóveis como pontos em $\mathbb{R}^2$.

2.  **O Problema de Aprendizado e a Intuição do $k$-NN** (~15 min) —
    Formalização do aprendizado supervisionado ($\mathcal{D}=\{(\mathbf{x}_i,y_i)\}$,
    classificação vs. regressão). Hipótese de suavidade: pontos próximos em
    $\mathbb{R}^d$ têm rótulos parecidos. Mecânica do $k$-NN (votação/média).
    Termina com o problema gerador: falta uma regra rigorosa de
    "proximidade" — o Bloco 4 resolve.

3.  **Espaços Vetoriais, Subespaços e a Hipótese da Variedade** (~30 min) —
    Definição formal de espaço vetorial e subespaço (teste de fechamento:
    contém $\mathbf{0}$, fechado sob soma e escalar); prova de que a solução
    de $A\mathbf{x}=\mathbf{0}$ é subespaço. Contraste com **variedades**
    (manifolds): localmente planas, globalmente curvas — e por isso
    violam o fechamento sob soma (dois pontos na esfera somados caem fora
    da esfera). Exemplo Swiss Roll (código, visualização 3D). Hipótese da
    Variedade: quando o manifold é aproximadamente plano, PCA funciona; se é
    curvo, precisa de mapas não-lineares para "desamassar" até um espaço
    latente onde volta a ser um subespaço.

4.  **Normas e Produtos Internos** (~20 min) — Definição formal de norma
    (homogeneidade absoluta, desigualdade triangular, positiva definida).
    $L_1$ (Manhattan), $L_2$ (Euclidiana), $L_\infty$ (máximo). Visualização
    das bolas unitárias de cada norma em $\mathbb{R}^2$. *Nota: produto
    interno é usado a partir do Bloco 5 (fórmula do cosseno) mas não é
    definido formalmente nesta seção — só a norma é. Considerar adicionar a
    Definição 3.2/3.3 do MathML (bilinear, simétrico, positivo definido) se
    sobrar tempo.*

5.  **Métricas e a Ilusão da Distância Reta** (~25 min) — Axiomas formais de
    métrica (não-negatividade, simetria, desigualdade triangular); métrica
    induzida por norma ($d(x,y)=\|x-y\|$). Colapso da distância Euclidiana
    em alta dimensão (concentração de distâncias, viés de magnitude).
    Similaridade e distância do cosseno — **com a prova corrigida nesta
    sessão**: $\sqrt{2\,d_{\cos}}$ é métrica (distância cordal), $d_{\cos}$
    em si não é (contraexemplo a $0^\circ,90^\circ,135^\circ$).

6.  **$k$-NN e Limitações Geométricas, e Fechamento** (~20 min) — Sob que
    condições o $k$-NN com $L_2$ funciona (densidade amostral alta, operar
    na porção localmente plana da variedade); fronteiras de Voronoi;
    necessidade de *feature scaling*. Exemplo das duas luas (não-linear,
    $k=3$ pequeno funciona). Fechamento: RAG (*Retrieval-Augmented
    Generation*) como $k$-NN em embeddings de texto — consolida todos os
    conceitos da aula numa aplicação atual.
