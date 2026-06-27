# app_web.py
import streamlit as st
from database_core import crear_tablas
from motor_diagnostico import evaluar_caso_clinico

# Inicializar la base de datos de manera segura antes de renderizar
crear_tablas()

# Configuración estructural de la página
st.set_page_config(page_title="IA DSM-5-TR Educativa", page_icon="🧠", layout="centered")

st.title("🧠 Asistente Diagnóstico Presuntivo DSM-5-TR")
st.caption("Entorno Práctico Educativo para Estudiantes de Psicología")

st.markdown("""
Esta herramienta simula el análisis sintomático estructurado basándose en los criterios 
almacenados en la base de datos local. **Inserte un caso clínico abajo para comenzar.**
""")

caso_clinico = st.text_area(
    "📝 Ingrese el fragmento del caso o la descripción de la entrevista:",
    placeholder="Ej: Paciente refiere desinterés generalizado, insomnio de conciliación y llanto fácil...",
    height=150
)

# Creamos un contenedor vacío fijo abajo. Esto previene el error 'removeChild' al 100%
zona_resultados = st.container()

if st.button("🔍 Analizar Caso Clínico", type="primary"):
    if not caso_clinico.strip():
        st.warning("⚠️ Por favor, ingrese algún texto para poder realizar el análisis clínico.")
    else:
        analisis = evaluar_caso_clinico(caso_clinico)
        
        # Todo lo visual se dibuja rígidamente dentro de la zona reservada
        with zona_resultados:
            if analisis:
                # 1. Alertas de Riesgo
                if analisis["alertas"]:
                    st.markdown("### 🚨 Alertas de Riesgo Detectadas")
                    for al in analisis["alertas"]:
                        st.markdown(f"🔴 **[{al['nivel']}]**: {al['mensaje']}")
                    st.markdown("---")
                
                # 2. Diagnósticos Presuntivos
                st.markdown("### 📊 Compatibilidad con Criterios Oficiales")
                
                for diag in analisis["diagnosticos"]:
                    st.markdown(f"#### 🔹 {diag['nombre']} ({diag['cie10']}) — **{diag['compatibilidad']}%**")
                    st.markdown(f"*Categoría:* {diag['categoria']}")
                    
                    # Usamos listas simples estáticas muy estables
                    cumplidos_txt = ""
                    if diag["cumplidos"]:
                        for c in diag["cumplidos"]:
                            cumplidos_txt += f"✅ {c}\n\n"
                    else:
                        cumplidos_txt = "Ninguno detectado directamente.\n\n"
                        
                    faltantes_txt = ""
                    if diag["faltantes"]:
                        for f in diag["faltantes"]:
                            faltantes_txt += f"▫️ {f}\n\n"
                    
                    st.markdown("**Criterios Identificados:**")
                    st.markdown(cumplidos_txt)
                    st.markdown("**Criterios Ausentes o No Registrados:**")
                    st.markdown(faltantes_txt)
                    st.markdown("---")
                                    
                # 3. Descargo de responsabilidad ético
                st.markdown("💡 **AVISO LEGAL:** Este resultado corresponde a un diagnóstico presuntivo basado en los síntomas ingresados y tiene únicamente fines pedagógicos. No sustituye la evaluación clínica formal de un profesional.")
