import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Configuración de la página
st.set_page_config(
    page_title="Análisis Univariado y Línea Base - Albergue UNSE",
    page_icon="📈",
    layout="wide"
)

# Estilos premium consistentes con el diseño de home.py
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700&display=swap');
    
    .main-title {
        font-family: 'Outfit', sans-serif;
        color: #2E5B88;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        font-family: 'Inter', sans-serif;
        color: #5C768D;
        font-size: 1.15rem;
        margin-bottom: 1.5rem;
    }
    .kpi-container {
        background-color: #fff1f2;
        border-radius: 12px;
        padding: 24px;
        border: 1px solid #fecdd3;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 1.5rem;
    }
    .kpi-title {
        font-family: 'Outfit', sans-serif;
        color: #be123c;
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .kpi-value {
        font-family: 'Outfit', sans-serif;
        color: #e11d48;
        font-size: 3rem;
        font-weight: 700;
        line-height: 1;
    }
    .kpi-desc {
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        color: #9f1239;
        margin-top: 0.5rem;
    }
    .insight-card {
        background-color: #f8fafc;
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-top: 1.5rem;
    }
    .step-title {
        font-family: 'Outfit', sans-serif;
        color: #2E5B88;
        font-weight: 600;
        font-size: 1.3rem;
        margin-top: 15px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

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

st.markdown('<div class="main-title">📈 Análisis Univariado y Línea Base</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Análisis del comportamiento individual de variables críticas y cuantificación de la problemática de cancelaciones.</div>', unsafe_allow_html=True)
st.write("---")

if df is not None:
    # 1. Bloque de Línea Base Crítica (KPI Destacado)
    total_res = len(df)
    total_canceled = len(df[df['estado'] == 'cancelada'])
    cancel_rate = (total_canceled / total_res) * 100
    
    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-title">🚨 Línea Base Crítica Operativa</div>
        <div class="kpi-value">{cancel_rate:.2f}%</div>
        <div class="kpi-desc">
            De las <strong>{total_res:,}</strong> reservas procesadas en el histórico del albergue, 
            <strong>{total_canceled:,}</strong> terminaron en cancelación efectiva. 
            Esta tasa de cancelación es más del doble de la media promedio de la industria hotelera (15%-19%), 
            generando graves problemas de sobreocupación fantasma y una severa ineficiencia presupuestaria.
        </div>
    </div>
    """.replace(",", "."), unsafe_allow_html=True)
    
    # 2. Selector de Variable a Analizar
    st.markdown('<div class="step-title">🔍 Selector de Variables Analíticas</div>', unsafe_allow_html=True)
    option = st.selectbox(
        "Selecciona el análisis que deseas inspeccionar en detalle:",
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
            st.write("### Frecuencia y Proporción de Estados de Reserva")
            
            # Gráfico de barras de checkout vs cancelada
            fig, ax = plt.subplots(figsize=(8, 5))
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
            
            # Anotaciones de porcentajes en las barras
            for i, val in enumerate(state_counts.values):
                pct = (val / total_res) * 100
                ax.text(i, val + 1500, f"{val:,} ({pct:.2f}%)".replace(",", "."), ha='center', fontweight='bold', color='#1e293b')
                
            ax.set_ylabel("Cantidad de Reservas", fontsize=11, color='#475569')
            ax.set_xlabel("Estado Final", fontsize=11, color='#475569')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            plt.tight_layout()
            st.pyplot(fig)
            plt.close(fig)
            
        with col_right:
            st.markdown('<div class="insight-card">', unsafe_allow_html=True)
            st.write("### 📌 Insights del Análisis de Estados")
            st.markdown("""
            * **Impacto del No-Show**: Una tasa de cancelación del **37.24%** representa **44.189 habitaciones bloqueadas** en el sistema que finalmente no generaron ocupación ni beneficio social directo.
            * **Ineficiencia de Ocupación**: El albergue tiene plazas limitadas destinadas principalmente a estudiantes y convenios gremiales. Cada reserva cancelada que no es detectada a tiempo bloquea la oportunidad de hospedar a un estudiante vulnerable de la **UNSE**.
            * **Necesidad de Modelado**: Dado que casi 4 de cada 10 reservas no se concretan, resulta indispensable contar con un modelo que anticipe la probabilidad de no-show para aplicar depósitos de garantía o políticas dinámicas de sobreventa (overbooking).
            """)
            st.markdown('</div>', unsafe_allow_html=True)

    elif "Análisis de Tarifas" in option:
        col_left, col_right = st.columns([3, 2])
        
        with col_left:
            st.write("### Comparativa de Distribución: Tarifa Base vs. Tarifa Efectiva")
            
            # Gráfico de densidad (KDE) para comparar las tarifas
            fig, ax = plt.subplots(figsize=(8, 5))
            
            # Filtrar tarifas por seguridad visual (evitar outliers extremos para la visualización de la densidad)
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
            
            ax.set_xlabel("Tarifa por Noche ($)", fontsize=11, color='#475569')
            ax.set_ylabel("Densidad de Reservas", fontsize=11, color='#475569')
            ax.legend(frameon=True, facecolor='white', edgecolor='#e2e8f0')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            plt.tight_layout()
            st.pyplot(fig)
            plt.close(fig)
            
            # Mostrar métricas promedio en columnas secundarias
            mean_base = df['tarifa_base'].mean()
            mean_effective = df['tarifa_efectiva'].mean()
            mean_subsidy = df['monto_subsidiado_total'].mean()
            
            sub_col1, sub_col2, sub_col3 = st.columns(3)
            with sub_col1:
                st.metric("Tarifa Base Promedio", f"${mean_base:.2f}")
            with sub_col2:
                st.metric("Tarifa Efectiva Promedio", f"${mean_effective:.2f}")
            with sub_col3:
                st.metric("Monto Subsidiado Promedio", f"${mean_subsidy:.2f}", help="Subsidio total acumulado promedio por reserva")
            
        with col_right:
            st.markdown('<div class="insight-card">', unsafe_allow_html=True)
            st.write("### 📌 Insights del Análisis de Tarifas")
            st.markdown("""
            * **Carga de Subsidios**: La diferencia entre la curva gris (tarifa comercial de mercado) y la curva azul (tarifa real cobrada) representa el **subsidio social directo** que la institución absorbe para garantizar el acceso al hospedaje.
            * **Desplazamiento a la Izquierda**: Se observa cómo la tarifa efectiva se concentra en valores muy bajos, lo cual es coherente con las políticas de fomento estudiantil de la **UNSE**.
            * **Costo de Oportunidad**: Cuando ocurre una cancelación (37.24% de probabilidad), el costo de oportunidad no es solo la tarifa base perdida, sino el hecho de tener recursos y subsidios ociosos bloqueados en el sistema sin cumplir su rol de bienestar estudiantil.
            """)
            st.markdown('</div>', unsafe_allow_html=True)

    elif "Demografía" in option:
        col_left, col_right = st.columns([3, 2])
        
        with col_left:
            st.write("### Reservas por Categorías de Huésped")
            
            # Gráfico de barras horizontal para categorías de huésped
            fig, ax = plt.subplots(figsize=(8, 5))
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
                ax.text(val + 500, i, f"{val:,}".replace(",", "."), va='center', fontweight='bold', color='#1e293b')
                
            ax.set_xlabel("Cantidad de Reservas", fontsize=11, color='#475569')
            ax.set_ylabel("Categoría del Huésped", fontsize=11, color='#475569')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            plt.tight_layout()
            st.pyplot(fig)
            plt.close(fig)
            
            # Mostrar distribución de origen en columnas
            st.write("")
            st.write("### Distribución por Canal de Gestión de la Reserva")
            origin_counts = df['origen'].value_counts()
            origin_col1, origin_col2 = st.columns(2)
            with origin_col1:
                st.metric("Gestión Externa (Online / Convenios)", f"{origin_counts.get('Gestión Externa', 0):,}".replace(",", "."), f"{origin_counts.get('Gestión Externa', 0)/total_res*100:.1f}%")
            with origin_col2:
                st.metric("Gestión Interna (Directo UNSE / Gremio)", f"{origin_counts.get('Gestión Interna', 0):,}".replace(",", "."), f"{origin_counts.get('Gestión Interna', 0)/total_res*100:.1f}%")
            
        with col_right:
            st.markdown('<div class="insight-card">', unsafe_allow_html=True)
            st.write("### 📌 Insights Demográficos")
            st.markdown("""
            * **Población Dominante**: El perfil **Particular Trabajo** lidera ampliamente la ocupación de camas, seguido por particulares genéricos. Los **Afiliados directos** y la **Actividad Académica UNSE** representan núcleos sociales de alta prioridad que reciben los subsidios más altos.
            * **Canales de Gestión**: Más del **87%** de las reservas ingresan vía *Gestión Externa*. Históricamente, las reservas autogestionadas por internet o canales no directos sufren de un menor grado de compromiso, disparando las cancelaciones.
            * **Acción sugerida**: El análisis univariado demuestra que las estrategias de confirmación y sobreventa no deben ser uniformes; deben focalizarse en los canales de mayor riesgo de cancelación para proteger el inventario de camas de los afiliados y estudiantes directos.
            """)
            st.markdown('</div>', unsafe_allow_html=True)

else:
    st.error(f"⚠️ Error: No se pudo cargar el archivo procesado en la ruta `{DATA_PATH}`. Por favor, verifica que los archivos estén en su ubicación correcta en el repositorio.")
