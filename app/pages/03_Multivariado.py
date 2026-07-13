import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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
st.caption("Exploración de relaciones bivariadas y multivariadas para comprender el comportamiento de los subsidios y las cancelaciones.")
st.write("---")

if df is not None:
    # Definir pestañas principales
    tab_bivariado, tab_multivariado = st.tabs([
        "🔗 Análisis Bivariado (Canales y Subsidios)", 
        "🕸️ Análisis Multivariado (Correlaciones)"
    ])
    
    # Configuración de estilo global para gráficos de Matplotlib
    plt.rcParams['figure.facecolor'] = 'none'
    plt.rcParams['axes.facecolor'] = 'none'
    sns.set_theme(style="whitegrid")
    
    # --- PESTAÑA 1: ANÁLISIS BIVARIADO ---
    with tab_bivariado:
        st.subheader("1. Tasa de Cancelación por Canal de Origen de la Reserva")
        col1, col2 = st.columns([3, 2])
        
        with col1:
            # Calcular tasas de cancelación por origen
            origen_cross = pd.crosstab(df['origen'], df['estado'], normalize='index') * 100
            
            fig1, ax1 = plt.subplots(figsize=(8, 4.5))
            fig1.patch.set_alpha(0.0)
            ax1.patch.set_alpha(0.0)
            
            # Graficar barra apilada horizontal
            origen_cross.plot(
                kind='barh', 
                stacked=True, 
                color=['#EF4444', '#10B981'], # Rojo para cancelada, Verde para checkout
                ax=ax1
            )
            
            # Agregar textos de porcentajes dentro de las barras
            for n in range(len(origen_cross)):
                val_canceled = origen_cross.iloc[n, 0]
                val_checkout = origen_cross.iloc[n, 1]
                # Anotación para cancelación (Rojo)
                ax1.text(val_canceled / 2, n, f"{val_canceled:.1f}%", va='center', ha='center', color='white', fontweight='bold')
                # Anotación para checkout (Verde)
                ax1.text(val_canceled + (val_checkout / 2), n, f"{val_checkout:.1f}%", va='center', ha='center', color='white', fontweight='bold')
                
            ax1.set_xlabel("Porcentaje (%)", fontsize=11)
            ax1.set_ylabel("Canal de Origen", fontsize=11)
            ax1.legend(["Cancelada", "Checkout"], frameon=True, loc='lower left')
            ax1.spines['top'].set_visible(False)
            ax1.spines['right'].set_visible(False)
            plt.tight_layout()
            st.pyplot(fig1, clear_figure=True)
            plt.close(fig1)
            
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
        col3, col4 = st.columns([3, 2])
        
        with col3:
            # Gráfico de caja (Boxplot) para comparar el monto subsidiado total por categoría
            fig2, ax2 = plt.subplots(figsize=(8, 5))
            fig2.patch.set_alpha(0.0)
            ax2.patch.set_alpha(0.0)
            
            # Ordenar las categorías por el promedio del monto subsidiado
            order = df.groupby('categoria_huesped')['monto_subsidiado_total'].median().sort_values(ascending=False).index
            
            sns.boxplot(
                data=df, 
                y='categoria_huesped', 
                x='monto_subsidiado_total', 
                order=order,
                palette="Blues_r",
                ax=ax2,
                orient='h',
                hue='categoria_huesped',
                legend=False
            )
            
            ax2.set_xlabel("Monto Subsidiado Total por Reserva ($)", fontsize=11)
            ax2.set_ylabel("Categoría del Huésped", fontsize=11)
            ax2.spines['top'].set_visible(False)
            ax2.spines['right'].set_visible(False)
            plt.tight_layout()
            st.pyplot(fig2, clear_figure=True)
            plt.close(fig2)
            
        with col4:
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
            
            # Graficar Heatmap
            fig3, ax3 = plt.subplots(figsize=(8, 6.5))
            fig3.patch.set_alpha(0.0)
            ax3.patch.set_alpha(0.0)
            
            # Usar RdBu_r para visualizar claramente correlaciones positivas (Rojo) y negativas (Azul)
            sns.heatmap(
                correlation_matrix, 
                annot=True, 
                cmap="RdBu_r", 
                vmin=-1, 
                vmax=1, 
                fmt=".2f",
                ax=ax3,
                square=True,
                cbar_kws={"shrink": 0.8}
            )
            
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            st.pyplot(fig3, clear_figure=True)
            plt.close(fig3)
            
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
