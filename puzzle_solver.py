import numpy as np
import heapq
import random
import time
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
        self.move_history.clear()
        state_copy = np.copy(self.state)
        last_move = None

        for _ in range(steps):
            i, j = np.where(state_copy == 0)
            i, j = int(i[0]), int(j[0])

            possible_moves = []
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
                state_copy[i, j], state_copy[new_i, new_j] = state_copy[new_i, new_j], state_copy[i, j]
                self.move_history.append((new_i, new_j))
                last_move = move_direction

    def apply_move_history(self):
        for move in self.move_history:
            new_i, new_j = move
            i, j = np.where(self.state == 0)
            i, j = int(i[0]), int(j[0])
            self.state[i, j], self.state[new_i, new_j] = self.state[new_i, new_j], self.state[i, j]

    def is_solvable(self, state):
        flat_state = state.flatten()
        inv_count = 0
        for i in range(len(flat_state)):
            for j in range(i + 1, len(flat_state)):
                if flat_state[i] > flat_state[j] and flat_state[j] != 0:
                    inv_count += 1
        return inv_count % 2 == 0

    def is_solved(self):
        return np.array_equal(self.state, self.goal_state)

    def misplaced_tiles(self, state):
        return max(np.sum(state != self.goal_state) - 1, 0)

    def manhattan_distance(self, state):
        distance = 0
        for i in range(self.n):
            for j in range(self.n):
                num = state[i, j]
                if num != 0:
                    goal_i, goal_j = divmod(num - 1, self.n)
                    distance += abs(i - goal_i) + abs(j - goal_j)
        return distance

    def get_possible_moves(self, state):
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
        def reconstruct_path(came_from, current):
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            return path[::-1]

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
        return None, nodes_visited, end_time - start_time

    def best_first_search(self, heuristic):
        def reconstruct_path(came_from, current):
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            return path[::-1]

        start_time = time.time()
        frontier = []
        start_tuple = tuple(map(tuple, self.state))
        heapq.heappush(frontier, (heuristic(self.state), start_tuple))
        came_from = {}
        visited = set()
        nodes_visited = 0

        logging.info('Iniciando Best-First Search...')
        while frontier:
            current_heuristic, current_tuple = heapq.heappop(frontier)
            
            if current_tuple in visited:
                continue
            
            visited.add(current_tuple)
            nodes_visited += 1
            current = np.array(current_tuple)

            logging.debug(f'Visitando nó com heurística={current_heuristic}, estado=\n{current}')

            if np.array_equal(current, self.goal_state):
                end_time = time.time()
                path = reconstruct_path(came_from, current_tuple)
                path = [np.array(state) for state in path]
                logging.info('Solução encontrada pelo Best-First!')
                return path, nodes_visited, end_time - start_time

            for neighbor in self.get_possible_moves(current):
                neighbor_tuple = tuple(map(tuple, neighbor))

                if neighbor_tuple not in visited:
                    came_from[neighbor_tuple] = current_tuple
                    heapq.heappush(frontier, (heuristic(neighbor), neighbor_tuple))

                    logging.debug(f'Explorando vizinho com heurística={heuristic(neighbor)}:\n{neighbor}')

        end_time = time.time()
        logging.info('Best-First não conseguiu encontrar uma solução.')
        return None, nodes_visited, end_time - start_time 

    def print_state(self):
        for row in self.state:
            print(' '.join(str(num) for num in row))
        print()

class TextHandler(logging.Handler):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record):
        msg = self.format(record)
        self.text_widget.configure(state='normal')
        self.text_widget.insert(tk.END, msg + '\n')
        self.text_widget.configure(state='disabled')
        self.text_widget.see(tk.END)
