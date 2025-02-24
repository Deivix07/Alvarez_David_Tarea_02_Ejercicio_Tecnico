import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from database import obtener_conexion
from datetime import datetime
from funciones import mostrar_login_admin
from tkcalendar import DateEntry

def obtener_pacientes():
    conn = obtener_conexion()
    c = conn.cursor()
    c.execute("SELECT id, Nombre FROM usuarios WHERE Tipo = 'Paciente'")
    pacientes = [f"{row[1]}" for row in c.fetchall()]
    conn.close()
    return pacientes

def obtener_especialidades():
    conn = obtener_conexion()
    c = conn.cursor()
    c.execute("SELECT DISTINCT Especialidad FROM medicos")
    especialidades = [row[0] for row in c.fetchall()]
    conn.close()
    return especialidades

def obtener_medicos(especialidad):
    conn = obtener_conexion()
    c = conn.cursor()
    c.execute("SELECT Nombre FROM medicos WHERE Especialidad = ?", (especialidad,))
    medicos = [row[0] for row in c.fetchall()]
    conn.close()
    return medicos

def obtener_horas_disponibles(fecha, medico_id):
    """Devuelve una lista de horas disponibles para una fecha y médico específicos."""
    todas_las_horas = ["08:00", "09:00", "10:00", "11:00", "14:00", "15:00", "16:00"]

    conn = obtener_conexion()
    c = conn.cursor()
    c.execute("SELECT hora FROM citas WHERE fecha = ? AND medico_id = ?", (fecha, medico_id))
    horas_ocupadas = [row[0] for row in c.fetchall()]
    conn.close()

    return [hora for hora in todas_las_horas if hora not in horas_ocupadas]

def agendar_cita(usuario_id):
    """Ventana para agendar una cita."""
    agendar_window = tk.Toplevel()
    agendar_window.title("Agendar Cita")
    agendar_window.geometry("300x450")  # Ajuste de tamaño para incluir más campos

    # Combo de especialidad
    tk.Label(agendar_window, text="Especialidad").pack()
    especialidad_var = tk.StringVar()
    especialidad_menu = ttk.Combobox(agendar_window, textvariable=especialidad_var, values=obtener_especialidades())
    especialidad_menu.pack()

    # Combo de médico
    tk.Label(agendar_window, text="Médico").pack()
    medico_var = tk.StringVar()
    medico_menu = ttk.Combobox(agendar_window, textvariable=medico_var)
    medico_menu.pack()

    def actualizar_medicos(event):
        medicos = obtener_medicos(especialidad_var.get())
        medico_menu["values"] = medicos
        if medicos:
            medico_var.set(medicos[0])

    especialidad_menu.bind("<<ComboboxSelected>>", actualizar_medicos)

    # Combo de paciente
    tk.Label(agendar_window, text="Paciente").pack()
    paciente_var = tk.StringVar()
    paciente_menu = ttk.Combobox(agendar_window, textvariable=paciente_var, values=obtener_pacientes())
    paciente_menu.pack()

    # Calendario de fecha
    tk.Label(agendar_window, text="Fecha").pack()
    cal = Calendar(agendar_window, date_pattern="yyyy-mm-dd", locale="es_ES")
    cal.pack()

    # Combo de hora
    tk.Label(agendar_window, text="Hora").pack()
    hora_var = tk.StringVar()
    hora_menu = ttk.Combobox(agendar_window, textvariable=hora_var)
    hora_menu.pack()

    def actualizar_horas(event):
        fecha = cal.get_date()
        medico_nombre = medico_var.get()

        if not medico_nombre:
            return

        conn = obtener_conexion()
        c = conn.cursor()
        c.execute("SELECT id FROM medicos WHERE Nombre = ?", (medico_nombre,))
        medico_id = c.fetchone()[0]
        conn.close()

        horas_disponibles = obtener_horas_disponibles(fecha, medico_id)
        hora_menu["values"] = horas_disponibles
        if horas_disponibles:
            hora_var.set(horas_disponibles[0])
        else:
            hora_var.set("No disponible")

    cal.bind("<<CalendarSelected>>", actualizar_horas)

    def confirmar_agendar():
        fecha = cal.get_date()
        hora = hora_var.get()
        medico_nombre = medico_var.get()
        paciente_nombre = paciente_var.get()

        if hora == "No disponible":
            messagebox.showerror("Error", "No hay horas disponibles para este día.")
            return

        # Obtener el ID del paciente seleccionado
        paciente_id = paciente_nombre.split(" (ID: ")[1].strip(")")

        conn = obtener_conexion()
        c = conn.cursor()
        c.execute("SELECT id FROM medicos WHERE Nombre = ?", (medico_nombre,))
        medico_id = c.fetchone()[0]

        c.execute("INSERT INTO citas (usuario_id, medico_id, fecha, hora, estado) VALUES (?, ?, ?, ?, 'Pendiente')",
                  (paciente_id, medico_id, fecha, hora))  # Usar paciente_id en lugar de usuario_id
        conn.commit()
        conn.close()

        messagebox.showinfo("Cita Agendada", "Cita agendada con éxito.")
        agendar_window.destroy()
        
    tk.Button(agendar_window, text="Agendar Cita", command=confirmar_agendar, height=2, width=13, bg="green", fg="white", font=("Comic Sans", 10, "bold")).pack(pady=10)


def ver_citas(usuario_id):
    """Ventana para ver y cancelar citas (para administrador)."""
    citas_window = tk.Toplevel()
    citas_window.title("Ver Citas")
    citas_window.geometry("800x640")

    frame_paciente = tk.Frame(citas_window)
    frame_paciente.pack(pady=5)

    paciente_var = tk.StringVar()
    paciente_combo = ttk.Combobox(frame_paciente, textvariable=paciente_var, state="readonly")
    paciente_combo.pack(side=tk.LEFT, padx=5)

    def filtrar_por_paciente():
        mostrar_citas(None, paciente_var.get(), None)

    btn_paciente = tk.Button(frame_paciente, text="Filtrar por Paciente", command=filtrar_por_paciente, height=1, width=20, bg="blue", fg="white", font=("Comic Sans", 8, "bold"))
    btn_paciente.pack(side=tk.LEFT)

    frame_medico = tk.Frame(citas_window)
    frame_medico.pack(pady=5)

    medico_var = tk.StringVar()
    medico_combo = ttk.Combobox(frame_medico, textvariable=medico_var, state="readonly")
    medico_combo.pack(side=tk.LEFT, padx=5)

    def filtrar_por_medico():
        mostrar_citas(None, None, medico_var.get())

    btn_medico = tk.Button(frame_medico, text="Filtrar por Médico", command=filtrar_por_medico, height=1, width=20, bg="blue", fg="white", font=("Comic Sans", 8, "bold"))
    btn_medico.pack(side=tk.LEFT)

    tk.Label(citas_window, text="Filtrar por Fecha").pack(pady=5)
    # Calendario
    cal = Calendar(citas_window, date_pattern="yyyy-mm-dd", selectmode="day", locale="es_ES")
    cal.pack(pady=5)

    # Crear el Treeview (lista de citas)
    tk.Label(citas_window, text="Citas Agendadas").pack(pady=5)
    tree = ttk.Treeview(citas_window, columns=("Especialidad", "Médico", "Fecha", "Hora", "Estado"), show="headings")
    tree.heading("Especialidad", text="Especialidad")
    tree.heading("Médico", text="Médico")
    tree.heading("Fecha", text="Fecha")
    tree.heading("Hora", text="Hora")
    tree.heading("Estado", text="Estado")

    # Ajustar el ancho de las columnas
    tree.column("Especialidad", width=150)
    tree.column("Médico", width=150)
    tree.column("Fecha", width=100)
    tree.column("Hora", width=100)
    tree.column("Estado", width=100)

    # Ajustar la altura del Treeview
    tree.config(height=10)
    tree.pack(pady=5)

    # Función para cargar los filtros de paciente y médico
    def cargar_filtros():
        conn = obtener_conexion()
        c = conn.cursor()

        # Obtener lista de pacientes
        c.execute("SELECT id, Nombre FROM usuarios WHERE Tipo = 'Paciente'")
        pacientes = c.fetchall()
        paciente_combo['values'] = [f"{p[1]}" for p in pacientes]
        if pacientes:
            paciente_combo.set(paciente_combo['values'][0])
            
        

        # Obtener lista de médicos
        c.execute("SELECT id, Nombre FROM medicos")
        medicos = c.fetchall()
        medico_combo['values'] = [m[1] for m in medicos]
        if medicos:
            medico_combo.set(medico_combo['values'][0])

        conn.close()

    # Función para cargar las citas con los filtros aplicados
    def mostrar_citas(fecha=None, paciente=None, medico=None):
        # Limpiar el Treeview antes de agregar las nuevas citas
        for row in tree.get_children():
            tree.delete(row)

        # Conectar a la base de datos
        conn = obtener_conexion()
        c = conn.cursor()

        # Construir la consulta SQL con filtros
        query = """SELECT citas.id, medicos.Especialidad, medicos.Nombre, citas.fecha, citas.hora, citas.estado
                   FROM citas
                   JOIN medicos ON citas.medico_id = medicos.id
                   JOIN usuarios ON citas.usuario_id = usuarios.id
                   WHERE 1=1"""

        params = []

        if fecha:
            query += " AND citas.fecha = ?"
            params.append(fecha)
        if paciente:
            paciente_id = paciente.split(" (ID: ")[-1][:-1]  # Obtener el ID del paciente
            query += " AND usuarios.id = ?"
            params.append(paciente_id)
        if medico:
            query += " AND medicos.Nombre LIKE ?"
            params.append(f"%{medico}%")

        c.execute(query, tuple(params))
        citas = c.fetchall()
        conn.close()

        # Crear un diccionario para almacenar las fechas y sus estados
        fechas_marcar = {}

        if not citas:
            tree.insert("", "end", values=("No hay citas programadas", "", "", "", ""))
        else:
            for cita in citas:
                tree.insert("", "end", values=(cita[1], cita[2], cita[3], cita[4], cita[5]))

                # Marcar el evento en el calendario
                estado = cita[5]
                color = "red" if estado == "Cancelada" else "blue"

                # Usamos las fechas para agregar los eventos en el calendario
                fecha_obj = datetime.strptime(cita[3], "%Y-%m-%d").date()
                cal.calevent_create(fecha_obj, f"{cita[2]} - {cita[4]} ({estado})", tags=estado)
                cal.tag_config(estado, background=color)

                # Guardamos la fecha para marcarla después
                fechas_marcar[fecha_obj] = estado

        # Al abrir la ventana, marcamos las fechas con colores
        for fecha, estado in fechas_marcar.items():
            color = "red" if estado == "Cancelada" else "blue"
            cal.tag_config(estado, background=color)

    # Función para manejar la selección de fecha en el calendario
    def seleccionar_fecha(event):
        fecha_seleccionada = cal.get_date()
        mostrar_citas(fecha_seleccionada, None, None)

    # Enlazar la selección de fecha con la función
    cal.bind("<<CalendarSelected>>", seleccionar_fecha)

    # Llamar a la función para cargar los filtros al iniciar
    cargar_filtros()

    # Llamar a la función para mostrar las citas cuando se carga la ventana
    mostrar_citas(None, None, None)

    # Función para editar una cita (cambiar fecha y hora)
    def editar_cita():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Selecciona una cita para editar.")
            return

        cita = tree.item(selected_item)["values"]
        cita_id = cita[0]

        # Crear ventana para editar la cita
        editar_window = tk.Toplevel()
        editar_window.title("Editar Cita")
        editar_window.geometry("300x250")

        # Ingresar nueva fecha con DateEntry
        tk.Label(editar_window, text="Nueva Fecha (yyyy-mm-dd)").pack(pady=5)

        # Usamos DateEntry en lugar de Entry
        nueva_fecha_entry = DateEntry(editar_window, date_pattern='y-mm-dd')  # O puedes cambiar el formato si lo prefieres
        nueva_fecha_entry.pack(pady=5)
        
        tk.Label(editar_window, text="Nueva Hora").pack(pady=5)
        nueva_hora_var = tk.StringVar()
        nueva_hora_combobox = ttk.Combobox(editar_window, textvariable=nueva_hora_var, values=["08:00", "09:00", "10:00", "11:00", "14:00", "15:00", "16:00"])
        nueva_hora_combobox.pack(pady=5)

        def confirmar_editar():
            nueva_fecha = nueva_fecha_entry.get()
            nueva_hora = nueva_hora_var.get()

            if not nueva_fecha or not nueva_hora:
                messagebox.showerror("Error", "Por favor, ingrese ambos campos (Fecha y Hora).")
                return

            # Actualizar la cita en la base de datos
            conn = obtener_conexion()
            c = conn.cursor()
            c.execute("UPDATE citas SET fecha = ?, hora = ? WHERE id = ?", (nueva_fecha, nueva_hora, cita_id))
            conn.commit()
            conn.close()

            messagebox.showinfo("Cita Editada", "La cita ha sido editada con éxito.")
            editar_window.destroy()
            mostrar_citas(None, None, None)

        # Botón para confirmar edición
        tk.Button(editar_window, text="Editar Cita", command=confirmar_editar, height=2, width=13, bg="green", fg="white", font=("Comic Sans", 10, "bold")).pack(pady=10)
    
    def cancelar_cita():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Selecciona una cita para cancelar.")
            return

        cita = tree.item(selected_item)["values"]
        cita_id = cita[0]

        # Confirmar cancelación
        respuesta = messagebox.askyesno("Cancelar Cita", "¿Estás seguro de que deseas cancelar esta cita? Esta acción no se puede deshacer.")
        if respuesta:
            try:
                conn = obtener_conexion()
                c = conn.cursor()

                # Verificar si la conexión es exitosa
                if conn is None:
                    messagebox.showerror("Error", "No se pudo establecer conexión con la base de datos.")
                    return

                # Ejecutar la consulta SQL para eliminar la cita
                c.execute("DELETE FROM citas WHERE id = ?", (cita_id,))
                conn.commit()  # Asegurarse de guardar los cambios
                conn.close()

                # Eliminar la cita de la interfaz
                tree.delete(selected_item)

                messagebox.showinfo("Cita Cancelada", "La cita ha sido eliminada con éxito.")

                # Actualizar la lista de citas en la UI
                mostrar_citas(None, None, None)
            except Exception as e:
                messagebox.showerror("Error", f"Ha ocurrido un error al cancelar la cita: {e}")


    # Crear un Frame para contener los botones
    botones_frame = tk.Frame(citas_window)
    botones_frame.pack(pady=10)

    # Botón para cancelar una cita
    tk.Button(botones_frame, text="Cancelar Cita", command=cancelar_cita, height=2, width=20, bg="red", fg="white", font=("Comic Sans", 10, "bold")).pack(side=tk.LEFT, padx=10)

    # Botón para editar una cita
    tk.Button(botones_frame, text="Editar Cita", command=editar_cita, height=2, width=20, bg="dark orange", fg="white", font=("Comic Sans", 10, "bold")).pack(side=tk.LEFT, padx=10)

# Ejemplo de llamada
# ver_citas(usuario_id=1)

    
def obtener_nombre_usuario(usuario_id):
    """Obtiene el nombre y apellido del usuario desde la base de datos con su ID."""
    conn = obtener_conexion()
    c = conn.cursor()
    c.execute("SELECT nombre, apellido FROM usuarios WHERE id = ?", (usuario_id,))
    usuario = c.fetchone()
    conn.close()
    
    if usuario:  # Verificar que se haya encontrado el usuario
        nombre_usuario, apellido_usuario = usuario
        return nombre_usuario, apellido_usuario
    else:
        return None, None  # Retorna None si no se encuentra el usuario


def open_admin_dashboard(usuario_id):
    patient_window = tk.Tk()
    patient_window.title("Panel del Paciente")
    patient_window.geometry("300x360")
    
    # Obtener el nombre y apellido del usuario
    nombre_usuario, apellido_usuario = obtener_nombre_usuario(usuario_id)
    
    # Verificar si el nombre y apellido fueron encontrados
    if nombre_usuario and apellido_usuario:
        # Mostrar nombre y apellido del usuario en el panel del paciente
        tk.Label(patient_window, text=f"Bienvenido, {nombre_usuario} {apellido_usuario}", font=("Comic Sans", 16, "bold"), pady=5).pack(pady=10)
    else:
        tk.Label(patient_window, text="Usuario no encontrado").pack()
        
    tk.Button(patient_window, text="Agendar Cita", command=lambda: agendar_cita(usuario_id), height=3, width=20, bg="dark orange", fg="white", font=("Comic Sans", 12, "bold")).pack(pady=10)
    
    tk.Button(patient_window, text="Ver Mis Citas", command=lambda: ver_citas(usuario_id), height=3, width=20, bg="dark orange", fg="white", font=("Comic Sans", 12, "bold")).pack(pady=10)
    # Función para cerrar sesión y regresar al login
    def cerrar_sesion():
        patient_window.destroy()  # Cierra el panel del paciente
        mostrar_login_admin()  # Abre el login nuevamente
    
    # Botón de cerrar sesión
    tk.Button(patient_window, text="Cerrar Sesión", command=cerrar_sesion, height=3, width=20, bg="red", fg="white", font=("Comic Sans", 12, "bold")).pack(pady=10)
    
    patient_window.mainloop()