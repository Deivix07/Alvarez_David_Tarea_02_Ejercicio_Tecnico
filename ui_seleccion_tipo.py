import tkinter as tk
from ui_login import mostrar_login_paciente, mostrar_login_admin

def mostrar_seleccion_tipo():
    ventana_seleccion = tk.Tk()
    ventana_seleccion.title("Identifícate")
    ventana_seleccion.geometry("800x620")

    # Canvas para la imagen de fondo
    canvas1 = tk.Canvas(ventana_seleccion, width=800, height=620)
    canvas1.pack(fill="both", expand=True)

    # Titulo
    titulo = tk.Label(canvas1, text="Bienvenido al Sistema de Agendamiento", fg="white", font=("Comic Sans", 16, "bold"), bg="steel blue", pady=5)
    titulo.pack(pady=20)
    
    tk.Label(canvas1, text="¿Eres Administrador o Paciente?").pack(pady=10)

    # Función para cerrar la ventana actual y abrir el login correspondiente
    def cerrar_y_mostrar_login(tipo):
        ventana_seleccion.destroy()  # Cerrar la ventana actual
        if tipo == "paciente":
            mostrar_login_paciente()
        else:
            mostrar_login_admin()

    # Botones para seleccionar tipo de usuario
    tk.Button(canvas1, text="Paciente", command=lambda: cerrar_y_mostrar_login("paciente")).pack(pady=5)
    tk.Button(canvas1, text="Administrador", command=lambda: cerrar_y_mostrar_login("administrador")).pack(pady=5)

    ventana_seleccion.mainloop()