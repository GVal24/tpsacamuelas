import sqlite3

class Consultorio:
    def __init__(self, db_name="consultorio.db"):
        self.db_name = db_name
        self.crearTablas()

    def connect(self):
        """Establece y retorna la conexión con la base de SQLite."""
        return sqlite3.connect(self.db_name)

    def crearTablas(self):
        """Crea las tablas del sistema utilizando una conexión limpia."""
        connection = self.connect()
        cursor = connection.cursor()
        try:
            # Tabla de Pacientes
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS pacientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    dni TEXT UNIQUE NOT NULL,
                    nombre TEXT NOT NULL,
                    apellido TEXT NOT NULL,
                    telefono TEXT
                )
            """)
            # Tabla de Tratamientos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tratamientos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    precio REAL NOT NULL
                )
            """)
            # Tabla de Turnos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS turnos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fecha TEXT NOT NULL,
                    hora TEXT NOT NULL,
                    paciente_id INTEGER NOT NULL,
                    tratamiento_id INTEGER NOT NULL,
                    FOREIGN KEY (paciente_id) REFERENCES pacientes(id) ON DELETE CASCADE,
                    FOREIGN KEY (tratamiento_id) REFERENCES tratamientos(id) ON DELETE CASCADE
                )
            """)
            connection.commit()
        finally:
            connection.close()

    def ejecutarConsulta(self, query, parametros=()):
        """Ejecuta cualquier sentencia SQL."""
        connection = self.connect()
        cursor = connection.cursor()
        resultado = None
        try:
            cursor.execute(query, parametros)
            if query.strip().upper().startswith("SELECT"):
                resultado = cursor.fetchall()
            else:
                connection.commit()
        except sqlite3.Error as e:
            print(f"Error en la base de datos: {e}")
            raise e
        finally:
            connection.close()
        return resultado