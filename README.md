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

## Conclusión

Este laboratorio permitió llevar el pipeline de clasificación con SVM del
LAB01 —construido sobre un dataset guiado y ya limpio— a un escenario más
realista: elegir, justificar, descargar y auditar un dataset público desde
cero. El dataset elegido fue Adult Census Income, publicado en Kaggle por
UCI Machine Learning, cuya tarea es predecir si el ingreso anual de una
persona supera los 50 000 USD a partir de variables demográficas y laborales
del censo de 1994 de Estados Unidos. Se validó que cumplía los criterios de
aceptación del laboratorio: más de 30 000 filas, un target binario
(`income`) con clases claramente observables, y una licencia CC BY 4.0 que
permite su uso académico con atribución.

Encapsular la descarga en `src/inf8239_u01/data.py`, en vez de depender de
una ruta local o de una carpeta de Google Drive, fue uno de los aprendizajes
más prácticos del proceso. El primer intento, usando una URL directa de la
ficha de Kaggle con `pd.read_csv`, falló porque Kaggle no permite descargas
directas de esa forma. Resolverlo implicó entender la diferencia entre
`kagglehub` (que sí permite descargar datasets públicos sin credenciales) y
la API oficial de `kaggle` (que siempre las exige), y ajustar la función para
que el archivo quedara reproduciblemente ubicado en `data/raw`, sin rutas
absolutas ni dependencias de una máquina en particular.

La auditoría del dataset —tipos de dato, valores ausentes, duplicados y
balance de clases— confirmó que `income` está desbalanceado hacia la clase
`<=50K`, lo que justificó usar F1 macro como métrica principal en lugar de
accuracy, ya que esta última puede resultar engañosamente alta si el modelo
simplemente predice siempre la clase mayoritaria. Comparar la SVM contra un
`DummyClassifier` como línea base permitió confirmar que el modelo aprende
un patrón real y no solo repite la clase dominante del desbalance.

Definir el target y evaluar posibles fugas de información también resultó
relevante para este dataset en particular: variables como `fnlwgt` (un peso
muestral del censo, no una característica real de la persona) y la
redundancia entre `education` y `education-num` obligaron a pensar qué
información está legítimamente disponible al momento de predecir, en lugar
de incluir todo lo que mejora la métrica sin justificación. Encapsular el
preprocesamiento (imputación, escalado, codificación one-hot) dentro de un
`ColumnTransformer` integrado al `Pipeline`, en vez de aplicarlo directamente
sobre el DataFrame completo, evitó fugas de información adicionales, ya que
el ajuste de esas transformaciones ocurre únicamente sobre el conjunto de
entrenamiento. En conjunto, el laboratorio deja como aprendizaje central que
la calidad de un modelo sobre Adult Census Income depende tanto de las
decisiones tomadas antes de tocar el algoritmo —procedencia, licencia,
definición de target, tratamiento de fugas— como del ajuste de
hiperparámetros en sí.