import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
from ui_paciente import open_patient_dashboard
from ui_admin import open_admin_dashboard
from database import obtener_conexion
from recursos import obtener_ruta_recurso
from ui_regis import registrar
        
def mostrar_login_paciente(ventana_seleccion):
    def login():
        username = dni.get()
        password = passw.get()

        conn = obtener_conexion()
        c = conn.cursor()
        c.execute("SELECT * FROM usuarios WHERE Cedula = ? AND Tipo = 'Paciente'", (username,))
        usuario = c.fetchone()

        if usuario and password == usuario[7]:  # Contraseña simple para ejemplo
            open_patient_dashboard()
            root.destroy()  # Cierra la ventana de login
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")

    root = tk.Toplevel()
    root.title("Inicio de Sesión - Paciente")
    root.geometry("800x620")

    ruta_fondo_2 = obtener_ruta_recurso("img_recursos/fondo1.jpg")
    ruta_user = obtener_ruta_recurso("img_recursos/rec1.png")
    ruta_pass = obtener_ruta_recurso("img_recursos/rec2.png")
    
    img_fondo = ImageTk.PhotoImage(Image.open(ruta_fondo_2).resize((800, 620)))

    # Canvas para la imagen de fondo
    canvas1 = tk.Canvas(root, width=800, height=620)
    canvas1.pack(fill="both", expand=True)

    # Coloca la imagen en el canvas
    canvas1.create_image(0, 0, anchor="nw", image=img_fondo)

    # Titulo
    titulo = tk.Label(canvas1, text="Iniciar Sesión", fg="white", font=("Comic Sans", 16, "bold"), bg="steel blue", pady=5)
    titulo.pack(pady=20)

    # Intruccion Cédula
    label_ced = tk.Label(canvas1, text="Cédula: ", fg="white", font=("Comic Sans", 16, "bold"), bg="steel blue", pady=5)
    label_ced.pack(pady=5)
    
    # Contenedor para el campo de cédula con el icono
    frame_dni = tk.Frame(canvas1, bg="steel blue", pady=5)
    frame_dni.pack()

    # Cargar el icono de cédula
    icono_dni = ImageTk.PhotoImage(Image.open(ruta_user).resize((30, 30)))

    # Mostrar la imagen del icono
    icono_label = tk.Label(frame_dni, image=icono_dni, fg="white", font=("Comic Sans", 16, "bold"), bg="steel blue", pady=5)
    icono_label.pack(side="left")

    # Caja para ingresar el número de cédula
    dni = tk.Entry(frame_dni, width=20, font=("Comic Sans", 14, "bold"))
    dni.pack(side="left", padx=5)
    
    # Contenedor para el campo de password con el icono
    label_password = tk.Label(canvas1, text="Contraseña: ", fg="white", font=("Comic Sans", 16, "bold"), bg="steel blue", pady=5)
    label_password.pack(pady=5)
    
    # Contenedor para el campo pass
    frame_pass= tk.Frame(canvas1, bg="steel blue", pady=5)
    frame_pass.pack()

    # Cargar el icono de pass
    icono_pass = ImageTk.PhotoImage(Image.open(ruta_pass).resize((30, 30)))

    # Crear un label para mostrar la imagen
    icono_label_pass = tk.Label(frame_pass, image=icono_pass, bg="steel blue", pady=5)
    icono_label_pass.pack(side="left")

    # Caja para ingresar pass
    passw = tk.Entry(frame_pass, width=20, font=("Comic Sans", 14, "bold"), show="*")
    passw.pack(side="left", padx=5)

    # Botón para verificar
    boton_verificar = tk.Button(canvas1, text="Iniciar Sesión", command=login, height=2, width=15, bg="sea green", fg="white", font=("Comic Sans", 10, "bold"))
    boton_verificar.pack(pady=20)
    
    # Intruccion registro
    label_reg = tk.Label(canvas1, text="¿Eres un paciente nuevo?", fg="white", font=("Comic Sans", 12, "bold italic"), bg="blue2", pady=5)
    label_reg.pack(pady=5)
    
    # Botón para abrir el registro
    boton_registro = tk.Button(canvas1, text="Registrarse", command=registrar, height=2, width=15, bg="SkyBlue3", fg="white", font=("Comic Sans", 10, "bold"))
    boton_registro.pack(padx=50, pady=20)

    # Botón para salir de la aplicación
    boton_salir = tk.Button(canvas1, text="Regresar", command=lambda: regresar(ventana_seleccion, root), height=2, width=10, bg="red", fg="white", font=("Comic Sans", 10, "bold"))
    boton_salir.pack(padx=50, pady=20)

    root.mainloop()

def mostrar_login_admin(ventana_seleccion):  # Acepta el argumento
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

    root = tk.Toplevel()
    root.title("Inicio de Sesión - Paciente")
    root.geometry("800x620")

    ruta_fondo_2 = obtener_ruta_recurso("img_recursos/fondo1.jpg")
    ruta_user = obtener_ruta_recurso("img_recursos/rec1.png")
    ruta_pass = obtener_ruta_recurso("img_recursos/rec2.png")
    
    img_fondo = ImageTk.PhotoImage(Image.open(ruta_fondo_2).resize((800, 620)))

    # Canvas para la imagen de fondo
    canvas1 = tk.Canvas(root, width=800, height=620)
    canvas1.pack(fill="both", expand=True)

    # Coloca la imagen en el canvas
    canvas1.create_image(0, 0, anchor="nw", image=img_fondo)

    # Titulo
    titulo = tk.Label(canvas1, text="Iniciar Sesión", fg="white", font=("Comic Sans", 16, "bold"), bg="steel blue", pady=5)
    titulo.pack(pady=20)

    # Intruccion Cédula
    label_ced = tk.Label(canvas1, text="Cédula: ", fg="white", font=("Comic Sans", 16, "bold"), bg="steel blue", pady=5)
    label_ced.pack(pady=5)
    
    # Contenedor para el campo de cédula con el icono
    frame_dni = tk.Frame(canvas1, bg="steel blue", pady=5)
    frame_dni.pack()

    # Cargar el icono de cédula
    icono_dni = ImageTk.PhotoImage(Image.open(ruta_user).resize((30, 30)))

    # Mostrar la imagen del icono
    icono_label = tk.Label(frame_dni, image=icono_dni, fg="white", font=("Comic Sans", 16, "bold"), bg="steel blue", pady=5)
    icono_label.pack(side="left")

    # Caja para ingresar el número de cédula
    dni = tk.Entry(frame_dni, width=20, font=("Comic Sans", 14, "bold"))
    dni.pack(side="left", padx=5)
    
    # Contenedor para el campo de password con el icono
    label_password = tk.Label(canvas1, text="Contraseña: ", fg="white", font=("Comic Sans", 16, "bold"), bg="steel blue", pady=5)
    label_password.pack(pady=5)
    
    # Contenedor para el campo pass
    frame_pass= tk.Frame(canvas1, bg="steel blue", pady=5)
    frame_pass.pack()

    # Cargar el icono de pass
    icono_pass = ImageTk.PhotoImage(Image.open(ruta_pass).resize((30, 30)))

    # Crear un label para mostrar la imagen
    icono_label_pass = tk.Label(frame_pass, image=icono_pass, bg="steel blue", pady=5)
    icono_label_pass.pack(side="left")

    # Caja para ingresar pass
    passw = tk.Entry(frame_pass, width=20, font=("Comic Sans", 14, "bold"), show="*")
    passw.pack(side="left", padx=5)

    # Botón para verificar
    boton_verificar = tk.Button(canvas1, text="Iniciar Sesión", command=login, height=2, width=15, bg="sea green", fg="white", font=("Comic Sans", 10, "bold"))
    boton_verificar.pack(pady=20)
    
    # Botón para salir de la aplicación
    boton_salir = tk.Button(canvas1, text="Regresar", command=lambda: regresar(ventana_seleccion, root), height=2, width=10, bg="red", fg="white", font=("Comic Sans", 10, "bold"))
    boton_salir.pack(padx=50, pady=20)

    root.mainloop()

def regresar(ventana_seleccion, ventana_login):
    ventana_login.destroy()  # Cierra la ventana de login
    ventana_seleccion.deiconify()  # Hace visible la ventana de selección
