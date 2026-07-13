import streamlit as st

# 1. Configuración de la página (Debe ser la primera instrucción de Streamlit)
st.set_page_config(
    page_title="Caja Complementaria UNSE - Sostenibilidad Financiera",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cabecera principal con componentes nativos (compatibilidad total con Light/Dark Theme)
st.title("🏨 Castelli 90 - Caja Complementaria (UNSE)")
st.subheader("Sostenibilidad Financiera y Costo de Oportunidad por Cancelaciones")

# Mensaje elegante de navegación lateral
st.info("👈 Utilice el menú lateral izquierdo para navegar por las distintas fases del análisis de datos y el simulador predictivo.")

st.divider()

# Resumen Ejecutivo en un contenedor con borde
with st.container(border=True):
    st.markdown("### 📖 Resumen Ejecutivo")
    st.markdown("""
    Este proyecto audita, visualiza y modela la sostenibilidad económica de **Castelli 90 - Caja Complementaria (UNSE)**. 
    A través de un flujo analítico estructurado, investigamos las ineficiencias de las cancelaciones de reservas (tasa histórica de no-show del **37.24%**), 
    mapeamos el impacto de los subsidios sociales otorgados y entrenamos un modelo de Inteligencia Artificial (*Random Forest Classifier* con **82%** de precisión para el segmento de riesgo alto) para mitigar pérdidas económicas.
    """)

st.write("")

# Organización del pie de página en columnas
col_left, col_right = st.columns(2)

with col_left:
    with st.container(border=True):
        st.markdown("### 👥 Integrantes del Proyecto")
        st.markdown("""
        *   **Bucci, Carlos Matias**
        *   **Carabajal, Elba Julieta** 
        *   **Segovia Albarado, Nicolas Daniel** 
        """)
        
with col_right:
    with st.container(border=True):
        st.markdown("### 🔗 Enlaces del Proyecto")
        st.markdown("""
        *   [💻 Repositorio en GitHub](https://github.com/BucciCarlos/entregafinal_pp)
        *   [📊 Aplicación en Streamlit Cloud](https://entregafinalpp-grupo1.streamlit.app/)
        """)
        st.write("")
        st.link_button("Ir al Repositorio de GitHub 🚀", "https://github.com/BucciCarlos/entregafinal_pp", use_container_width=True)
