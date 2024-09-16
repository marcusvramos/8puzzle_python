# Relatório do Projeto: Resolução do 8-Puzzle com Busca A* e Best-First

## 📋 Introdução

Este projeto consiste em implementar um solucionador para o jogo **8-Puzzle** utilizando métodos de busca **A\*** com heurísticas (**Distância de Manhattan** e **Misplaced Tiles**) e **Best-First**. O objetivo é analisar o desempenho desses algoritmos para encontrar a solução mais eficiente, comparando métricas como número de movimentos, nós visitados e tempo gasto.

## 🔧 Itens Selecionados para Desenvolvimento

- **Busca A\***:
  - Implementada com duas heurísticas:
    - **Distância de Manhattan**: Calcula a soma das distâncias das peças até suas posições corretas.
    - **Misplaced Tiles**: Conta a quantidade de peças fora do lugar.
  
- **Best-First**:
  - Algoritmo de busca que seleciona o nó a ser expandido com base na menor avaliação heurística (função de avaliação).
  - Utiliza tanto a heurística de **Distância de Manhattan** quanto a de **Misplaced Tiles**.
  
- **Embaralhamento Personalizado**:
  - Implementação da possibilidade de embaralhamento, permitindo ajustar a complexidade do estado inicial.
  
- **Animação da Resolução**:
  - Visualização passo a passo da solução encontrada pelos algoritmos.
  - Ajuste da velocidade das animações através de um **Scale** (barra deslizante).

## 🧪 Testes Realizados e Resultados

### 1. Busca A\* com Heurística Manhattan

- **Estado Inicial Embaralhado:**

    ```
    2 6 -
    1 3 5
    4 7 8
    ```
  
- **Estado Final Desejado:**

    ```
    1 2 3
    4 5 6
    7 8 -
    ```
  
- **Método de Busca**: A* com heurística Manhattan
- **Resultados**:
  - **Movimentos:** 10
  - **Nós Visitados:** 16
  - **Tempo Gasto:** 0.0219 segundos
- **Logs Resumidos:**
  - Início da busca com o estado inicial.
  - Exploração de vizinhos com diferentes valores de f e heurísticas.
  - Movimentos sucessivos até atingir o estado final.
  - **Solução encontrada pelo A\***.

### 2. Busca A\* com Heurística Misplaced Tiles

- **Estado Inicial Embaralhado:**

    ```
    4 1 3
    5 7 6
    - 2 8
    ```
  
- **Estado Final Desejado:**

    ```
    1 2 3
    4 5 6
    7 8 -
    ```
  
- **Método de Busca**: A* com Misplaced Tiles
- **Resultados**:
  - **Movimentos:** 10
  - **Nós Visitados:** 44
  - **Tempo Gasto:** 0.0461 segundos
- **Logs Resumidos:**
  - Início da busca com o estado inicial.
  - Exploração de vizinhos com diferentes valores de f e heurísticas.
  - Maior número de nós visitados comparado à heurística Manhattan.
  - **Solução encontrada pelo A\***.

### 3. Best-First com Heurística Manhattan

- **Estado Inicial Embaralhado:**

    ```
    2 3 6
    1 5 8
    - 4 7
    ```
  
- **Estado Final Desejado:**

    ```
    1 2 3
    4 5 6
    7 8 -
    ```
  
- **Método de Busca**: Best-First com heurística Manhattan
- **Resultados**:
  - **Movimentos:** 12
  - **Nós Visitados:** 18
  - **Tempo Gasto:** 0.0345 segundos
- **Logs Resumidos:**
  - Início do Best-First Search.
  - Avaliação e movimento para vizinhos com menor heurística.
  - Movimentos sucessivos até atingir o estado final.
  - **Solução encontrada pelo Best-First**.

### 4. Best-First com Heurística Misplaced Tiles

- **Estado Inicial Embaralhado:**

    ```
    2 3 6
    1 5 8
    - 4 7
    ```
  
- **Estado Final Desejado:**

    ```
    1 2 3
    4 5 6
    7 8 -
    ```
  
- **Método de Busca**: Best-First com Misplaced Tiles
- **Resultados**:
  - **Movimentos:** 15
  - **Nós Visitados:** 25
  - **Tempo Gasto:** 0.0412 segundos
- **Logs Resumidos:**
  - Início do Best-First Search.
  - Avaliação de vizinhos com heurísticas menores.
  - Exploração de diferentes caminhos até encontrar a solução.
  - **Solução encontrada pelo Best-First**.

## 🕵️‍♂️ Comparações e Observações

- **A\* com Distância de Manhattan**:
  - **Desempenho:** Excelente, com baixo número de nós visitados e tempo gasto.
  - **Eficiência:** Encontrou a solução rapidamente e de forma otimizada.
  
- **A\* com Misplaced Tiles**:
  - **Desempenho:** Bom, mas com maior número de nós visitados e tempo gasto em comparação com Manhattan.
  - **Eficiência:** Ainda eficaz, mas menos otimizado que Manhattan.
  
- **Best-First com Manhattan**:
  - **Desempenho:** Rápido em encontrar soluções, mas pode explorar caminhos menos ideais em comparação com A*.
  - **Eficiência:** Geralmente encontra uma solução, mas nem sempre a mais curta devido à falta de componente de custo acumulado.
  
- **Best-First com Misplaced Tiles**:
  - **Desempenho:** Pode encontrar soluções, mas com maior número de movimentos e nós visitados comparado à heurística Manhattan.
  - **Limitações:** Pode ser mais propenso a seguir caminhos menos eficientes do que a busca A* devido à falta de custo acumulado.

## 🔍 Conclusão

Os testes realizados demonstraram que o método **A\*** com a heurística de **Distância de Manhattan** continua sendo o mais eficiente para resolver o **8-Puzzle**, apresentando o menor número de nós visitados e o tempo de execução mais rápido. A heurística de **Misplaced Tiles** também foi eficaz, porém consumiu mais recursos computacionais.

O **Best-First Search** se mostrou útil, fornecendo resultados rápidos. No entanto, como ele não leva em consideração o custo acumulado do caminho (diferente do A*), pode acabar explorando caminhos menos ótimos, resultando em soluções que, embora válidas, não sejam as mais curtas.

Para a resolução geral do 8-Puzzle, o método **A\*** com a heurística de **Distância de Manhattan** continua sendo a abordagem mais robusta e confiável, garantindo soluções rápidas e eficientes, mesmo em estados iniciais mais complexos. O **Best-First** é uma alternativa interessante, mas seu desempenho pode variar dependendo do problema específico e da heurística utilizada.
