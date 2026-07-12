from database.consultorio import Consultorio
from datetime import datetime

db = Consultorio()

class Turno:
    def __init__(self, fecha, hora, paciente_id, tratamiento_id, id=None):
        self.id = id
        self.fecha = fecha
        self.hora = hora
        self.paciente_id = paciente_id
        self.tratamiento_id = tratamiento_id

    def agendar(self) -> bool:
        """Registra un nuevo turno asociado a un paciente y tratamiento, con validaciones."""
        try:
            # Validar formato de fecha y hora
            try:
                fecha_dt = datetime.strptime(self.fecha, "%Y-%m-%d")
                hora_dt = datetime.strptime(self.hora, "%H:%M")
            except ValueError:
                raise ValueError("Formato de fecha u hora inválido. Use YYYY-MM-DD y HH:MM.")

            # Validar que la fecha no sea pasada
            hoy = datetime.now()
            if fecha_dt.date() < hoy.date():
                raise ValueError("No se pueden agendar turnos en fechas pasadas.")

            # --- CORRECCIÓN ACÁ ---
            # Validar superposición de turnos (misma fecha y hora)
            sql_check = "SELECT id FROM turnos WHERE fecha=? AND hora=?"
            resultado_check = db.ejecutarConsulta(sql_check, (self.fecha, self.hora))
            
            # Si la lista tiene elementos, significa que el turno ya está ocupado
            if resultado_check:  
                raise ValueError("Ya existe un turno en esa fecha y hora.")

            # Insertar turno si pasa las validaciones
            sql = "INSERT INTO turnos (fecha, hora, paciente_id, tratamiento_id) VALUES (?, ?, ?, ?)"
            db.ejecutarConsulta(sql, (self.fecha, self.hora, self.paciente_id, self.tratamiento_id))
            return True
        except Exception as e:
            print(f"Error al agendar turno: {e}")
            return False

    def cancelar(self) -> bool:
        """Elimina un turno programado."""
        try:
            if self.id is None:
                raise ValueError("Debe indicar el ID del turno para cancelarlo.")
            sql = "DELETE FROM turnos WHERE id=?"
            db.ejecutarConsulta(sql, (self.id,))
            return True
        except Exception as e:
            print(f"Error al cancelar turno: {e}")
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