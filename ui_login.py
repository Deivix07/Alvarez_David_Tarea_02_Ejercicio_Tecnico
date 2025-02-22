import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
from ui_paciente import open_patient_dashboard
from ui_admin import open_admin_dashboard
from database import obtener_conexion
from recursos import obtener_ruta_recurso
from ui_regis import registrar
from funciones import mostrar_seleccion_tipo

def mostrar_login_paciente():
    def login():
        username = dni.get()
        password = passw.get()

        conn = obtener_conexion()
        c = conn.cursor()
        c.execute("SELECT * FROM usuarios WHERE Cedula = ? AND Tipo = 'Paciente'", (username,))
        usuario = c.fetchone()

        if usuario and password == usuario[7]:  # Contraseña simple para ejemplo
            usuario_id = usuario[0]  # Recupera el ID del usuario desde la base de datos
            root.destroy()  # Cierra la ventana de login
            open_patient_dashboard(usuario_id)  # Pasa el usuario_id a la interfaz del paciente
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")
            

    root = tk.Tk()  # Usar Tk() en lugar de Toplevel()
    root.title("Inicio de Sesión - Paciente")
    root.geometry("800x620")  # Ajustar el tamaño de la ventana

    # Cargar imágenes para los íconos
    ruta_user = obtener_ruta_recurso("img_recursos/rec1.png")
    ruta_pass = obtener_ruta_recurso("img_recursos/rec2.png")
    
    icono_dni = ImageTk.PhotoImage(Image.open(ruta_user).resize((30, 30)))  # Cédula
    icono_pass = ImageTk.PhotoImage(Image.open(ruta_pass).resize((30, 30)))  # Contraseña
    
    # Canvas para la imagen de fondo
    canvas1 = tk.Canvas(root, width=800, height=620)
    canvas1.pack(fill="both", expand=True)

    # Titulo
    titulo = tk.Label(canvas1, text="Iniciar Sesión", fg="white", font=("Comic Sans", 16, "bold"), bg="steel blue", pady=5)
    titulo.pack(pady=20)

    # Cédula
    label_ced = tk.Label(canvas1, text="Cédula: ", fg="white", font=("Comic Sans", 16, "bold"), bg="steel blue", pady=5)
    label_ced.pack(pady=5)

    # Contenedor para el campo de cédula con el icono
    frame_dni = tk.Frame(canvas1, bg="steel blue", pady=5)
    frame_dni.pack()

    # Mostrar la imagen del icono de cédula
    icono_label = tk.Label(frame_dni, image=icono_dni, fg="white", font=("Comic Sans", 16, "bold"), bg="steel blue", pady=5)
    icono_label.pack(side="left")

    # Caja para ingresar el número de cédula
    dni = tk.Entry(frame_dni, width=20, font=("Comic Sans", 14, "bold"))
    dni.pack(side="left", padx=5)
    
    # Contraseña
    label_password = tk.Label(canvas1, text="Contraseña: ", fg="white", font=("Comic Sans", 16, "bold"), bg="steel blue", pady=5)
    label_password.pack(pady=5)

    # Contenedor para el campo de contraseña con el icono
    frame_pass = tk.Frame(canvas1, bg="steel blue", pady=5)
    frame_pass.pack()

    # Mostrar la imagen del icono de contraseña
    icono_label_pass = tk.Label(frame_pass, image=icono_pass, bg="steel blue", pady=5)
    icono_label_pass.pack(side="left")

    # Caja para ingresar la contraseña
    passw = tk.Entry(frame_pass, width=20, font=("Comic Sans", 14, "bold"), show="*")
    passw.pack(side="left", padx=5)

    # Botón para verificar
    boton_verificar = tk.Button(canvas1, text="Iniciar Sesión", command=login, height=2, width=15, bg="sea green", fg="white", font=("Comic Sans", 10, "bold"))
    boton_verificar.pack(pady=20)

    # Botón para regresar a la selección de tipo de usuario
    boton_salir = tk.Button(canvas1, text="Regresar", command= lambda: [root.destroy(), mostrar_seleccion_tipo()], height=2, width=10, bg="red", fg="white", font=("Comic Sans", 10, "bold"))
    boton_salir.pack(pady=20)

    root.mainloop()


def mostrar_login_admin():
    def login():
        username = dni.get()
        password = passw.get()

        conn = obtener_conexion()
        c = conn.cursor()
        c.execute("SELECT * FROM usuarios WHERE Cedula = ? AND Tipo = 'Administrador'", (username,))
        usuario = c.fetchone()

        if usuario and password == usuario[7]:  # Contraseña simple para ejemplo
            open_admin_dashboard()
            root.destroy()  # Cierra la ventana de login
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")

    root = tk.Tk()  # Usar Tk() en lugar de Toplevel()
    root.title("Inicio de Sesión - Administrador")
    root.geometry("800x620")  # Ajustar el tamaño de la ventana

    # Cargar imágenes para los íconos
    ruta_user = obtener_ruta_recurso("img_recursos/rec1.png")
    ruta_pass = obtener_ruta_recurso("img_recursos/rec2.png")
    
    icono_dni = ImageTk.PhotoImage(Image.open(ruta_user).resize((30, 30)))  # Cédula
    icono_pass = ImageTk.PhotoImage(Image.open(ruta_pass).resize((30, 30)))  # Contraseña

    # Canvas para la imagen de fondo
    canvas1 = tk.Canvas(root, width=800, height=620)
    canvas1.pack(fill="both", expand=True)

    # Titulo
    titulo = tk.Label(canvas1, text="Iniciar Sesión", fg="white", font=("Comic Sans", 16, "bold"), bg="steel blue", pady=5)
    titulo.pack(pady=20)

    # Cédula
    label_ced = tk.Label(canvas1, text="Cédula: ", fg="white", font=("Comic Sans", 16, "bold"), bg="steel blue", pady=5)
    label_ced.pack(pady=5)

    # Contenedor para el campo de cédula con el icono
    frame_dni = tk.Frame(canvas1, bg="steel blue", pady=5)
    frame_dni.pack()

    # Mostrar la imagen del icono de cédula
    icono_label = tk.Label(frame_dni, image=icono_dni, fg="white", font=("Comic Sans", 16, "bold"), bg="steel blue", pady=5)
    icono_label.pack(side="left")

    # Caja para ingresar el número de cédula
    dni = tk.Entry(frame_dni, width=20, font=("Comic Sans", 14, "bold"))
    dni.pack(side="left", padx=5)

    # Contraseña
    label_password = tk.Label(canvas1, text="Contraseña: ", fg="white", font=("Comic Sans", 16, "bold"), bg="steel blue", pady=5)
    label_password.pack(pady=5)

    # Contenedor para el campo de contraseña con el icono
    frame_pass = tk.Frame(canvas1, bg="steel blue", pady=5)
    frame_pass.pack()

    # Mostrar la imagen del icono de contraseña
    icono_label_pass = tk.Label(frame_pass, image=icono_pass, bg="steel blue", pady=5)
    icono_label_pass.pack(side="left")

    # Caja para ingresar la contraseña
    passw = tk.Entry(frame_pass, width=20, font=("Comic Sans", 14, "bold"), show="*")
    passw.pack(side="left", padx=5)

    # Botón para verificar
    boton_verificar = tk.Button(canvas1, text="Iniciar Sesión", command=login, height=2, width=15, bg="sea green", fg="white", font=("Comic Sans", 10, "bold"))
    boton_verificar.pack(pady=20)

    # Botón para regresar a la selección de tipo de usuario
    boton_salir = tk.Button(canvas1, text="Regresar", command= lambda: [root.destroy(), mostrar_seleccion_tipo()], height=2, width=10, bg="red", fg="white", font=("Comic Sans", 10, "bold"))
    boton_salir.pack(pady=20)

    root.mainloop()
