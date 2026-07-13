import streamlit as st

st.set_page_config(
    page_title="Predicción - Machine Learning",
    page_icon="🔮",
    layout="wide"
)

st.title("🔮 Modelo Predictivo")
st.write("---")

st.markdown("""
Utiliza esta interfaz interactiva para realizar predicciones en tiempo real utilizando el modelo de Machine Learning entrenado.
""")

st.subheader("Ingreso de Parámetros")
st.write("Configura las características de entrada para obtener la predicción:")

# Aquí se pueden agregar inputs interactivos como st.slider, st.selectbox, etc.
# Ejemplo:
# feature_1 = st.slider("Característica 1", 0.0, 100.0, 50.0)

if st.button("Realizar Predicción"):
    st.info("Predicción simulada. Carga el modelo entrenado (.pkl) en tu backend para realizar inferencias reales.")
