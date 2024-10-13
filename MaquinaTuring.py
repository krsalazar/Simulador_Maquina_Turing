import tkinter as tk
from tkinter import messagebox, filedialog

class SimuladorMaquinaTuring(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simulador de Máquina de Turing")

        # Variables de la máquina
        self.estados = []
        self.alfabeto = []
        self.cinta_alfabeto = []
        self.transiciones = {}
        self.estado_inicial = ""
        self.estado_aceptacion = []
        self.estado_rechazado = []
        self.maquina_turing = None

        # Interfaz de usuario
        self.crea_ventana()

    def crea_ventana(self):
        # Entrada para el alfabeto
        tk.Label(self, text="Alfabeto de entrada:").grid(row=0, column=0, sticky="w")
        self.alfabeto_entrada = tk.Entry(self)
        self.alfabeto_entrada.grid(row=0, column=1)

        # Entrada para los estados
        tk.Label(self, text="Estados:").grid(row=1, column=0, sticky="w")
        self.estados_entrada = tk.Entry(self)
        self.estados_entrada.grid(row=1, column=1)

        # Estado inicial
        tk.Label(self, text="Estado inicial:").grid(row=2, column=0, sticky="w")
        self.estado_inicial_entrada = tk.Entry(self)
        self.estado_inicial_entrada.grid(row=2, column=1)

        # Estados de aceptación
        tk.Label(self, text="Estados de aceptación:").grid(row=3, column=0, sticky="w")
        self.estado_aceptacion_entrada = tk.Entry(self)
        self.estado_aceptacion_entrada.grid(row=3, column=1)

        # Estados de rechazo
        tk.Label(self, text="Estados de rechazo:").grid(row=4, column=0, sticky="w")
        self.estado_rechazado_entrada = tk.Entry(self)
        self.estado_rechazado_entrada.grid(row=4, column=1)

        # Cinta
        tk.Label(self, text="Entrada de cinta:").grid(row=5, column=0, sticky="w")
        self.cinta_entrada = tk.Entry(self)
        self.cinta_entrada.grid(row=5, column=1)

        # Botón para iniciar la simulación
        self.boton_inicio = tk.Button(self, text="Iniciar Simulación", command=self.iniciar_simulacion)
        self.boton_inicio.grid(row=6, column=0, columnspan=2)

        # Área de visualización de la cinta
        self.cinta_etiqueta = tk.Label(self, text="Cinta: ")
        self.cinta_etiqueta.grid(row=7, column=0, columnspan=2)

        # Botón de paso a paso
        self.boton_pasos = tk.Button(self, text="Paso a Paso", command=self.step_simulation)
        self.boton_pasos.grid(row=8, column=0, columnspan=2)
        self.boton_pasos.config(state=tk.DISABLED)

    def iniciar_simulacion(self):
        # Inicializar la máquina de Turing
        self.estados = self.estados_entrada.get().split(',')
        self.alfabeto = self.alfabeto_entrada.get().split(',')
        self.estado_inicial = self.estado_inicial_entrada.get()
        self.estado_aceptacion = self.estado_aceptacion_entrada.get().split(',')
        self.estado_rechazado = self.estado_rechazado_entrada.get().split(',')
        
        # Definir las transiciones
        self.transiciones = {
            ('q0', '0'): ('q1', '1', 'R'),
            ('q1', '1'): ('q2', '0', 'L'),
            # Agregar más transiciones aquí
        }
        
        # Inicializar la cinta
        cadena_entrada = self.cinta_entrada.get()
        
        # Crear la máquina de Turing
        self.maquina_turing = TuringMachine(self.estados, self.alfabeto, self.alfabeto, self.transiciones,
                                            self.estado_inicial, self.estado_aceptacion, self.estado_rechazado)
        self.maquina_turing.reset(cadena_entrada)

        self.actualiza_vista_cinta()
        self.boton_pasos.config(state=tk.NORMAL)

    def step_simulation(self):
        # Ejecutar un paso de la simulación
        resultado = self.maquina_turing.step()
        self.actualiza_vista_cinta()

        if resultado == "ACCEPTED":
            messagebox.showinfo("Resultado", "Cadena aceptada")
            self.boton_pasos.config(state=tk.DISABLED)
        elif resultado == "REJECTED":
            messagebox.showinfo("Resultado", "Cadena rechazada")
            self.boton_pasos.config(state=tk.DISABLED)

    def actualiza_vista_cinta(self):
        # Actualizar la visualización de la cinta
        contenido_cinta = ''.join(self.maquina_turing.cinta)
        posicion_cabeza = self.maquina_turing.head_position
        mostrar_cinta = contenido_cinta[:posicion_cabeza] + "[" + contenido_cinta[posicion_cabeza] + "]" + contenido_cinta[posicion_cabeza+1:]
        self.cinta_etiqueta.config(text=f"Cinta: {mostrar_cinta}")

# Iniciar la aplicación
if __name__ == "__main__":
    app = SimuladorMaquinaTuring()
    app.mainloop()