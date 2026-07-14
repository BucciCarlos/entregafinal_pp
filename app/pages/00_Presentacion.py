import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

# Configuración de la página
st.set_page_config(
    page_title="Presentación y Defensa de Proyecto - Caja UNSE",
    page_icon="📊",
    layout="wide"
)

# Título formal de la defensa
st.title("Defensa de Proyecto: Sostenibilidad Financiera y Optimización de Reservas")
st.markdown("---")

# Integración del iframe de Gamma
iframe_code = (
    '<iframe src="https://gamma.app/embed/edbsm69r7x7d7i1" '
    'style="width: 100%; height: 700px; border: none; border-radius: 8px;" '
    'allow="fullscreen" title="Sostenibilidad Financiera y Optimizacion de Reservas"></iframe>'
)

components.html(iframe_code, height=700)

# Botón de Respaldo Local (Hard Backup)
st.divider()
st.subheader("Material de Respaldo")

# Resolución de path dinámico para el archivo PDF
current_dir = Path(__file__).resolve().parent
pdf_path = current_dir.parent / "assets" / "PresentacionPP2.pdf"

try:
    with open(pdf_path, "rb") as f:
        pdf_data = f.read()
    
    st.download_button(
        label="📥 Descargar Presentación de Respaldo (PDF)",
        data=pdf_data,
        file_name="Presentacion_Caja_Complementaria_UNSE.pdf",
        mime="application/pdf"
    )
except FileNotFoundError:
    st.error("⚠️ El archivo de presentación de respaldo no se encuentra disponible localmente.")
