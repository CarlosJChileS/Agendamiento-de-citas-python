import sqlite3
from contextlib import closing

def crear_tablas():
    with closing(sqlite3.connect('agendamiento_clinico.db')) as con:
        with con:
            con.execute('''
            CREATE TABLE IF NOT EXISTS pacientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                email TEXT NOT NULL,
                telefono TEXT NOT NULL,
                cedula TEXT NOT NULL,
                edad INTEGER,
                sexo TEXT,
                estado_civil TEXT,
                ocupacion TEXT,
                residencia_actual TEXT,
                residencia_anterior TEXT
            )
            ''')
            con.execute('''
            CREATE TABLE IF NOT EXISTS citas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                paciente_id INTEGER,
                fecha TEXT NOT NULL,
                hora TEXT NOT NULL,
                descripcion TEXT,
                ubicacion TEXT,
                FOREIGN KEY(paciente_id) REFERENCES pacientes(id)
            )
            ''')
            con.execute('''
            CREATE TABLE IF NOT EXISTS historia_clinica (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                paciente_id INTEGER,
                fecha TEXT NOT NULL,
                motivo_consulta TEXT,
                antecedentes_enfermedades TEXT,
                medicamentos_habituales TEXT,
                habitos_nocivos TEXT,
                metodos_anticonceptivos TEXT,
                examen_fisico TEXT,
                diagnostico_definitivo TEXT,
                FOREIGN KEY(paciente_id) REFERENCES pacientes(id)
            )
            ''')

if __name__ == "__main__":
    crear_tablas()
