# INF8239_U01 · LAB01 + LAB02 — SVM sobre Adult Census Income

Proyecto de la asignatura INF-8239 Ciencia de Datos II, Unidad 01. Este
repositorio contiene las evidencias del **Ejercicio 01**, que combina:

- **LAB01**: SVM con pipeline, búsqueda de parámetros y evaluación (dataset guiado).
- **LAB02**: Búsqueda, selección y auditoría de un dataset público propio, y
  adaptación del pipeline del LAB01 a variables reales.

## Dataset

- **Nombre:** Adult Census Income
- **Fuente:** Kaggle — [uciml/adult-census-income](https://www.kaggle.com/datasets/uciml/adult-census-income)
- **Ficha original (documentación):** [UCI Machine Learning Repository — Adult](https://archive.ics.uci.edu/dataset/2/adult)
- **Licencia:** CC BY 4.0 (según la ficha de UCI)
- **Tarea:** Clasificación binaria — predecir si el ingreso anual de una
  persona supera los 50 000 USD.
- **Target:** `income` (`<=50K` / `>50K`)
- **Ficha completa de procedencia, comparación de candidatos y criterios de
  aceptación:** [`docs/ficha_dataset.md`](docs/ficha_dataset.md)

## Estructura del proyecto

```
INF8239_U01/
├── .kaggle/
│   └── kaggle.json                # credenciales locales (no versionado)
├── .pytest_cache/
├── .venv/
├── data/
│   └── raw/                       # datasets descargados (no versionado)
├── docs/
│   └── ficha_dataset.md           # ficha de procedencia y comparación de candidatos
├── notebooks/
│   ├── 00_verificacion.ipynb
│   ├── 01_svm_guiada.ipynb        # LAB01
│   └── 02_svm_uci.ipynb           # LAB02
├── reports/
│   ├── svm_best.joblib            # mejor modelo entrenado
│   └── svm_cv_results.csv         # resultados de validación cruzada
├── src/
│   └── inf8239_u01/
│       ├── __pycache__/
│       ├── __init__.py
│       ├── data.py                # descarga reproducible del dataset
│       ├── environment.py
│       └── models.py              # construcción del pipeline SVM
├── tests/
│   ├── test_models.py
│   └── test_data_contract.py      # contrato mínimo del dataset (LAB02)
├── .gitignore
├── README.md
└── requirements.txt
```

## Instalación

```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
# source .venv/bin/activate # Linux/Mac

pip install -r requirements.txt
pip install -e .             # instala el paquete src en modo editable
```

## Descarga del dataset

La descarga es reproducible y no depende de rutas locales ni de Google Drive.
Se encapsula en `src/inf8239_u01/data.py`:

```python
from src.inf8239_u01.data import get_adult_census_data

csv_path = get_adult_census_data()
print(csv_path)  # data/raw/adult.csv
```

El dataset se descarga automáticamente vía [`kagglehub`](https://pypi.org/project/kagglehub/)
(no requiere credenciales de Kaggle para este dataset público) y se copia a
`data/raw/`.

## Ejecución

1. Ejecutar `notebooks/02_svm_uci.ipynb` de principio a fin. El notebook:
   - descarga el dataset con `get_adult_census_data()`
   - carga el CSV y reconoce su esquema (`shape`, `dtypes`, `head`, `tail`)
   - audita tipos, ausentes, porcentaje de ausentes y duplicados
   - define el target (`income`) y retira columnas de fuga si aplica
   - separa variables numéricas/categóricas y arma el preprocesamiento
     (`ColumnTransformer` con imputación, escalado y one-hot encoding)
   - divide en entrenamiento/prueba (80/20, estratificado, `random_state=42`)
   - entrena un `DummyClassifier` (línea base) y una `SVC` dentro de un `Pipeline`
   - reporta F1 macro y `classification_report` de ambos modelos

2. Correr las pruebas del dataset:
```bash
   $env:PYTHONPATH="src"
   python -m pytest -q
```

## Métrica

Se usa **F1 macro** como métrica principal de comparación entre el modelo
`dummy` (línea base) y la `SVM`, por tratarse de un problema de clasificación
binaria con clases desbalanceadas (`income` tiene una proporción marcada
hacia `<=50K`).

## Evidencias

- Ficha de procedencia/licencia: [`docs/ficha_dataset.md`](docs/ficha_dataset.md)
- Diccionario de datos: incluido en `docs/ficha_dataset.md`
- Notebook completo: [`notebooks/02_svm_uci.ipynb`](notebooks/02_svm_uci.ipynb)
- Pruebas del contrato de datos: [`tests/test_data_contract.py`](tests/test_data_contract.py)
- Resultados de validación cruzada: [`reports/svm_cv_results.csv`](reports/svm_cv_results.csv)
- Modelo entrenado: [`reports/svm_best.joblib`](reports/svm_best.joblib)

