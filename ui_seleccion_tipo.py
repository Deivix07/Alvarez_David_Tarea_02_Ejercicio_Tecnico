import tkinter as tk
from PIL import ImageTk, Image
from ui_login import mostrar_login_paciente, mostrar_login_admin
from recursos import obtener_ruta_recurso

def mostrar_seleccion_tipo():
    ventana_seleccion = tk.Tk()
    ventana_seleccion.title("Identifícate")
    ventana_seleccion.geometry("800x620")

    ruta_fondo_1 = obtener_ruta_recurso("img_recursos/fondo1.jpg")
    img_fondo = ImageTk.PhotoImage(Image.open(ruta_fondo_1).resize((800, 620)))

    # Canvas para la imagen de fondo
    canvas1 = tk.Canvas(ventana_seleccion, width=800, height=620)
    canvas1.pack(fill="both", expand=True)

    # Coloca la imagen en el canvas
    canvas1.create_image(0, 0, anchor="nw", image=img_fondo)

    # Titulo
    titulo = tk.Label(canvas1, text="Bienvenido al Sistema de Agendamiento", fg="white", font=("Comic Sans", 16, "bold"), bg="steel blue", pady=5)
    titulo.pack(pady=20)
    
    tk.Label(canvas1, text="¿Eres Administrador o Paciente?").pack(pady=10)

    # Botones para seleccionar tipo de usuario
    tk.Button(canvas1, text="Paciente", command=lambda: seleccionar_paciente(ventana_seleccion)).pack(pady=5)
    tk.Button(canvas1, text="Administrador", command=lambda: seleccionar_admin(ventana_seleccion)).pack(pady=5)

    ventana_seleccion.mainloop()

# Función para seleccionar paciente
def seleccionar_paciente(ventana_seleccion):
    ventana_seleccion.withdraw()  # Oculta la ventana de selección
    mostrar_login_paciente(ventana_seleccion)  # Llama al login de paciente

# Función para seleccionar administrador
def seleccionar_admin(ventana_seleccion):
    ventana_seleccion.withdraw()  # Oculta la ventana de selección
    mostrar_login_admin(ventana_seleccion)  # Llama al login de administrador