import os
import streamlit as st
import pandas as pd
from pathlib import Path

# Configuración de la página
st.set_page_config(
    page_title="Auditoría y Limpieza de Datos - Caja Complementaria UNSE",
    page_icon="📊",
    layout="wide"
)

# Cabecera principal con componentes nativos (compatibilidad total con Light/Dark Theme)
st.title("📊 Auditoría y Limpieza de Datos")
st.subheader("Comparativa del dataset bruto frente al procesado y auditoría de calidad de datos para la Caja Complementaria (UNSE).")
st.write("---")

# CSS quirúrgico: delta inline al lado del valor
st.markdown("""
<style>
/* El wrapper interno de stMetric (hijo directo) usa flex-direction: column.
   Lo cambiamos a row con wrap para que el label ocupe toda la línea
   y el value + delta-wrapper queden juntos en la siguiente línea. */
div[data-testid="stMetric"] > div {
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: wrap !important;
    align-items: baseline !important;
    gap: 0 8px !important;
}
/* El label debe ocupar el 100% del ancho para forzar el wrap */
div[data-testid="stMetric"] > div > label[data-testid="stMetricLabel"] {
    flex-basis: 100% !important;
    width: 100% !important;
}
</style>
""", unsafe_allow_html=True)

# Ruta robusta para cargar el archivo
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / 'data' / 'processed' / 'dataset_hospedaje_features.csv'

@st.cache_data
def load_data(path):
    if path.exists():
        return pd.read_csv(path)
    else:
        # Fallback local relative path
        fallback_path = Path("data/processed/dataset_hospedaje_features.csv")
        if fallback_path.exists():
            return pd.read_csv(fallback_path)
        return None

df = load_data(DATA_PATH)

if df is not None:
    # 1. KPIs del Proceso de Calidad de Datos dentro de contenedores estéticos individuales
    original_rows = 119390
    processed_rows = len(df)
    filtered_rows = original_rows - processed_rows
    retention_rate = (processed_rows / original_rows) * 100
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        with st.container(border=True):
            st.metric("Registros Originales", f"{original_rows:,}".replace(",", "."), help="Total de reservas en la base de datos cruda")
    with col2:
        with st.container(border=True):
            st.metric("Registros Procesados", f"{processed_rows:,}".replace(",", "."), help="Total de reservas tras aplicar filtros de calidad y limpieza")
    with col3:
        with st.container(border=True):
            st.metric("Registros Excluidos", f"{filtered_rows:,}".replace(",", "."), f"-{filtered_rows/original_rows*100:.2f}%", delta_color="inverse", help="Registros inconsistentes o nulos depurados")
    with col4:
        with st.container(border=True):
            st.metric("Tasa de Retención", f"{retention_rate:.2f}%", help="Porcentaje de datos conservados para el análisis y modelado")
        
    st.write("")
    
    # 2. Información del proceso en formato Expanders/Cards
    st.subheader("🛠️ Proceso de Limpieza y Transformación en 6 Pasos")
    
    # Fila 1: Paso 1 y Paso 2
    col_r1a, col_r1b = st.columns(2)
    with col_r1a:
        with st.expander("🌍 Paso 1: Transformación Geográfica y Contextualización", expanded=True):
            st.markdown("""
            * **Problema**: Datos de origen con códigos de países y localizaciones extranjeras incompatibles con el contexto local de **Castelli 90 - Caja Complementaria (UNSE)**.
            * **Acción**: Imputación de provincias argentinas a partir de los orígenes de los huéspedes (con un foco prioritario en el Noroeste Argentino) y unificación de la variable geográfica para un análisis regional coherente.
            """)
    with col_r1b:
        with st.expander("📅 Paso 2: Transformación Temporal y Cálculo de Estadía", expanded=True):
            st.markdown("""
            * **Problema**: Columnas de fechas fragmentadas en año, mes y día de llegada, lo que dificultaba análisis temporales y estacionales continuos.
            * **Acción**: Unificación y conversión en objetos `datetime` (`fecha_checkin` y `fecha_checkout`) y cálculo exacto de la duración de la estadía (`noches_totales`).
            """)

    # Fila 2: Paso 3 y Paso 4
    col_r2a, col_r2b = st.columns(2)
    with col_r2a:
        with st.expander("👥 Paso 3: Categorización del Negocio (Contexto Gremial/UNSE)", expanded=True):
            st.markdown("""
            * **Problema**: Segmentos de mercado genéricos orientados a hotelería comercial tradicional.
            * **Acción**: Mapeo y re-categorización a perfiles de usuarios institucionales de la Caja Complementaria (UNSE): **Afiliado**, **Particular** y **Particular trabajo** (convenios gremiales y académicos).
            """)
    with col_r2b:
        with st.expander("💰 Paso 4: Ingeniería Financiera (Métricas Core)", expanded=True):
            st.markdown("""
            * **Problema**: Falta de variables explícitas que cuantifiquen el beneficio social otorgado y la ineficiencia económica de los no-shows.
            * **Acción**: Creación del `porcentaje_subsidio` (descuento real según categoría) y el `costo_oportunidad_perdido` (tarifa efectiva no cobrada debido a cancelaciones de reservas confirmadas).
            """)

    # Fila 3: Paso 5 y Paso 6
    col_r3a, col_r3b = st.columns(2)
    with col_r3a:
        with st.expander("🧹 Paso 5: Limpieza Demográfica y Control de Inconsistencias", expanded=True):
            st.markdown("""
            * **Problema**: Existencia de reservas imposibles o erróneas (ej. 0 adultos, menores e infantes simultáneamente) y outliers de precios inverosímiles.
            * **Acción**: Remoción de registros inconsistentes (716 filas excluidas), estandarización de estados a valores únicos (`checkout`, `canceled`) y acotación de tarifas base extremas.
            """)
    with col_r3b:
        with st.expander("📦 Paso 6: Extracción y Exportación Final", expanded=True):
            st.markdown("""
            * **Problema**: Formato final del archivo óptimo para la lectura veloz tanto en el entrenamiento de modelos de Machine Learning como en la renderización de la app.
            * **Acción**: Exportación del archivo procesado `dataset_hospedaje_features.csv` con 22 columnas estructuradas de tipos limpios.
            """)
            
    # Decisiones clave de limpieza en un st.info premium
    st.info("""
    💡 **Decisión de Negocio Crítica**: Se determinó que eliminar los registros con tarifa cero o con 0 ocupantes era vital para evitar sesgos en el cálculo del costo de oportunidad. Además, la tasa de retención del **99.42%** demuestra que la limpieza fue sumamente quirúrgica, garantizando que el modelado predictivo posterior posea un volumen de datos robusto y representativo.
    """)
    
    st.write("")
    st.subheader("🔍 Explorador de Registros Limpios")
    st.write("Filtra el dataset interactivo según el estado de la reserva y la categoría de huésped:")
    
    # Filtros interactivos para el explorador de datos
    filter_col1, filter_col2 = st.columns(2)
    with filter_col1:
        all_states = ["Todos"] + list(df['estado'].unique())
        selected_state = st.selectbox("Estado de la Reserva:", all_states)
    with filter_col2:
        all_categories = ["Todas"] + list(df['categoria_huesped'].unique())
        selected_category = st.selectbox("Categoría de Huésped:", all_categories)
        
    filtered_df = df.copy()
    if selected_state != "Todos":
        filtered_df = filtered_df[filtered_df['estado'] == selected_state]
    if selected_category != "Todas":
        filtered_df = filtered_df[filtered_df['categoria_huesped'] == selected_category]
        
    # Mostrar el dataframe filtrado
    st.write(f"Mostrando {len(filtered_df):,} registros filtrados:")
    st.dataframe(filtered_df.head(100), use_container_width=True)
    
else:
    st.error(f"⚠️ Error: No se pudo cargar el archivo procesado en la ruta `{DATA_PATH}`. Por favor, verifica que los archivos estén en su ubicación correcta en el repositorio.")
