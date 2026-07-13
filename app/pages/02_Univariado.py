import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Configuración de la página
st.set_page_config(
    page_title="Análisis Univariado y Línea Base - Caja Complementaria UNSE",
    page_icon="📈",
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
st.title("📈 Análisis Univariado y Línea Base")
st.caption("Análisis del comportamiento individual de variables críticas y cuantificación de la problemática de cancelaciones.")
st.write("---")

if df is not None:
    # 1. Bloque de Línea Base Crítica (KPI Destacado)
    total_res = len(df)
    total_canceled = len(df[df['estado'] == 'cancelada'])
    cancel_rate = (total_canceled / total_res) * 100
    
    with st.container(border=True):
        st.error(f"🚨 **Línea Base Crítica Operativa: {cancel_rate:.2f}%**")
        st.markdown(f"""
        De las **{total_res:,}** reservas procesadas en el histórico de Castelli 90, 
        **{total_canceled:,}** terminaron en cancelación efectiva (no-show). 
        Esta tasa es más del doble de la media promedio de la industria hotelera (15%-19%), 
        generando graves problemas de sobreocupación fantasma y una severa ineficiencia presupuestaria.
        """.replace(",", "."))
        
    # 2. Selector de Variable en la barra lateral para dejar limpio el lienzo principal
    with st.sidebar:
        st.subheader("🔍 Filtros y Controles")
        option = st.selectbox(
            "Selecciona la variable a analizar:",
            [
                "📊 Distribución de Estados (Checkout vs. Cancelada)",
                "💸 Análisis de Tarifas (Base vs. Efectiva con subsidio)",
                "👥 Demografía (Categorías de Huéspedes e Ingesta)"
            ]
        )
    
    # Configuración de estilo global para gráficos de Matplotlib
    plt.rcParams['figure.facecolor'] = 'none'
    plt.rcParams['axes.facecolor'] = 'none'
    sns.set_theme(style="whitegrid")
    
    # 3. Lógica de renderizado según la selección
    if "Distribución de Estados" in option:
        col_left, col_right = st.columns([3, 2])
        
        with col_left:
            st.subheader("Frecuencia y Proporción de Estados de Reserva")
            
            # Gráfico de barras de checkout vs cancelada
            fig, ax = plt.subplots(figsize=(8, 5))
            fig.patch.set_alpha(0.0)
            ax.patch.set_alpha(0.0)
            
            colors = ['#10B981', '#EF4444'] # Verde para checkout, Rojo para cancelada
            state_counts = df['estado'].value_counts()
            
            sns.barplot(
                x=state_counts.index.map({'checkout': 'Checkout (Éxito)', 'cancelada': 'Cancelada (No-Show)'}), 
                y=state_counts.values, 
                palette=colors,
                ax=ax,
                hue=state_counts.index,
                legend=False
            )
            
            # Anotaciones de porcentajes en las barras (omitiendo color hardcodeado para que use el del tema)
            for i, val in enumerate(state_counts.values):
                pct = (val / total_res) * 100
                ax.text(i, val + 1500, f"{val:,} ({pct:.2f}%)".replace(",", "."), ha='center', fontweight='bold')
                
            ax.set_ylabel("Cantidad de Reservas", fontsize=11)
            ax.set_xlabel("Estado Final", fontsize=11)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            plt.tight_layout()
            st.pyplot(fig, clear_figure=True)
            plt.close(fig)
            
        with col_right:
            with st.container(border=True):
                st.write("### 📌 Insights del Análisis de Estados")
                st.markdown("""
                * **Impacto del No-Show**: Una tasa de cancelación del **37.24%** representa **44.189 habitaciones bloqueadas** en el sistema que finalmente no generaron ocupación ni beneficio social directo.
                * **Ineficiencia de Ocupación**: Castelli 90 tiene plazas limitadas destinadas principalmente a estudiantes y convenios gremiales. Cada reserva cancelada que no es detectada a tiempo bloquea la oportunidad de hospedar a un estudiante vulnerable de la **UNSE**.
                * **Necesidad de Modelado**: Dado que casi 4 de cada 10 reservas no se concretan, resulta indispensable contar con un modelo que anticipe la probabilidad de no-show para aplicar depósitos de garantía o políticas dinámicas de sobreventa (overbooking).
                """)

    elif "Análisis de Tarifas" in option:
        col_left, col_right = st.columns([3, 2])
        
        with col_left:
            st.subheader("Comparativa de Distribución: Tarifa Base vs. Tarifa Efectiva")
            
            # Gráfico de densidad (KDE) para comparar las tarifas
            fig, ax = plt.subplots(figsize=(8, 5))
            fig.patch.set_alpha(0.0)
            ax.patch.set_alpha(0.0)
            
            # Filtrar tarifas por seguridad visual
            q_limit = df['tarifa_base'].quantile(0.99)
            filtered_prices = df[df['tarifa_base'] <= q_limit]
            
            sns.kdeplot(
                data=filtered_prices['tarifa_base'], 
                fill=True, 
                color='#94a3b8', 
                label='Tarifa Base (Comercial)', 
                ax=ax,
                linewidth=2
            )
            sns.kdeplot(
                data=filtered_prices['tarifa_efectiva'], 
                fill=True, 
                color='#2E5B88', 
                label='Tarifa Efectiva (Con Subsidio)', 
                ax=ax,
                linewidth=2
            )
            
            ax.set_xlabel("Tarifa por Noche ($)", fontsize=11)
            ax.set_ylabel("Densidad de Reservas", fontsize=11)
            ax.legend(frameon=True)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            plt.tight_layout()
            st.pyplot(fig, clear_figure=True)
            plt.close(fig)
            
            # Mostrar métricas promedio en columnas secundarias
            mean_base = df['tarifa_base'].mean()
            mean_effective = df['tarifa_efectiva'].mean()
            mean_subsidy = df['monto_subsidiado_total'].mean()
            
            sub_col1, sub_col2, sub_col3 = st.columns(3)
            with sub_col1:
                with st.container(border=True):
                    st.metric("Tarifa Base Promedio", f"${mean_base:.2f}")
            with sub_col2:
                with st.container(border=True):
                    st.metric("Tarifa Efectiva Promedio", f"${mean_effective:.2f}")
            with sub_col3:
                with st.container(border=True):
                    st.metric("Monto Subsidiado Promedio", f"${mean_subsidy:.2f}", help="Subsidio total acumulado promedio por reserva")
            
        with col_right:
            with st.container(border=True):
                st.write("### 📌 Insights del Análisis de Tarifas")
                st.markdown("""
                * **Carga de Subsidios**: La diferencia entre la curva gris (tarifa comercial de mercado) y la curva azul (tarifa real cobrada) representa el **subsidio social directo** que la institución absorbe para garantizar el acceso al hospedaje.
                * **Desplazamiento a la Izquierda**: Se observa cómo la tarifa efectiva se concentra en valores muy bajos, lo cual es coherente con las políticas de fomento estudiantil de la **UNSE**.
                * **Costo de Oportunidad**: Cuando ocurre una cancelación (37.24% de probabilidad), el costo de oportunidad no es solo la tarifa base perdida, sino el hecho de tener recursos y subsidios ociosos bloqueados en el sistema sin cumplir su rol de bienestar estudiantil.
                """)

    elif "Demografía" in option:
        col_left, col_right = st.columns([3, 2])
        
        with col_left:
            st.subheader("Reservas por Categorías de Huésped")
            
            # Gráfico de barras horizontal para categorías de huésped
            fig, ax = plt.subplots(figsize=(8, 5))
            fig.patch.set_alpha(0.0)
            ax.patch.set_alpha(0.0)
            
            cat_counts = df['categoria_huesped'].value_counts()
            
            sns.barplot(
                y=cat_counts.index, 
                x=cat_counts.values, 
                palette="Blues_r", 
                ax=ax,
                hue=cat_counts.index,
                legend=False
            )
            
            # Agregar etiquetas de cantidad
            for i, val in enumerate(cat_counts.values):
                ax.text(val + 500, i, f"{val:,}".replace(",", "."), va='center', fontweight='bold')
                
            ax.set_xlabel("Cantidad de Reservas", fontsize=11)
            ax.set_ylabel("Categoría del Huésped", fontsize=11)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            plt.tight_layout()
            st.pyplot(fig, clear_figure=True)
            plt.close(fig)
            
            # Mostrar distribución de origen en columnas
            st.write("")
            st.subheader("Distribución por Canal de Gestión de la Reserva")
            origin_counts = df['origen'].value_counts()
            origin_col1, origin_col2 = st.columns(2)
            with origin_col1:
                with st.container(border=True):
                    st.metric("Gestión Externa (Online / Convenios)", f"{origin_counts.get('Gestión Externa', 0):,}".replace(",", "."), f"{origin_counts.get('Gestión Externa', 0)/total_res*100:.1f}%")
            with origin_col2:
                with st.container(border=True):
                    st.metric("Gestión Interna (Directo UNSE / Gremio)", f"{origin_counts.get('Gestión Interna', 0):,}".replace(",", "."), f"{origin_counts.get('Gestión Interna', 0)/total_res*100:.1f}%")
            
        with col_right:
            with st.container(border=True):
                st.write("### 📌 Insights Demográficos")
                st.markdown("""
                * **Población Dominante**: El perfil **Particular Trabajo** lidera ampliamente la ocupación de camas, seguido por particulares genéricos. Los **Afiliados directos** y la **Actividad Académica UNSE** representan núcleos sociales de alta prioridad que reciben los subsidios más altos.
                * **Canales de Gestión**: Más del **87%** de las reservas ingresan vía *Gestión Externa*. Históricamente, las reservas autogestionadas por internet o canales no directos sufren de un menor grado de compromiso, disparando las cancelaciones.
                * **Acción sugerida**: El análisis univariado demuestra que las estrategias de confirmación y sobreventa no deben ser uniformes; deben focalizarse en los canales de mayor riesgo de cancelación para proteger el inventario de camas de los afiliados y estudiantes directos.
                """)

else:
    st.error(f"⚠️ Error: No se pudo cargar el archivo procesado en la ruta `{DATA_PATH}`. Por favor, verifica que los archivos estén en su ubicación correcta en el repositorio.")
