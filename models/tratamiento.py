from database.consultorio import Consultorio

db = Consultorio()

class Tratamiento:
    def __init__(self, nombre, precio, id=None):
        self.id = id
        self.nombre = nombre
        self.precio = precio

    def insertar(self) -> bool:
        """Registra un nuevo tipo de tratamiento."""
        try:
            sql = "INSERT INTO tratamientos (nombre, precio) VALUES (?, ?)"
            db.ejecutarConsulta(sql, (self.nombre, self.precio))
            return True
        except Exception:
            return False

    def actualizar(self) -> bool:
        """Modifica el nombre o precio de un tratamiento existente."""
        try:
            sql = "UPDATE tratamientos SET nombre=?, precio=? WHERE id=?"
            db.ejecutarConsulta(sql, (self.nombre, self.precio, self.id))
            return True
        except Exception:
            return False

    def eliminar(self) -> bool:
        """Elimina el tratamiento según su ID."""
        try:
            sql = "DELETE FROM tratamientos WHERE id=?"
            db.ejecutarConsulta(sql, (self.id,))
            return True
        except Exception:
            return False

    @staticmethod
    def obtenerTodos() -> list:
        """Retorna una lista de objetos Tratamiento con todos los registros de la tabla."""
        sql = "SELECT id, nombre, precio FROM tratamientos"
        resultados = db.ejecutarConsulta(sql)
        lista_tratamientos = []
        if resultados:
            for fila in resultados:
                lista_tratamientos.append(Tratamiento(id=fila[0], nombre=fila[1], precio=fila[2]))
        return lista_tratamientos