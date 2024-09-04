import os
import sqlite3
import pandas as pd
import json
from contextlib import closing
from datetime import datetime

def conectar_db():
    return sqlite3.connect('agendamiento_clinico.db')

def agregar_paciente(nombre, apellido, email, telefono, cedula, edad=None, sexo=None, estado_civil=None, ocupacion=None, residencia_actual=None, residencia_anterior=None):
    con = conectar_db()
    cursor = con.cursor()
    cursor.execute("""
    INSERT INTO pacientes (nombre, apellido, email, telefono, cedula, edad, sexo, estado_civil, ocupacion, residencia_actual, residencia_anterior)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (nombre, apellido, email, telefono, cedula, edad, sexo, estado_civil, ocupacion, residencia_actual, residencia_anterior))
    con.commit()
    con.close()

def obtener_pacientes():
    con = conectar_db()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM pacientes")
    pacientes = cursor.fetchall()
    con.close()
    return pacientes

def obtener_pacientes_por_nombre(nombre):
    con = conectar_db()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM pacientes WHERE nombre=?", (nombre,))
    pacientes = cursor.fetchall()
    con.close()
    return pacientes

def obtener_pacientes_por_ubicacion(ubicacion):
    con = conectar_db()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM pacientes WHERE residencia_actual=?", (ubicacion,))
    pacientes = cursor.fetchall()
    con.close()
    return pacientes

def obtener_paciente_por_id(paciente_id):
    con = conectar_db()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM pacientes WHERE id=?", (paciente_id,))
    paciente = cursor.fetchone()
    con.close()
    return paciente

def obtener_paciente_por_cedula(cedula):
    con = conectar_db()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM pacientes WHERE cedula=?", (cedula,))
    paciente = cursor.fetchone()
    con.close()
    return paciente

def obtener_nombre_paciente(paciente_id):
    con = conectar_db()
    cursor = con.cursor()
    cursor.execute("SELECT nombre, apellido FROM pacientes WHERE id=?", (paciente_id,))
    nombre = cursor.fetchone()
    con.close()
    return f"{nombre[0]} {nombre[1]}" if nombre else "Desconocido"

def actualizar_paciente(paciente_id, nombre, apellido, email, telefono, cedula, edad=None, sexo=None, estado_civil=None, ocupacion=None, residencia_actual=None, residencia_anterior=None):
    con = conectar_db()
    cursor = con.cursor()
    cursor.execute("""
    UPDATE pacientes
    SET nombre=?, apellido=?, email=?, telefono=?, cedula=?, edad=?, sexo=?, estado_civil=?, ocupacion=?, residencia_actual=?, residencia_anterior=?
    WHERE id=?
    """, (nombre, apellido, email, telefono, cedula, edad, sexo, estado_civil, ocupacion, residencia_actual, residencia_anterior, paciente_id))
    con.commit()
    con.close()

def eliminar_paciente(paciente_id):
    con = conectar_db()
    cursor = con.cursor()
    cursor.execute("DELETE FROM pacientes WHERE id=?", (paciente_id,))
    con.commit()
    con.close()

def agregar_cita(paciente_id, fecha, hora, descripcion, ubicacion):
    con = conectar_db()
    cursor = con.cursor()
    cursor.execute("""
    INSERT INTO citas (paciente_id, fecha, hora, descripcion, ubicacion)
    VALUES (?, ?, ?, ?, ?)
    """, (paciente_id, fecha, hora, descripcion, ubicacion))
    con.commit()
    con.close()

def obtener_citas_dia(fecha):
    con = conectar_db()
    cursor = con.cursor()
    cursor.execute("""
    SELECT c.id, c.paciente_id, c.fecha, c.hora, c.descripcion, p.nombre, p.apellido
    FROM citas c
    JOIN pacientes p ON c.paciente_id = p.id
    WHERE c.fecha = ?
    """, (fecha,))
    citas = cursor.fetchall()
    con.close()
    return citas

def exportar_historial_citas_excel(filename):
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    if not os.path.exists('exportaciones'):
        os.makedirs('exportaciones')
    con = conectar_db()
    query = """
    SELECT c.fecha, c.hora, p.nombre || ' ' || p.apellido AS paciente, c.descripcion, c.ubicacion
    FROM citas c
    JOIN pacientes p ON c.paciente_id = p.id
    """
    citas = pd.read_sql_query(query, con)
    citas.to_excel(filename, index=False)
    con.close()
    return filename

def exportar_historial_pacientes_excel(filename):
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    if not os.path.exists('exportaciones'):
        os.makedirs('exportaciones')
    con = conectar_db()
    pacientes = pd.read_sql_query("SELECT * FROM pacientes", con)
    pacientes.to_excel(filename, index=False)
    con.close()
    return filename

def obtener_historial_clinico(paciente_id):
    con = conectar_db()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM historia_clinica WHERE paciente_id=?", (paciente_id,))
    historial = cursor.fetchall()
    con.close()
    historial = [(h[0], h[1], h[2], h[3], h[4], h[5], h[6], json.loads(h[7]), h[8]) for h in historial]
    return historial

def agregar_historia_clinica(paciente_id, fecha, motivo_consulta, antecedentes, medicamentos, habitos, anticonceptivos, examen_fisico, diagnostico):
    with closing(sqlite3.connect('agendamiento_clinico.db')) as con:
        with con:
            con.execute('''
            INSERT INTO historia_clinica (paciente_id, fecha, motivo_consulta, antecedentes_enfermedades, medicamentos_habituales, habitos_nocivos, metodos_anticonceptivos, examen_fisico, diagnostico_definitivo)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (paciente_id, fecha, motivo_consulta, antecedentes, medicamentos, habitos, anticonceptivos, examen_fisico, diagnostico))

def actualizar_historial(historial_id, fecha, motivo_consulta, antecedentes, medicamentos, habitos, anticonceptivos, examen_fisico, diagnostico):
    con = conectar_db()
    cursor = con.cursor()
    cursor.execute("""
    UPDATE historia_clinica
    SET fecha=?, motivo_consulta=?, antecedentes_enfermedades=?, medicamentos_habituales=?, habitos_nocivos=?, metodos_anticonceptivos=?, examen_fisico=?, diagnostico_definitivo=?
    WHERE id=?
    """, (fecha, motivo_consulta, antecedentes, medicamentos, habitos, anticonceptivos, examen_fisico, diagnostico, historial_id))
    con.commit()
    con.close()

def eliminar_historial(historial_id):
    con = conectar_db()
    cursor = con.cursor()
    cursor.execute("DELETE FROM historia_clinica WHERE id=?", (historial_id,))
    con.commit()
    con.close()

def eliminar_historia_clinica(paciente_id):
    con = conectar_db()
    cursor = con.cursor()
    cursor.execute("DELETE FROM historia_clinica WHERE paciente_id=?", (paciente_id,))
    con.commit()
    con.close()

def obtener_cita_por_id(cita_id):
    con = conectar_db()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM citas WHERE id=?", (cita_id,))
    cita = cursor.fetchone()
    con.close()
    return cita

def actualizar_cita(cita_id, fecha, hora, ubicacion, descripcion):
    con = conectar_db()
    cursor = con.cursor()
    cursor.execute("""
    UPDATE citas
    SET fecha=?, hora=?, ubicacion=?, descripcion=?
    WHERE id=?
    """, (fecha, hora, ubicacion, descripcion, cita_id))
    con.commit()
    con.close()

def eliminar_cita(cita_fecha, cita_hora):
    con = conectar_db()
    cursor = con.cursor()
    cursor.execute("DELETE FROM citas WHERE fecha=? AND hora=?", (cita_fecha, cita_hora))
    con.commit()
    con.close()

def obtener_proximas_citas():
    con = conectar_db()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM citas WHERE fecha >= date('now') ORDER BY fecha ASC, hora ASC")
    citas = cursor.fetchall()
    con.close()
    return citas

def obtener_historial_clinico_completo():
    conexion = sqlite3.connect('agendamiento_clinico.db')
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT hc.id, p.cedula, p.nombre, p.apellido, hc.fecha, hc.motivo_consulta
        FROM historia_clinica hc
        JOIN pacientes p ON hc.paciente_id = p.id
    """)
    historial = cursor.fetchall()
    conexion.close()
    return historial

def obtener_historia_clinica_por_id(historia_id):
    con = conectar_db()
    cursor = con.cursor()
    cursor.execute("SELECT id, cedula, nombre, apellido, fecha, motivo_consulta, antecedentes_enfermedades, medicamentos_habituales, habitos_nocivos, metodos_anticonceptivos, examen_fisico, diagnostico_definitivo FROM historia_clinica WHERE id=?", (historia_id,))
    historia = cursor.fetchone()
    con.close()
    return historia

def exportar_historial_clinico_excel(filename):
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    if not os.path.exists('exportaciones'):
        os.makedirs('exportaciones')
    con = conectar_db()
    query = """
    SELECT hc.fecha, p.cedula, p.nombre || ' ' || p.apellido AS paciente, hc.motivo_consulta, hc.antecedentes_enfermedades, 
           hc.medicamentos_habituales, hc.habitos_nocivos, hc.metodos_anticonceptivos, hc.examen_fisico, hc.diagnostico_definitivo
    FROM historia_clinica hc
    JOIN pacientes p ON hc.paciente_id = p.id
    """
    historial_clinico = pd.read_sql_query(query, con)
    historial_clinico.to_excel(filename, index=False)
    con.close()
    return filename

def exportar_historial_clinico_seleccionado_excel(historia_id, filename):
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    if not os.path.exists('exportaciones'):
        os.makedirs('exportaciones')
    con = conectar_db()
    query = """
    SELECT hc.fecha, p.cedula, p.nombre || ' ' || p.apellido AS paciente, hc.motivo_consulta, hc.antecedentes_enfermedades, 
           hc.medicamentos_habituales, hc.habitos_nocivos, hc.metodos_anticonceptivos, hc.examen_fisico, hc.diagnostico_definitivo
    FROM historia_clinica hc
    JOIN pacientes p ON hc.paciente_id = p.id
    WHERE hc.id = ?
    """
    historial_clinico = pd.read_sql_query(query, con, params=(historia_id,))
    historial_clinico.to_excel(filename, index=False)
    con.close()
    return filename

def obtener_historial_clinico_por_cedula(cedula):
    con = conectar_db()
    cursor = con.cursor()
    cursor.execute("""
    SELECT hc.id, p.cedula, p.nombre, p.apellido, hc.fecha, hc.motivo_consulta, hc.antecedentes_enfermedades, hc.medicamentos_habituales, 
           hc.habitos_nocivos, hc.metodos_anticonceptivos, hc.examen_fisico, hc.diagnostico_definitivo
    FROM historia_clinica hc
    JOIN pacientes p ON hc.paciente_id = p.id
    WHERE p.cedula = ?
    """, (cedula,))
    historial = cursor.fetchall()
    con.close()
    return historial
