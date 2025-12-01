import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import random
from fpdf import FPDF  # Importamos la librería para PDF

# Variable global para guardar los datos y poder imprimirlos luego
datos_globales = []
columnas_globales = []


def generar_tabla_simulada():
    """
    Genera la tabla en la interfaz y guarda los datos en memoria.
    """
    global datos_globales, columnas_globales

    try:
        n_dias = int(entry_dias.get())
        n_horas = int(entry_horas.get())

        # 1. Configurar columnas
        columnas_globales = ["Hora"] + [f"Día {i + 1}" for i in range(n_dias)]

        # Limpiar tabla GUI
        tabla.delete(*tabla.get_children())
        tabla["columns"] = columnas_globales

        # Configurar cabeceras GUI
        tabla.column("#0", width=0, stretch=tk.NO)
        tabla.column("Hora", anchor=tk.CENTER, width=80)
        tabla.heading("Hora", text="Hora", anchor=tk.CENTER)

        for col in columnas_globales[1:]:
            tabla.column(col, anchor=tk.CENTER, width=100)
            tabla.heading(col, text=col, anchor=tk.CENTER)

        # 2. Generar Datos (Aquí iría tu algoritmo genético)
        asignaturas_falsas = ["IA", "BBDD", "Algoritmia", "Redes", "Estadística", "---", "Prog.", "Física"]
        datos_globales = []  # Reiniciamos la lista de datos

        for h in range(1, n_horas + 1):
            fila = [f"{h}:00"]  # Primera columna es la hora
            for d in range(n_dias):
                asignatura = random.choice(asignaturas_falsas)
                fila.append(asignatura)

            # Guardamos en la variable global y en la tabla visual
            datos_globales.append(fila)
            tabla.insert("", tk.END, values=fila)

        # Habilitar el botón de PDF
        btn_pdf.config(state="normal")

    except ValueError:
        messagebox.showerror("Error", "Introduce números válidos.")


def guardar_pdf():
    """
    Toma los datos de 'datos_globales' y crea un archivo PDF.
    """
    if not datos_globales:
        messagebox.showwarning("Aviso", "Primero genera el horario.")
        return

    # Preguntar dónde guardar el archivo
    archivo = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("Archivos PDF", "*.pdf")],
        title="Guardar Horario"
    )

    if not archivo:  # Si el usuario cancela
        return

    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=10)

        # Título
        pdf.set_font("Arial", style="B", size=16)
        pdf.cell(0, 10, "Horario Boadilla", ln=True, align='C')
        pdf.ln(10)  # Salto de línea

        # Configuración de ancho de celdas
        ancho_hora = 20
        # Calculamos ancho para los días (ancho página A4 es aprox 190 útil)
        ancho_dia = (190 - ancho_hora) / (len(columnas_globales) - 1)

        # --- CABECERA ---
        pdf.set_font("Arial", style="B", size=10)
        # Dibujar celda Hora
        pdf.cell(ancho_hora, 10, columnas_globales[0], border=1, align='C')
        # Dibujar celdas Días
        for col in columnas_globales[1:]:
            pdf.cell(ancho_dia, 10, col, border=1, align='C')
        pdf.ln()  # Salto de línea al terminar cabecera

        # --- DATOS ---
        pdf.set_font("Arial", size=10)
        for fila in datos_globales:
            # Celda Hora
            pdf.cell(ancho_hora, 10, str(fila[0]), border=1, align='C')
            # Celdas Asignaturas
            for dato in fila[1:]:
                pdf.cell(ancho_dia, 10, str(dato), border=1, align='C')
            pdf.ln()

        pdf.output(archivo)
        messagebox.showinfo("Éxito", "PDF guardado correctamente.")

    except Exception as e:
        messagebox.showerror("Error al guardar PDF", str(e))


# --- INTERFAZ GRÁFICA ---
ventana = tk.Tk()
ventana.title("Generador de Horarios + PDF")
ventana.geometry("900x550")

# Panel superior
frame_top = ttk.Frame(ventana, padding=10)
frame_top.pack(fill="x")

ttk.Label(frame_top, text="Días:").pack(side=tk.LEFT)
entry_dias = ttk.Entry(frame_top, width=5)
entry_dias.insert(0, "5")
entry_dias.pack(side=tk.LEFT, padx=5)

ttk.Label(frame_top, text="Horas:").pack(side=tk.LEFT)
entry_horas = ttk.Entry(frame_top, width=5)
entry_horas.insert(0, "6")
entry_horas.pack(side=tk.LEFT, padx=5)

btn_generar = ttk.Button(frame_top, text="Generar Tabla", command=generar_tabla_simulada)
btn_generar.pack(side=tk.LEFT, padx=15)

# BOTÓN PDF (Empieza desactivado)
btn_pdf = ttk.Button(frame_top, text="💾 Guardar como PDF", command=guardar_pdf, state="disabled")
btn_pdf.pack(side=tk.LEFT, padx=5)

# Tabla
frame_tabla = ttk.Frame(ventana, padding=10)
frame_tabla.pack(fill="both", expand=True)

scroll_y = ttk.Scrollbar(frame_tabla, orient="vertical")
scroll_x = ttk.Scrollbar(frame_tabla, orient="horizontal")
tabla = ttk.Treeview(frame_tabla, show="headings",
                     yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

scroll_y.config(command=tabla.yview)
scroll_x.config(command=tabla.xview)
scroll_y.pack(side=tk.RIGHT, fill="y")
scroll_x.pack(side=tk.BOTTOM, fill="x")
tabla.pack(side=tk.LEFT, fill="both", expand=True)

ventana.mainloop()