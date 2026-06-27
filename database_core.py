# database_core.py
import sqlite3

def obtener_conexion():
    try:
        # Esto creará el archivo en el servidor de la nube de forma automática
        conexion = sqlite3.connect("dsm5tr_educativo.db")
        return conexion
    except Exception as e:
        print(f"Error de conexión a la base de datos: {e}")
        return None

def crear_tablas():
    conexion = obtener_conexion()
    if conexion is None:
        return
    
    cursor = conexion.cursor()
    
    # Crear tablas indispensables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trastornos (
            id INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            codigo_cie10 TEXT,
            categoria TEXT,
            descripcion TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS criterios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trastorno_id INTEGER,
            codigo_criterio TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            FOREIGN KEY (trastorno_id) REFERENCES trastornos(id)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alertas_riesgo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            palabra_clave TEXT UNIQUE,
            nivel_riesgo TEXT,
            mensaje_educativo TEXT
        )
    """)
    
    # --- AUTO-POBLADO INMEDIATO PARA LA NUBE ---
    # Insertar Trastornos
    cursor.execute("INSERT OR IGNORE INTO trastornos VALUES (1, 'Trastorno Depresivo Mayor', 'F32.9', 'Trastornos del Estado de Ánimo', 'Caracterizado por episodios de al menos dos semanas con ánimo deprimido.')")
    cursor.execute("INSERT OR IGNORE INTO trastornos VALUES (2, 'Trastorno Depresivo Persistente (Distimia)', 'F34.1', 'Trastornos del Estado de Ánimo', 'Estado de ánimo deprimido crónico de al menos dos años.')")
    
    # Insertar Criterios
    criterios = [
        (1, 'A1', 'Estado de ánimo deprimido la mayor parte del día'),
        (1, 'A2', 'Anhedonia (disminución notable del interés o placer)'),
        (1, 'A3', 'Pérdida o aumento importante de peso / apetito'),
        (1, 'A4', 'Insomnio o hipersomnia casi todos los días'),
        (1, 'A5', 'Agitación o retraso psicomotor'),
        (1, 'A6', 'Fatiga o pérdida de energía casi todos los días'),
        (1, 'A7', 'Sentimiento de culpabilidad excesiva o inutilidad'),
        (1, 'A8', 'Disminución de la capacidad para pensar o concentrarse'),
        (1, 'A9', 'Ideas de suicidio o de muerte recurrentes'),
        (1, 'B', 'Los síntomas causan malestar clínicamente significativo'),
        (1, 'C', 'El episodio no se puede atribuir a efectos de una sustancia')
    ]
    for trastorno_id, cod, desc in criterios:
        cursor.execute("INSERT OR IGNORE INTO criterios (trastorno_id, codigo_criterio, descripcion) VALUES (?, ?, ?)", (trastorno_id, cod, desc))
        
    # Insertar Alertas
    alertas = [
        ('suicidio', 'ALTO', 'Se detectaron ideas de muerte o suicidio. Se requiere evaluación de riesgo y derivación inmediata.'),
        ('morir', 'ALTO', 'El estudiante reporta deseos de morir. Active el protocolo de emergencia de su institución.'),
        ('cortarme', 'ALTO', 'Posible conducta autolesiva no suicida. Requiere contención psicológica.')
    ]
    for palabra, nivel, mensaje in alertas:
        cursor.execute("INSERT OR IGNORE INTO alertas_riesgo (palabra_clave, nivel_riesgo, mensaje_educativo) VALUES (?, ?, ?)", (palabra, nivel, mensaje))
        
    conexion.commit()
    conexion.close()
