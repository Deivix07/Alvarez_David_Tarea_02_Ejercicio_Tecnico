import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from database import obtener_conexion
from datetime import datetime
from funciones import mostrar_login_paciente

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
    agendar_window.geometry("300x400")

    tk.Label(agendar_window, text="Especialidad").pack()
    especialidad_var = tk.StringVar()
    especialidad_menu = ttk.Combobox(agendar_window, textvariable=especialidad_var, values=obtener_especialidades())
    especialidad_menu.pack()

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

    tk.Label(agendar_window, text="Fecha").pack()
    cal = Calendar(agendar_window, date_pattern="yyyy-mm-dd", locale="es_ES")
    cal.pack()

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

        if hora == "No disponible":
            messagebox.showerror("Error", "No hay horas disponibles para este día.")
            return

        conn = obtener_conexion()
        c = conn.cursor()
        c.execute("SELECT id FROM medicos WHERE Nombre = ?", (medico_nombre,))
        medico_id = c.fetchone()[0]

        c.execute("INSERT INTO citas (usuario_id, medico_id, fecha, hora, estado) VALUES (?, ?, ?, ?, 'Pendiente')",
                  (usuario_id, medico_id, fecha, hora))
        conn.commit()
        conn.close()

        messagebox.showinfo("Cita Agendada", "Cita agendada con éxito.")
        agendar_window.destroy()
        
    tk.Button(agendar_window, text="Agendar Cita", command=confirmar_agendar, height=2, width=13, bg="green", fg="white", font=("Comic Sans", 10, "bold")).pack(pady=10)

def ver_citas(usuario_id):
    """Ventana para ver y cancelar citas."""
    citas_window = tk.Toplevel()
    citas_window.title("Mis Citas")
    citas_window.geometry("650x550")

    # Crear el calendario estático
    cal = Calendar(citas_window, date_pattern="yyyy-mm-dd", selectmode="day", locale="es_ES")
    cal.pack()

    # Crear la lista de citas
    tk.Label(citas_window, text="Mis Citas Agendadas").pack()

    # Crear el Treeview (lista)
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
    tree.config(height=10)  # Número de filas visibles

    tree.pack()

    # Función para cargar las citas y marcar las fechas en el calendario
    def mostrar_citas():
        # Limpiar el Treeview antes de agregar las nuevas citas
        for row in tree.get_children():
            tree.delete(row)

        # Consultar todas las citas para este usuario
        conn = obtener_conexion()
        c = conn.cursor()
        c.execute("""SELECT citas.id, medicos.Especialidad, medicos.Nombre, citas.fecha, citas.hora, citas.estado
                     FROM citas JOIN medicos ON citas.medico_id = medicos.id
                     WHERE citas.usuario_id = ?""", (usuario_id,))
        citas = c.fetchall()
        conn.close()

        # Crear un diccionario para almacenar las fechas y sus estados
        fechas_marcar = {}

        if not citas:
            tree.insert("", "end", values=("No hay citas programadas", "", "", "", ""))
        else:
            # Rellenar la lista con las citas
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

    # Llamar a la función para mostrar las citas cuando se carga la ventana
    mostrar_citas()

    # Función para cancelar una cita
    def cancelar_cita():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Selecciona una cita para cancelar.")
            return

        cita = tree.item(selected_item)["values"]
        fecha = cita[2]
        estado = cita[4]

        if estado == "Cancelada":
            messagebox.showinfo("Información", "La cita ya está cancelada.")
            return

        conn = obtener_conexion()
        c = conn.cursor()
        c.execute("UPDATE citas SET estado = 'Cancelada' WHERE usuario_id = ? AND fecha = ? AND hora = ?",
                  (usuario_id, fecha, cita[3]))
        conn.commit()

        # Liberar la hora cancelada
        c.execute("DELETE FROM citas WHERE usuario_id = ? AND fecha = ? AND hora = ?",
                  (usuario_id, fecha, cita[3]))
        conn.commit()

        conn.close()

        # Actualizar la vista
        tree.item(selected_item, values=(cita[0], cita[1], cita[2], cita[3], "Cancelada"))
        cal.tag_config("Cancelada", background="red")

        messagebox.showinfo("Cita Cancelada", "La cita ha sido cancelada.")
        citas_window.destroy()
        ver_citas(usuario_id)

    # Botón para cancelar cita
    tk.Button(citas_window, text="Cancelar Cita", command=cancelar_cita, height=2, width=13, bg="maroon", fg="white", font=("Comic Sans", 10, "bold")).pack(pady=5)

    # Botón para cerrar la ventana
    tk.Button(citas_window, text="Cerrar", command=citas_window.destroy, height=2, width=13, bg="red", fg="white", font=("Comic Sans", 10, "bold")).pack(pady=5)

    citas_window.mainloop()

    
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


def open_patient_dashboard(usuario_id):
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
        mostrar_login_paciente()  # Abre el login nuevamente
    
    # Botón de cerrar sesión
    tk.Button(patient_window, text="Cerrar Sesión", command=cerrar_sesion, height=3, width=20, bg="red", fg="white", font=("Comic Sans", 12, "bold")).pack(pady=10)
    
    patient_window.mainloop()