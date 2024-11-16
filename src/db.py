import sqlite3
import pandas as pd
from datetime import datetime

def conectar_db():
    conn = sqlite3.connect('data/gestion_aulas.db')  # Guardar en la carpeta 'data'
    return conn

def crear_tablas():
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS aulas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aula TEXT NOT NULL,
        capacidad INTEGER NOT NULL
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS uso_aulas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aula TEXT NOT NULL,
        docente TEXT NOT NULL,
        materia TEXT NOT NULL,
        grado TEXT NOT NULL,
        fecha DATE NOT NULL,
        horario_inicio TIME NOT NULL,
        horario_fin TIME NOT NULL
    )''')

    # Insertar aulas iniciales
    cursor.execute("INSERT INTO aulas (aula, capacidad) VALUES ('Aula 1: Laboratorio', 30)")
    cursor.execute("INSERT INTO aulas (aula, capacidad) VALUES ('Aula 2: Educación Física', 40)")
    cursor.execute("INSERT INTO aulas (aula, capacidad) VALUES ('Aula 3: Proyector', 20)")

    conn.commit()
    conn.close()

def agregar_reserva(aula, docente, materia, grado, fecha, horario_inicio, horario_fin):
    conn = conectar_db()
    cursor = conn.cursor()

    # Convertir fecha y horarios a string
    fecha_str = fecha.strftime("%Y-%m-%d")  # Formato: YYYY-MM-DD
    horario_inicio_str = horario_inicio.strftime("%H:%M:%S")  # Formato: HH:MM:SS
    horario_fin_str = horario_fin.strftime("%H:%M:%S")  # Formato: HH:MM:SS

    cursor.execute('''
    INSERT INTO uso_aulas (aula, docente, materia, grado, fecha, horario_inicio, horario_fin)
    VALUES (?, ?, ?, ?, ?, ?, ?)''',
    (aula, docente, materia, grado, fecha_str, horario_inicio_str, horario_fin_str))

    conn.commit()
    conn.close()

def ver_reservas():
    conn = conectar_db()
    reservas_df = pd.read_sql_query("SELECT * FROM uso_aulas", conn)
    conn.close()
    return reservas_df

def eliminar_reserva(reserva_id):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM uso_aulas WHERE id = ?", (reserva_id,))
    conn.commit()
    conn.close()
