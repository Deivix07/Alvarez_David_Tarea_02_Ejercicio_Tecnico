# gestor_citas.py
from database import obtener_conexion

class GestorCitas:
    def __init__(self):
        self.conn = obtener_conexion()

    def agendar_cita(self, usuario_id, medico_id, fecha, hora):
        if not self._horario_disponible(medico_id, fecha, hora):
            return False

        c = self.conn.cursor()
        c.execute("INSERT INTO citas (usuario_id, medico_id, fecha, hora, estado) VALUES (?, ?, ?, ?, ?)",
                  (usuario_id, medico_id, fecha, hora, "Programada"))
        self.conn.commit()
        return True

    def cancelar_cita(self, cita_id):
        c = self.conn.cursor()
        c.execute("UPDATE citas SET estado = ? WHERE id = ?", ("Cancelada", cita_id))
        self.conn.commit()
        return c.rowcount > 0

    def obtener_citas_por_usuario(self, usuario_id):
        c = self.conn.cursor()
        c.execute("SELECT * FROM citas WHERE usuario_id = ?", (usuario_id,))
        return c.fetchall()

    def _horario_disponible(self, medico_id, fecha, hora):
        c = self.conn.cursor()
        c.execute("SELECT * FROM citas WHERE medico_id = ? AND fecha = ? AND hora = ?",
                  (medico_id, fecha, hora))
        return c.fetchone() is None