# Proyecto de Ciencia de Datos - Minería de Datos y Machine Learning

Este proyecto implementa una estructura estándar para el análisis, exploración y modelado predictivo de datos.

## Estructura del Proyecto

- `data/`: Contiene los conjuntos de datos en su estado original y procesado.
  - `raw/`: Datos originales sin modificar.
  - `processed/`: Datos limpios y listos para el modelado.
- `notebooks/`: Cuadernos de Jupyter para las distintas fases del ciclo de vida del proyecto.
  - `01_calidad_y_limpieza.ipynb`: Análisis de calidad de datos, imputación de nulos y limpieza.
  - `02_analisis_univariado.ipynb`: Exploración individual de variables.
  - `03_analisis_bivariado.ipynb`: Relaciones entre pares de variables.
  - `04_analisis_multivariado.ipynb`: Correlaciones, reducciones de dimensionalidad, etc.
  - `05_modelo_predictivo.ipynb`: Entrenamiento, evaluación y ajuste de modelos.
  - `06_conclusiones.ipynb`: Interpretación de resultados y conclusiones.
- `app/`: Aplicación interactiva en Streamlit.
  - `Home.py`: Página de inicio de la aplicación.
  - `pages/`: Vistas adicionales (Dataset, EDA, Predicción, Conclusiones).
- `reports/`: Informes generados, gráficos exportados y documentación.
- `logs/`: Registro de la ejecución del pipeline.

## Requisitos e Instalación

Para instalar las dependencias necesarias:

```bash
pip install -r requirements.txt
```

Para iniciar la aplicación interactiva de Streamlit:

```bash
streamlit run app/Home.py
```
