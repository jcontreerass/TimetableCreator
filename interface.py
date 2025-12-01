# interfaz.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from fpdf import FPDF

# IMPORTANTE: Aquí importamos el otro archivo
import algorythm


class AplicacionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador de Horarios")
        self.root.geometry("800x600")

        self.datos_globales = []
        self.columnas_globales = []

        self.crear_widgets()

    def crear_widgets(self):
        # ... (Aquí va to do tu código de botones, entradas y Treeview) ...
        # ... (Es el mismo código de tkinter que te di antes) ...

        # Ejemplo de botón:
        btn = ttk.Button(self.root, text="Generar", command=self.ejecutar_logica)
        btn.pack()

    def ejecutar_logica(self):
        # 1. Recoger datos de la interfaz
        dias = 5  # (O lo que diga tu entry_dias.get())
        horas = 6

        # 2. Preparar el dataset
        dataset_actual = algorythm.dataset_ejemplo.copy()  # Usamos el dataset del otro archivo
        dataset_actual['n_days'] = dias
        dataset_actual['n_hours_day'] = horas

        # 3. LLAMAR A LA LÓGICA DEL OTRO ARCHIVO
        # Fíjate en el prefijo "algoritmo."
        mejor_ind, fit, _, _, _ = algorythm.run_ga(
            dataset=dataset_actual,
            pop_size=50
            # ... resto de parámetros
        )

        print(f"Algoritmo terminado. Mejor individuo: {mejor_ind}")

        # 4. Actualizar la tabla visual (Treeview)
        # Aquí llamarías a tu función de llenar tabla usando 'mejor_ind'
        self.llenar_tabla(mejor_ind, dias, horas)

    def llenar_tabla(self, individuo, dias, horas):
        # Tu lógica para pintar en el Treeview
        pass

    def generar_pdf(self):
        # Tu lógica de FPDF
        pass

