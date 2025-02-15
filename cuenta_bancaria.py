# Importación de bibliotecas necesarias
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import ImageTk, Image
import os, sys, io, random, sqlite3
from datetime import datetime

# Alvarez_David_Lección_02_Cuenta_Bancaria

""" Desarrollar un programa que simule el comportamiento básico de una cuenta bancaria.
El programa debe permitir realizar operaciones comunes de una cuenta, como consultar el saldo, depositar dinero, retirar dinero, y transferir fondos a otra cuenta """

# Obtiene la ruta de la carpeta de recursos dependiendo de si estamos en un archivo empaquetado o no
def obtener_ruta_recurso(ruta_recurso):
    if getattr(sys, 'frozen', False):  # Si estamos ejecutando el .exe
        return os.path.join(sys._MEIPASS, ruta_recurso)
    else:  # Si estamos ejecutando el código fuente
        return os.path.join(os.path.dirname(__file__), ruta_recurso)

# Cargar imágenes de fondo
ruta_fondo_1 = obtener_ruta_recurso("img_recursos/fondo1.jpg")
ruta_fondo_2 = obtener_ruta_recurso("img_recursos/fondo2.jpg")

# Cargar imágenes interfaz inicio y registro
ruta_user = obtener_ruta_recurso("img_recursos/rec1.png")
ruta_pass = obtener_ruta_recurso("img_recursos/rec2.png")
ruta_datos = obtener_ruta_recurso("img_recursos/rec3.png")
ruta_cuenta = obtener_ruta_recurso("img_recursos/rec4.png")

# Cargar imágenes de operaciones
ruta_dep = obtener_ruta_recurso("img_recursos/img1.png")
ruta_ret = obtener_ruta_recurso("img_recursos/img2.png")
ruta_transf = obtener_ruta_recurso("img_recursos/img3.png")
ruta_historial = obtener_ruta_recurso("img_recursos/img4.png")

# Cargar imágenes de validación
ruta_correcto = obtener_ruta_recurso("img_recursos/img5.png")
ruta_incorrecto = obtener_ruta_recurso("img_recursos/img6.png")
    
# Función para crear la base de datos  
def crear_base_datos():
    # Conectar a la base de datos SQLite (se crea si no existe)
    conexion = sqlite3.connect('database_proyecto.db')
    cursor = conexion.cursor()
    
    # Crear tabla de historial
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Historial (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Cédula INTEGER NOT NULL,
        Tipo_Operacion TEXT NOT NULL,
        Monto NUMERIC NOT NULL,
        Fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (Cédula) REFERENCES Usuarios(Cédula)
    )
    ''')
    
    # Crear la tabla de Usuarios
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Cédula INTEGER UNIQUE NOT NULL,
        Nombre TEXT NOT NULL,
        Apellido TEXT NOT NULL,
        Sexo TEXT NOT NULL,
        Edad NUMERIC NOT NULL,
        Correo TEXT NOT NULL,
        Contraseña TEXT NOT NULL,
        FotoPerfil BLOB
    )
    ''')
    
    # Crear la tabla de Cuenta
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Cuenta (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Cédula INTEGER NOT NULL,
        Tipo_Cuenta TEXT NOT NULL,
        Número_Cuenta NUMERIC UNIQUE NOT NULL,
        Saldo NUMERIC NOT NULL,
        FOREIGN KEY (Cédula) REFERENCES Usuarios(Cédula)
    )
    ''')
    
    # Confirmar los cambios y cerrar la conexión
    conexion.commit()
    conexion.close()

# Llamar a la función para crear la base de datos y las tablas
crear_base_datos()


"---------------------------------------- INICIO-- -----------------------------------------------------------------------"

# Clase Inicio, ventana principal del sistema
class Inicio:
    # Configura la ventana principal
    def __init__(self, ventana_principal):
        self.ventana_principal = ventana_principal
        self.ventana_principal.title("INICIO BANCARIO")
        self.ventana_principal.geometry("800x620")
        
        # Canvas para la imagen de fondo
        self.canvas1 = tk.Canvas(self.ventana_principal, width=400, height=500)
        self.canvas1.pack(fill="both", expand=True)

        # Cargar la imagen de fondo
        self.img_fondo = ImageTk.PhotoImage(Image.open(ruta_fondo_1).resize((800, 620)))
        
        # Coloca la imagen en el canvas
        self.canvas1.create_image(0, 0, anchor="nw", image=self.img_fondo)
        
        # Titulo
        titulo = tk.Label(self.canvas1, text="Bienvenido al Sistema Bancario", fg="white", font=("Comic Sans", 16, "bold"), bg="steel blue", pady=5)
        titulo.pack(pady=20)
        
        # Intruccion Cédula
        label_ced = tk.Label(self.canvas1, text="Cédula: ", fg="white", font=("Comic Sans", 16, "bold"), bg="steel blue", pady=5)
        label_ced.pack(pady=5)
        
        # Contenedor para el campo de cédula con el icono
        frame_dni = tk.Frame(self.canvas1, bg="steel blue", pady=5)
        frame_dni.pack()

        # Cargar el icono de cédula
        self.icono_dni = ImageTk.PhotoImage(Image.open(ruta_user).resize((30, 30)))

        # Mostrar la imagen del icono
        icono_label = tk.Label(frame_dni, image=self.icono_dni, fg="white", font=("Comic Sans", 16, "bold"), bg="steel blue", pady=5)
        icono_label.pack(side="left")

        # Caja para ingresar el número de cédula
        self.dni = tk.Entry(frame_dni, width=20, font=("Comic Sans", 14, "bold"))
        self.dni.pack(side="left", padx=5)
        
        # Contenedor para el campo de password con el icono
        label_password = tk.Label(self.canvas1, text="Contraseña: ", fg="white", font=("Comic Sans", 16, "bold"), bg="steel blue", pady=5)
        label_password.pack(pady=5)
        
        # Contenedor para el campo pass
        frame_pass= tk.Frame(self.canvas1, bg="steel blue", pady=5)
        frame_pass.pack()

        # Cargar el icono de pass
        self.icono_pass = ImageTk.PhotoImage(Image.open(ruta_pass).resize((30, 30)))

        # Crear un label para mostrar la imagen
        icono_label_pass = tk.Label(frame_pass, image=self.icono_pass, bg="steel blue", pady=5)
        icono_label_pass.pack(side="left")

        # Caja para ingresar pass
        self.passw = tk.Entry(frame_pass, width=20, font=("Comic Sans", 14, "bold"), show="*")
        self.passw.pack(side="left", padx=5)

        # Botón para verificar
        boton_verificar = tk.Button(self.canvas1, text="Iniciar Sesión", command=self.Verificar_usuario, height=2, width=15, bg="sea green", fg="white", font=("Comic Sans", 10, "bold"))
        boton_verificar.pack(pady=20)

        # Intruccion registro
        label_reg = tk.Label(self.canvas1, text="¿Es tu primera vez? ", fg="white", font=("Comic Sans", 12, "bold italic"), bg="blue2", pady=5)
        label_reg.pack(pady=5)
        
        # Botón para abrir el registro
        boton_registro = tk.Button(self.canvas1, text="Abri mi Cuenta", command=self.Abrir_registro, height=2, width=15, bg="SkyBlue3", fg="white", font=("Comic Sans", 10, "bold"))
        boton_registro.pack(padx=50, pady=20)

        # Botón para salir de la aplicación
        boton_salir = tk.Button(self.canvas1, text="Salir", command=self.ventana_principal.quit, height=2, width=10, bg="red", fg="white", font=("Comic Sans", 10, "bold"))
        boton_salir.pack(padx=50, pady=20)

    # Método para verificar si el usuario y la contraseña son correctos
    def Verificar_usuario(self):
        dni = self.dni.get()             # Obtener el número de cédula ingresado
        password = self.passw.get()      # Obtener la contraseña ingresada

        # Verificar si la cédula y la contraseña son correctos
        with sqlite3.connect(Registro.db_name) as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM Usuarios WHERE Cédula = ? AND Contraseña = ?", (dni, password))
            usuario = cursor.fetchone()

        if usuario:
             # Oculta la ventana principal y abre la ventana de cuenta
            self.ventana_principal.withdraw()  # Oculta la ventana principal
            application_cta = Mostrar_cta(self.ventana_principal, dni)  # Llama a la clase Registro, pasa la ventana principal
            self.dni.delete(0, tk.END)         # Limpia el campo
            self.passw.delete(0, tk.END)       # Limpia el campo
        else:
            messagebox.showerror("ERROR", "Cédula o contraseña incorrectos.")       # Muestra error si no encuentra el usuario
    
    # Método para abrir la ventana de registro
    def Abrir_registro(self):
        self.ventana_principal.withdraw()  # Oculta la ventana principal
        application_reg = Registro(self.ventana_principal)  # Llama a la clase Registro

"------------------------------------- CUENTA BANCARIA -------------------------------------------------------------------"

class Mostrar_cta:
    def __init__(self, ventana_principal, dni_usuario):
        self.dni_usuario = dni_usuario  # Se pasa el DNI del usuario para buscar los datos
        
        # Crear una nueva ventana para mostrar los datos
        self.ventana_mostrar_cuenta = tk.Toplevel(ventana_principal)
        self.ventana_mostrar_cuenta.title("Detalles de la Cuenta")
        self.ventana_mostrar_cuenta.geometry("800x630")
        
        # Obtener los datos del usuario y de la cuenta
        self.obtener_datos_usuario()

        # Crear un canvas para la interfaz
        self.canvas_cta = tk.Canvas(self.ventana_mostrar_cuenta, width=400, height=500)
        self.canvas_cta.pack(fill="both", expand=True)
        
        # Cargar la imagen de fondo
        self.img_fondo = ImageTk.PhotoImage(Image.open(ruta_fondo_2).resize((800, 630)))

        # Coloca la imagen en el canvas
        self.canvas_cta.create_image(0, 0, anchor="nw", image=self.img_fondo)
        
        # Mostrar datos
        self.mostrar_datos_usuario()

    # Consultar los datos del usuario y de la cuenta en la base de datos
    def obtener_datos_usuario(self):
        with sqlite3.connect('database_proyecto.db') as conexion:
            cursor = conexion.cursor()
            cursor.execute('''SELECT u.Nombre, u.Apellido, u.FotoPerfil, c.Número_Cuenta, c.Tipo_Cuenta, c.Saldo 
                              FROM Usuarios u
                              JOIN Cuenta c ON u.Cédula = c.Cédula
                              WHERE u.Cédula = ?''', (self.dni_usuario,))
            datos = cursor.fetchone()
        
        if datos:
            # Asignar los datos obtenidos
            self.nombre = datos[0]
            self.apellido = datos[1]
            self.foto_perfil = datos[2]
            self.numero_cuenta = datos[3]
            self.tipo_cuenta = datos[4]
            self.saldo = datos[5]
        else: 
            # Si no se encontraron datos para el usuario, mostrar error
            messagebox.showerror("Error", "No se encontraron datos para este usuario.")
            self.ventana_mostrar_cuenta.destroy()

    # Muestra los datos del usuario en la interfaz gráfica
    def mostrar_datos_usuario(self):
        # Crear un marco para la foto de perfil
        marco_foto = tk.LabelFrame(self.canvas_cta, font=("Comic Sans", 12, "bold"), pady=10, bd=0)
        marco_foto.pack(padx=20, pady=10)

        if self.foto_perfil:
            # Convertir la foto de perfil de binario a imagen
            foto_imagen = Image.open(io.BytesIO(self.foto_perfil))
            foto_imagen = foto_imagen.resize((100, 100))  # Redimensionamos para ajustarlo
            foto_render = ImageTk.PhotoImage(foto_imagen)

            # Mostrar la foto en la interfaz
            foto_label = tk.Label(marco_foto, image=foto_render)
            foto_label.image = foto_render  # Mantener una referencia de la imagen
            foto_label.pack()

        # Mostrar nombre y apellido
        label_nombre = tk.Label(self.canvas_cta, text=f"{self.nombre} {self.apellido}", font=("Comic Sans", 14, "bold"), fg="black")
        label_nombre.pack(pady=10)

        # Mostrar el tipo de cuenta
        label_tipo_cuenta = tk.Label(self.canvas_cta, text=f"Cuenta {self.tipo_cuenta}",font=("Comic Sans", 14, "bold"), fg="black")
        label_tipo_cuenta.pack(pady=10)
        
        # Mostrar el número de cuenta
        label_numero_cuenta = tk.Label(self.canvas_cta, text=f"Nro. {self.numero_cuenta}",font=("Comic Sans", 14, "bold"), fg="black")
        label_numero_cuenta.pack(pady=10)
        
        # Mostrar el saldo de la cuenta
        self.label_saldo = tk.Label(self.canvas_cta, text=f"$ {self.saldo:.2f}",font=("Comic Sans", 14, "bold"), fg="black")
        self.label_saldo.pack(pady=10)
        
        # Cargar las imágenes para los botones de operaciones
        self.img_dep = ImageTk.PhotoImage(Image.open(ruta_dep).resize((100, 100)))
        self.img_ret = ImageTk.PhotoImage(Image.open(ruta_ret).resize((100, 100)))
        self.img_transf = ImageTk.PhotoImage(Image.open(ruta_transf).resize((100, 100)))
        self.img_historial = ImageTk.PhotoImage(Image.open(ruta_historial).resize((100, 100)))

        # Frame para los botones
        frame_bot_operaciones = tk.Frame(self.canvas_cta)
        frame_bot_operaciones.pack(pady=20)
        
        # Botón de depósito
        self.boton_dep = tk.Button(frame_bot_operaciones, image=self.img_dep, command=self.abrir_ventana_deposito, bd=0, relief="flat")
        self.boton_dep.grid(row=0, column=0, padx=10, pady=5)
        tk.Label(frame_bot_operaciones, text="Depósito", font=("Arial", 12)).grid(row=1, column=0)

        # Botón de retiro
        self.boton_ret = tk.Button(frame_bot_operaciones, image=self.img_ret, command=self.abrir_ventana_retiro, bd=0, relief="flat")
        self.boton_ret.grid(row=0, column=1, padx=10, pady=5)
        tk.Label(frame_bot_operaciones, text="Retiro", font=("Arial", 12)).grid(row=1, column=1)

        # Botón de transferencia
        self.boton_transf = tk.Button(frame_bot_operaciones, image=self.img_transf, command=self.abrir_ventana_transferencia, bd=0, relief="flat")
        self.boton_transf.grid(row=0, column=2, padx=10, pady=5)
        tk.Label(frame_bot_operaciones, text="Transferencia", font=("Arial", 12)).grid(row=1, column=2)

        # Botón de historial
        self.boton_historial = tk.Button(frame_bot_operaciones, image=self.img_historial, command=self.mostrar_historial, bd=0, relief="flat")
        self.boton_historial.grid(row=0, column=3, padx=10, pady=5)
        tk.Label(frame_bot_operaciones, text="Historial", font=("Arial", 12)).grid(row=1, column=3)

        # Botón para cerrar la ventana
        boton_cerrar = tk.Button(self.canvas_cta, text="Cerrar Sesión", command=self.Atras, height=2, width=15, bg="red", fg="white", font=("Comic Sans", 10, "bold"))
        boton_cerrar.pack(pady=40)
      
    # Cierra la ventana de datos y vuelve a la ventana principal  
    def Atras(self):
        self.ventana_mostrar_cuenta.destroy()  # Cierra la ventana de registro
        self.ventana_mostrar_cuenta.master.deiconify()  # Muestra la ventana principal nuevamente

    "---------------------------------------- DEPOSITO -----------------------------------------------------------------------"
    
    # Crear una ventana para el depósito
    def abrir_ventana_deposito(self):
        self.ventana_deposito = tk.Toplevel(self.ventana_mostrar_cuenta)
        self.ventana_deposito.title("Depósito")
        self.ventana_deposito.geometry("300x250")
        
        # Label operación
        label_dep = tk.Label(self.ventana_deposito, text=f"Depósito", font=("Arial", 14, 'bold'))
        label_dep.pack(pady=20)
    
        # Instrucción
        label = tk.Label(self.ventana_deposito, text="Ingrese la cantidad a depositar:", font=("Arial", 14))
        label.pack(pady=10)
        
        # Entry para ingresar el monto
        self.entry_deposito = tk.Entry(self.ventana_deposito, font=("Arial", 12), bg='linen', width=10)
        self.entry_deposito.pack(pady=10)
        
        # Botón confirmar la operación
        boton_confirmar = tk.Button(self.ventana_deposito, text="Confirmar", command=self.depositar, relief='solid')
        boton_confirmar.pack(pady=30)
        
    # Realiza el depósito de la cantidad ingresada y actualiza el saldo
    def depositar(self):
        cantidad = self.entry_deposito.get()
        if cantidad:
            # Reemplazar la coma por punto
            cantidad = cantidad.replace(",", ".")
            try:
                cantidad = float(cantidad)
                if cantidad > 0:
                    self.saldo += cantidad
                    self.actualizar_saldo()       # Actualizar
                    self.actualizar_saldo_base_datos()
                    self.insertar_historial("Depósito", cantidad)  # Insertar en historial
                    self.ventana_dep_ex()
                    self.ventana_deposito.destroy()
                else:
                    self.ventana_dep_inc()    # Mostrar error
            except ValueError:
                self.ventana_dep_error()      # Mostrar error
    
    # Muestra una ventana de éxito
    def ventana_dep_ex(self):
        dep = tk.Toplevel()
        dep.title("Depósito exitoso")
        dep.geometry("250x320")

        # Imagen
        self.img_visto = ImageTk.PhotoImage(Image.open(ruta_correcto).resize((130, 130)))
        self.correcto = tk.Label(dep, image=self.img_visto)
        self.correcto.pack(pady=20)
        
        # Texto del mensaje
        mensaje = tk.Label(dep, text="¡Depósito exitoso!", font=("Arial", 16,'bold'))
        mensaje.pack(pady=20)

        # Botón para cerrar
        boton_cerrar = tk.Button(dep, text="Aceptar", command=dep.destroy, bg="azure", font=("Arial", 12, "bold"), relief='solid')
        boton_cerrar.pack(pady=10)
    
    # Muestra una ventana de error    
    def ventana_dep_inc(self):
        dep_inc = tk.Toplevel()
        dep_inc.title("Error")
        dep_inc.geometry("300x350")

        # Imagen
        self.img_dep_inc = ImageTk.PhotoImage(Image.open(ruta_incorrecto).resize((130, 130))) 
        self.correcto = tk.Label(dep_inc, image=self.img_dep_inc)
        self.correcto.pack(pady=25)
        
        # Texto del mensaje
        mensaje = tk.Label(dep_inc, text="¡Ups, algo salió mal!", font=("Arial", 16,'bold'))
        mensaje.pack(pady=5)
        
        error = tk.Label(dep_inc, text="La cantidad debe ser mayor que 0", font=("Arial", 14))
        error.pack(pady=20)

        # Botón para cerrar
        boton_cerrar = tk.Button(dep_inc, text="Aceptar", command=dep_inc.destroy, bg="azure", font=("Arial", 12, "bold"), relief='solid')
        boton_cerrar.pack(pady=10)
    
    # Muestra una ventana de error  
    def ventana_dep_error(self):
        dep_error = tk.Toplevel()
        dep_error.title("Error")
        dep_error.geometry("300x370")

        # Imagen
        self.img_dep_error = ImageTk.PhotoImage(Image.open(ruta_incorrecto).resize((130, 130)))
        self.correcto = tk.Label(dep_error, image=self.img_dep_error)
        self.correcto.pack(pady=25)
        
        # Texto del mensaje
        mensaje = tk.Label(dep_error, text="¡Ups, algo salió mal!", font=("Arial", 16,'bold'))
        mensaje.pack(pady=5)
        
        error = tk.Label(dep_error, text="Cantidad inválida.\nPor favor ingrese un número válido", font=("Arial", 14))
        error.pack(pady=20)

        # Botón para cerrar
        boton_cerrar = tk.Button(dep_error, text="Aceptar", command=dep_error.destroy, bg="azure", font=("Arial", 12, "bold"), relief='solid')
        boton_cerrar.pack(pady=10)

    "---------------------------------------- RETIRO -----------------------------------------------------------------------"
    # Crear una ventana para el retiro
    def abrir_ventana_retiro(self):
        self.ventana_retiro = tk.Toplevel(self.ventana_mostrar_cuenta)
        self.ventana_retiro.title("Retiro")
        self.ventana_retiro.geometry("300x250")
        
        # Label operación
        label_saldo = tk.Label(self.ventana_retiro, text="Retiro", font=("Arial", 14, 'bold'))
        label_saldo.pack(pady=20)
        
        # Instrucción
        label = tk.Label(self.ventana_retiro, text="Ingrese la cantidad a retirar:", font=("Arial", 14))
        label.pack(pady=10)
        
        # Entry para el monto
        self.entry_retiro = tk.Entry(self.ventana_retiro, font=("Arial", 12), bg='linen', width=10)
        self.entry_retiro.pack(pady=10)
        
        # Confirmar operación
        boton_confirmar = tk.Button(self.ventana_retiro, text="Confirmar", command=self.retirar, relief='solid')
        boton_confirmar.pack(pady=30)
    
    # Realiza el retiro de la cantidad ingresada y actualiza el saldo
    def retirar(self):
        cantidad = self.entry_retiro.get()
        if cantidad:
            # Reemplazar la coma por punto
            cantidad = cantidad.replace(",", ".")
            try:
                cantidad = float(cantidad)
                if cantidad > 0 and cantidad <= self.saldo:
                    self.saldo -= cantidad
                    self.actualizar_saldo()           # Actualizar saldo
                    self.actualizar_saldo_base_datos()
                    self.insertar_historial("Retiro", cantidad)  # Insertar en historial
                    self.ventana_ret_ex()
                    self.ventana_retiro.destroy()
                else:
                    self.ventana_ret_inc()     # Mostrar error
            except ValueError:
                self.ventana_ret_error()
     
    # Muestra una ventana de éxito           
    def ventana_ret_ex(self):
        ret = tk.Toplevel()
        ret.title("Depósito exitoso")
        ret.geometry("250x320")

        # Imagen
        self.img_visto_ret = ImageTk.PhotoImage(Image.open(ruta_correcto).resize((130, 130)))
        
        self.ret_correcto = tk.Label(ret, image=self.img_visto_ret)
        self.ret_correcto.pack(pady=20)
        
        # Texto del mensaje
        mensaje = tk.Label(ret, text="¡Retiro exitoso!", font=("Arial", 16,'bold'))
        mensaje.pack(pady=20)

        # Botón para cerrar
        boton_cerrar = tk.Button(ret, text="Aceptar", command=ret.destroy, bg="azure", font=("Arial", 12, "bold"), relief='solid')
        boton_cerrar.pack(pady=10)

    # Muestra una ventana de error
    def ventana_ret_inc(self):
        ret_inc = tk.Toplevel()
        ret_inc.title("Error")
        ret_inc.geometry("300x370")

        # Imagen
        self.img_ret_inc = ImageTk.PhotoImage(Image.open(ruta_incorrecto).resize((130, 130)))
        
        self.correcto = tk.Label(ret_inc, image=self.img_ret_inc)
        self.correcto.pack(pady=25)
        
        # Texto del mensaje
        mensaje = tk.Label(ret_inc, text="¡Ups, algo salió mal!", font=("Arial", 16,'bold'))
        mensaje.pack(pady=5)
        
        error = tk.Label(ret_inc, text="Fondos insuficientes o\ncantidad inválida", font=("Arial", 14))
        error.pack(pady=20)

        # Botón para cerrar
        boton_cerrar = tk.Button(ret_inc, text="Aceptar", command=ret_inc.destroy, bg="azure", font=("Arial", 12, "bold"), relief='solid')
        boton_cerrar.pack(pady=10)
    
    # Muestra una ventana de error
    def ventana_ret_error(self):
        ret_error = tk.Toplevel()
        ret_error.title("Error")
        ret_error.geometry("300x370")

        # Imagen
        self.img_ret_error = ImageTk.PhotoImage(Image.open(ruta_incorrecto).resize((130, 130)))
        
        self.correcto = tk.Label(ret_error, image=self.img_ret_error)
        self.correcto.pack(pady=25)
        
        # Texto del mensaje
        mensaje = tk.Label(ret_error, text="¡Ups, algo salió mal!", font=("Arial", 16,'bold'))
        mensaje.pack(pady=5)
        
        error = tk.Label(ret_error, text="Cantidad inválida.\nPor favor ingrese un número válido", font=("Arial", 14))
        error.pack(pady=20)

        # Botón para cerrar
        boton_cerrar = tk.Button(ret_error, text="Aceptar", command=ret_error.destroy, bg="azure", font=("Arial", 12, "bold"), relief='solid')
        boton_cerrar.pack(pady=10)

    "---------------------------------------- TRANFERENCIA -----------------------------------------------------------------------"
    
    # Crear una ventana emergente para la transferencia
    def abrir_ventana_transferencia(self):
        self.ventana_transferencia = tk.Toplevel(self.ventana_mostrar_cuenta)
        self.ventana_transferencia.title("Transferencia")
        self.ventana_transferencia.geometry("350x300")
        
        # Label operación
        label_saldo = tk.Label(self.ventana_transferencia, text="Transferencia", font=("Arial", 14, 'bold'))
        label_saldo.pack(pady=20)
        
        # Instrucción
        label_destino = tk.Label(self.ventana_transferencia, text="Ingrese el número de cuenta destino:", font=("Arial", 14))
        label_destino.pack(pady=10)
        
        # Entry número de cuenta
        self.entry_destino = tk.Entry(self.ventana_transferencia, font=("Arial", 12), bg='linen', width=22)
        self.entry_destino.pack(pady=10)
        
        # Botón "Validar cuenta"
        boton_validar = tk.Button(self.ventana_transferencia, text="Validar cuenta", font=("Arial", 12), command=self.validar_cuenta, relief='solid')
        boton_validar.pack(pady=20)
        
        # Etiqueta para mostrar datos
        self.label_usuario_destino = tk.Label(self.ventana_transferencia, text="", font=("Arial", 12))
        self.label_usuario_destino.pack(pady=10)
        
    # Valida las cuentas si existen o son iguales     
    def validar_cuenta(self):
        self.numero_cuenta_destino = self.entry_destino.get()

        if self.numero_cuenta_destino:
            # Verificar si la cuenta destino es la misma que la cuenta del usuario
            if str(self.numero_cuenta) == str(self.numero_cuenta_destino):
                self.label_usuario_destino.config(text="No puedes transferir a tu propia cuenta.")
                return
                
            # Si la cuenta no es la misma, verificar si existe en la base de datos
            with sqlite3.connect('database_proyecto.db') as conexion:
                cursor = conexion.cursor()
                cursor.execute('''SELECT u.Nombre, u.Apellido, c.Número_Cuenta
                                FROM Usuarios u
                                JOIN Cuenta c ON u.Cédula = c.Cédula
                                WHERE c.Número_Cuenta = ?''', (self.numero_cuenta_destino,))
                datos = cursor.fetchone()

            if datos:
                nombre, apellido, numero_cuenta = datos
                
                # Cerrar la ventana de validación
                self.ventana_transferencia.destroy()
                
                # Abrir la ventana de ingresar monto
                self.abrir_ventana_ingresar_monto(nombre, apellido, numero_cuenta)
            else:
                # Si no se encuentra la cuenta, mostrar error
                self.label_usuario_destino.config(text="Usuario no existe")
        else:
            self.label_usuario_destino.config(text="Por favor ingrese un número de cuenta")

    def abrir_ventana_ingresar_monto(self, nombre_destino, apellido_destino, numero_cuenta_destino):
        # Crear una nueva ventana para ingresar el monto
        self.ventana_ingresar_monto = tk.Toplevel(self.ventana_mostrar_cuenta)
        self.ventana_ingresar_monto.title("Transferir")
        self.ventana_ingresar_monto.geometry("350x300")

        # Mostrar información de la cuenta destino
        label_info_destino = tk.Label(self.ventana_ingresar_monto, text=f"{nombre_destino} {apellido_destino}\n\nNro. {numero_cuenta_destino}", font=("Arial", 14, 'bold'))
        label_info_destino.pack(pady=20)
        
        # Intrucciones
        label_cantidad = tk.Label(self.ventana_ingresar_monto, text="Ingrese la cantidad a transferir:", font=("Arial", 14))
        label_cantidad.pack(pady=10)
        
        # Entry para el monto
        self.entry_transferencia = tk.Entry(self.ventana_ingresar_monto, font=("Arial", 12), bg='linen', width=11)
        self.entry_transferencia.pack(pady=10)
        
        # Confirmar operación
        boton_confirmar = tk.Button(self.ventana_ingresar_monto, text="Confirmar", font=("Arial", 12), command=lambda: self.transferir(numero_cuenta_destino), relief='solid')
        boton_confirmar.pack(pady=20)
        
        
    # Método ejecutar operación
    def transferir(self, numero_cuenta_destino):
        self.cantidad = self.entry_transferencia.get()  # Obtener la cantidad a transferir

        if self.cantidad:
            # Reemplazar la coma por punto en la cantidad
            self.cantidad = self.cantidad.replace(",", ".")
            
            try:
                self.cantidad = float(self.cantidad)  # Convertir a float la cantidad

                # Verificar que la cantidad sea válida y que no exceda el saldo
                if self.cantidad > 0 and self.cantidad <= self.saldo:
                    # Verificar si la cuenta destino existe
                    with sqlite3.connect('database_proyecto.db') as conexion:
                        cursor = conexion.cursor()
                        cursor.execute('''SELECT c.Número_Cuenta, c.Saldo
                                        FROM Cuenta c
                                        WHERE c.Número_Cuenta = ?''', (self.numero_cuenta_destino,))
                        cuenta_destino = cursor.fetchone()
                    
                    if cuenta_destino:
                        saldo_destino = cuenta_destino[1]  # Obtener saldo de la cuenta destino
                        
                        # Actualizar saldos
                        nuevo_saldo_origen = self.saldo - self.cantidad
                        nuevo_saldo_destino = saldo_destino + self.cantidad
                        
                        # Realizar las actualizaciones de los saldos en la base de datos
                        cursor.execute('''UPDATE Cuenta SET Saldo = ? WHERE Número_Cuenta = ?''', (nuevo_saldo_origen, self.numero_cuenta))
                        cursor.execute('''UPDATE Cuenta SET Saldo = ? WHERE Número_Cuenta = ?''', (nuevo_saldo_destino, self.numero_cuenta_destino))
                        conexion.commit()

                        # Actualizar el saldo de la cuenta origen en la interfaz
                        self.saldo = nuevo_saldo_origen
                        self.actualizar_saldo()

                        # Registrar en el historial
                        self.insertar_historial("Transferencia", self.cantidad)

                        # Mostrar mensaje de éxito
                        self.ventana_trans_ex()
                        self.ventana_ingresar_monto.destroy()  # Cerrar la ventana de ingreso de monto
                else:
                    # Si la cantidad es inválida o si el saldo es insuficiente
                    self.ventana_trans_inc()
            except ValueError:
                # Si no se puede convertir la cantidad a float
                self.ventana_trans_error()
                
    # Muestra una ventana de éxito         
    def ventana_trans_ex(self):
        trans = tk.Toplevel()
        trans.title("Depósito exitoso")
        trans.geometry("270x415")

        # Imagen
        self.img_visto_trans = ImageTk.PhotoImage(Image.open(ruta_correcto).resize((130, 130)))
        
        self.trans_correcto = tk.Label(trans, image=self.img_visto_trans)
        self.trans_correcto.pack(pady=20)
        
        # Texto del mensaje
        mensaje = tk.Label(trans, text="¡Transferencia exitosa!", font=("Arial", 16,'bold'))
        mensaje.pack(pady=20)
        
        # Mostrar datos transferencia
        comprobante = tk.Label(trans, text=f"Monto:             $ {self.cantidad}\n\nNro. Cuenta:     {self.numero_cuenta_destino}", font=("Arial", 14, 'bold'))
        comprobante.pack(pady=20)

        # Botón para cerrar
        boton_cerrar = tk.Button(trans, text="Aceptar", command=trans.destroy, bg="azure", font=("Arial", 12, "bold"), relief='solid')
        boton_cerrar.pack(pady=10)

    # Mostrar error
    def ventana_trans_inc(self):
        trans_inc = tk.Toplevel()
        trans_inc.title("Error")
        trans_inc.geometry("300x370")

        # Imagen
        self.img_trans_inc = ImageTk.PhotoImage(Image.open(ruta_incorrecto).resize((130, 130)))
        
        self.correcto = tk.Label(trans_inc, image=self.img_trans_inc)
        self.correcto.pack(pady=25)
        
        # Texto del mensaje
        mensaje = tk.Label(trans_inc, text="¡Ups, algo salió mal!", font=("Arial", 16,'bold'))
        mensaje.pack(pady=5)
        
        error = tk.Label(trans_inc, text="Fondos insuficientes o\ncantidad inválida", font=("Arial", 14))
        error.pack(pady=20)

        # Botón para cerrar
        boton_cerrar = tk.Button(trans_inc, text="Aceptar", command=trans_inc.destroy, bg="azure", font=("Arial", 12, "bold"), relief='solid')
        boton_cerrar.pack(pady=10)
    
    # Mostrar error
    def ventana_trans_error(self):
        trans_error = tk.Toplevel()
        trans_error.title("Error")
        trans_error.geometry("300x370")

        # Imagen
        self.img_ret_error = ImageTk.PhotoImage(Image.open(ruta_incorrecto).resize((130, 130)))
        
        self.correcto = tk.Label(trans_error, image=self.img_ret_error)
        self.correcto.pack(pady=25)
        
        # Texto del mensaje
        mensaje = tk.Label(trans_error, text="¡Ups, algo salió mal!", font=("Arial", 16,'bold'))
        mensaje.pack(pady=5)
        
        error = tk.Label(trans_error, text="Cantidad inválida.\nPor favor ingrese un número válido", font=("Arial", 14))
        error.pack(pady=20)

        # Botón para cerrar
        boton_cerrar = tk.Button(trans_error, text="Aceptar", command=trans_error.destroy, bg="azure", font=("Arial", 12, "bold"), relief='solid')
        boton_cerrar.pack(pady=10)

    
    "---------------------------------------- ACTUALIZAR SALDO -----------------------------------------------------------------------"
    
    def actualizar_saldo(self): # Actualizar el saldo en la interfaz
        self.label_saldo.config(text=f"$ {self.saldo:.2f}")

    def actualizar_saldo_base_datos(self):  # Actualizar el saldo en la base de datos
        with sqlite3.connect('database_proyecto.db') as conexion:
            cursor = conexion.cursor()
            cursor.execute('''UPDATE Cuenta SET Saldo = ? WHERE Número_Cuenta = ?''', (self.saldo, self.numero_cuenta))
            conexion.commit()
    
    "---------------------------------------- HISTORIAL -----------------------------------------------------------------------"

    # Método insertar en el historial
    def insertar_historial(self, tipo_operacion, monto):
        # Obtener la fecha y hora actual
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Insertar el historial de la operación en la base de datos
        with sqlite3.connect('database_proyecto.db') as conexion:
            cursor = conexion.cursor()
            cursor.execute('''INSERT INTO Historial (Cédula, Tipo_Operacion, Monto, Fecha)
                              VALUES (?, ?, ?, ?)''', 
                           (self.dni_usuario, tipo_operacion, monto, fecha_actual))
            conexion.commit()

    # Crear ventana para mostrar historial
    def mostrar_historial(self):
        ventana_historial = tk.Toplevel(self.ventana_mostrar_cuenta)
        ventana_historial.title("Historial de Transacciones")

        # Crear un Canvas para la ventana de historial
        canvas_historial = tk.Canvas(ventana_historial)
        canvas_historial.pack(fill="both", expand=True)

        # Crear un Treeview para mostrar el historial
        tree = ttk.Treeview(canvas_historial, columns=("Tipo Operación", "Monto", "Fecha"), show="headings")
        
        # Configurar las columnas
        tree.heading("Tipo Operación", text="Tipo Operación")
        tree.heading("Monto", text="Monto")
        tree.heading("Fecha", text="Fecha")

        tree.column("Tipo Operación", width=150, anchor="center")
        tree.column("Monto", width=100, anchor="center")
        tree.column("Fecha", width=150, anchor="center")

        tree.pack(padx=10, pady=10, fill="both", expand=True)

        # Obtener historial de la base de datos
        with sqlite3.connect('database_proyecto.db') as conexion:
            cursor = conexion.cursor()
            cursor.execute('''SELECT Tipo_Operacion, Monto, Fecha FROM Historial WHERE Cédula = ? ORDER BY Fecha DESC''', (self.dni_usuario,))
            historial = cursor.fetchall()

        # Insertar los registros en el Treeview
        for tipo_operacion, monto, fecha in historial:
            # Convertir la fecha al formato deseado (dd/mm/yyyy HH:MM)
            fecha_formateada = datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y %H:%M")

            # Insertar los datos en el Treeview
            tree.insert("", "end", values=(tipo_operacion, f"{monto:.2f}", fecha_formateada))

        # Botón errar ventana
        boton_cerrar_historial = tk.Button(ventana_historial, text="Cerrar", command=ventana_historial.destroy)
        boton_cerrar_historial.pack(pady=10)

"---------------------------------------- REGISTRO -----------------------------------------------------------------------"

class Registro:
    db_name='database_proyecto.db'
    
    def __init__(self, ventana_principal):
        # Ventana secundaria para el registro
        self.regis = tk.Toplevel(ventana_principal) 
        self.regis.title("REGISTRO BANCARIO")
        self.regis.geometry("800x620")
    
        self.imagen_binaria = None   # Variable para guardar la imagen como binario
        
        # Título
        titulo= tk.Label(self.regis, text="REGISTRO DE USUARIO",fg="black",font=("Comic Sans", 13,"bold"),pady=5)
        titulo.grid(row=0, column=0, columnspan=2, padx=10, pady=5)

        # Marco principal
        marcop = tk.LabelFrame(self.regis,font=("Comic Sans", 10,"bold"))
        marcop.config(bd=0,pady=5)
        marcop.grid(row=2, column=0, padx=10, pady=10, sticky="n")
        
        # Carga la imagen para el registro de usuario
        self.imagen_registro = ImageTk.PhotoImage(Image.open(ruta_datos).resize((70, 50)))
        
        label_imagen= tk.Label(marcop, image= self.imagen_registro)
        label_imagen.grid(row=1, column=0, pady=5)
        
        marco = tk.LabelFrame(marcop, text="Datos personales",font=("Comic Sans", 10,"bold"))
        marco.config(bd=2,pady=5)
        marco.grid(row=2, column=0, padx=10, pady=10, sticky="n")

        # Marco para datos personales
        label_dni=tk.Label(marco,text="DNI: ",font=("Comic Sans", 10,"bold")).grid(row=0,column=0,sticky='s',padx=5,pady=8)
        self.dni=tk.Entry(marco,width=25)
        self.dni.focus()
        self.dni.grid(row=0, column=1, padx=5, pady=8)
        
        # Formulario de registro de datos personales
        label_nombres=tk.Label(marco,text="Nombre: ",font=("Comic Sans", 10,"bold")).grid(row=1,column=0,sticky='s',padx=10,pady=8)
        self.nombres=tk.Entry(marco,width=25)
        self.nombres.grid(row=1, column=1, padx=10, pady=8)

        label_apellidos=tk.Label(marco,text="Apellidos: ",font=("Comic Sans", 10,"bold")).grid(row=2,column=0,sticky='s',padx=10,pady=8)
        self.apellidos=tk.Entry(marco,width=25)
        self.apellidos.grid(row=2, column=1, padx=10, pady=8)

        label_sexo=tk.Label(marco,text="Sexo: ",font=("Comic Sans", 10,"bold")).grid(row=3,column=0,sticky='s',padx=10,pady=8)
        self.combo_sexo=ttk.Combobox(marco,values=["Masculino", "Femenino"], width=22,state="readonly")
        self.combo_sexo.current(0)
        self.combo_sexo.grid(row=3,column=1,padx=10,pady=8)

        label_edad=tk.Label(marco,text="Edad: ",font=("Comic Sans", 10,"bold")).grid(row=4,column=0,sticky='s',padx=10,pady=8)
        self.edad=tk.Entry(marco,width=25)
        self.edad.grid(row=4, column=1, padx=10, pady=8)

        label_correo=tk.Label(marco,text="Correo electronico: ",font=("Comic Sans", 10,"bold")).grid(row=5,column=0,sticky='s',padx=10,pady=8)
        self.correo=tk.Entry(marco,width=25)
        self.correo.grid(row=5, column=1, padx=10, pady=8)

        label_password=tk.Label(marco,text="Contraseña: ",font=("Comic Sans", 10,"bold")).grid(row=6,column=0,sticky='s',padx=10,pady=8)
        self.password=tk.Entry(marco,width=25,show="*")
        self.password.grid(row=6, column=1, padx=10, pady=8)

        label_password=tk.Label(marco,text="Repetir contraseña: ",font=("Comic Sans", 10,"bold")).grid(row=7,column=0,sticky='s',padx=10,pady=8)
        self.repetir_password=tk.Entry(marco,width=25,show="*")
        self.repetir_password.grid(row=7, column=1, padx=10, pady=8)
        
        # Marco para datos bancarios
        marco_principal_cta = tk.LabelFrame(self.regis,font=("Comic Sans", 10,"bold"),pady=10)
        marco_principal_cta.config(bd=0,pady=5)
        marco_principal_cta.grid(row=2, column=1, padx=10, pady=10, sticky="n")
        
        marco_foto = tk.LabelFrame(marco_principal_cta, text="Foto de Perfil",font=("Comic Sans", 10,"bold"), labelanchor="n", pady=10)
        marco_foto.config(bd=2,pady=5)
        marco_foto.grid(row=1, column=1, padx=10, pady=10, sticky="n")
        
        self.imagen_cuenta = ImageTk.PhotoImage(Image.open(ruta_cuenta).resize((60, 50)))
        
        label_imagen= tk.Label(marco_principal_cta, image= self.imagen_cuenta)
        label_imagen.grid(row=2, column=1, pady=5)
        
        marco_pregunta = tk.LabelFrame(marco_principal_cta, text="Datos Bancarios",font=("Comic Sans", 10,"bold"),pady=10)
        marco_pregunta.config(bd=2,pady=5)
        marco_pregunta.grid(row=3, column=1, padx=10, pady=10, sticky="n")
        
        # Marco para cargar la foto
        marco_foto = tk.LabelFrame(marco_principal_cta, text="Foto de Perfil", font=("Comic Sans", 10, "bold"), labelanchor="n", pady=10)
        marco_foto.config(bd=2)
        marco_foto.grid(row=1, column=1, padx=10, pady=10, sticky="n")
        
        # Botón para cargar la foto de perfil
        self.boton_imagen = tk.Button(marco_foto, text="Cargar Foto", font=("Comic Sans", 12, "bold"), command=self.Cargar_foto)
        self.boton_imagen.config(bd=0, padx=50, pady=60)
        self.boton_imagen.grid(row=1, column=1, padx=10, pady=10, sticky="n")
        
        # Variable para guardar la ruta de la imagen
        self.ruta_foto = None
        
        # Campos para tipo de cuenta y monto inicial
        label_tip_cta=tk.Label(marco_pregunta,text="Tipo de cuenta: ",font=("Comic Sans", 10,"bold")).grid(row=0,column=0,sticky='s',padx=10,pady=8)
        self.tip_cta=ttk.Combobox(marco_pregunta,values=["Ahorros","Corriente"], width=30,state="readonly")
        self.tip_cta.current(0)
        self.tip_cta.grid(row=0,column=1,padx=10,pady=8)
        
        label_monto_inicial=tk.Label(marco_pregunta,text="Monto inicial $: ",font=("Comic Sans", 10,"bold")).grid(row=1,column=0,sticky='s',padx=10,pady=8)
        self.monto_inicial=tk.Entry(marco_pregunta, width=33)
        self.monto_inicial.grid(row=1, column=1, padx=10, pady=8)          
        

        # Frame botones
        frame_botones=tk.Frame(self.regis)
        frame_botones.grid(row=3, column=0, columnspan=2, pady=10)

        # Botones
        boton_registrar=tk.Button(frame_botones,text="REGISTRAR",command=self.Registrar_usuario ,height=2,width=10,bg="green",fg="white",font=("Comic Sans", 10,"bold")).grid(row=0, column=1, padx=10, pady=15)
        boton_limpiar=tk.Button(frame_botones,text="LIMPIAR",command=self.Limpiar_formulario ,height=2,width=10,bg="gray",fg="white",font=("Comic Sans", 10,"bold")).grid(row=0, column=2, padx=10, pady=15)
        boton_cancelar=tk.Button(frame_botones,text="ATRAS",command=self.Atras, height=2,width=10,bg="red",fg="white",font=("Comic Sans", 10,"bold")).grid(row=0, column=3, padx=10, pady=15)

    # Cierra la ventana de registro y vuelve a la ventana principal
    def Atras(self):
        self.regis.destroy()  # Cierra la ventana de registro
        self.regis.master.deiconify()  # Muestra la ventana principal nuevamente
        
    # Método para cargar una foto de perfil
    def Cargar_foto(self):
        # Abrir un cuadro de diálogo para seleccionar un archivo de imagen
        archivo = filedialog.askopenfilename(
            title="Seleccionar Foto de Perfil",
            filetypes=(("Archivos de imagen", "*.jpg;*.jpeg;*.png"), ("Todos los archivos", "*.*"))
        )
        if archivo:
            self.ruta_foto = archivo
            # Mostrar una vista previa de la foto seleccionada
            imagen_cargada = Image.open(self.ruta_foto)
            imagen_cargada = imagen_cargada.resize((140, 140))  # Redimensionar para que quepa en el marco
            render = ImageTk.PhotoImage(imagen_cargada)

            # Actualizar el botón con la nueva imagen
            self.boton_imagen.config(image=render, text="")
            self.boton_imagen.image = render  # Guardar la referencia para evitar que se pierda
            
            # Convertir la imagen a binario
            with io.BytesIO() as byte_io:
                imagen_cargada.save(byte_io, format="PNG")  # Guardar como PNG o el formato que prefieras
                self.imagen_binaria = byte_io.getvalue()  # Obtener el valor binario de la imagen
        else:
            # Si no se selecciona una imagen, asignar None (NULL en la base de datos)
            self.imagen_binaria = None    
            
    def Ejecutar_consulta_user(self, consulta_user, parameters_user=()):
        with sqlite3.connect(self.db_name) as conexion:
            cursor=conexion.cursor()
            result=cursor.execute(consulta_user,parameters_user)
            conexion.commit()
        return result
    
    #Método consultar cuenta
    def Ejecutar_consulta_cta(self, consulta_cta, parameters_cta=()):
        with sqlite3.connect(self.db_name) as conexion:
            cursor1=conexion.cursor()
            result=cursor1.execute(consulta_cta,parameters_cta)
            conexion.commit()
        return result 
    
    #Método limpiar formulario
    def Limpiar_formulario(self):
        self.dni.delete(0, tk.END)
        self.nombres.delete(0, tk.END)
        self.apellidos.delete(0, tk.END)
        self.combo_sexo.delete(0, tk.END)
        self.edad.delete(0, tk.END)
        self.correo.delete(0, tk.END)
        self.password.delete(0, tk.END)
        self.repetir_password.delete(0, tk.END)
        self.tip_cta.delete(0, tk.END)
        self.monto_inicial.delete(0, tk.END) 
    
    # Métodos para validar formulario
    def Validar_formulario_completo(self):
        if len(self.dni.get()) !=0 and len(self.nombres.get()) !=0 and len(self.apellidos.get()) !=0 and len(self.combo_sexo.get()) !=0 and len(self.edad.get()) !=0 and len(self.password.get()) !=0 and len(self.repetir_password.get()) !=0 and len(self.correo.get()) !=0 :
                    # Verifica que la edad sea un número
            if not self.edad.get().isdigit():
                messagebox.showerror("ERROR EN REGISTRO", "La edad debe ser un número.")
                return False
        
                 # Verifica que el DNI sea un número
            if not self.dni.get().isdigit():
                messagebox.showerror("ERROR EN REGISTRO", "El DNI debe ser un número.")
                return False
            
                # Verifica que el monto inicial sea un número válido
            monto = self.monto_inicial.get()
            try:
                # Convierte el monto a flotante, reemplazando la coma por punto si es necesario
                monto_float = float(monto.replace(',', '.'))
            except ValueError:
                messagebox.showerror("ERROR EN REGISTRO", "El monto inicial no es un número válido.")
                return False
            
            return True
        else:
             messagebox.showerror("ERROR EN REGISTRO", "Complete todos los campos del formulario")
    
    # Método para validar contraseña
    def Validar_contraseña(self):
        if(str(self.password.get()) == str(self.repetir_password.get())):
            return True
        else:
            messagebox.showerror("ERROR EN REGISTRO", "Contraseñas no coinciden")
 
    # Método buscar dni
    def Buscar_dni(self, dni):
        with sqlite3.connect(self.db_name) as conexion:
            cursor=conexion.cursor()
            sql="SELECT * FROM Usuarios WHERE Cédula = ?"
            sql="SELECT * FROM Cuenta WHERE Cédula = ?"
            cursor.execute(sql, (dni,))
            dnix= cursor.fetchall() # obtener respuesta como lista
            cursor.close()
            return dnix
    
    # Método para validar dni
    def Validar_dni(self):
        dni= self.dni.get()
        dato = self.Buscar_dni(dni)
        if (dato == []):
            return True
        else:
            messagebox.showerror("ERROR EN REGISTRO", "DNI registrado anteriormente")

    # Método generar un número de cuenta
    def Generar_numero_cuenta(self, dni):
        # Utilizar el DNI del usuario y un número aleatorio para generar un número de cuenta único
        # Aquí se está concatenando el DNI con un número aleatorio de 4 dígitos
        return str(dni) + str(random.randint(1000, 9999))
    
    # Método insetar los datos en la data base
    def Registrar_usuario(self):
        if self.Validar_formulario_completo() and self.Validar_contraseña() and self.Validar_dni():
            numero_cuenta = self.Generar_numero_cuenta(self.dni.get())
            consulta_user='INSERT INTO Usuarios VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?)'
            parameters_user = (self.dni.get(),self.nombres.get(),self.apellidos.get(),self.combo_sexo.get(),self.edad.get(),self.correo.get(),self.password.get(), self.imagen_binaria)
            self.Ejecutar_consulta_user(consulta_user, parameters_user)
            consulta_cta='INSERT INTO Cuenta VALUES(NULL, ?, ?, ?, ?)'
            parameters_cta = (self.dni.get(),self.tip_cta.get(),numero_cuenta,self.monto_inicial.get())
            self.Ejecutar_consulta_cta(consulta_cta, parameters_cta) 
            messagebox.showinfo("REGISTRO EXITOSO", f'Bienvenido {self.nombres.get()} {self.apellidos.get()}')
            self.Limpiar_formulario()
  
            
if __name__ == '__main__':
    ventana = tk.Tk()                    # Crea una instancia de la ventana principal 
    application = Inicio(ventana)        # Crea una instancia de la clase 'Inicio'
    ventana.mainloop()                   # Inicia el bucle principal del programa