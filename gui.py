import tkinter as tk
from tkinter import simpledialog, messagebox
import tkinter.ttk as ttk  # Import adicional para Spinbox
from puzzle_solver import PuzzleSolver
import numpy as np
import time
import logging

class PuzzleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🧩 8-Puzzle Solver 🧩")
        self.puzzle = PuzzleSolver()
        self.selected_heuristic = None
        self.create_widgets()

    def create_widgets(self):
        # Frame principal
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=10, pady=10)

        # Títulos
        self.label_initial = tk.Label(self.frame, text="🔢 Estado Inicial 🔢", font=("Helvetica", 14))
        self.label_initial.grid(row=0, column=0, padx=20, pady=10)

        self.label_goal = tk.Label(self.frame, text="🎯 Estado Final 🎯", font=("Helvetica", 14))
        self.label_goal.grid(row=0, column=1, padx=150, pady=10)

        # Canvases
        self.canvas_initial = tk.Canvas(self.frame, width=300, height=300, bg="white")
        self.canvas_initial.grid(row=1, column=0, padx=20, pady=20)

        self.canvas_goal = tk.Canvas(self.frame, width=300, height=300, bg="white")
        self.canvas_goal.grid(row=1, column=1, padx=150, pady=20)

        # Frame para Seleções
        selection_frame = tk.Frame(self.root)
        selection_frame.pack(pady=10)

        # Seleção do Método de Busca
        tk.Label(selection_frame, text="🔍 Método de Busca:", font=("Helvetica", 12)).grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.search_var = tk.StringVar(value="A*")  # Inicialização correta
        search_options = ["A*", "Hill Climbing"]
        self.search_menu = tk.OptionMenu(selection_frame, self.search_var, *search_options)
        self.search_menu.config(width=30)
        self.search_menu.grid(row=0, column=1, padx=5, pady=5)

        # Seleção da Heurística
        tk.Label(selection_frame, text="📏 Heurística:", font=("Helvetica", 12)).grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.heuristic_var = tk.StringVar(value="Manhattan")  # Inicialização correta
        heuristic_options = ["Manhattan", "Misplaced Tiles"]
        self.heuristic_menu = tk.OptionMenu(selection_frame, self.heuristic_var, *heuristic_options)
        self.heuristic_menu.config(width=30)
        self.heuristic_menu.grid(row=1, column=1, padx=5, pady=5)

        # Adicionando Spinbox para Passos de Embaralhamento
        tk.Label(selection_frame, text="🎲 Passos de Embaralhamento:", font=("Helvetica", 12)).grid(row=2, column=0, padx=5, pady=5, sticky='e')
        
        self.shuffle_steps_var = tk.IntVar(value=10)  # Valor padrão
        self.shuffle_steps_spinbox = tk.Spinbox(selection_frame, from_=1, to=1000, textvariable=self.shuffle_steps_var, width=28)
        self.shuffle_steps_spinbox.grid(row=2, column=1, padx=5, pady=5)

        # Adicionando Scale para Velocidade da Animação
        tk.Label(selection_frame, text="⏱️ Velocidade da Animação (ms):", font=("Helvetica", 12)).grid(row=3, column=0, padx=5, pady=5, sticky='e')
        
        self.animation_speed_var = tk.IntVar(value=500)  # Valor padrão em milissegundos
        self.animation_speed_scale = tk.Scale(selection_frame, from_=100, to=2000, orient=tk.HORIZONTAL, variable=self.animation_speed_var, length=200)
        self.animation_speed_scale.grid(row=3, column=1, padx=5, pady=5)

        # Botões
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        shuffle_button = tk.Button(button_frame, text="🔄 Embaralhar", command=self.shuffle_puzzle)
        shuffle_button.pack(side=tk.LEFT, padx=5)

        define_goal_button = tk.Button(button_frame, text="🎯 Definir Estado Final", command=self.set_goal_state)
        define_goal_button.pack(side=tk.LEFT, padx=5)

        solve_button = tk.Button(button_frame, text="✅ Resolver", command=self.solve)
        solve_button.pack(side=tk.LEFT, padx=5)

        clear_logs_button = tk.Button(button_frame, text="🧹 Limpar Logs", command=self.clear_logs)
        clear_logs_button.pack(side=tk.LEFT, padx=5)

        # Labels para Métricas
        self.metrics_label = tk.Label(self.root, text="", font=("Helvetica", 12), justify=tk.LEFT)
        self.metrics_label.pack(side=tk.BOTTOM, pady=10)

        self.heuristic_label = tk.Label(self.root, text="", font=("Helvetica", 12), justify=tk.LEFT)
        self.heuristic_label.pack(side=tk.BOTTOM, pady=5)

        # Frame para Logs
        log_frame = tk.Frame(self.root)
        log_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.log_text = tk.Text(log_frame, height=10, state='disabled')
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(log_frame, command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.log_text['yscrollcommand'] = scrollbar.set

        # Redirecionar logs para o widget de texto
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        text_handler = TextHandler(self.log_text)
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        text_handler.setFormatter(formatter)
        logger.addHandler(text_handler)

        # Inicializar a exibição
        self.update_initial_canvas()
        self.update_goal_canvas()

    def shuffle_puzzle(self):
        """Embaralha o quebra-cabeça com um número especificado de passos e anima a sequência."""
        steps = self.shuffle_steps_var.get()
        self.puzzle.shuffle(steps=steps)
        self.animate_shuffling(self.puzzle.move_history)

    def update_initial_canvas(self):
        """Atualiza o canvas do estado inicial com o estado atual do quebra-cabeça."""
        self.canvas_initial.delete("all")
        for i in range(self.puzzle.n):
            for j in range(self.puzzle.n):
                x1, y1 = 10 + j * 100, 10 + i * 100
                x2, y2 = x1 + 90, y1 + 90
                num = self.puzzle.state[i, j]
                self.canvas_initial.create_rectangle(x1, y1, x2, y2, outline="black", width=2)
                if num != 0:
                    self.canvas_initial.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=str(num), font=("Helvetica", 32))

    def update_goal_canvas(self):
        """Atualiza o canvas do estado final com o estado objetivo do quebra-cabeça."""
        self.canvas_goal.delete("all")
        for i in range(self.puzzle.n):
            for j in range(self.puzzle.n):
                x1, y1 = 10 + j * 100, 10 + i * 100
                x2, y2 = x1 + 90, y1 + 90
                num = self.puzzle.goal_state[i, j]
                self.canvas_goal.create_rectangle(x1, y1, x2, y2, outline="black", width=2)
                if num != 0:
                    self.canvas_goal.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=str(num), font=("Helvetica", 32))

    def animate_shuffling(self, move_history):
        """Anima os movimentos de embaralhamento."""
        # Reseta o estado para o estado final antes de embaralhar
        self.puzzle.state = np.copy(self.puzzle.goal_state)
        self.update_initial_canvas()

        animation_speed = self.animation_speed_var.get()

        # Aplicar os movimentos de embaralhamento com animação
        for idx, move in enumerate(move_history):
            self.root.after(animation_speed * idx, lambda m=move: self.apply_move(m))  # Usa animation_speed

    def apply_move(self, move):
        """Aplica um movimento específico e atualiza o canvas."""
        new_i, new_j = move
        i, j = np.where(self.puzzle.state == 0)
        i, j = int(i[0]), int(j[0])
        self.puzzle.state[i, j], self.puzzle.state[new_i, new_j] = self.puzzle.state[new_i, new_j], self.puzzle.state[i, j]
        self.update_initial_canvas()

    def set_goal_state(self):
        """Permite que o usuário defina o estado final via entrada."""
        input_state = simpledialog.askstring("🔢 Input", "Digite o estado final (ex: 1 2 3 4 5 6 0 7 8):")
        if input_state:
            try:
                numbers = list(map(int, input_state.strip().split()))
                if len(numbers) != self.puzzle.n * self.puzzle.n:
                    messagebox.showerror("❌ Erro", f"O estado final deve conter {self.puzzle.n * self.puzzle.n} números.")
                    return
                if sorted(numbers) != list(range(self.puzzle.n * self.puzzle.n)):
                    messagebox.showerror("❌ Erro", "O estado deve conter os números de 0 a 8, sem repetições.")
                    return
                new_goal = np.array(numbers).reshape(self.puzzle.n, self.puzzle.n)
                self.puzzle.goal_state = new_goal
                self.puzzle.state = new_goal.copy()  # Define o Estado Inicial igual ao Estado Final
                self.update_goal_canvas()
                self.update_initial_canvas()  # Atualiza a exibição do Estado Inicial
            except ValueError:
                messagebox.showerror("❌ Erro", "Entrada inválida! Certifique-se de inserir números inteiros separados por espaço.")

    def solve(self):
        """Inicia o processo de resolução com base nas escolhas do usuário."""
        search_type = self.search_var.get()
        heuristic_type = self.heuristic_var.get()

        if heuristic_type == "Manhattan":
            heuristic_func = self.puzzle.manhattan_distance
        elif heuristic_type == "Misplaced Tiles":
            heuristic_func = self.puzzle.misplaced_tiles
        else:
            messagebox.showerror("❌ Erro", "Heurística inválida!")
            return

        self.selected_heuristic = heuristic_func

        if not self.puzzle.is_solvable(self.puzzle.state):
            messagebox.showerror("❌ Erro", "O estado atual não é solucionável.")
            return

        self.metrics_label.config(text="🔄 Resolvendo...")
        self.heuristic_label.config(text="")
        self.root.update()

        path = None
        nodes_visited = 0
        time_taken = 0.0

        if search_type == "A*":
            path, nodes_visited, time_taken = self.puzzle.a_star(heuristic_func)
            if path:
                heuristic_value = heuristic_func(self.puzzle.state)
                heuristic_name = "Manhattan" if heuristic_func == self.puzzle.manhattan_distance else "Misplaced Tiles"
                self.heuristic_label.config(text=f"📏 Heurística ({heuristic_name}): {heuristic_value}")
        elif search_type == "Hill Climbing":
            path, nodes_visited, time_taken = self.puzzle.hill_climbing(heuristic_func)
            if path:
                heuristic_value = heuristic_func(self.puzzle.state)
                heuristic_name = "Manhattan" if heuristic_func == self.puzzle.manhattan_distance else "Misplaced Tiles"
                self.heuristic_label.config(text=f"📏 Heurística ({heuristic_name}): {heuristic_value}")
        else:
            messagebox.showerror("❌ Erro", "Tipo de busca inválido!")
            return

        if path:
            num_moves = len(path) - 1
            message = f"Solução encontrada com {num_moves} movimentos! 🎉\nNós visitados: {nodes_visited} 📊\nTempo gasto: {time_taken:.4f} segundos ⏱️"
            self.metrics_label.config(text=message)
            self.animate_solution(path)
        else:
            messagebox.showerror("❌ Erro", "Não foi possível encontrar uma solução.")
            self.metrics_label.config(text="❌ Nenhuma solução encontrada.")

    def animate_solution(self, path):
        """Anima a solução passo a passo."""
        animation_speed = self.animation_speed_var.get()
        
        def animate_step(step_index):
            if step_index < len(path):
                current_state = path[step_index]
                self.puzzle.state = current_state
                self.update_initial_canvas()
                
                if self.selected_heuristic == self.puzzle.manhattan_distance:
                    heuristic_value = self.puzzle.manhattan_distance(current_state)
                    heuristic_name = "Manhattan"
                elif self.selected_heuristic == self.puzzle.misplaced_tiles:
                    heuristic_value = self.puzzle.misplaced_tiles(current_state)
                    heuristic_name = "Misplaced Tiles"
                else:
                    heuristic_value = "N/A"
                    heuristic_name = "Heurística Não Definida"
                
                self.heuristic_label.config(text=f"📏 Heurística ({heuristic_name}): {heuristic_value}")
                self.root.after(animation_speed, lambda: animate_step(step_index + 1))
            else:
                pass

        animate_step(0)

    def clear_logs(self):
        """Limpa o conteúdo da caixa de logs."""
        self.log_text.configure(state='normal')
        self.log_text.delete('1.0', tk.END)
        self.log_text.configure(state='disabled')

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

if __name__ == '__main__':
    root = tk.Tk()
    app = PuzzleApp(root)
    root.mainloop()
