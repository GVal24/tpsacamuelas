from database.consultorio import Consultorio

# Instancia de la db local
db = Consultorio()

class Paciente:
    def __init__(self, dni, nombre, apellido, telefono, id=None):
        self.id = id
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono

    def guardar(self) -> bool:
        """Inserta la ficha del paciente en la base de datos."""
        try:
            sql = "INSERT INTO pacientes (dni, nombre, apellido, telefono) VALUES (?, ?, ?, ?)"
            db.ejecutarConsulta(sql, (self.dni, self.nombre, self.apellido, self.telefono))
            return True
        except Exception:
            return False

    def modificar(self) -> bool:
        """Actualiza los datos del paciente usando el ID como identificador."""
        try:
            sql = "UPDATE pacientes SET dni=?, nombre=?, apellido=?, telefono=? WHERE id=?"
            db.ejecutarConsulta(sql, (self.dni, self.nombre, self.apellido, self.telefono, self.id))
            return True
        except Exception as e:
            print("Error al modificar paciente:", e)
            return False

    def eliminar(self) -> bool:
        """Elimina al paciente del sistema."""
        try:
            sql = "DELETE FROM pacientes WHERE dni=?"
            db.ejecutarConsulta(sql, (self.dni,))
            return True
        except Exception:
            return False

    @staticmethod
    def buscarPorDni(dni):
        """Busca un paciente por su DNI y retorna una instancia de la clase Paciente o None."""
        sql = "SELECT id, dni, nombre, apellido, telefono FROM pacientes WHERE dni=?"
        resultado = db.ejecutarConsulta(sql, (dni,))
        
        if resultado:
            fila = resultado[0] 
            return Paciente(id=fila[0], dni=fila[1], nombre=fila[2], apellido=fila[3], telefono=fila[4])
        return None
    
    @staticmethod
    def obtenerTodos() -> list:
        """Retorna una lista de tuplas con todos los pacientes."""
        sql = "SELECT id, dni, nombre, apellido, telefono FROM pacientes ORDER BY apellido ASC"
        resultados = db.ejecutarConsulta(sql)
        return resultados
