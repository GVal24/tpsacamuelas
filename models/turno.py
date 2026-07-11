from database.consultorio import Consultorio

db = Consultorio()

class Turno:
    def __init__(self, fecha, hora, paciente_id, tratamiento_id, id=None):
        self.id = id
        self.fecha = fecha
        self.hora = hora
        self.paciente_id = paciente_id
        self.tratamiento_id = tratamiento_id

    def agendar(self) -> bool:
        """Registra un nuevo turno asociado a un paciente y tratamiento."""
        try:
            sql = "INSERT INTO turnos (fecha, hora, paciente_id, tratamiento_id) VALUES (?, ?, ?, ?)"
            db.ejecutarConsulta(sql, (self.fecha, self.hora, self.paciente_id, self.tratamiento_id))
            return True
        except Exception:
            return False

    def cancelar(self) -> bool:
        """Elimina un turno programado."""
        try:
            sql = "DELETE FROM turnos WHERE id=?"
            db.ejecutarConsulta(sql, (self.id,))
            return True
        except Exception:
            return False

    @staticmethod
    def obtenerAgendaDiaria(fecha) -> list:
        """Trae los turnos de una fecha específica uniendo información de pacientes y tratamientos."""
        sql = """
            SELECT t.id, t.fecha, t.hora, p.nombre || ' ' || p.apellido, tr.nombre
            FROM turnos t
            INNER JOIN pacientes p ON t.paciente_id = p.id
            INNER JOIN tratamientos tr ON t.tratamiento_id = tr.id
            WHERE t.fecha = ?
            ORDER BY t.hora ASC
        """
        return db.ejecutarConsulta(sql, (fecha,))