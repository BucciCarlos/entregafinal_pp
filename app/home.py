import streamlit as st

# 1. Configuración de la página (Debe ser la primera instrucción de Streamlit)
st.set_page_config(
    page_title="Albergue UNSE - Sostenibilidad Financiera",
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
    .sidebar-msg {
        background-color: #eff6ff;
        color: #1e40af;
        border: 1px solid #bfdbfe;
        border-radius: 12px;
        padding: 16px;
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        font-weight: 500;
        margin-bottom: 2rem;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Cabecera principal
col_title, col_badge = st.columns([4, 1.2])
with col_title:
    st.markdown('<div class="main-title">🏨 Albergue Institucional UNSE</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Sostenibilidad Financiera y Costo de Oportunidad por Cancelaciones</div>', unsafe_allow_html=True)

with col_badge:
    st.markdown('<div style="text-align: right; padding-top: 15px;"><span class="badge-prod">✓ Ready for Production</span></div>', unsafe_allow_html=True)

# Mensaje para guiar al usuario a la barra lateral (Navegación nativa)
st.markdown('<div class="sidebar-msg">👈 Utilice la barra lateral para navegar por las distintas fases del análisis y predicción.</div>', unsafe_allow_html=True)

# Renderizar el Resumen del Proyecto
st.markdown("""
    <div class="custom-card">
        <h3 style="font-family: 'Outfit', sans-serif; color: #2E5B88; margin-top:0;">📖 Resumen Ejecutivo</h3>
        <p style="font-family: 'Inter', sans-serif; font-size: 1.1rem; color: #334155; line-height: 1.7;">
            Este proyecto audita, visualiza y modela la sostenibilidad económica del albergue de la <strong>UNSE</strong>. 
            A través de un flujo analítico estructurado, investigamos las ineficiencias de las cancelaciones de reservas (tasa histórica de no-show del 37.24%), 
            mapeamos el impacto de los subsidios sociales otorgados y entrenamos un modelo de Inteligencia Artificial (Random Forest Classifier con 82% de precisión para el segmento de riesgo alto) para mitigar pérdidas económicas.
        </p>
    </div>
""", unsafe_allow_html=True)

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
        *   [📊 Aplicación en Streamlit Cloud](https://entregafinalpp-grupo1.streamlit.app/)
    """)
    
    st.write("")
    st.link_button("Ir al Repositorio de GitHub", "https://github.com/BucciCarlos/entregafinal_pp", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
