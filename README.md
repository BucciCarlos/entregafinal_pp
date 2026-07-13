# 🏨 Sostenibilidad Financiera y Costo de Oportunidad - Castelli 90 - Caja Complementaria (UNSE)

![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat-square&logo=python)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebooks-orange?style=flat-square&logo=jupyter)
![Machine Learning](https://img.shields.io/badge/Machine_Learning-Random_Forest-green?style=flat-square)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red?style=flat-square&logo=streamlit)

## 🎯 Objetivo del Proyecto
Este proyecto de Ciencia de Datos tiene como objetivo mitigar el impacto financiero derivado de una **tasa de cancelación histórica del 37.24%** en Castelli 90. Mediante el análisis exploratorio exhaustivo y modelos predictivos de Machine Learning, evaluamos la eficiencia de los subsidios otorgados y desarrollamos una segmentación de riesgo operativo para optimizar la toma de decisiones.

## 🔗 Enlaces Rápidos
- [💻 Repositorio en GitHub](#) *https://github.com/BucciCarlos/entregafinal_pp*
- [🚀 Dashboard e Informe Interactivo en Streamlit](#) *https://entregafinalpp-grupo1.streamlit.app/*

## 👥 Integrantes del Equipo
- **Bucci, Carlos Matias** 
- **Carabajal, Elba Julieta** 
- **Segovia Albarado, Nicolas Daniel** 

## 📂 Arquitectura del Proyecto
- `data/`: Almacenamiento estructurado de datasets crudos y procesados.
- `notebooks/`: Flujo de trabajo analítico, desde la limpieza hasta el modelado predictivo.
- `reports/`: Informes ejecutivos estáticos generados en PDF/HTML.
- `app/` Aplicación web interactiva.

## 📓 Flujo de Trabajo Analítico
1. **`01_calidad_y_limpieza.ipynb`**: Limpieza de datos demográficos, tipado e imputación de valores atípicos.
2. **`02_analisis_univariado.ipynb`**: Establecimiento de la línea base operativa y Feature Engineering (Costo de Oportunidad).
3. **`03_analisis_bivariado.ipynb`**: Evaluación de eficiencia por canales de reserva, subsidios promedio y estacionalidad.
4. **`04_analisis_multivariado.ipynb`**: Matrices de correlación, interacciones complejas y evaluación de la carga social institucional.
5. **`05_modelado_predictivo.ipynb`**: Entrenamiento de un `RandomForestClassifier` optimizado con Validación Cruzada (CV) y segmentación del riesgo.
6. **`06_conclusiones.ipynb`**: Resumen ejecutivo y plan estratégico de negocio.

## 📈 Resultados Clave
- **Optimización Predictiva:** El ajuste de hiperparámetros incrementó la precisión en la detección de cancelaciones a un **65%**, logrando un modelo robusto frente al desbalance de clases.
- **Segmentación Operativa:** Se identificó un segmento crítico de **Riesgo Alto** (probabilidad predictiva >65%), en el cual **el 76% de las reservas terminan en no-show real**. Esto permite a la dirección aplicar políticas dinámicas de pre-pago o sobreventa con altísima certeza.

