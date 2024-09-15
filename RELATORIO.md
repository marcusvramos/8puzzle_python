# Relatório do Projeto: Resolução do 8-Puzzle com Busca A* e Hill Climbing

## 📋 Introdução

Este projeto consiste em implementar um solucionador para o jogo **8-Puzzle** utilizando métodos de busca **A\*** com heurísticas (**Distância de Manhattan** e **Misplaced Tiles**) e **Hill Climbing**. O objetivo é analisar o desempenho desses algoritmos para encontrar a solução mais eficiente, comparando métricas como número de movimentos, nós visitados e tempo gasto.

## 🔧 Itens Selecionados para Desenvolvimento

- **Busca A\***:
  - Implementada com duas heurísticas:
    - **Distância de Manhattan**: Calcula a soma das distâncias das peças até suas posições corretas.
    - **Misplaced Tiles**: Conta a quantidade de peças fora do lugar.
  
- **Hill Climbing**:
  - Algoritmo de busca local que tenta otimizar a heurística a cada movimento.
  - Utiliza tanto a heurística de **Distância de Manhattan** quanto a de **Misplaced Tiles**.
  
- **Embaralhamento Personalizado**:
  - Implementação de um **Spinbox** para definir o número de passos de embaralhamento, permitindo ajustar a complexidade do estado inicial.
  
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

### 3. Hill Climbing com Heurística Manhattan

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
  
- **Método de Busca**: Hill Climbing com heurística Manhattan
- **Resultados**:
  - **Movimentos:** 10
  - **Nós Visitados:** 11
  - **Tempo Gasto:** 0.0296 segundos
- **Logs Resumidos:**
  - Início do Hill Climbing.
  - Avaliação e movimento para vizinhos com menor heurística.
  - Movimentos sucessivos até atingir o estado final.
  - **Solução encontrada pelo Hill Climbing**.

### 4. Hill Climbing com Heurística Misplaced Tiles

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
  
- **Método de Busca**: Hill Climbing com Misplaced Tiles
- **Resultados**:
  - **Movimentos:** Não foi possível encontrar a solução.
  - **Nós Visitados:** Vários testes resultaram em picos locais ou platôs.
  - **Tempo Gasto:** Variável (não conclusivo devido à não convergência).
- **Logs Resumidos:**
  - Início do Hill Climbing.
  - Avaliação de vizinhos com heurísticas menores.
  - Entrou em situações de pico local ou platô, sem encontrar a solução.

## 🕵️‍♂️ Comparações e Observações

- **A\* com Distância de Manhattan**:
  - **Desempenho:** Excelente, com baixo número de nós visitados e tempo gasto.
  - **Eficiência:** Encontrou a solução rapidamente e de forma otimizada.
  
- **A\* com Misplaced Tiles**:
  - **Desempenho:** Bom, mas com maior número de nós visitados e tempo gasto em comparação com Manhattan.
  - **Eficiência:** Ainda eficaz, mas menos otimizado que Manhattan.
  
- **Hill Climbing com Manhattan**:
  - **Desempenho:** Rápido e eficiente em encontrar soluções para estados menos complexos.
  - **Limitações:** Pode não ser tão robusto quanto A\* em casos mais complexos.
  
- **Hill Climbing com Misplaced Tiles**:
  - **Desempenho:** Ineficaz em alguns casos, entrando em picos locais ou platôs.
  - **Limitações:** Falha em encontrar soluções para estados mais desafiadores.

## 🔍 Conclusão

Os testes realizados demonstraram que o método **A\*** com a heurística de **Distância de Manhattan** é o mais eficiente para resolver o **8-Puzzle**, apresentando menor número de nós visitados e tempo de execução mais rápido. A heurística de **Misplaced Tiles** também foi eficaz, porém menos otimizada, consumindo mais recursos computacionais.

Por outro lado, o **Hill Climbing** mostrou-se eficiente em situações menos complexas quando utilizando a heurística de Manhattan, mas enfrentou dificuldades significativas ao utilizar a heurística de Misplaced Tiles, frequentemente entrando em situações de pico local ou platô que impediram a conclusão da solução.

Portanto, para a resolução geral do 8-Puzzle, o método **A\*** com a heurística de **Distância de Manhattan** é a abordagem mais robusta e confiável, proporcionando soluções rápidas e eficientes mesmo em estados iniciais mais complexos.


