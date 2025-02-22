# database.py
import sqlite3

def crear_tablas():
    conn = sqlite3.connect('clinica.db')
    c = conn.cursor()
    
    # Tabla de usuarios
    c.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 Cedula TEXT UNIQUE NOT NULL,
                 Nombre TEXT NOT NULL,
                 Apellido TEXT NOT NULL,
                 Sexo TEXT NOT NULL,
                 FechaNacimiento DATE NOT NULL,
                 Correo TEXT NOT NULL,
                 Contraseña TEXT NOT NULL,
                 Tipo TEXT NOT NULL)''')
    
    # Tabla de médicos
    c.execute('''CREATE TABLE IF NOT EXISTS medicos (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 Nombre TEXT NOT NULL,
                 Especialidad TEXT NOT NULL)''')
    
    # Tabla de citas
    c.execute('''CREATE TABLE IF NOT EXISTS citas (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 usuario_id INTEGER,
                 medico_id INTEGER,
                 fecha TEXT,
                 hora TEXT,
                 estado TEXT,
                 FOREIGN KEY(usuario_id) REFERENCES usuarios(id),
                 FOREIGN KEY(medico_id) REFERENCES medicos(id))''')

    # Insertar un administrador por defecto
    c.execute("INSERT OR IGNORE INTO usuarios (Cedula, Nombre, Apellido, Sexo, FechaNacimiento, Correo, Contraseña, Tipo) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
              ("123456789", "admin", "admin", "Masculino", "1995-01-04", "admin@clinica.com", "admin123", "Administrador"))
    
    # Insertar médicos con especialidad (solo si no existen)
    insertar_medicos(c)

    conn.commit()
    conn.close()

def insertar_medicos(c):
    # Lista de médicos y especialidades
    medicos = [
        ("Dr. Juan Pérez", "Cardiología"),
        ("Dr. Ana López", "Pediatría"),
        ("Dr. Carlos García", "Neurología"),
        ("Dr. María Sánchez", "Ginecología")
    ]
    
    for medico in medicos:
        # Verificar si el médico con esa especialidad ya existe
        c.execute("SELECT COUNT(*) FROM medicos WHERE Nombre = ? AND Especialidad = ?", (medico[0], medico[1]))
        count = c.fetchone()[0]
        
        if count == 0:  # Solo insertamos si no existe
            c.execute("INSERT INTO medicos (Nombre, Especialidad) VALUES (?, ?)", medico)

def obtener_conexion():
    return sqlite3.connect('clinica.db')