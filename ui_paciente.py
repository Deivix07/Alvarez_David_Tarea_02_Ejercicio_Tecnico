from tkinter import Tk, Label, Button, OptionMenu, StringVar, Toplevel, Listbox, Entry
from tkinter import messagebox
from database import obtener_conexion
from funciones import mostrar_login_paciente

def obtener_medicos():
    conn = obtener_conexion()
    c = conn.cursor()
    c.execute("SELECT * FROM medicos")
    medicos = c.fetchall()
    conn.close()
    return medicos

def agendar_cita(usuario_id):
    # Ventana para agendar la cita
    agendar_window = Toplevel()
    agendar_window.title("Agendar Cita")

    # Lista de médicos
    medicos = obtener_medicos()
    medico_var = StringVar(agendar_window)
    medico_var.set(medicos[0][1])  # Inicializa con el primer médico

    Label(agendar_window, text="Seleccione un médico").pack()
    medico_menu = OptionMenu(agendar_window, medico_var, *[medico[1] for medico in medicos])
    medico_menu.pack()

    # Fecha y hora (esto puede mejorarse con un widget de calendario o validación)
    Label(agendar_window, text="Fecha (YYYY-MM-DD)").pack()
    fecha_entry = Entry(agendar_window)
    fecha_entry.pack()

    Label(agendar_window, text="Hora (HH:MM)").pack()
    hora_entry = Entry(agendar_window)
    hora_entry.pack()

    def confirmar_agendar():
        medico_seleccionado = medico_var.get()
        fecha = fecha_entry.get()
        hora = hora_entry.get()

        # Obtener el id del médico seleccionado
        conn = obtener_conexion()
        c = conn.cursor()
        c.execute("SELECT id FROM medicos WHERE Nombre = ?", (medico_seleccionado,))
        medico_id = c.fetchone()[0]

        # Insertar la cita en la base de datos
        c.execute("INSERT INTO citas (usuario_id, medico_id, fecha, hora, estado) VALUES (?, ?, ?, ?, ?)", 
                  (usuario_id, medico_id, fecha, hora, "Pendiente"))
        conn.commit()
        conn.close()

        # Mostrar mensaje de éxito
        messagebox.showinfo("Cita Agendada", "Cita agendada con éxito.")
        agendar_window.destroy()

    Button(agendar_window, text="Confirmar", command=confirmar_agendar).pack()

def ver_citas(usuario_id):
    # Ventana para ver las citas
    citas_window = Toplevel()
    citas_window.title("Mis Citas")

    conn = obtener_conexion()
    c = conn.cursor()
    c.execute("SELECT citas.id, medicos.Nombre, citas.fecha, citas.hora, citas.estado "
              "FROM citas JOIN medicos ON citas.medico_id = medicos.id "
              "WHERE citas.usuario_id = ?", (usuario_id,))
    citas = c.fetchall()
    conn.close()

    # Lista de citas
    listbox = Listbox(citas_window, height=5, width=50, selectmode="single")
    listbox.pack()

    if citas:
        for cita in citas:
            cita_info = f"{cita[1]} - {cita[2]} {cita[3]} - {cita[4]}"
            listbox.insert("end", cita_info)

        def cancelar_cita():
            # Cancelar la cita seleccionada
            selected_cita_index = listbox.curselection()
            if selected_cita_index:
                selected_cita = listbox.get(selected_cita_index)
                cita_id = selected_cita.split(' ')[0]
                conn = obtener_conexion()
                c = conn.cursor()
                c.execute("UPDATE citas SET estado = 'Cancelada' WHERE id = ?", (cita_id,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Cita Cancelada", "La cita ha sido cancelada.")
                citas_window.destroy()
            else:
                messagebox.showwarning("Seleccionar Cita", "Por favor, selecciona una cita para cancelar.")
    else:
        Label(citas_window, text="No tienes citas programadas.").pack()

def open_patient_dashboard(usuario_id):
    patient_window = Tk()
    patient_window.title("Panel del Paciente")

    # Bienvenida
    Label(patient_window, text="Bienvenido al Panel del Paciente").pack()

    # Botones para agendar y ver citas
    Button(patient_window, text="Agendar Cita", command=lambda: agendar_cita(usuario_id)).pack()
    Button(patient_window, text="Ver Mis Citas", command=lambda: ver_citas(usuario_id)).pack()

    # Función para cerrar sesión y regresar al login
    def cerrar_sesion():
        patient_window.destroy()  # Cierra el panel del paciente
        mostrar_login_paciente()  # Abre el login nuevamente
    
    # Botón de cerrar sesión
    Button(patient_window, text="Cerrar Sesión", command=cerrar_sesion).pack()

    patient_window.mainloop()