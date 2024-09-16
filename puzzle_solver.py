import numpy as np
import heapq
import random
import time
from collections import deque
import logging
import tkinter as tk

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s')

class PuzzleSolver:
    def __init__(self, n=3):
        self.n = n 
        self.goal_state = np.arange(1, n * n + 1).reshape(n, n)
        self.goal_state[-1, -1] = 0 
        self.state = np.copy(self.goal_state)
        self.move_history = []

    def shuffle(self, steps=100):
        """Embaralha o quebra-cabeça"""
        self.move_history.clear()
        state_copy = np.copy(self.state)  # Inicia a partir do Estado Atual
        last_move = None  # Para evitar movimentos redundantes

        for _ in range(steps):
            i, j = np.where(state_copy == 0)
            i, j = int(i[0]), int(j[0])

            possible_moves = []
            # Define possíveis movimentos, evitando a reversão imediata
            if i > 0 and last_move != 'down':
                possible_moves.append(('up', (i - 1, j)))
            if i < self.n - 1 and last_move != 'up':
                possible_moves.append(('down', (i + 1, j)))
            if j > 0 and last_move != 'right':
                possible_moves.append(('left', (i, j - 1)))
            if j < self.n - 1 and last_move != 'left':
                possible_moves.append(('right', (i, j + 1)))

            if possible_moves:
                move_direction, (new_i, new_j) = random.choice(possible_moves)
                # Troca o espaço vazio com a peça escolhida
                state_copy[i, j], state_copy[new_i, new_j] = state_copy[new_i, new_j], state_copy[i, j]
                self.move_history.append((new_i, new_j))
                last_move = move_direction

    def apply_move_history(self):
        """Aplica todos os movimentos armazenados em move_history ao estado atual."""
        for move in self.move_history:
            new_i, new_j = move
            i, j = np.where(self.state == 0)
            i, j = int(i[0]), int(j[0])
            self.state[i, j], self.state[new_i, new_j] = self.state[new_i, new_j], self.state[i, j]

    def is_solvable(self, state):
        """Verifica se um determinado estado é solucionável."""
        flat_state = state.flatten()
        inv_count = 0
        for i in range(len(flat_state)):
            for j in range(i + 1, len(flat_state)):
                if flat_state[i] > flat_state[j] and flat_state[j] != 0:
                    inv_count += 1
        return inv_count % 2 == 0

    def is_solved(self):
        """Verifica se o estado atual é o estado final."""
        return np.array_equal(self.state, self.goal_state)

    def misplaced_tiles(self, state):
        """Conta quantas peças estão fora do lugar, excluindo o espaço vazio."""
        return max(np.sum(state != self.goal_state) - 1, 0)  # Garante não ser negativo

    def manhattan_distance(self, state):
        """Calcula a soma das distâncias de Manhattan das peças até suas posições corretas."""
        distance = 0
        for i in range(self.n):
            for j in range(self.n):
                num = state[i, j]
                if num != 0:
                    goal_i, goal_j = divmod(num - 1, self.n)
                    distance += abs(i - goal_i) + abs(j - goal_j)
        return distance

    def get_possible_moves(self, state):
        """Gera todos os movimentos possíveis (estados sucessores) a partir do estado atual."""
        i, j = np.where(state == 0)
        i, j = int(i[0]), int(j[0])

        possible_moves = []
        if i > 0:
            new_state = np.copy(state)
            new_state[i, j], new_state[i - 1, j] = new_state[i - 1, j], new_state[i, j]
            possible_moves.append(new_state)
        if i < self.n - 1:
            new_state = np.copy(state)
            new_state[i, j], new_state[i + 1, j] = new_state[i + 1, j], new_state[i, j]
            possible_moves.append(new_state)
        if j > 0:
            new_state = np.copy(state)
            new_state[i, j], new_state[i, j - 1] = new_state[i, j - 1], new_state[i, j]
            possible_moves.append(new_state)
        if j < self.n - 1:
            new_state = np.copy(state)
            new_state[i, j], new_state[i, j + 1] = new_state[i, j + 1], new_state[i, j]
            possible_moves.append(new_state)

        return possible_moves

    def a_star(self, heuristic):
        """Executa o algoritmo A* com a heurística especificada."""
        def reconstruct_path(came_from, current):
            """Reconstrói o caminho do início até o objetivo."""
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            return path[::-1]  # Inverte o caminho

        start_time = time.time()
        frontier = []
        start_tuple = tuple(map(tuple, self.state))
        heapq.heappush(frontier, (0, start_tuple))
        came_from = {}
        g_score = {start_tuple: 0}
        f_score = {start_tuple: heuristic(self.state)}
        nodes_visited = 0
        visited = set()

        while frontier:
            current_f, current_tuple = heapq.heappop(frontier)
            if current_tuple in visited:
                continue
            visited.add(current_tuple)
            nodes_visited += 1
            current = np.array(current_tuple)

            logging.debug(f'Visitando nó com f={current_f}, estado=\n{current}')

            if np.array_equal(current, self.goal_state):
                end_time = time.time()
                path = reconstruct_path(came_from, current_tuple)
                # Converter caminho para arrays NumPy
                path = [np.array(state) for state in path]
                logging.info('Solução encontrada pelo A*!')
                return path, nodes_visited, end_time - start_time

            for neighbor in self.get_possible_moves(current):
                neighbor_tuple = tuple(map(tuple, neighbor))
                tentative_g_score = g_score[current_tuple] + 1

                if neighbor_tuple in g_score and tentative_g_score >= g_score[neighbor_tuple]:
                    continue

                came_from[neighbor_tuple] = current_tuple
                g_score[neighbor_tuple] = tentative_g_score
                f_score_neighbor = tentative_g_score + heuristic(neighbor)
                f_score[neighbor_tuple] = f_score_neighbor
                heapq.heappush(frontier, (f_score_neighbor, neighbor_tuple))

                logging.debug(f'Explorando vizinho com f={f_score_neighbor}, heurística={heuristic(neighbor)}:\n{neighbor}')

        end_time = time.time()
        logging.info('A* não conseguiu encontrar uma solução.')
        return None, nodes_visited, end_time - start_time  # Sem solução encontrada

    def hill_climbing(self, heuristic):
        """Executa o algoritmo Hill-Climbing padrão com a heurística especificada."""
        def get_best_neighbor(current_state):
            neighbors = self.get_possible_moves(current_state)
            best_neighbor = None
            best_heuristic = float('inf')

            for neighbor in neighbors:
                h = heuristic(neighbor)
                logging.debug(f'Vizinho Avaliado com heurística {h}:\n{neighbor}')
                if h < best_heuristic:
                    best_heuristic = h
                    best_neighbor = neighbor

            return best_neighbor, best_heuristic

        start_time = time.time()
        current_state = np.copy(self.state)
        path = [current_state.copy()]
        nodes_visited = 1

        logging.info('Iniciando Hill-Climbing...')
        while True:
            logging.debug(f'Estado Atual:\n{current_state}')
            
            if np.array_equal(current_state, self.goal_state):
                logging.info('Solução encontrada!')
                end_time = time.time()
                return path, nodes_visited, end_time - start_time

            best_neighbor, best_heuristic = get_best_neighbor(current_state)
            current_heuristic = heuristic(current_state)
            logging.debug(f'Heurística Atual: {current_heuristic}')
            logging.debug(f'Melhor heurística do vizinho: {best_heuristic}')

            if best_neighbor is None or best_heuristic >= current_heuristic:
                logging.info('Pico local ou platô alcançado.')
                break

            current_state = best_neighbor
            path.append(current_state.copy())
            nodes_visited += 1
            logging.debug(f'Movendo para o vizinho com heurística {best_heuristic}')

        end_time = time.time()
        return None, nodes_visited, end_time - start_time  # Sem solução encontrada

    def print_state(self):
        """Imprime o estado atual do quebra-cabeça."""
        for row in self.state:
            print(' '.join(str(num) for num in row))
        print()

class TextHandler(logging.Handler):
    """Classe para redirecionar logs para um widget de texto do Tkinter."""
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record):
        msg = self.format(record)
        self.text_widget.configure(state='normal')
        self.text_widget.insert(tk.END, msg + '\n')
        self.text_widget.configure(state='disabled')
        self.text_widget.see(tk.END)

