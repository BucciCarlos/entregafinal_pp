import streamlit as st
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

# Explicación y botón de enlace externo a Gamma
st.markdown("Haz clic en el botón inferior para abrir la presentación interactiva en una nueva pestaña a pantalla completa.")

# Envolver el botón en columnas para centrarlo y destacarlo en la UI
col_left, col_center, col_right = st.columns([1, 2, 1])
with col_center:
    st.link_button(
        "🚀 Abrir Presentación Interactiva (Gamma)", 
        url="https://gamma.app/docs/Sostenibilidad-Financiera-y-Optimizacion-de-Reservas-edbsm69r7x7d7i1?mode=present#card-fz8bxh3kqdzlsfi",
        use_container_width=True
    )

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
