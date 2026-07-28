import streamlit as st
from google import genai
import datetime

# Configuración de la página con diseño limpio
st.set_page_config(page_title="MasterCuota - BetPlay", page_icon="⚽", layout="centered")

# Estilos CSS personalizados para imitar el diseño de la imagen (Modo Oscuro y Tarjetas Doradas)
st.markdown("""
    <style>
    .stApp {
        background-color: #0d1117;
        color: #ffffff;
    }
    .header-box {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #161b22;
        padding: 10px 15px;
        border-radius: 12px;
        border: 1px solid #30363d;
        margin-bottom: 20px;
    }
    .pick-card {
        background: #161b22;
        border: 2px solid #f1e05a;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(241, 224, 90, 0.15);
    }
    .match-row {
        background: #21262d;
        padding: 12px 15px;
        border-radius: 12px;
        margin-bottom: 10px;
        border: 1px solid #30363d;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    </style>
""", unsafe_allow_html=True)

# Encabezado estilo App
st.markdown("""
    <div class="header-box">
        <h2 style="margin:0; color:#f1e05a; font-size:24px;">👑 MasterCuota</h2>
        <span style="background:#238636; color:white; padding:4px 12px; border-radius:20px; font-size:12px; font-weight:bold;">🟢 IA online</span>
    </div>
""", unsafe_allow_html=True)

api_key = st.text_input("Ingresa tu API Key de Google Gemini:", type="password")

if api_key:
    st.divider()
    fecha_seleccionada = st.date_input("Selecciona la fecha para los partidos:", datetime.date.today())
    
    if st.button("🚀 Generar Panel de Alertas (MasterCuota)", use_container_width=True):
        with st.spinner(f"Analizando cuotas reales de BetPlay y generando entre 8 y 16 alertas para el {fecha_seleccionada}..."):
            
            prompt_mastercuota = f"""
            Actúa como el motor de inteligencia artificial de la plataforma "MasterCuota", experto analista cuantitativo de apuestas deportivas especializado en cuotas en tiempo real de BetPlay.
            
            Tu objetivo: Consultar y escanear los partidos destacados de la jornada de hoy [{fecha_seleccionada}], evaluando mercados principales y LÍNEAS ALTERNATIVAS (Córners totales 8.5, 10.5; Goles alternativos 2.5, 3.5) priorizando cuotas entre [1.50 y 1.80].
            
            REQUISITO ESTRICTO:
            Genera entre **8 a 16 alertas/picks** de valor (EV+ superior al 5%) ordenados por solidez técnica.
            
            Para cada partido o alerta generada, entrégalo en un formato limpio estructurado exactamente con estos datos:
            - **Partido:** [Equipo A vs Equipo B]
            - **Lectura Principal / Best Pick:** [Mercado y Línea seleccionada]
            - **Cuota Promedio BetPlay:** [Ej: 1.75]
            - **Value (EV+):** [Valor numérico]
            - **Edge (%):** [Porcentaje superior al 5%]
            - **Confianza (%):** [Ej: 85%]
            """
            
            try:
                client = genai.Client(api_key=api_key)
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt_mastercuota,
                    config={
                        'tools': [{'google_search': {}}]
                    }
                )
                
                st.markdown("### ⭐ MEJOR PICK DESTACADO")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Ocurrió un error al procesar el panel: {e}")
else:
    st.info("Por favor, ingresa tu API Key para activar la interfaz de MasterCuota.")
