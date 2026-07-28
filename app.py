import streamlit as st
from google import genai
import datetime
import urllib.parse

st.set_page_config(page_title="Buscador Real de Best Picks - BetPlay", page_icon="⚽", layout="centered")

st.title("⚽ Buscador Real de Best Picks (BetPlay)")
st.markdown("Analiza partidos reales de hoy consultando cuotas y aplicando tu **prompt cuantitativo estricto**.")

api_key = st.text_input("Ingresa tu API Key de Google Gemini:", type="password")

if api_key:
    st.divider()
    fecha_seleccionada = st.date_input("Selecciona la fecha para los partidos:", datetime.date.today())
    
    if st.button("🚀 Generar Best Picks con Cuotas Reales"):
        with st.spinner(f"Buscando partidos reales y analizando cuotas en BetPlay para el {fecha_seleccionada}..."):
            
            # Construimos una consulta de búsqueda para guiar al modelo a buscar los eventos del día
            consulta_busqueda = f"partidos de futbol programados para hoy {fecha_seleccionada} y cuotas de BetPlay"
            
            prompt_real = f"""
            Actúa como un analista cuantitativo estricto de apuestas deportivas especializado en BetPlay.
            Hoy es la fecha: {fecha_seleccionada}.
            
            Tu tarea es investigar o utilizar información actualizada y real sobre los partidos de fútbol reales programados para esta fecha (liga colombiana BetPlay, ligas sudamericanas o europeas principales).
            Para cada partido real identificado:
            1. Consulta y contrasta el mercado principal (Ganador, Goles Over/Under, etc.) con las cuotas reales que ofrece la casa de apuestas **BetPlay**.
            2. Aplica los cálculos matemáticos de probabilidad implícita y Edge (EV+).
            
            APLICA TU PROMPT CUANTITATIVO ESTRICTO (#5):
            - Exige un Edge mínimo del +5% (EV+).
            - Si las cuotas de BetPlay son bajas (como 1.43 o similares que destruyen el valor), APLICA LA REGLA DE DESCARTE INMEDIATO. 
            - Solo selecciona como **Best Pick** aquellos partidos reales que matemáticamente superen el filtro de valor. Si ninguno cumple, indícalo claramente justificando el porqué.
            
            Entrega el resultado en español, ordenado por tablas limpias, indicando claramente los partidos reales analizados, las cuotas de BetPlay encontradas, cuáles pasan el filtro y cuáles se descartan.
            """
            
            try:
                client = genai.Client(api_key=api_key)
                # Usamos la capacidad de Google Search integrada en Gemini para buscar datos reales en internet
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt_real,
                    config={
                        'tools': [{'google_search': {}}]
                    }
                )
                
                st.subheader(f"📊 Best Picks Reales (BetPlay) - {fecha_seleccionada}")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Ocurrió un error al procesar la solicitud con datos reales: {e}")
else:
    st.info("Por favor, ingresa tu API Key de Google Gemini para habilitar el buscador.")
