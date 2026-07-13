import streamlit as st

st.set_page_config(
    page_title="Dataset - Exploración de Datos",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Exploración del Dataset")
st.write("---")

st.markdown("""
En esta sección se presenta la estructura de los datos utilizados en el proyecto. 
Puedes cargar tus archivos en formato CSV o Excel para previsualizarlos aquí.
""")

uploaded_file = st.file_uploader("Cargar archivo de datos (CSV o Excel)", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        import pandas as pd
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        st.success("¡Archivo cargado con éxito!")
        
        st.subheader("Muestra de Datos (Primeras 5 filas)")
        st.dataframe(df.head())
        
        st.subheader("Información del Dataset")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total de Filas", df.shape[0])
        with col2:
            st.metric("Total de Columnas", df.shape[1])
            
        st.subheader("Estadísticas Descriptivas")
        st.dataframe(df.describe(include='all'))
    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")
else:
    st.info("Sube un archivo de datos en la barra superior para explorar sus propiedades.")
