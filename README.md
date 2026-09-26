# INF8239_U01 · LAB01 + LAB02 + LAB03 — SVM, Ensambles y Green AI sobre Adult Census Income

Proyecto de la asignatura INF-8239 Ciencia de Datos II, Unidad 01. Este
repositorio contiene las evidencias de los ejercicios de la unidad:

- **LAB01**: SVM con pipeline, búsqueda de parámetros y evaluación (dataset guiado).
- **LAB02 (Ejercicio 01)**: Búsqueda, selección y auditoría de un dataset público propio, y
  adaptación del pipeline del LAB01 a variables reales.
- **LAB03 (Ejercicio 02)**: Ensambles, reducción dimensional (PCA, t-SNE),
  mediciones repetidas y selección bajo criterio Green AI.

## Dataset

- **Nombre:** Adult Census Income
- **Fuente:** Kaggle — [uciml/adult-census-income](https://www.kaggle.com/datasets/uciml/adult-census-income)
- **Ficha original (documentación):** [UCI Machine Learning Repository — Adult](https://archive.ics.uci.edu/dataset/2/adult)
- **Licencia:** CC BY 4.0 (según la ficha de UCI)
- **Tarea:** Clasificación binaria — predecir si el ingreso anual de una
  persona supera los 50 000 USD.
- **Target:** `income` (`<=50K` / `>50K`)
- **Partición:** 80/20, estratificada, `random_state=42` (misma para
  LAB02 y LAB03, sin modificar para favorecer ningún modelo)
- **Ficha completa de procedencia, comparación de candidatos y criterios de
  aceptación:** [`ficha_dataset.md`](ficha_dataset.md)

## Estructura del proyecto

```
INF8239_U01/
├── .kaggle/
│   └── kaggle.json                 # credenciales locales (no versionado)
├── .pytest_cache/
├── .venv/
├── data/
│   └── raw/
│       └── adult.csv               # dataset descargado (no versionado)
├── docs/
│   └── ficha_dataset.md            # ficha de procedencia y comparación de candidatos
├── notebooks/
│   ├── 00_verificacion.ipynb
│   ├── 01_svm_guiada.ipynb         # LAB01
│   ├── 02_svm_uci.ipynb            # LAB02 / Ejercicio 01
│   └── 03_ensambles_green_ai.ipynb # LAB03 / Ejercicio 02
├── reports/
│   ├── models/                     # modelos serializados por configuración
│   │   ├── logistic.joblib
│   │   ├── svm_c1.joblib
│   │   ├── svm_c10.joblib
│   │   ├── rf_100.joblib
│   │   ├── rf_300.joblib
│   │   └── boost.joblib
│   ├── svm_best.joblib             # mejor modelo del LAB02
│   ├── svm_cv_results.csv          # validación cruzada del LAB02
│   ├── green_ai_results.csv        # tabla comparativa y frontera de Pareto (LAB03)
│   ├── tsne_two_seeds.png          # mapas t-SNE con dos semillas (LAB03)
│   └── pareto.png                  # gráfico de rendimiento vs. costo (LAB03)
├── src/
│   └── inf8239_u01/
│       ├── __pycache__/
│       ├── __init__.py
│       ├── data.py                 # descarga reproducible del dataset
│       ├── environment.py
│       ├── green.py                # función pareto_flags (LAB03)
│       └── models.py               # construcción del pipeline SVM
├── tests/
│   ├── test_models.py
│   ├── test_data_contract.py       # contrato mínimo del dataset (LAB02)
│   └── test_green.py               # pruebas de pareto_flags (LAB03)
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

## Ejercicio 01 (LAB02) — Ejecución

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

### Métrica (Ejercicio 01)

Se usa **F1 macro** como métrica principal de comparación entre el modelo
`dummy` (línea base) y la `SVM`, por tratarse de un problema de clasificación
binaria con clases desbalanceadas (`income` tiene una proporción marcada
hacia `<=50K`).

## Ejercicio 02 (LAB03) — Ensambles, reducción dimensional y Green AI

Extiende el Ejercicio 01 sobre el mismo dataset, target y partición,
comparando seis configuraciones de modelos bajo un criterio de
costo-beneficio (Green AI).

### Catálogo de modelos comparados

| Modelo | Tipo | F1 macro | Mediana ajuste | Predicción | Tamaño |
|---|---|---|---|---|---|
| `boost` | HistGradientBoosting | **0.8122** | 2.75 s | 116.9 ms | 364.0 KB |
| `logistic` | Regresión logística | 0.7875 | 1.62 s | 38.1 ms | 8.0 KB |
| `svm_c10` | SVM (C=10) | 0.7859 | 610.85 s | 13 672 ms | 7 746.5 KB |
| `svm_c1` | SVM (C=1) | 0.7835 | 375.42 s | 11 843 ms | 7 603.7 KB |
| `rf_100` | Random Forest (100 árboles) | 0.7695 | 2.97 s | 119.3 ms | 2 070.6 KB |
| `rf_300` | Random Forest (300 árboles) | 0.7686 | 8.22 s | 261.7 ms | 6 085.6 KB |

### Reducción dimensional

- **PCA** sobre las variables preprocesadas retiene **32 componentes**
  para explicar el 95% de la varianza.
- **t-SNE** con dos semillas distintas (42 y 7) sobre una muestra de 1000
  filas de variables numéricas, para verificar la estabilidad visual de
  los clusters frente al cambio de semilla.

### Ejecución (Ejercicio 02)

1. Ejecutar `notebooks/03_ensambles_green_ai.ipynb` de principio a fin
   (`Restart` + `Run All` recomendado, para evitar estados intermedios
   inconsistentes entre celdas). El notebook:
   - reconstruye el pipeline de datos del Ejercicio 01 (dataset, target,
     `preprocess`, partición train/test)
   - entrena y mide seis configuraciones de modelos con tres repeticiones
     cada una
   - compara SVM con y sin PCA
   - genera dos mapas t-SNE con semillas distintas
   - calcula la frontera de Pareto (F1 macro vs. tiempo de ajuste)
   - grafica y cuantifica la decisión final

2. Correr las pruebas de la frontera de Pareto:
```bash
   $env:PYTHONPATH="src"
   python -m pytest -q
```

### Conclusión — Decisión sobre la frontera de Pareto

El modelo con mayor F1 macro fue **HistGradientBoostingClassifier**
(`boost`), con un valor de **0.8122**, superando a la regresión logística
(0.7875), a ambas configuraciones de SVM (0.7859 y 0.7835) y a los dos
Random Forest (0.7695 y 0.7686). Además de tener el mejor desempeño,
`boost` fue también uno de los modelos más rápidos de ajustar, con una
mediana de **2.75 segundos** frente a los **610.85 segundos** (~10.2
minutos) de `svm_c10` y los **375.42 segundos** (~6.3 minutos) de
`svm_c1`. Esto lo convierte en el modelo dominante de la frontera de
Pareto: ningún otro modelo lo supera simultáneamente en F1 y en costo de
entrenamiento.

**Alternativa seleccionada:** `boost` (HistGradientBoostingClassifier). No
solo alcanza el mejor F1 macro, sino que su costo computacional es
prácticamente despreciable frente a las alternativas más lentas, lo que lo
hace la elección más razonable bajo un criterio de Green AI (máximo
desempeño con mínimo consumo de recursos).

**Diferencia absoluta de F1** respecto a la segunda mejor alternativa
(`svm_c10`, con 0.7859): **0.0263 puntos** de F1 macro. Es una diferencia
modesta en desempeño, pero la comparación de costo la vuelve irrelevante en
la práctica.

**Porcentaje de ahorro temporal:** comparando `boost` (2.75 s) contra
`svm_c10` (610.85 s), el ahorro es de aproximadamente **99.5%** en tiempo
de ajuste. Incluso contra la SVM más económica (`svm_c1`, 375.42 s), el
ahorro sigue siendo de **99.3%**. Esta diferencia se sostiene también en
tiempo de inferencia: `boost` predice en 116.9 ms frente a los 13 672 ms
de `svm_c10` y los 11 843 ms de `svm_c1` — casi dos órdenes de magnitud
más lento.

**Diferencia de tamaño en disco:** el modelo `boost` serializado ocupa
363.99 KB, considerablemente menor que las SVM (7 746.5 KB para `svm_c10`
y 7 603.66 KB para `svm_c1`), aunque mayor que `logistic` (7.99 KB). El
tamaño de `boost` es razonable para despliegue, sin acercarse a la huella
de las SVM.

**Limitaciones:** la comparación se hizo con una sola partición de
entrenamiento/prueba y sin búsqueda exhaustiva de hiperparámetros para
cada familia de modelos (por ejemplo, no se probaron distintos valores de
`learning_rate` o `max_iter` para `boost`, ni un rango más amplio de `C` y
`gamma` para las SVM), por lo que los resultados reflejan configuraciones
razonables pero no necesariamente óptimas de cada algoritmo. La mediana de
tiempo se calculó con solo tres repeticiones, lo que limita la robustez de
la estimación de varianza en el tiempo de ajuste, especialmente para
modelos con mayor variabilidad como las SVM.

**Contexto de hardware:** las mediciones se realizaron en un equipo local
(no en un servicio en la nube ni en un entorno estandarizado de
benchmarking), por lo que los tiempos absolutos pueden variar en otro
hardware; sin embargo, la relación de órdenes de magnitud entre `boost` y
las SVM es lo suficientemente amplia como para esperar que la conclusión
se mantenga en la mayoría de los entornos de cómputo disponibles para este
curso.

## Evidencias

- Ficha de procedencia/licencia: [`docs/ficha_dataset.md`](ficha_dataset.md)
- Diccionario de datos: incluido en `docs/ficha_dataset.md`
- Notebooks completos:
  [`notebooks/02_svm_uci.ipynb`](notebooks/02_svm_uci.ipynb),
  [`notebooks/03_ensambles_green_ai.ipynb`](notebooks/03_ensambles_green_ai.ipynb)
- Pruebas del contrato de datos: [`tests/test_data_contract.py`](tests/test_data_contract.py)
- Pruebas de la frontera de Pareto: [`tests/test_green.py`](tests/test_green.py)
- Resultados de validación cruzada (LAB02): [`reports/svm_cv_results.csv`](reports/svm_cv_results.csv)
- Resultados comparativos y Pareto (LAB03): [`reports/green_ai_results.csv`](reports/green_ai_results.csv)
- Mapas t-SNE: [`reports/tsne_two_seeds.png`](reports/tsne_two_seeds.png)
- Gráfico de la frontera de Pareto: [`reports/pareto.png`](reports/pareto.png)
- Modelo entrenado (LAB02): [`reports/svm_best.joblib`](reports/svm_best.joblib)
- Modelos serializados (LAB03): `reports/models/*.joblib`
- Función de la frontera de Pareto: [`src/inf8239_u01/green.py`](src/inf8239_u01/green.py)

## Notas de seguridad

El archivo `.kaggle/kaggle.json` contiene credenciales personales y **no debe
subirse al repositorio**. Está excluido vía `.gitignore`.