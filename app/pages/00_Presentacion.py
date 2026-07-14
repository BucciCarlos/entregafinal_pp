import streamlit as st
from pathlib import Path

# Configuración de la página
st.set_page_config(
    page_title="Presentación y Defensa de Proyecto - Caja UNSE",
    page_icon="📊",
    layout="wide"
)

# Estilos CSS personalizados para simetría perfecta de las cajas
st.markdown(
    """
    <style>
        /* Forzar altura mínima idéntica y distribución flexbox en contenedores con borde */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            min-height: 280px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        /* Alinear botones en la parte inferior del contenedor */
        div[data-testid="stVerticalBlockBorderWrapper"] > div {
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Título principal de la defensa
st.title("📊 Defensa de Proyecto: Sostenibilidad Financiera y Reservas")
st.subheader("Acceso a la presentación interactiva del proyecto y material de respaldo para el tribunal académico.")
st.markdown("---")

# Organización en columnas de la misma altura con st.container(border=True)
col_left, col_right = st.columns(2)

with col_left:
    with st.container(border=True):
        st.markdown("### 🚀 Presentación Interactiva (Gamma)")
        st.markdown("""
        Accede a las diapositivas dinámicas de la defensa del proyecto alojadas en la plataforma **Gamma**. 
        Esta versión interactiva contiene transiciones fluidas y es ideal para la exposición en vivo ante el tribunal académico.
        """)
        st.link_button(
            "Abrir Presentación Interactiva 🔗", 
            url="https://gamma.app/docs/Sostenibilidad-Financiera-y-Optimizacion-de-Reservas-edbsm69r7x7d7i1?mode=present#card-fz8bxh3kqdzlsfi",
            use_container_width=True
        )

with col_right:
    with st.container(border=True):
        st.markdown("### 📥 Material de Respaldo (PDF)")
        st.markdown("""
        Descarga la copia estática local de la presentación en formato PDF. 
        Este archivo sirve como contingencia (*Hard Backup*) garantizando el acceso a las diapositivas en caso de fallas de conectividad.
        """)
        
        # Resolución de path dinámico para el archivo PDF
        current_dir = Path(__file__).resolve().parent
        pdf_path = current_dir.parent / "assets" / "PresentacionPP2.pdf"

        try:
            with open(pdf_path, "rb") as f:
                pdf_data = f.read()
            
            st.download_button(
                label="Descargar PDF de Respaldo 📥",
                data=pdf_data,
                file_name="Presentacion_Caja_Complementaria_UNSE.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        except FileNotFoundError:
            st.error("⚠️ El archivo de presentación de respaldo no se encuentra disponible localmente.")
