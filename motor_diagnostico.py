# motor_diagnostico.py
import sqlite3
from database_core import obtener_conexion

def evaluar_caso_clinico(texto_usuario):
    """
    Analiza el texto ingresado por el estudiante buscando alertas de riesgo 
    y calculando el porcentaje de compatibilidad con los trastornos guardados.
    """
    conexion = obtener_conexion()
    if conexion is None:
        return None

    cursor = conexion.cursor()
    texto_minusculas = texto_usuario.lower()

    # --- 1. EVALUACIÓN DE ALERTAS DE RIESGO ---
    alertas_detectadas = []
    try:
        cursor.execute("SELECT palabra_clave, nivel_riesgo, mensaje_educativo FROM alertas_riesgo")
        todas_las_alertas = cursor.fetchall()
        
        for palabra, nivel, mensaje in todas_las_alertas:
            if palabra in texto_minusculas:
                alertas_detectadas.append({
                    "palabra": palabra,
                    "nivel": nivel,
                    "mensaje": mensaje
                })
    except Exception as e:
        print(f"Error al evaluar riesgos: {e}")

    # --- 2. EVALUACIÓN DE TRASTORNOS Y CRITERIOS ---
    resultados_diagnosticos = []
    try:
        # Traemos todos los trastornos cargados
        cursor.execute("SELECT id, nombre, codigo_cie10, categoria, descripcion FROM trastornos")
        trastornos = cursor.fetchall()

        for t_id, t_nombre, t_cie10, t_categoria, t_descripcion in trastornos:
            # Traemos los criterios asociados a este trastorno específico
            cursor.execute("SELECT codigo_criterio, descripcion FROM criterios WHERE trastorno_id = ?", (t_id,))
            criterios = cursor.fetchall()

            criterios_cumplidos = []
            criterios_faltantes = []

            # Mapeo manual simple de palabras clave clínicas (simulando un primer filtro)
            # En fases posteriores, aquí conectaremos la API de IA para mayor precisión lingüística
            diccionario_sinonimos = {
                "tristeza": "deprimido", "ánimo deprimido": "deprimido",
                "interés": "anhedonia", "placer": "anhedonia",
                "insomnio": "insomnio", "sueño": "insomnio",
                "fatiga": "fatiga", "energía": "fatiga",
                "culpa": "culpa", "inutilidad": "culpa",
                "concentrarse": "concentrarse", "pensar": "concentrarse"
            }

            for cod, desc in criterios:
                # Buscamos si alguna palabra clave del criterio aparece en el texto del caso
                encontrado = False
                for palabra_clave, criterio_asociado in diccionario_sinonimos.items():
                    if palabra_clave in texto_minusculas and criterio_asociado in desc.lower():
                        encontrado = True
                        break
                
                if encontrado:
                    criterios_cumplidos.append(f"{cod}: {desc}")
                else:
                    criterios_faltantes.append(f"{cod}: {desc}")

            # Calcular porcentaje matemático de compatibilidad
            total_criterios = len(criterios)
            cumplidos_count = len(criterios_cumplidos)
            
            # Evitamos dividir entre cero si un trastorno no tiene criterios asignados
            porcentaje_compatibilidad = (cumplidos_count / total_criterios) * 100 if total_criterios > 0 else 0

            resultados_diagnosticos.append({
                "nombre": t_nombre,
                "cie10": t_cie10,
                "categoria": t_categoria,
                "compatibilidad": round(porcentaje_compatibilidad, 1),
                "cumplidos": criterios_cumplidos,
                "faltantes": criterios_faltantes
            })

    except Exception as e:
        print(f"Error al calcular compatibilidades: {e}")
    finally:
        conexion.close()

    # Retornamos el análisis empaquetado para que la interfaz lo muestre
    return {
        "alertas": alertas_detectadas,
        "diagnosticos": sorted(resultados_diagnosticos, key=lambda x: x['compatibilidad'], reverse=True)
    }
