# app_web.py
import streamlit as st
from motor_diagnostico import evaluar_caso_clinico

# Configuración de la página web
st.set_page_config(page_title="IA DSM-5-TR Educativa", page_icon="🧠", layout="centered")

st.title("🧠 Asistente Diagnóstico Presuntivo DSM-5-TR")
st.caption("Entorno Práctico Educativo para Estudiantes de Psicología")

st.markdown("""
Esta herramienta simula el análisis sintomático estructurado basándose en los criterios 
almacenados en la base de datos local. **Inserte un caso clínico abajo para comenzar.**
""")

# Cuadro de texto para el caso clínico
caso_clinico = st.text_area(
    "📝 Ingrese el fragmento del caso o la descripción de la entrevista:",
    placeholder="Ej: Paciente refiere desinterés generalizado, insomnio de conciliación y llanto fácil...",
    height=150
)

# Usamos un contenedor estático para evitar el error de renderizado dinámico en la nube
if st.button("🔍 Analizar Caso Clínico", type="primary"):
    if not caso_clinico.strip():
        st.warning("⚠️ Por favor, ingrese algún texto para poder realizar el análisis clínico.")
    else:
        # Ejecutamos el motor de análisis
        analisis = evaluar_caso_clinico(caso_clinico)
        
        if analisis:
            # 1. Bloque de Alertas Críticas (Si existen)
            if analisis["alertas"]:
                st.subheader("🚨 Alertas de Riesgo Detectadas")
                for al in analisis["alertas"]:
                    st.error(f"**[{al['nivel']}]**: {al['mensaje']}")
            
            # 2. Despliegue de los Diagnósticos Presuntivos
            st.subheader("📊 Compatibilidad con Criterios Oficiales")
            
            for diag in analisis["diagnosticos"]:
                st.markdown(f"### 🔹 {diag['nombre']} ({diag['cie10']}) — **{diag['compatibilidad']}%**")
                st.markdown(f"**Categoría:** {diag['categoria']}")
                
                # Despliegue en formato de texto directo scannable (más estable que columnas/expanders en la nube)
                st.markdown("**✔ Criterios Identificados:**")
                if diag["cumplidos"]:
                    for c in diag["cumplidos"]:
                        st.markdown(f"✅ {c}")
                else:
                    st.caption("Ninguno detectado directamente.")
                    
                st.markdown("**❌ Criterios Ausentes o No Registrados:**")
                if diag["faltantes"]:
                    for f in diag["faltantes"]:
                        st.markdown(f"▫️ {f}")
                
                st.markdown("---")
                                
            # 3. Descargo de responsabilidad ético
            st.info("⚠️ **AVISO LEGAL:** Este resultado corresponde a un diagnóstico presuntivo basado en los síntomas ingresados y tiene únicamente fines pedagógicos. No sustituye la evaluación clínica formal de un profesional.")
