# 🧩 Solucionador de 8-Puzzle 🧩

Bem-vindo ao **Solucionador de 8-Puzzle**, uma aplicação Python com interface gráfica desenvolvida usando Tkinter. Este projeto permite que você embaralhe um quebra-cabeça 8-puzzle, defina estados finais personalizados e encontre soluções utilizando algoritmos de busca **A\*** e **Hill Climbing**. Além disso, a aplicação oferece animações das soluções e logs detalhados para acompanhamento do processo de resolução.

## 📋 Funcionalidades

- **🔄 Embaralhamento Personalizado:**
  - Defina o número de passos para embaralhar o quebra-cabeça usando o Spinbox.

- **🎯 Definição de Estado Final Personalizado:**
  - Insira manualmente um estado final desejado para o quebra-cabeça.

- **🔍 Algoritmos de Busca:**
  - **A\***: Encontra o caminho mais curto até a solução utilizando heurísticas.
  - **Hill Climbing**: Busca local para encontrar soluções iterativamente.

- **⏱️ Animação de Resolução:**
  - Visualize passo a passo a solução encontrada pelos algoritmos.
  - Ajuste a velocidade das animações conforme sua preferência.

- **📊 Logs Detalhados:**
  - Monitore o progresso dos algoritmos e eventos do sistema.

- **🧹 Limpeza de Logs:**
  - Limpe os logs gerados durante as sessões anteriores para uma melhor organização.

## 🚀 Instalação

### 🔧 Pré-requisitos

- **Python 3.x**
- **Bibliotecas Python:**
  - `tkinter` (geralmente incluída no Python padrão)
  - `numpy`

### 🛠️ Passos para Instalar

1. **Clone o Repositório:**

    ```bash
    git clone https://github.com/seu-usuario/8-puzzle-solver.git
    ```

2. **Acesse o Diretório do Projeto:**

    ```bash
    cd 8-puzzle-solver
    ```

3. **Crie e Ative um Ambiente Virtual (opcional, mas recomendado):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    ```

4. **Instale as Dependências:**

    ```bash
    pip install -r requirements.txt
    ```

5. **Executar a Aplicação:**

    ```bash
    python main.py
    ```

## 🖥️ Uso

1. **🔄 Embaralhar o Quebra-Cabeça:**
   - Defina o número de passos de embaralhamento no campo **"Passos de Embaralhamento"**.
   - Ajuste a velocidade da animação usando o controle deslizante **"Velocidade da Animação (ms)"**.
   - Clique no botão **"🔄 Embaralhar"** para iniciar o processo.

2. **🎯 Definir Estado Final:**
   - Clique no botão **"🎯 Definir Estado Final"**.
   - Insira o estado final desejado no formato: `1 2 3 4 5 6 0 7 8`.
   - Confirme para atualizar o estado final e o estado inicial.

3. **🔍 Selecionar Algoritmo de Busca e Heurística:**
   - Escolha entre **A\*** e **Hill Climbing** no menu **"Método de Busca"**.
   - Selecione a heurística desejada (**Manhattan** ou **Misplaced Tiles**) no menu **"Heurística"**.

4. **✅ Resolver o Quebra-Cabeça:**
   - Clique no botão **"✅ Resolver"** para iniciar o processo de resolução.
   - Observe a animação da solução e consulte as métricas exibidas na parte inferior.

5. **🧹 Limpar Logs:**
   - Clique no botão **"🧹 Limpar Logs"** para limpar as informações de log exibidas.

## 📚 Detalhes Técnicos

### 📦 Estrutura do Projeto

- **main.py:** Ponto de entrada da aplicação que inicializa a interface gráfica.
- **gui.py:** Contém a classe `PuzzleApp` responsável pela interface do usuário e interação com os algoritmos de resolução.
- **puzzle_solver.py:** Implementa a lógica de resolução do quebra-cabeça, incluindo os algoritmos de busca **A\*** e **Hill Climbing**.
