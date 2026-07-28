import streamlit as st
from google import genai
import datetime

# Configuración de la interfaz en español
st.set_page_config(page_title="Generador de Best Picks - BetPlay", page_icon="⚽", layout="centered")

st.title("⚽ Buscador Automático de Best Picks")
st.markdown("Selecciona una fecha y deja que la IA analice los partidos del día aplicando tu **prompt cuantitativo estricto** para BetPlay.")

# Pedir la llave de la API
api_key = st.text_input("Ingresa tu API Key de Google Gemini:", type="password")

if api_key:
    client = genai.Client(api_key=api_key)
    st.divider()
    
    # Selector de fecha para el usuario
    fecha_seleccionada = st.date_input("Selecciona la fecha para los partidos:", datetime.date.today())
    
    # Botón único de análisis masivo
    if st.button("🚀 Generar Best Picks del Día"):
        with st.spinner(f"Escaneando partidos, cuotas de BetPlay y aplicando filtros de valor para el {fecha_seleccionada}..."):
            
            prompt_masivo = f"""
            Actúa como un analista cuantitativo estricto de apuestas deportivas especializado en BetPlay.
            Hoy es la fecha: {fecha_seleccionada}.
            
            Tu tarea es simular el análisis de los partidos más importantes o relevantes programados para esta fecha en las ligas principales (o fútbol colombiano/internacional).
            Para cada partido que identifiques:
            1. Evalúa el mercado principal (Ej: Goles o Ganador).
            2. Revisa la cuota estimada de BetPlay de manera realista.
            3. Aplica los cálculos matemáticos de probabilidad implícita y Edge.
            
            REGLA DE ORO ESTRICTA:
            - Exige un Edge mínimo del +5% (EV+).
            - Si las cuotas de BetPlay son bajas (como 1.43 o similares que destruyen el valor), APLICA LA REGLA DE DESCARTE INMEDIATO. 
            - Solo selecciona como **Best Pick** aquellos partidos que matemáticamente superen el filtro de valor. Si ninguno cumple, indícalo claramente.
            
            Entrega el resultado en español, ordenado por tablas limpias, indicando claramente cuáles partidos pasan el filtro y cuáles se descartan por alta varianza o valor nulo.
            """
            
            try:
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt_masivo
                )
                
                st.subheader(f"📊 Best Picks y Veredictos - {fecha_seleccionada}")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Ocurrió un error al procesar la solicitud: {e}")
else:
    st.info("Por favor, ingresa tu API Key de Google Gemini para habilitar la aplicación.")
