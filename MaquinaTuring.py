import json
import tkinter as tk
from tkinter import messagebox, filedialog

class TuringMachine:
    def __init__(self, states, alphabet, tape_alphabet, transitions, initial_state, accept_states, reject_states):
        self.states = states
        self.alphabet = alphabet
        self.tape_alphabet = tape_alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.accept_states = accept_states
        self.reject_states = reject_states
        self.current_state = initial_state
        self.tape = []
        self.head_position = 0

    def reset(self, input_string):
        # Resetea la máquina para una nueva ejecución
        self.tape = list(input_string)
        self.head_position = 0
        self.current_state = self.initial_state

    def paso(self):
        # Ejecuta un paso de la simulación
        if self.current_state in self.accept_states:
            return "ACCEPTED"
        if self.current_state in self.reject_states:
            return "REJECTED"
        
        current_symbol = self.tape[self.head_position] if self.head_position < len(self.tape) else '_'
        transition_key = (self.current_state, current_symbol)

        if transition_key not in self.transitions:
            return "REJECTED"  # No hay transición definida

        new_state, new_symbol, direction = self.transitions[transition_key]
        self.tape[self.head_position] = new_symbol
        self.current_state = new_state
        
        # Mover el cabezal
        if direction == 'R':
            self.head_position += 1
        elif direction == 'L':
            self.head_position -= 1
            if self.head_position < 0:
                self.tape.insert(0, '_')
                self.head_position = 0

        return "CONTINUE"

    def is_accepted(self):
        return self.current_state in self.accept_states

    def is_rejected(self):
        return self.current_state in self.reject_states

class TuringMachineSimulator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simulador de Máquina de Turing")

        # Variables de la máquina
        self.states = []
        self.alphabet = []
        self.tape_alphabet = []
        self.transitions = {}
        self.initial_state = ""
        self.accept_states = []
        self.reject_states = []
        self.turing_machine = None

        # Interfaz de usuario
        self.create_widgets()

    def create_widgets(self):
        # Entrada para el alfabeto
        tk.Label(self, text="Alfabeto de entrada:").grid(row=0, column=0, sticky="w")
        self.alphabet_entry = tk.Entry(self)
        self.alphabet_entry.grid(row=0, column=1)

        # Entrada para los estados
        tk.Label(self, text="Estados:").grid(row=1, column=0, sticky="w")
        self.states_entry = tk.Entry(self)
        self.states_entry.grid(row=1, column=1)

        # Estado inicial
        tk.Label(self, text="Estado inicial:").grid(row=2, column=0, sticky="w")
        self.initial_state_entry = tk.Entry(self)
        self.initial_state_entry.grid(row=2, column=1)

        # Reglas de la maquina
        '''tk.Label(self, text="Reglas de Transicion:").grid(row=3, column=0, sticky="w")
        self.transitions_entry = tk.Text(self,height = 6, width = 30)
        self.transitions_entry.grid(row=3, column=1)'''

        # Estados de aceptación
        tk.Label(self, text="Estados de aceptación:").grid(row=4, column=0, sticky="w")
        self.accept_states_entry = tk.Entry(self)
        self.accept_states_entry.grid(row=4, column=1)

        # Estados de rechazo
        '''tk.Label(self, text="Estados de rechazo:").grid(row=5, column=0, sticky="w")
        self.reject_states_entry = tk.Entry(self)
        self.reject_states_entry.grid(row=5, column=1)'''

        # Cinta
        tk.Label(self, text="Entrada de cinta:").grid(row=6, column=0, sticky="w")
        self.tape_entry = tk.Entry(self)
        self.tape_entry.grid(row=6, column=1)

        # Botón para iniciar la simulación
        self.start_button = tk.Button(self, text="Iniciar Simulación", command=self.start_simulation)
        self.start_button.grid(row=7, column=0, columnspan=2)

        # Área de visualización de la cinta
        self.tape_label = tk.Label(self, text="Cinta: ")
        self.tape_label.grid(row=8, column=0, columnspan=2)

        # Botón de paso a paso
        self.paso_button = tk.Button(self, text="Paso a Paso", command=self.paso_simulation)
        self.paso_button.grid(row=9, column=0, columnspan=2)
        self.paso_button.config(state=tk.DISABLED)

    def start_simulation(self):
        # Inicializar la máquina de Turing
        self.states = self.states_entry.get().split(',')
        self.alphabet = self.alphabet_entry.get().split(',')
        self.initial_state = self.initial_state_entry.get()
        self.accept_states = self.accept_states_entry.get().split(',')
        #self.reject_states = self.reject_states_entry.get().split(',')
        
        # Definir las transiciones
        #self.transitions = self.transitions_entry.get("1.0",'end-1c').split('\n')
        self.transitions = {
            ('q0', 'a'): ('q0', '1', 'R'),
            ('q0', ' '): ('q1', ' ', 'L'),
            ('q1', 'a'): ('q1', 'a', 'L'),
            ('q1', '1'): ('q2', 'a', 'R'),
            ('q2', 'a'): ('q2', 'a', 'R'),
            ('q2', ' '): ('q1', 'a', 'L'),
            ('q1', ' '): ('q3', ' ', 'R'),
            # Agregar más transiciones aquí
        }
        
        for x in self.transitions:
            print(x)

        # Inicializar la cinta
        input_string = self.tape_entry.get()+'                              '
        
        # Crear la máquina de Turing
        self.turing_machine = TuringMachine(self.states, self.alphabet, self.alphabet, self.transitions,
                                            self.initial_state, self.accept_states, self.reject_states)
        self.turing_machine.reset(input_string)

        self.update_tape_view()
        self.paso_button.config(state=tk.NORMAL)

    def paso_simulation(self):
        # Ejecutar un paso de la simulación
        result = self.turing_machine.paso()
        self.update_tape_view()

        if result == "ACCEPTED":
            messagebox.showinfo("Resultado", "Cadena aceptada")
            self.paso_button.config(state=tk.DISABLED)
        elif result == "REJECTED":
            messagebox.showinfo("Resultado", "Cadena rechazada")
            self.paso_button.config(state=tk.DISABLED)

    def update_tape_view(self):
        # Actualizar la visualización de la cinta
        tape_content = ''.join(self.turing_machine.tape)
        head_pos = self.turing_machine.head_position
        tape_display = tape_content[:head_pos] + "[" + tape_content[head_pos] + "]" + tape_content[head_pos+1:]
        self.tape_label.config(text=f"Cinta: {tape_display}")

# Iniciar la aplicación
if __name__ == "__main__":
    app = TuringMachineSimulator()
    app.mainloop()

def save_configuration(self):
        config = {
            "states": self.states,
            "alphabet": self.alphabet,
            "tape_alphabet": self.alphabet,
            "transitions": self.transitions,
            "initial_state": self.initial_state,
            "accept_states": self.accept_states,
            "reject_states": self.reject_states
        }
        filepath = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        with open(filepath, 'w') as f:
            json.dump(config, f)

def load_configuration(self):
    filepath = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    with open(filepath, 'r') as f:
        config = json.load(f)
    
    self.states = config["states"]
    self.alphabet = config["alphabet"]
    self.transitions = config["transitions"]
    self.initial_state = config["initial_state"]
    self.accept_states = config["accept_states"]
    self.reject_states = config["reject_states"]

    # Actualizar entradas en la interfaz
    self.states_entry.delete(0, tk.END)
    self.states_entry.insert(0, ','.join(self.states))

    self.alphabet_entry.delete(0, tk.END)
    self.alphabet_entry.insert(0, ','.join(self.alphabet))