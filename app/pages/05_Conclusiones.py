import streamlit as st
import pandas as pd
from pathlib import Path

# Configuración de la página
st.set_page_config(
    page_title="Conclusiones y Reglas de Negocio - Caja Complementaria UNSE",
    page_icon="💡",
    layout="wide"
)

# Cabecera principal con componentes nativos (compatibilidad total con Light/Dark Theme)
st.title("💡 Conclusiones y Reglas de Negocio")
st.subheader("Síntesis estratégica de resultados del proyecto y matriz de decisiones operativas para la toma de decisiones.")
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

# 1. KPIs de Impacto Proyectado dentro de contenedores con borde
st.subheader("📈 Impacto Operativo y del Modelado")
col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)

with col_kpi1:
    with st.container(border=True):
        st.metric("Precisión del Modelo", "65%", "+15% vs base", help="Mejora en la precisión para detectar cancelaciones reales")
with col_kpi2:
    with st.container(border=True):
        st.metric("Exactitud Global (Accuracy)", "74%", help="Porcentaje de predicciones correctas del clasificador")
with col_kpi3:
    with st.container(border=True):
        st.metric("Cancelación de Línea Base", "37.24%", help="Tasa histórica de reservas canceladas en Castelli 90")
with col_kpi4:
    with st.container(border=True):
        st.metric("Tasa de Cancelación en Riesgo Alto", "82%", help="Tasa de cancelación empírica del segmento con riesgo >65%")

st.write("")

# 2. Políticas de Mitigación
st.subheader("🛠️ Políticas de Mitigación Recomendadas")

col_a, col_b = st.columns(2)
with col_a:
    with st.expander("🚀 Política Dinámica de Overbooking (Sobreventa)", expanded=True):
        st.markdown("""
        * **Justificación**: El modelo detecta con gran fiabilidad las reservas de **Riesgo Alto**, de las cuales el **82%** termina cancelándose efectivamente.
        * **Acción sugerida**: Autorizar una sobreventa moderada de hasta el **10%** en fechas críticas de alta demanda únicamente para plazas que coincidan con perfiles clasificados como de Riesgo Alto, amortiguando de forma controlada la ineficiencia operativa por no-show.
        """)
        
    with st.expander("🔒 Fricción Selectiva y Garantías", expanded=True):
        st.markdown("""
        * **Justificación**: Huéspedes de Riesgo Medio/Alto generan incertidumbre presupuestaria, mientras que los de Riesgo Bajo son sumamente seguros.
        * **Acción sugerida**: Implementar recordatorios telefónicos automáticos y solicitudes de depósito (pre-pagos) **exclusivamente al segmento de Riesgo Medio y Alto**. Las reservas de **Riesgo Bajo** deben gozar de un check-in rápido y sin fricciones.
        """)

with col_b:
    with st.expander("🌍 Auditoría y Ajuste de Canales Externos", expanded=True):
        st.markdown("""
        * **Justificación**: Las reservas procedentes de *Gestión Externa* presentan tasas de cancelación significativamente más elevadas (38.8%) que la gestión directa interna (25.7%).
        * **Acción sugerida**: Auditar cupos asignados a canales externos ineficientes y renegociar contratos o ajustar las políticas de confirmación para forzar un mayor compromiso del huésped antes del arribo.
        """)
        
    with st.expander("👥 Optimización del Subsidio Social Gremial", expanded=True):
        st.markdown("""
        * **Justificación**: Las familias numerosas asociadas a afiliados absorben gran cantidad de recursos institucionales en subsidios, y sus cancelaciones representan la mayor pérdida económica y social.
        * **Acción sugerida**: Establecer alertas de reconfirmación manual prioritaria para reservas de afiliados con más de 3 ocupantes y estadías de rango largo (7+ noches).
        """)

st.write("")

# 3. Matriz de Decisiones Operativas
st.subheader("📋 Matriz de Decisiones Operativas según Nivel de Riesgo")

# Crear DataFrame de la matriz
matriz_data = {
    "Nivel de Riesgo": ["1. Riesgo Bajo (< 35%)", "2. Riesgo Medio (35% - 65%)", "3. Riesgo Alto (> 65%)"],
    "Probabilidad de Cancelación": ["Mínima (17% de cancelaciones)", "Moderada (36% de cancelaciones)", "Crítica (82% de cancelaciones)"],
    "Acción Operativa Recomendada": [
        "Check-in directo sin fricciones. Experiencia de usuario ágil.",
        "Envío de recordatorio automático por WhatsApp / Mail 48 hs antes.",
        "Exigir depósito de garantía (pre-pago) o aplicar overbooking controlado."
    ]
}
df_matriz = pd.DataFrame(matriz_data)
# Mostrar como dataframe estilizado de ancho completo ocultando el índice para mayor elegancia
st.dataframe(df_matriz, use_container_width=True, hide_index=True)

st.write("")

# 4. Cierre Profesional y Equipo
with st.container(border=True):
    st.subheader("🤝 Agradecimientos y Cierre")
    st.markdown("""
    Este proyecto demuestra cómo la combinación de análisis exploratorio riguroso y técnicas modernas de Inteligencia Artificial puede traducirse de forma directa en reglas de negocio accionables, protegiendo la sostenibilidad financiera y el rol de fomento social de **Castelli 90 - Caja Complementaria (UNSE)**.
    """)
    
    st.divider()
    
    col_team, col_links = st.columns(2)
    with col_team:
        st.markdown("**👥 Integrantes del Equipo (Grupo 1):**")
        st.markdown("""
        *   Bucci, Carlos Matias
        *   Carabajal, Elba Julieta
        *   Segovia Albarado, Nicolas Daniel
        """)
    with col_links:
        st.markdown("**🔗 Enlaces del Proyecto:**")
        st.markdown("""
        *   [💻 Repositorio en GitHub](https://github.com/BucciCarlos/entregafinal_pp)
        *   [📓 Jupyter Notebooks del Flujo Analítico](file:///home/bucci/Proyectos/entregafinal_pp/notebooks/)
        """)

st.write("")
# Aviso de simulación académica en la parte inferior (footer)
st.error("⚠️ **Aviso:** Los datos presentados en este entorno son simulados con fines académicos y NO representan información real de la institución.")
