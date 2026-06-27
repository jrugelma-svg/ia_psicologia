# poblar_datos.py
from database_core import obtener_conexion

def insertar_datos_educativos():
    conexion = obtener_conexion()
    if conexion is None:
        return

    cursor = conexion.cursor()

    try:
        print("📥 Insertando trastornos de prueba...")
        
        # 1. Insertamos el Trastorno Depresivo Mayor
        cursor.execute("""
            INSERT OR IGNORE INTO trastornos (id, nombre, codigo_cie10, categoria, descripcion)
            VALUES (1, 'Trastorno Depresivo Mayor', 'F32.9', 'Trastornos del Estado de Ánimo', 
            'Caracterizado por episodios de al menos dos semanas con ánimo deprimido o pérdida de interés.')
        """)

        # 2. Insertamos el Trastorno Depresivo Persistente (Diferencial clave)
        cursor.execute("""
            INSERT OR IGNORE INTO trastornos (id, nombre, codigo_cie10, categoria, descripcion)
            VALUES (2, 'Trastorno Depresivo Persistente (Distimia)', 'F34.1', 'Trastornos del Estado de Ánimo', 
            'Estado de ánimo deprimido crónico que persiste la mayor parte del día durante al menos dos años.')
        """)

        print("📋 Insertando criterios específicos del DSM-5-TR...")
        
        # Criterios para el Trastorno Depresivo Mayor (ID: 1)
        criterios_depresion = [
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
        
        # Usamos 'executemany' para insertar la lista completa de una sola vez
        cursor.executemany("""
            INSERT OR IGNORE INTO criterios (trastorno_id, codigo_criterio, descripcion)
            VALUES (?, ?, ?)
        """, criterios_depresion)

        print("⚠️  Configurando palabras clave para Alertas de Riesgo...")
        
        # Alertas de riesgo (Ideación suicida / Autolesiones)
        alertas = [
            ('suicidio', 'ALTO', 'Se detectaron ideas de muerte o suicidio. Se requiere evaluación de riesgo y derivación inmediata.'),
            ('morir', 'ALTO', 'El estudiante reporta deseos de morir. Active el protocolo de emergencia de su institución.'),
            ('cortarme', 'ALTO', 'Posible conducta autolesiva no suicida. Requiere contención psicológica.')
        ]
        
        cursor.executemany("""
            INSERT OR IGNORE INTO alertas_riesgo (palabra_clave, nivel_riesgo, mensaje_educativo)
            VALUES (?, ?, ?)
        """, alertas)

        # Confirmamos los cambios en el archivo
        conexion.commit()
        print("✅ ¡Base de datos poblada con éxito con datos del DSM-5-TR!")

    except Exception as e:
        print(f"❌ Error al poblar los datos: {e}")
    finally:
        conexion.close()

if __name__ == "__main__":
    insertar_datos_educativos()
