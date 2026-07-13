import streamlit as st

st.set_page_config(
    page_title="Minería de Datos & ML - Home",
    page_icon="🤖",
    layout="wide"
)

st.title("Proyecto de Minería de Datos & Machine Learning")
st.write("---")

st.markdown("""
### ¡Bienvenido a la aplicación interactiva del proyecto!

Esta aplicación ha sido estructurada para complementar los cuadernos de análisis y modelado predictivo, permitiendo explorar los resultados de forma visual y dinámica.

#### Secciones Disponibles:

1. **📊 Dataset**: Vista preliminar de los datos y estadísticas descriptivas básicas.
2. **📈 EDA (Análisis Exploratorio)**: Visualizaciones univariadas, bivariadas y multivariadas.
3. **🔮 Predicción**: Interfaz para realizar predicciones interactivas utilizando el modelo entrenado.
4. **💡 Conclusiones**: Resumen de los hallazgos principales del proyecto.

---
*Navega a través de las diferentes páginas utilizando la barra lateral.*
""")
