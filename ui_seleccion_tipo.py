import tkinter as tk
from ui_login import mostrar_login_paciente, mostrar_login_admin

def mostrar_seleccion_tipo():
    ventana_seleccion = tk.Tk()
    ventana_seleccion.title("Identifícate")
    ventana_seleccion.geometry("800x620")

    # Canvas para la imagen de fondo
    canvas1 = tk.Canvas(ventana_seleccion, bg="SteelBlue3")
    canvas1.pack(fill="both", expand=True)

    # Titulo
    titulo = tk.Label(canvas1, text="Bienvenido al Sistema de Agendamiento", fg="white", font=("Comic Sans", 16, "bold"), bg="steel blue", pady=5)
    titulo.pack(pady=20)

    titulo2 = tk.Label(canvas1, text="¿Eres Administrador o Paciente?", fg="white", font=("Comic Sans", 16, "bold"), bg="steel blue", pady=5)
    titulo2.pack(pady=20)
    # Función para cerrar la ventana actual y abrir el login correspondiente
    def cerrar_y_mostrar_login(tipo):
        ventana_seleccion.destroy()  # Cerrar la ventana actual
        if tipo == "paciente":
            mostrar_login_paciente()
        else:
            mostrar_login_admin()

    # Botones para seleccionar tipo de usuario
    tk.Button(canvas1, text="Paciente", command= lambda: cerrar_y_mostrar_login("paciente"), height=3, width=20, bg="dark orange", fg="white", font=("Comic Sans", 12, "bold")).pack(pady=20)
    
    tk.Button(canvas1, text="Administrador", command= lambda: cerrar_y_mostrar_login("administrador"), height=3, width=20, bg="brown4", fg="white", font=("Comic Sans", 12, "bold")).pack(pady=20)
    
    ventana_seleccion.mainloop()