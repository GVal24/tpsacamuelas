import sqlite3

class Consultorio:
    def __init__(self, db_name="consultorio.db"):
        self.conexion = sqlite3.connect(db_name)
        self.crear_tablas()

    def crear_tablas(self):
        cursor = self.conexion.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dni TEXT UNIQUE NOT NULL,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            telefono TEXT NOT NULL
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS turnos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            hora TEXT NOT NULL,
            paciente_id INTEGER NOT NULL,
            FOREIGN KEY(paciente_id) REFERENCES pacientes(id)
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tratamientos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            paciente_id INTEGER NOT NULL,
            FOREIGN KEY(paciente_id) REFERENCES pacientes(id)
        )
        """)
        self.conexion.commit()
