import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

# Configuración de la página
st.set_page_config(
    page_title="Predicción de Cancelaciones - Caja Complementaria UNSE",
    page_icon="🔮",
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
    .result-container {
        background-color: #f8fafc;
        border-radius: 12px;
        padding: 24px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-top: 1rem;
    }
    .result-header {
        font-family: 'Outfit', sans-serif;
        color: #2E5B88;
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    .prob-display {
        font-family: 'Outfit', sans-serif;
        font-size: 3rem;
        font-weight: 700;
        line-height: 1;
        margin-bottom: 0.5rem;
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

# Carga del modelo optimizado usando st.cache_resource
BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_PATH = BASE_DIR / 'models' / 'rf_model_optimizado.pkl'

@st.cache_resource
def load_model(path):
    if path.exists():
        return joblib.load(path)
    else:
        # Fallback local path
        fallback_path = Path("models/rf_model_optimizado.pkl")
        if fallback_path.exists():
            return joblib.load(fallback_path)
        return None

model = load_model(MODEL_PATH)

st.markdown('<div class="main-title">🔮 Simulador de Riesgo y Predicción</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Ingresa los datos de una reserva potencial para evaluar en tiempo real su probabilidad de cancelación e impacto financiero.</div>', unsafe_allow_html=True)
st.write("---")

# Mapeo de meses y multiplicadores de tarifa según la categoría (obtenidos del análisis de datos)
MONTHS = {
    "Enero": 1, "Febrero": 2, "Marzo": 3, "Abril": 4, "Mayo": 5, "Junio": 6,
    "Julio": 7, "Agosto": 8, "Septiembre": 9, "Octubre": 10, "Noviembre": 11, "Diciembre": 12
}

MULTIPLIERS = {
    "Actividad Académica UNSE": 0.60,
    "Afiliado": 0.55,
    "Afiliado Jubilado": 0.50,
    "Institucional": 0.70,
    "Particular": 1.00,
    "Particular deporte": 0.85,
    "Particular trabajo": 0.90,
    "Particular vacaciones": 1.00
}

if model is not None:
    col_form, col_result = st.columns([1.1, 1])
    
    with col_form:
        st.markdown('<div class="step-title">📥 Datos de la Reserva</div>', unsafe_allow_html=True)
        with st.form("prediction_form"):
            # Campos del formulario
            noches = st.slider("Duración de la Estadía (Noches):", 1, 30, 3)
            adultos = st.slider("Cantidad de Adultos:", 1, 10, 2)
            menores = st.slider("Cantidad de Menores:", 0, 5, 0)
            tarifa_b = st.number_input("Tarifa Base por Noche ($):", min_value=10.0, max_value=2000.0, value=100.0, step=10.0)
            
            mes_sel = st.selectbox("Mes de Check-in:", list(MONTHS.keys()), index=6) # Default Julio
            origen_sel = st.selectbox("Canal de Origen de la Reserva:", ["Gestión Externa", "Gestión Interna"])
            categoria_sel = st.selectbox("Categoría de Huésped:", list(MULTIPLIERS.keys()), index=4) # Default Particular
            
            submit_button = st.form_submit_button("Calcular Probabilidad de Cancelación", type="primary")
            
    with col_result:
        st.markdown('<div class="step-title">📊 Resultados de la Inferencia</div>', unsafe_allow_html=True)
        if submit_button:
            # 1. Preparación de variables de entrada mapeando categorías a columnas de one-hot encoding
            origen_val = 1 if origen_sel == "Gestión Interna" else 0
            
            cat_cols = {
                'Afiliado': 'categoria_huesped_Afiliado',
                'Afiliado Jubilado': 'categoria_huesped_Afiliado Jubilado',
                'Institucional': 'categoria_huesped_Institucional',
                'Particular': 'categoria_huesped_Particular',
                'Particular deporte': 'categoria_huesped_Particular deporte',
                'Particular trabajo': 'categoria_huesped_Particular trabajo',
                'Particular vacaciones': 'categoria_huesped_Particular vacaciones'
            }
            
            cat_features = {col: 0 for col in cat_cols.values()}
            if categoria_sel in cat_cols:
                cat_features[cat_cols[categoria_sel]] = 1
                
            dur_larga = 1 if noches >= 7 else 0
            dur_mediana = 1 if 3 <= noches <= 6 else 0
            
            # Construir el DataFrame con las columnas en el orden exacto esperado por el modelo
            input_data = pd.DataFrame([{
                'noches_totales': noches,
                'cant_adultos': adultos,
                'cant_menores': menores,
                'tarifa_base': tarifa_b,
                'mes_num': MONTHS[mes_sel],
                'origen_Gestión Interna': origen_val,
                **cat_features,
                'duracion_categoria_Larga (7+ noches)': dur_larga,
                'duracion_categoria_Mediana (3-6 noches)': dur_mediana
            }])
            
            cols_order = [
                'noches_totales', 'cant_adultos', 'cant_menores', 'tarifa_base', 'mes_num',
                'origen_Gestión Interna', 'categoria_huesped_Afiliado',
                'categoria_huesped_Afiliado Jubilado', 'categoria_huesped_Institucional',
                'categoria_huesped_Particular', 'categoria_huesped_Particular deporte',
                'categoria_huesped_Particular trabajo',
                'categoria_huesped_Particular vacaciones',
                'duracion_categoria_Larga (7+ noches)',
                'duracion_categoria_Mediana (3-6 noches)'
            ]
            input_data = input_data[cols_order]
            
            # 2. Inferencia
            prob_cancelation = model.predict_proba(input_data)[0, 1]
            prob_pct = prob_cancelation * 100
            
            # 3. Cálculos Financieros Estimados
            multiplicador = MULTIPLIERS[categoria_sel]
            tarifa_efectiva_est = tarifa_b * multiplicador
            subsidio_total_est = (tarifa_b - tarifa_efectiva_est) * noches
            costo_oportunidad_est = tarifa_efectiva_est * noches
            costo_riesgo_est = costo_oportunidad_est * prob_cancelation
            
            # Mostrar resultados
            st.markdown('<div class="result-container">', unsafe_allow_html=True)
            st.write("#### Probabilidad de Cancelación:")
            
            # Lógica condicional de colores según la segmentación de riesgo
            if prob_pct < 35.0:
                st.markdown(f'<div class="prob-display" style="color: #10B981;">{prob_pct:.2f}%</div>', unsafe_allow_html=True)
                st.success("✅ **Riesgo Bajo (Segmento Seguro)**: Las reservas de esta categoría muestran una alta probabilidad de check-out exitoso (83% empírico). Se recomienda procesar sin fricciones adicionales.")
            elif prob_pct <= 65.0:
                st.markdown(f'<div class="prob-display" style="color: #F59E0B;">{prob_pct:.2f}%</div>', unsafe_allow_html=True)
                st.warning("⚠️ **Riesgo Medio (Incertidumbre)**: Probabilidad de cancelación intermedia. Se sugiere enviar un recordatorio automático de reconfirmación (correo o WhatsApp) 48 horas antes de la llegada.")
            else:
                st.markdown(f'<div class="prob-display" style="color: #EF4444;">{prob_pct:.2f}%</div>', unsafe_allow_html=True)
                st.error("🚨 **Riesgo Crítico (Alta Fuga)**: Históricamente, el **82%** de los casos clasificados aquí terminan en cancelación efectiva. Se recomienda aplicar reglas de negocio preventivas: exigir el pago de seña por adelantado o aplicar una sobreventa (overbooking) moderada de la plaza.")
                
            st.write("---")
            st.write("#### 💸 Análisis de Impacto Financiero")
            
            res_col1, res_col2 = st.columns(2)
            with res_col1:
                st.metric("Tarifa Efectiva por Noche", f"${tarifa_efectiva_est:.2f}", f"Subsidio: {int((1-multiplicador)*100)}%")
                st.metric("Subsidio Total Acumulado", f"${subsidio_total_est:.2f}", help="Importe total subsidiado por la institución para esta estadía")
            with res_col2:
                st.metric("Costo de Oportunidad Máximo", f"${costo_oportunidad_est:.2f}", help="Ingreso real que se pierde de forma directa si el huésped no asiste")
                st.metric("Costo de Oportunidad en Riesgo", f"${costo_riesgo_est:.2f}", f"Prob: {prob_pct:.1f}%", delta_color="inverse", help="Valor esperado de pérdida económica ajustado por la probabilidad de cancelación")
                
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("💡 **Simulador Listo**: Modifica los parámetros del formulario de la izquierda y presiona el botón para calcular las probabilidades de cancelación e impactos financieros.")
else:
    st.error("⚠️ Error crítico: No se encontró el archivo del modelo entrenado en `models/rf_model_optimizado.pkl`. Por favor, verifica que la fase de entrenamiento y guardado se haya ejecutado correctamente.")
