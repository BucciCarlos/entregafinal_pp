import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from pathlib import Path

# Configuración de la página
st.set_page_config(
    page_title="Análisis Bivariado y Multivariado - Caja Complementaria UNSE",
    page_icon="📊",
    layout="wide"
)

# Carga de datos robusta
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / 'data' / 'processed' / 'dataset_hospedaje_features.csv'

@st.cache_data
def load_data(path):
    if path.exists():
        return pd.read_csv(path)
    else:
        fallback_path = Path("data/processed/dataset_hospedaje_features.csv")
        if fallback_path.exists():
            return pd.read_csv(fallback_path)
        return None

df = load_data(DATA_PATH)

# Cabecera principal con componentes nativos (compatibilidad total con Light/Dark Theme)
st.title("📊 Análisis Cruzado e Interacciones")
st.subheader("Exploración de relaciones bivariadas y multivariadas para comprender el comportamiento de los subsidios y las cancelaciones.")
st.write("---")

if df is not None:
    # Definir pestañas principales
    tab_bivariado, tab_multivariado = st.tabs([
        "🔗 Análisis Bivariado (Canales y Subsidios)", 
        "🕸️ Análisis Multivariado (Correlaciones)"
    ])
    
    # Configuración de estilo global para gráficos
    pass
    
    # --- PESTAÑA 1: ANÁLISIS BIVARIADO ---
    with tab_bivariado:
        st.subheader("1. Tasa de Cancelación por Canal de Origen de la Reserva")
        col1, col2 = st.columns([3, 2])
        
        with col1:
            # Calcular tasas de cancelación por origen
            origen_cross = pd.crosstab(df['origen'], df['estado'], normalize='index') * 100
            df_origen = origen_cross.reset_index()
            df_origen_melt = df_origen.melt(
                id_vars='origen', 
                value_vars=['cancelada', 'checkout'], 
                var_name='Estado', 
                value_name='Porcentaje'
            )
            df_origen_melt['Estado'] = df_origen_melt['Estado'].map({'checkout': 'Checkout', 'cancelada': 'Cancelada'})
            df_origen_melt['Texto'] = df_origen_melt['Porcentaje'].apply(lambda x: f"{x:.1f}%")
            
            fig1 = px.bar(
                df_origen_melt,
                y='origen',
                x='Porcentaje',
                color='Estado',
                color_discrete_map={'Checkout': '#10B981', 'Cancelada': '#EF4444'},
                orientation='h',
                text='Texto',
                labels={'origen': 'Canal de Origen', 'Porcentaje': 'Porcentaje (%)'}
            )
            
            fig1.update_traces(
                textposition='inside',
                textfont=dict(color='white', weight='bold')
            )
            fig1.update_layout(
                barmode='stack',
                height=350,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                ),
                margin=dict(l=10, r=10, t=30, b=10)
            )
            fig1.update_layout(font=dict(size=15))
            fig1.update_xaxes(title_font=dict(size=17), tickfont=dict(size=14))
            fig1.update_yaxes(title_font=dict(size=17), tickfont=dict(size=14))
            
            st.plotly_chart(fig1, width="stretch", theme="streamlit")
            
        with col2:
            with st.container(border=True):
                st.write("#### 📌 Comportamiento de los Canales de Origen")
                st.markdown("""
                * **Fuga en Gestión Externa**: La tasa de cancelación en reservas tramitadas vía **Gestión Externa** alcanza el **38.8%**, en comparación con el **25.7%** en las de **Gestión Interna** (tramitadas directamente en la oficina del gremio o UNSE).
                * **Compromiso Diferenciado**: Las reservas directas (internas) tienen un compromiso sustancialmente mayor del huésped. Las externas, al no requerir interacción directa presencial al momento de reservar, facilitan el comportamiento no-show.
                * **Medida Recomendada**: Implementar el simulador de riesgo y aplicar fricción de reconfirmación obligatoria específicamente sobre el canal de *Gestión Externa*.
                """)
            
        st.divider()
        
        st.subheader("2. Distribución del Monto Subsidiado según Categoría de Huésped")
        # Ordenar las categorías por la mediana del monto subsidiado
        order = list(df.groupby('categoria_huesped')['monto_subsidiado_total'].median().sort_values(ascending=False).index)
        
        fig2 = px.box(
            df,
            y='categoria_huesped',
            x='monto_subsidiado_total',
            category_orders={'categoria_huesped': order},
            color='categoria_huesped',
            color_discrete_sequence=px.colors.sequential.Blues_r,
            orientation='h',
            labels={
                'categoria_huesped': 'Categoría del Huésped',
                'monto_subsidiado_total': 'Monto Subsidiado Total por Reserva ($)'
            }
        )
        fig2.update_layout(
            showlegend=False,
            height=500,
            margin=dict(l=10, r=10, t=10, b=10)
        )
        fig2.update_layout(font=dict(size=15))
        fig2.update_xaxes(title_font=dict(size=17), tickfont=dict(size=14))
        fig2.update_yaxes(title_font=dict(size=17), tickfont=dict(size=14))
        st.plotly_chart(fig2, width="stretch", theme="streamlit")
        
        with st.container(border=True):
            st.write("#### 📌 Distribución y Carga de Subsidios Sociales")
            st.markdown("""
            * **Afiliados y Actividad Académica**: Las categorías de **Afiliado** y **Actividad Académica UNSE** presentan los montos de subsidio total más altos por reserva (indicados por cajas desplazadas a la derecha y con medianas elevadas). Esto es coherente con el rol social de la institución.
            * **Impacto de la Sobreocupación**: Dado que estas categorías prioritarias reciben los mayores subsidios, cualquier cancelación de estas reservas implica bloquear recursos sociales de alto valor que podrían haber beneficiado a otros afiliados necesitados.
            * **Grupos Familiares Grandes**: El análisis del notebook demuestra que cuando estas reservas involucran grupos familiares numerosos (mayor número de noches y personas), el subsidio acumulado se dispara, lo que eleva significativamente el costo de oportunidad perdido si la reserva se cancela.
            """)

    # --- PESTAÑA 2: ANÁLISIS MULTIVARIADO ---
    with tab_multivariado:
        st.subheader("Matriz de Correlación de Variables Financieras y de Ocupación")
        col5, col6 = st.columns([3, 2])
        
        with col5:
            # Crear columna numérica indicadora de cancelación para incluirla en la correlación
            df_corr = df.copy()
            df_corr['cancelada_num'] = (df_corr['estado'] == 'cancelada').astype(int)
            
            # Seleccionar variables clave
            cols_to_correlate = [
                'tarifa_base', 
                'tarifa_efectiva', 
                'noches_totales', 
                'monto_subsidiado_total', 
                'porcentaje_subsidio',
                'costo_oportunidad_perdido',
                'cant_adultos',
                'cancelada_num'
            ]
            
            # Renombrar columnas para el gráfico
            rename_dict = {
                'tarifa_base': 'Tarifa Base',
                'tarifa_efectiva': 'Tarifa Efectiva',
                'noches_totales': 'Duración Estadía',
                'monto_subsidiado_total': 'Monto Subsidiado',
                'porcentaje_subsidio': '% Subsidio',
                'costo_oportunidad_perdido': 'Costo Oportunidad',
                'cant_adultos': 'Cant. Adultos',
                'cancelada_num': '¿Cancelada? (1/0)'
            }
            
            correlation_matrix = df_corr[cols_to_correlate].rename(columns=rename_dict).corr()
            
            # Graficar Heatmap con Plotly
            fig3 = px.imshow(
                correlation_matrix,
                text_auto=".2f",
                color_continuous_scale="RdBu_r",
                zmin=-1,
                zmax=1,
                labels=dict(color="Correlación")
            )
            fig3.update_layout(
                height=500,
                margin=dict(l=10, r=10, t=10, b=10)
            )
            fig3.update_layout(font=dict(size=15))
            fig3.update_xaxes(title_font=dict(size=17), tickfont=dict(size=14))
            fig3.update_yaxes(title_font=dict(size=17), tickfont=dict(size=14))
            st.plotly_chart(fig3, width="stretch", theme="streamlit")
            
            with st.expander("💡 ¿Cómo leer esta matriz?"):
                st.markdown("""
                La **Matriz de Correlación** mide la fuerza y dirección de la relación lineal entre pares de variables numéricas, oscilando en un rango de **-1 a 1**:
                *   **1 (Azul oscuro): Correlación positiva perfecta.** Cuando una variable aumenta, la otra aumenta en la misma proporción.
                *   **-1 (Rojo oscuro): Correlación negativa perfecta.** Cuando una variable aumenta, la otra disminuye en la misma proporción.
                *   **0 (Blanco): Correlación nula.** No existe una relación lineal directa entre las variables.

                **🔍 Hallazgo Principal del Análisis:**
                El **Costo de Oportunidad** presenta una fortísima correlación positiva con la **Duración de la Estadía (Duración Estadía)** y la **Tarifa Base**. Esto demuestra empíricamente que la mayor pérdida económica potencial para la Caja no surge de las reservas de bajo costo o de corta duración, sino de las **estadías prolongadas con tarifas comerciales más altas**. Al cancelarse en el último momento (no-show), estas reservas bloquean un inventario de cama de alta prioridad y costo que no puede ser reasignado a tiempo.
                """)
            
        with col6:
            with st.container(border=True):
                st.write("#### 📌 Análisis de Interacciones Multivariadas")
                st.markdown("""
                * **Correlación Directa de Pérdidas**: El **Costo de Oportunidad** presenta una fortísima correlación positiva con la **Tarifa Base** y las **Noches Totales (Duración de Estadía)**, lo que indica que las cancelaciones de estadías largas a tarifas estándar de mercado representan la mayor fuga de ingresos potenciales.
                * **Interacción de Ocupantes y Cancelaciones**: La variable `¿Cancelada?` muestra correlaciones positivas con la cantidad de adultos y el origen externo de la reserva. Las reservas de mayor tamaño grupal tramitadas por internet tienden a sufrir mayores tasas de cancelación.
                * **Impacto del Porcentaje de Subsidio**: Se observa que un mayor `% de Subsidio` tiene una correlación negativa moderada con la tarifa efectiva (a mayor subsidio, menor precio cobrado), pero influye directamente en el incremento del monto subsidiado final por reserva.
                """)

else:
    st.error(f"⚠️ Error: No se pudo cargar el archivo procesado en la ruta `{DATA_PATH}`. Por favor, verifica que los archivos estén en su ubicación correcta en el repositorio.")
