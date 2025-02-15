# models.py
class Usuario:
    def __init__(self, id, nombre, tipo):
        self.id = id
        self.nombre = nombre
        self.tipo = tipo  # "Paciente" o "Administrador"

class Medico:
    def __init__(self, id, nombre, especialidad):
        self.id = id
        self.nombre = nombre
        self.especialidad = especialidad

class Cita:
    def __init__(self, id, usuario_id, medico_id, fecha, hora, estado="Programada"):
        self.id = id
        self.usuario_id = usuario_id
        self.medico_id = medico_id
        self.fecha = fecha
        self.hora = hora
        self.estado = estado

    def cancelar(self):
        self.estado = "Cancelada"

    def reprogramar(self, nueva_fecha, nueva_hora):
        self.fecha = nueva_fecha
        self.hora = nueva_hora