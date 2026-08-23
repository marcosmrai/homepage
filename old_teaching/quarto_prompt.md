Atue como um professor especialista e crie um material didático completo utilizando a linguagem Quarto (.qmd). O documento deve funcionar simultaneamente como um artigo/apostila detalhada e como uma apresentação de slides profissional.

Tema da Aula: [INSIRA O TEMA DA AULA AQUI]
Público-alvo: [EX: Alunos de Graduação/Pós-Graduação em Computação/Engenharia]

Siga estritamente as regras de estruturação e formatação abaixo:

1. CABEÇALHO YAML:
O documento deve começar com o cabeçalho configurado para HTML e RevealJS:
---
title: "[TÍTULO DA AULA]"
subtitle: "[SUBTÍTULO/DISCIPLINA]"
author: "[SEU NOME]"
format:
  html:
    output-dir: "output"
    code-fold: false
  revealjs:
    output-dir: "output"
    slide-number: true
---

2. VISIBILIDADE CONDICIONAL E CONTEÚDO:
Divida TODO o conteúdo conceitual utilizando as divs condicionais do Quarto:
- Para as NOTAS DE AULA (Apostila):
  ::: {.content-visible when-format="html" unless-format="revealjs"}
  [Insira aqui uma explicação profunda, rigorosa, com texto corrido, formalismo matemático em LaTeX, intuição teórica e provas/demonstrações completas.]
  :::

- Para os SLIDES (Apresentação):
  ::: {.content-visible when-format="revealjs"}
  [Insira o mesmo conceito de forma resumida, utilizando bullet points curtos, destaque para conceitos-chave em negrito e formulas essenciais isoladas.]
  :::

3. ESTRUTURA DOS SLIDES E SEÇÕES:
- Use `#` para seções principais/capítulos.
- Use `---` para indicar quebras de slides ou transições de tópicos.

4. CÓDIGO PYTHON E ILUSTRAÇÕES GEOMÉTRICAS/GRÁFICAS:
- Inclua blocos de código Python embutidos (```{python}) usando bibliotecas como Matplotlib, Numpy ou Scikit-Learn para ilustrar visualmente os conceitos teóricos da aula.
- Todos os blocos de código gráficos devem conter no topo as diretivas Quarto:
  #| echo: false
  #| fig-align: center
- Os gráficos devem ser esteticamente limpos, com legendas legíveis, títulos representativos e paletas de cores adequadas (ex: usando plt.style.use('seaborn-v0_8-whitegrid')).

5. FECHAMENTO PRÁTICO:
Ao final da aula, faça uma conexão prática ligando toda a teoria matemática construída a uma aplicação moderna no estado da arte (ex: Redes Neurais, LLMs, Processamento de Sinais, Otimização, etc.).

Gere o arquivo `.qmd` completo e pronto para compilação.