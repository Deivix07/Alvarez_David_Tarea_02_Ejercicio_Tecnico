import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
from recursos import obtener_ruta_recurso
from tkcalendar import Calendar
import sqlite3

# Globales para las entradas de texto
dni, nombres, apellidos, combo_sexo, calendario, correo, password, repetir_password = None, None, None, None, None, None, None, None

def registrar():
    global dni, nombres, apellidos, combo_sexo, calendario, correo, password, repetir_password
    # Ventana secundaria para el registro
    regis = tk.Toplevel() 
    regis.title("REGISTRO BANCARIO")
    regis.geometry("380x620")
    
    # Título
    titulo= tk.Label(regis, text="REGISTRO DE USUARIO",fg="black",font=("Comic Sans", 13,"bold"),pady=5)
    titulo.grid(row=0, column=0, columnspan=1, padx=10, pady=5)

    # Marco principal
    marcop = tk.LabelFrame(regis,font=("Comic Sans", 10,"bold"))
    marcop.config(bd=0,pady=5)
    marcop.grid(row=2, column=0, padx=10, pady=10, sticky="n")
    
    ruta_datos = obtener_ruta_recurso("img_recursos/rec3.png")
    
    # Carga la imagen para el registro de usuario
    imagen_registro = ImageTk.PhotoImage(Image.open(ruta_datos).resize((70, 50)))
    
    label_imagen= tk.Label(marcop, image= imagen_registro)
    label_imagen.grid(row=1, column=0, pady=5)
    
    marco = tk.LabelFrame(marcop, text="Datos personales",font=("Comic Sans", 10,"bold"))
    marco.config(bd=2,pady=5)
    marco.grid(row=2, column=0, padx=10, pady=10, sticky="n")

    # Marco para datos personales
    label_dni=tk.Label(marco,text="DNI: ",font=("Comic Sans", 10,"bold")).grid(row=0,column=0,sticky='s',padx=5,pady=8)
    dni=tk.Entry(marco,width=25)
    dni.focus()
    dni.grid(row=0, column=1, padx=5, pady=8)
    
    # Formulario de registro de datos personales
    label_nombres=tk.Label(marco,text="Nombre: ",font=("Comic Sans", 10,"bold")).grid(row=1,column=0,sticky='s',padx=10,pady=8)
    nombres=tk.Entry(marco,width=25)
    nombres.grid(row=1, column=1, padx=10, pady=8)

    label_apellidos=tk.Label(marco,text="Apellidos: ",font=("Comic Sans", 10,"bold")).grid(row=2,column=0,sticky='s',padx=10,pady=8)
    apellidos=tk.Entry(marco,width=25)
    apellidos.grid(row=2, column=1, padx=10, pady=8)

    label_sexo=tk.Label(marco,text="Sexo: ",font=("Comic Sans", 10,"bold")).grid(row=3,column=0,sticky='s',padx=10,pady=8)
    combo_sexo=ttk.Combobox(marco,values=["Masculino", "Femenino"], width=22,state="readonly")
    combo_sexo.current(0)
    combo_sexo.grid(row=3,column=1,padx=10,pady=8)
    
    # Calendario para la fecha de nacimiento
    label_fecha_nacimiento = tk.Label(marco, text="Fecha de nacimiento: ", font=("Comic Sans", 10,"bold"))
    label_fecha_nacimiento.grid(row=4, column=0, sticky='s', padx=10, pady=8)
    
    # Crear un calendario para seleccionar la fecha
    calendario = Calendar(marco, selectmode="day", date_pattern="dd/mm/yyyy", width=20, font=("Comic Sans", 10))
    calendario.grid(row=4, column=1, padx=10, pady=8)

    label_correo=tk.Label(marco,text="Correo electronico: ",font=("Comic Sans", 10,"bold")).grid(row=5,column=0,sticky='s',padx=10,pady=8)
    correo=tk.Entry(marco,width=25)
    correo.grid(row=5, column=1, padx=10, pady=8)

    label_password=tk.Label(marco,text="Contraseña: ",font=("Comic Sans", 10,"bold")).grid(row=6,column=0,sticky='s',padx=10,pady=8)
    password=tk.Entry(marco,width=25,show="*")
    password.grid(row=6, column=1, padx=10, pady=8)

    label_password=tk.Label(marco,text="Repetir contraseña: ",font=("Comic Sans", 10,"bold")).grid(row=7,column=0,sticky='s',padx=10,pady=8)
    repetir_password=tk.Entry(marco,width=25,show="*")
    repetir_password.grid(row=7, column=1, padx=10, pady=8)

    # Frame botones
    frame_botones=tk.Frame(regis)
    frame_botones.grid(row=3, column=0, columnspan=1, pady=10)

    # Botones
    boton_registrar=tk.Button(frame_botones,text="REGISTRAR",command=Registrar_usuario ,height=2,width=10,bg="green",fg="white",font=("Comic Sans", 10,"bold")).grid(row=0, column=1, padx=10, pady=15)
    boton_limpiar=tk.Button(frame_botones,text="LIMPIAR",command=Limpiar_formulario ,height=2,width=10,bg="gray",fg="white",font=("Comic Sans", 10,"bold")).grid(row=0, column=2, padx=10, pady=15)
    boton_cancelar=tk.Button(frame_botones,text="CERRAR",command=regis.destroy, height=2,width=10,bg="red",fg="white",font=("Comic Sans", 10,"bold")).grid(row=0, column=3, padx=10, pady=15)

# Función para obtener la fecha seleccionada y convertirla
def obtener_fecha():
    fecha_seleccionada = calendario.get_date()  # Devuelve la fecha en formato dd/mm/yyyy
    fecha_convertida = "/".join(reversed(fecha_seleccionada.split("/")))  # Convertir a yyyy-mm-dd
    return fecha_convertida
    
# Método para ejecutar una consulta en la base de datos
def Ejecutar_consulta_user(consulta_user, parameters_user=()):
    with sqlite3.connect('clinica.db') as conexion:
        cursor = conexion.cursor()
        result = cursor.execute(consulta_user, parameters_user)
        conexion.commit()
    return result

# Método para limpiar el formulario de registro
def Limpiar_formulario():
    dni.delete(0, tk.END)
    nombres.delete(0, tk.END)
    apellidos.delete(0, tk.END)
    combo_sexo.set('')  # Restablecer el combobox
    correo.delete(0, tk.END)
    password.delete(0, tk.END)
    repetir_password.delete(0, tk.END)

# Método para validar que el formulario esté completo
def Validar_formulario_completo():
    if len(dni.get()) != 0 and len(nombres.get()) != 0 and len(apellidos.get()) != 0 and len(combo_sexo.get()) != 0 and len(correo.get()) != 0 and len(password.get()) != 0 and len(repetir_password.get()) != 0:
        if not dni.get().isdigit():
            messagebox.showerror("ERROR EN REGISTRO", "El DNI debe ser un número.")
            return False
        return True
    else:
        messagebox.showerror("ERROR EN REGISTRO", "Complete todos los campos del formulario")
        return False

# Método para validar que las contraseñas coincidan
def Validar_contraseña():
    if password.get() == repetir_password.get():
        return True
    else:
        messagebox.showerror("ERROR EN REGISTRO", "Contraseñas no coinciden")
        return False

# Método para verificar si el DNI ya está registrado
def Validar_dni():
    dni_input = dni.get()
    with sqlite3.connect('clinica.db') as conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE Cedula = ?", (dni_input,))
        dnix = cursor.fetchall()
        if len(dnix) > 0:
            messagebox.showerror("ERROR EN REGISTRO", "DNI registrado anteriormente")
            return False
    return True

# Método para registrar al usuario
def Registrar_usuario():
    fecha_nacimiento = obtener_fecha()  # Obtener la fecha de nacimiento convertida
    if Validar_formulario_completo() and Validar_contraseña() and Validar_dni():
        consulta_user = '''INSERT INTO usuarios (Cedula, Nombre, Apellido, Sexo, FechaNacimiento, Correo, Contraseña, Tipo)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
        parameters_user = (
            dni.get(),
            nombres.get(),
            apellidos.get(),
            combo_sexo.get(),
            fecha_nacimiento,  # Usamos la fecha convertida
            correo.get(),
            password.get(),
            "Paciente"  # Asignamos tipo 'Paciente' por defecto, puedes cambiarlo si es necesario
        )
        Ejecutar_consulta_user(consulta_user, parameters_user)
        messagebox.showinfo("REGISTRO EXITOSO", f'Bienvenido {nombres.get()} {apellidos.get()}')
        Limpiar_formulario()