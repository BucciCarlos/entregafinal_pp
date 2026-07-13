import streamlit as st

st.set_page_config(
    page_title="EDA - Análisis Exploratorio de Datos",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Análisis Exploratorio de Datos (EDA)")
st.write("---")

st.markdown("""
Visualización interactiva para el análisis de variables. 
Selecciona el tipo de análisis que deseas explorar:
""")

tab1, tab2, tab3 = st.tabs(["Univariado", "Bivariado", "Multivariado"])

with tab1:
    st.header("Análisis Univariado")
    st.write("Visualiza la distribución de frecuencias y estadísticas individuales de cada variable.")

with tab2:
    st.header("Análisis Bivariado")
    st.write("Explora las relaciones, dispersión y comportamiento conjunto entre dos variables.")

with tab3:
    st.header("Análisis Multivariado")
    st.write("Visualiza matrices de correlación, clustering y proyecciones de reducción de dimensionalidad (PCA).")
