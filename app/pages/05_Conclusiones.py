import streamlit as st
import pandas as pd
from pathlib import Path

# Configuración de la página
st.set_page_config(
    page_title="Conclusiones y Reglas de Negocio - Albergue UNSE",
    page_icon="💡",
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
    .custom-card {
        background-color: #f8fafc;
        border-radius: 12px;
        padding: 24px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 1.5rem;
    }
    .step-title {
        font-family: 'Outfit', sans-serif;
        color: #2E5B88;
        font-weight: 600;
        font-size: 1.3rem;
        margin-top: 20px;
        margin-bottom: 12px;
    }
    .member-badge {
        background-color: #eff6ff;
        color: #1e40af;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        display: inline-block;
        margin-right: 8px;
        margin-bottom: 8px;
        font-family: 'Inter', sans-serif;
        border: 1px solid #bfdbfe;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">💡 Conclusiones y Reglas de Negocio</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Síntesis estratégica de resultados del proyecto y matriz de decisiones operativas para la toma de decisiones.</div>', unsafe_allow_html=True)
st.write("---")

# 1. KPIs de Impacto Proyectado
st.markdown('<div class="step-title">📈 Impacto Operativo y del Modelado</div>', unsafe_allow_html=True)
col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)

with col_kpi1:
    st.metric("Precisión del Modelo", "65%", "+15% vs base", help="Mejora en la precisión para detectar cancelaciones reales")
with col_kpi2:
    st.metric("Exactitud Global (Accuracy)", "74%", help="Porcentaje de predicciones correctas del clasificador")
with col_kpi3:
    st.metric("Cancelación de Línea Base", "37.24%", help="Tasa histórica de reservas canceladas en el albergue")
with col_kpi4:
    st.metric("Tasa de Cancelación en Riesgo Alto", "76%", help="Tasa de cancelación empírica del segmento con riesgo >65%")

st.write("")

# 2. Políticas de Mitigación
st.markdown('<div class="step-title">🛠️ Políticas de Mitigación Recomendadas</div>', unsafe_allow_html=True)

col_a, col_b = st.columns(2)
with col_a:
    with st.expander("🚀 Política Dinámica de Overbooking (Sobreventa)", expanded=True):
        st.markdown("""
        * **Justificación**: El modelo detecta con gran fiabilidad las reservas de **Riesgo Alto**, de las cuales el **76%** termina cancelándose efectivamente.
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
st.markdown('<div class="step-title">📋 Matriz de Decisiones Operativas según Nivel de Riesgo</div>', unsafe_allow_html=True)

# Crear DataFrame de la matriz
matriz_data = {
    "Nivel de Riesgo": ["1. Riesgo Bajo (< 35%)", "2. Riesgo Medio (35% - 65%)", "3. Riesgo Alto (> 65%)"],
    "Probabilidad de Cancelación": ["Mínima (17% de cancelaciones)", "Moderada (36% de cancelaciones)", "Crítica (76% de cancelaciones)"],
    "Acción Operativa Recomendada": [
        "Check-in directo sin fricciones. Experiencia de usuario ágil.",
        "Envío de recordatorio automático por WhatsApp / Mail 48 hs antes.",
        "Exigir depósito de garantía (pre-pago) o aplicar overbooking controlado."
    ]
}
df_matriz = pd.DataFrame(matriz_data)
st.table(df_matriz)

st.write("")

# 4. Cierre Profesional y Equipo
st.markdown('<div class="custom-card">', unsafe_allow_html=True)
st.markdown("### 🤝 Agradecimientos y Cierre")
st.markdown("""
Este proyecto demuestra cómo la combinación de análisis exploratorio riguroso y técnicas modernas de Inteligencia Artificial puede traducirse de forma directa en reglas de negocio accionables, protegiendo la sostenibilidad financiera y el rol de fomento social del **Albergue UNSE**.
""")

st.markdown("#### 👥 Integrantes del Equipo (Grupo 1):")
st.markdown("""
<span class="member-badge">Bucci, Carlos Matias</span>
<span class="member-badge">Carabajal, Elba Julieta</span>
<span class="member-badge">Segovia Albarado, Nicolas Daniel</span>
""", unsafe_allow_html=True)

st.write("")
st.markdown("#### 🔗 Enlaces del Proyecto:")
st.markdown("""
*   [💻 Repositorio en GitHub](https://github.com/BucciCarlos/entregafinal_pp)
*   [📓 Jupyter Notebooks del Flujo Analítico](file:///home/bucci/Proyectos/entregafinal_pp/notebooks/)
""")
st.markdown('</div>', unsafe_allow_html=True)
