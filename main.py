# main.py
from database_core import crear_tablas
from motor_diagnostico import evaluar_caso_clinico

AVISO_LEGAL = (
    "Este resultado corresponde a un diagnóstico presuntivo basado en los "
    "síntomas ingresados y no sustituye la evaluación realizada por un "
    "profesional de la salud mental."
)

def iniciar_aplicacion():
    print("====================================================")
    print("   IA de Apoyo al Diagnóstico Presuntivo (DSM-5-TR) ")
    print("   [Entorno Educativo para Estudiantes de Psicología] ")
    print("====================================================")
    
    # Asegurar que las tablas existan al iniciar
    crear_tablas()

    # SIMULACIÓN DE CASO CLÍNICO INGRESADO POR UN ESTUDIANTE:
    # Este caso incluye síntomas depresivos y una palabra gatillo de riesgo ("suicidio")
    caso_estudiante = (
        "Mujer de 20 años que presenta tristeza constante, pérdida de interés "
        "en actividades, insomnio, fatiga, sentimientos de culpa y dificultad para "
        "concentrarse desde hace tres semanas. Refiere ideas de suicidio esporádicas."
    )

    print(f"\n📝 Caso Clínico Analizado:\n'{caso_estudiante}'\n")
    print("⚙️  Procesando análisis sintomático y matriz DSM-5-TR...")
    
    # Ejecutamos el motor de análisis
    analisis = evaluar_caso_clinico(caso_estudiante)

    if analisis:
        # 1. Despliegue de Alertas Académicas Prioritarias
        if analisis["alertas"]:
            print("\n🚨 ¡ALERTA DE RIESGO DETECTADA EN EL TEXTO!")
            for al in analisis["alertas"]:
                print(f"   • Nivel [{al['nivel']}]: {al['mensaje']}")
        
        # 2. Despliegue de Resultados del Diagnóstico Presuntivo
        print("\n📊 Ranking de Diagnósticos Presuntivos:")
        for diag in analisis["diagnosticos"]:
            print(f"\n▪️ {diag['nombre']} ({diag['cie10']})")
            print(f"   Compatibilidad de Criterios: {diag['compatibilidad']}%")
            print(f"   ✔ Criterios Identificados ({len(diag['cumplidos'])}):")
            for c in diag["cumplidos"]:
                print(f"      - {c}")
            print(f"   ❌ Criterios Ausentes o No Registrados ({len(diag['faltantes'])}):")
            for f in diag["faltantes"]:
                print(f"      - {f}")

    print("\n----------------------------------------------------")
    print(f"⚠️  ATENCIÓN: {AVISO_LEGAL}")
    print("----------------------------------------------------")

if __name__ == "__main__":
    iniciar_aplicacion()
