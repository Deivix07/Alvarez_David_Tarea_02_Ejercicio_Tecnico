import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
from recursos import obtener_ruta_recurso
from tkcalendar import DateEntry
import sqlite3
import re


# Globales para las entradas de texto
dni, nombres, apellidos, combo_sexo, calendario, correo, password, repetir_password = None, None, None, None, None, None, None, None

def registrar():
    global dni, nombres, apellidos, combo_sexo, calendario, correo, password, repetir_password  # Asegúrate de declarar las variables globales
    # Ventana secundaria para el registro
    regis = tk.Toplevel() 
    regis.title("REGISTRO PACIENTES")
    regis.geometry("380x620")
    
    # Título
    titulo= tk.Label(regis, text="REGISTRO DE PACIENTE",fg="black",font=("Comic Sans", 13,"bold"),pady=5)
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
    
    # Calendario desplegable para la fecha de nacimiento
    label_fecha_nacimiento = tk.Label(marco, text="Fecha de nacimiento: ", font=("Comic Sans", 10,"bold"))
    label_fecha_nacimiento.grid(row=4, column=0, sticky='s', padx=10, pady=8)

    calendario = DateEntry(marco, width=22, date_pattern="dd/mm/yyyy", font=("Comic Sans", 10))
    calendario.grid(row=4, column=1, padx=10, pady=8)

    label_correo=tk.Label(marco,text="Correo electrónico: ",font=("Comic Sans", 10,"bold")).grid(row=5,column=0,sticky='s',padx=10,pady=8)
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

# Función para obtener la fecha seleccionada
def obtener_fecha():
    return calendario.get_date()  # Devuelve la fecha en formato dd/mm/yyyy

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
    combo_sexo.set('')  
    correo.delete(0, tk.END)
    password.delete(0, tk.END)
    repetir_password.delete(0, tk.END)

def Validar_formulario_completo():
    # Verifica que todos los campos tengan contenido válido
    for field in [dni, nombres, apellidos, correo, password, repetir_password, combo_sexo, calendario]:
        # Si el campo es un Entry o un Combobox, verificamos su valor
        if isinstance(field, tk.Entry):
            if len(field.get()) == 0:
                messagebox.showerror("ERROR", "Complete todos los campos.")
                return False
        elif isinstance(field, ttk.Combobox):
            if not field.get():  # Verifica si el ComboBox tiene un valor seleccionado
                messagebox.showerror("ERROR", "Seleccione un sexo.")
                return False
        elif isinstance(field, DateEntry):
            if not field.get_date():  # Verifica si se ha seleccionado una fecha en el calendario
                messagebox.showerror("ERROR", "Seleccione una fecha de nacimiento.")
                return False
    
    # Verifica que el DNI sea un número
    if not dni.get().isdigit():
        messagebox.showerror("ERROR", "El DNI debe ser un número.")
        return False

    # Verifica que el DNI tenga 10 dígitos
    if len(dni.get()) != 10:
        messagebox.showerror("ERROR", "El DNI debe tener 10 dígitos.")
        return False

    # Verifica que las contraseñas coincidan
    if password.get() != repetir_password.get():
        messagebox.showerror("ERROR", "Las contraseñas no coinciden.")
        return False
    
        # Validación del correo electrónico
    correo_usuario = correo.get()
    if not re.match(r"[^@]+@[^@]+\.[^@]+", correo_usuario):
        messagebox.showerror("ERROR", "El correo electrónico no tiene un formato válido.")
        return False
    
    return True


# Método para validar el DNI
def Validar_dni():
    dni_usuario = dni.get()
    with sqlite3.connect('clinica.db') as conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE Cedula = ?", (dni_usuario,))
        if cursor.fetchone():  # Si el DNI ya está registrado
            messagebox.showerror("ERROR", "El DNI ya está registrado anteriormente.")
            return False
    return True

# Método para registrar al usuario
def Registrar_usuario():
    if Validar_formulario_completo():  # Verifica si el formulario es válido
        if not Validar_dni():  # Verifica si el DNI ya está registrado
            return  # Si el DNI ya está registrado, no continúa con el registro
        
        # Si todo está bien, realiza la inserción en la base de datos
        fecha_nacimiento = obtener_fecha()
        consulta_user = '''INSERT INTO usuarios (Cedula, Nombre, Apellido, Sexo, FechaNacimiento, Correo, Contraseña, Tipo)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
        parameters_user = (dni.get(), nombres.get(), apellidos.get(), combo_sexo.get(), fecha_nacimiento, correo.get(), password.get(), "Paciente")
        Ejecutar_consulta_user(consulta_user, parameters_user)
        messagebox.showinfo("REGISTRO EXITOSO", f'Bienvenido {nombres.get()} {apellidos.get()}')
        Limpiar_formulario()
