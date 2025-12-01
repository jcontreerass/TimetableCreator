# main.py
import tkinter as tk
from interface import AplicacionGUI  # Importamos la clase de la interfaz

if __name__ == "__main__":
    # Creamos la ventana raíz
    root = tk.Tk()

    # Iniciamos la aplicación que está definida en el otro archivo
    app = AplicacionGUI(root)

    # Bucle principal
    root.mainloop()