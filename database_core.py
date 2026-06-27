# database_core.py
import sqlite3

# Definimos dónde se guardará el archivo de la base de datos
DB_NAME = "dsm5tr_educativo.db"

def obtener_conexion():
    """Establece una conexión segura con el archivo de la base de datos."""
    try:
        conexion = sqlite3.connect(DB_NAME)
        conexion.execute("PRAGMA foreign_keys = ON;") # Asegura que las tablas estén bien conectadas
        return conexion
    except Exception as e:
        print(f"❌ Error al conectar a la base de datos: {e}")
        return None

def crear_tablas():
    """Crea las tablas de Trastornos, Criterios y Alertas de Riesgo si no existen."""
    conexion = obtener_conexion()
    if conexion is None:
        return

    cursor = conexion.cursor()

    # 1. Tabla de Trastornos (Guarda los nombres y categorías del DSM)
    tabla_trastornos = """
    CREATE TABLE IF NOT EXISTS trastornos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE,
        codigo_cie10 TEXT,
        categoria TEXT NOT NULL,
        descripcion TEXT
    );
    """

    # 2. Tabla de Criterios (Guarda los síntomas oficiales de cada trastorno)
    tabla_criterios = """
    CREATE TABLE IF NOT EXISTS criterios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        trastorno_id INTEGER NOT NULL,
        codigo_criterio TEXT NOT NULL, -- Ej: 'A1', 'B'
        descripcion TEXT NOT NULL,
        FOREIGN KEY (trastorno_id) REFERENCES trastornos(id) ON DELETE CASCADE
    );
    """

    # 3. Tabla de Alertas de Riesgo (Para detectar autolesiones o ideación suicida)
    tabla_alertas = """
    CREATE TABLE IF NOT EXISTS alertas_riesgo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        palabra_clave TEXT NOT NULL UNIQUE,
        nivel_riesgo TEXT NOT NULL,
        mensaje_educativo TEXT NOT NULL
    );
    """

    try:
        cursor.execute(tabla_trastornos)
        cursor.execute(tabla_criterios)
        cursor.execute(tabla_alertas)
        conexion.commit()
        print("💾 Base de datos y tablas estructuradas correctamente.")
    except Exception as e:
        print(f"❌ Error al crear las tablas: {e}")
    finally:
        conexion.close()
