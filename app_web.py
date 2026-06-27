# app_web.py
import streamlit as st
from motor_diagnostico import evaluar_caso_clinico

# Configuración de la página web
st.set_page_config(page_title="IA DSM-5-TR Educativa", page_icon="🧠", layout="centered")

# Encabezado de la aplicación
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

# Botón para activar el análisis
if st.button("🔍 Analizar Caso Clínico", type="primary"):
    if caso_clinico.strip() == "":
        st.warning("⚠️ Por favor, ingrese algún texto para poder realizar el análisis clínico.")
    else:
        st.subheader("⚙️ Resultado del Análisis Estructurado")
        
        # Ejecutamos el motor que creaste
        analisis = evaluar_caso_clinico(caso_clinico)
        
        if analisis:
            # 1. Bloque de Alertas Críticas (Si existen)
            if analisis["alertas"]:
                for al in analisis["alertas"]:
                    st.error(f"🚨 **ALERTA DE RIESGO DETECTADA ({al['nivel']})**: {al['mensaje']}")
            
            # 2. Despliegue de los Diagnósticos Presuntivos
            st.markdown("### 📊 Compatibilidad con Criterios Oficiales")
            
            for diag in analisis["diagnosticos"]:
                # Creamos una tarjeta expandible para cada trastorno
                with st.expander(f"🔹 {diag['nombre']} ({diag['cie10']}) — **{diag['compatibilidad']}%**"):
                    st.markdown(f"**Categoría:** {diag['categoria']}")
                    
                    # Columnas para organizar Criterios Presentes vs Ausentes
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.success(f"✔ **Identificados ({len(diag['cumplidos'])})**")
                        if diag["cumplidos"]:
                            for c in diag["cumplidos"]:
                                st.write(f"• {c}")
                        else:
                            st.caption("Ninguno detectado directamente.")
                            
                    with col2:
                        st.text("❌ **Ausentes o No Reportados**")
                        if diag["faltantes"]:
                            for f in diag["faltantes"]:
                                st.write(f"• {f}")
                                
            # 3. Descargo de responsabilidad ético
            st.info("⚠️ **AVISO LEGAL:** Este resultado corresponde a un diagnóstico presuntivo basado en los síntomas ingresados y tiene únicamente fines pedagógicos. No sustituye la evaluación clínica formal de un profesional.")
