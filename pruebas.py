import tkinter as tk
from tkcalendar import Calendar
from datetime import datetime

# Función para resaltar la fecha seleccionada
def marcar_fecha():
    # Obtener la fecha seleccionada en formato de texto
    fecha_seleccionada = cal.get_date()
    
    # Convertir la fecha seleccionada a tipo datetime.date
    fecha = datetime.strptime(fecha_seleccionada, "%m/%d/%y").date()
    
    # Marcar la fecha seleccionada con color rojo
    cal.calevent_create(fecha, "Fecha destacada", 'highlight')
    
    # Configurar el color de fondo para las fechas destacadas
    cal.tag_config('highlight', background='red')

# Crear la ventana principal
root = tk.Tk()
root.title("Calendario con Fecha Seleccionada")

# Crear un calendario
cal = Calendar(root, selectmode='day', year=2025, month=2, day=21)
cal.pack(pady=20)

# Botón para marcar la fecha seleccionada
btn_marcar = tk.Button(root, text="Marcar Fecha Seleccionada", command=marcar_fecha)
btn_marcar.pack(pady=10)

# Ejecutar la aplicación
root.mainloop()
