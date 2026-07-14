from database.consultorio import Consultorio
from datetime import datetime

db = Consultorio()

class Turno:
    def __init__(self, fecha, hora, paciente_id, tratamiento_id, id=None):
        self.id = int(id) if id is not None else None
        self.fecha = fecha
        self.hora = hora
        self.paciente_id = paciente_id
        self.tratamiento_id = tratamiento_id

    def _validar_fecha_hora(self, permitir_id=None):
        """Valida formato, fecha futura y superposición de turnos."""
        try:
            # Normalizar fecha: siempre YYYY-MM-DD
            fecha_dt = datetime.strptime(str(self.fecha).strip(), "%Y-%m-%d")
            self.fecha = fecha_dt.strftime("%Y-%m-%d")

            # Normalizar hora: siempre HH:MM
            hora_dt = datetime.strptime(str(self.hora).strip(), "%H:%M")
            self.hora = hora_dt.strftime("%H:%M")
        except ValueError:
            raise ValueError("Formato de fecha u hora inválido. Use YYYY-MM-DD y HH:MM.")

        hoy = datetime.now()
        if fecha_dt.date() < hoy.date():
            raise ValueError("No se pueden agendar turnos en fechas pasadas.")

        sql_check = "SELECT id FROM turnos WHERE fecha=? AND hora=?"
        params = (self.fecha, self.hora)
        resultado_check = db.ejecutarConsulta(sql_check, params)

        if resultado_check:
            ids_encontrados = [fila[0] for fila in resultado_check]
            if permitir_id is not None:
                otros = [i for i in ids_encontrados if i != permitir_id]
                if otros:
                    raise ValueError("Ya existe un turno en esa fecha y hora.")
            else:
                raise ValueError("Ya existe un turno en esa fecha y hora.")

    def agendar(self) -> bool:
        """Registra un nuevo turno asociado a un paciente y tratamiento."""
        try:
            self._validar_fecha_hora()
            sql = "INSERT INTO turnos (fecha, hora, paciente_id, tratamiento_id) VALUES (?, ?, ?, ?)"
            db.ejecutarConsulta(sql, (self.fecha, self.hora, self.paciente_id, self.tratamiento_id))
            return True
        except Exception as e:
            print(f"Error al agendar turno: {e}")
            return False

    def actualizar(self) -> bool:
        """Modifica un turno existente."""
        try:
            if self.id is None:
                raise ValueError("Debe indicar el ID del turno para modificarlo.")
            self._validar_fecha_hora(permitir_id=self.id)
            sql = "UPDATE turnos SET fecha=?, hora=?, paciente_id=?, tratamiento_id=? WHERE id=?"
            db.ejecutarConsulta(sql, (self.fecha, self.hora, self.paciente_id, self.tratamiento_id, self.id))
            return True
        except Exception as e:
            print(f"Error al actualizar turno: {e}")
            return False

    def cancelar(self) -> bool:
        """Elimina un turno programado y limpia huérfanos."""
        try:
            if self.id is None:
                raise ValueError("Debe indicar el ID del turno para cancelarlo.")

            # 1. Borra el turno actual por ID
            sql = "DELETE FROM turnos WHERE id=?"
            db.ejecutarConsulta(sql, (self.id,))

            # 2. Limpieza extra: elimina turnos huérfanos en la misma fecha
            sql_check = """
                SELECT t.id
                FROM turnos t
                LEFT JOIN pacientes p ON t.paciente_id = p.id
                LEFT JOIN tratamientos tr ON t.tratamiento_id = tr.id
                WHERE t.fecha=? AND (p.id IS NULL OR tr.id IS NULL)
            """
            huerfanos = db.ejecutarConsulta(sql_check, (self.fecha,))
            for fila in huerfanos:
                db.ejecutarConsulta("DELETE FROM turnos WHERE id=?", (fila[0],))

            return True
        except Exception as e:
            print(f"Error al cancelar turno: {e}")
            return False


    @staticmethod
    def obtenerAgendaDiaria(fecha) -> list:
        """Trae los turnos de una fecha específica con DNI incluido."""
        sql = """
            SELECT t.id, t.fecha, t.hora, p.dni, p.nombre || ' ' || p.apellido, tr.nombre
            FROM turnos t
            INNER JOIN pacientes p ON t.paciente_id = p.id
            INNER JOIN tratamientos tr ON t.tratamiento_id = tr.id
            WHERE t.fecha = ?
            ORDER BY t.hora ASC
        """
        return db.ejecutarConsulta(sql, (fecha,))
