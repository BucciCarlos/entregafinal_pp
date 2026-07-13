import streamlit as st
import pandas as pd
from pathlib import Path

# 1. Configuración de la página
st.set_page_config(
    page_title="Caja Complementaria - UNSE",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo personalizado para un diseño premium
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700&display=swap');
    
    .main-title {
        font-family: 'Outfit', sans-serif;
        color: #2E5B88;
        font-size: 2.8rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        font-family: 'Inter', sans-serif;
        color: #5C768D;
        font-size: 1.3rem;
        margin-bottom: 2rem;
    }
    .custom-card {
        background-color: #f8fafc;
        border-radius: 12px;
        padding: 24px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 1.5rem;
    }
    .badge-prod {
        background-color: #10b981;
        color: white;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        font-family: 'Inter', sans-serif;
    }
    .slide-container {
        background: white;
        border-radius: 16px;
        padding: 40px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05);
        border: 1px solid #e2e8f0;
        margin-top: 20px;
        min-height: 350px;
    }
    .slide-title {
        font-family: 'Outfit', sans-serif;
        color: #2E5B88;
        font-size: 2rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
    }
    .slide-desc {
        font-family: 'Inter', sans-serif;
        font-size: 1.2rem;
        line-height: 1.8;
        color: #334155;
    }
    </style>
""", unsafe_allow_html=True)

# Inicializar st.session_state para la presentación
if 'in_presentation' not in st.session_state:
    st.session_state.in_presentation = False
if 'slide_index' not in st.session_state:
    st.session_state.slide_index = 0

# Definición de diapositivas
slides = [
    {
        "titulo": "🎯 Problema de Negocio y Línea Base",
        "descripcion": "El albergue de la UNSE opera históricamente con una **tasa de cancelación del 37.24%**, generando ineficiencias críticas de ocupación. Cada habitación reservada que resulta en cancelación bloquea plazas para estudiantes vulnerables y representa ingresos perdidos directos para la sostenibilidad del albergue."
    },
    {
        "titulo": "🛠️ Ingeniería de Características (Feature Engineering)",
        "descripcion": "Derivamos tres métricas core para modelar la sostenibilidad financiera: **Costo de Oportunidad Perdido** (cuantificación monetaria del no-show), **Porcentaje de Subsidio** (descuento real aplicado por reserva) y **Categoría de Estadía** (clasificación cualitativa de la ocupación en Corta, Mediana y Larga)."
    },
    {
        "titulo": "📊 Resultados del Modelado Predictivo",
        "descripcion": "Desarrollamos un modelo `RandomForestClassifier` optimizado mediante Validación Cruzada Estratificada y ajuste aleatorio de hiperparámetros. El modelo logró incrementar la exactitud al **74%** y la precisión del modelo en cancelaciones de un 50% a un **65%**."
    },
    {
        "titulo": "🏨 Segmentación de Riesgo y Reglas de Negocio",
        "descripcion": "Clasificamos las reservas futuras en tres segmentos accionables: **Riesgo Bajo** (check-out exitoso del 83%), **Riesgo Medio** e **Riesgo Alto** (donde el **76%** cancela efectivamente). Esto permite aplicar depósitos de pre-pago u overbooking dinámico en plazas con alto riesgo."
    },
    {
        "titulo": "🚀 Plan de Acción e Implementación",
        "descripcion": "Recomendamos implementar **fricción selectiva**: flujo directo de check-in sin fricciones para reservas de Riesgo Bajo, recordatorio automático proactivo para Riesgo Medio, y cobros de seña por adelantado o reconfirmación obligatoria para Riesgo Alto."
    }
]

# Cabecera principal
col_title, col_badge = st.columns([4, 1.2])
with col_title:
    st.markdown('<div class="main-title">🏨 Caja Complementaria - UNSE</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Sostenibilidad Financiera y Costo de Oportunidad por Cancelaciones</div>', unsafe_allow_html=True)


# Comprobar si estamos en modo presentación
if st.session_state.in_presentation:
    # Renderizar Slide actual
    current_slide = slides[st.session_state.slide_index]
    
    st.markdown(f"### Presentación Ejecutiva (Diapositiva {st.session_state.slide_index + 1} de {len(slides)})")
    
    st.markdown('<div class="slide-container">', unsafe_allow_html=True)
    st.markdown(f'<div class="slide-title">{current_slide["titulo"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="slide-desc">{current_slide["descripcion"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Navegación del slideshow
    st.write("")
    col_prev, col_exit, col_next = st.columns([1, 2, 1])
    
    with col_prev:
        if st.button("⬅️ Anterior", use_container_width=True):
            if st.session_state.slide_index > 0:
                st.session_state.slide_index -= 1
                st.rerun()
                
    with col_exit:
        if st.button("Salir de la Presentación", use_container_width=True, type="secondary"):
            st.session_state.in_presentation = False
            st.session_state.slide_index = 0
            st.rerun()
            
    with col_next:
        if st.button("Siguiente ➡️", use_container_width=True, type="primary"):
            if st.session_state.slide_index < len(slides) - 1:
                st.session_state.slide_index += 1
                st.rerun()
            else:
                # Llegó al final, salimos de la presentación
                st.session_state.in_presentation = False
                st.session_state.slide_index = 0
                st.toast("¡Presentación finalizada con éxito! 🚀")
                st.rerun()

else:
    # Renderizar la Página de Inicio por defecto
    st.write("")
    st.markdown("""
        <div class="custom-card">
            <h3 style="font-family: 'Outfit', sans-serif; color: #2E5B88; margin-top:0;">📖 Resumen del Proyecto</h3>
            <p style="font-family: 'Inter', sans-serif; font-size: 1.05rem; color: #334155;">
                Este proyecto audita y modela la sostenibilidad económica de Casteñño 90 de la <strong>UNSE</strong>. 
                A través de un flujo analítico estructurado en seis fases, investigamos las ineficiencias de las cancelaciones de reservas, 
                mapeamos el impacto de los subsidios sociales y entrenamos un modelo de Inteligencia Artificial para mitigar pérdidas económicas.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Botón para iniciar la presentación (posicionado debajo del resumen)
    st.write("")
    if st.button("🚀 Iniciar Presentación Ejecutiva", use_container_width=True, type="primary"):
        st.session_state.in_presentation = True
        st.session_state.slide_index = 0
        st.rerun()
        
    st.write("")
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown('<div class="custom-card" style="min-height: 250px;">', unsafe_allow_html=True)
        st.markdown("### 👥 Integrantes del Proyecto")
        st.markdown("""
            *   **Bucci, Carlos Matias**
            *   **Carabajal, Elba Julieta** 
            *   **Segovia Albarado, Nicolas Daniel** 
        """)
        st.markdown('</div>', unsafe_allow_html=True)
            
    with col_right:
        st.markdown('<div class="custom-card" style="min-height: 250px;">', unsafe_allow_html=True)
        st.markdown("### 🔗 Enlaces del Proyecto")
        st.markdown("""
            *   [💻 Repositorio en GitHub](https://github.com/BucciCarlos/entregafinal_pp)
            *   [📊 Informe Ejecutivo en HTML](https://entregafinalpp-grupo1.streamlit.app/)
        """)
        
        # Enlaces en forma de botones
        st.write("")
        st.link_button("Ir al Repositorio de GitHub", "https://github.com/BucciCarlos/entregafinal_pp", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
