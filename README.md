# LAB01: SVM con Pipeline sobre Breast Cancer Wisconsin

Laboratorio guiado que construye un clasificador SVM de forma correcta, sin fuga de información, y lo deja reproducible, probado y versionado. LAB01 no se califica por separado: prepara el método que se exigirá en el Ejercicio 01.

## Objetivo

Clasificar tumores como malignos (0) o benignos (1) con el dataset *Breast Cancer Wisconsin* de `scikit-learn` (569 filas, 30 predictores numéricos, dos clases). El foco no es el modelo en sí, sino el método:

- Auditar los datos antes de modelar.
- Reservar el conjunto de prueba antes de cualquier transformación.
- Comparar contra una línea base.
- Ajustar hiperparámetros solo con validación cruzada.
- Guardar resultados y probar el código reutilizable.

## Estructura del proyecto

```
.
├── src/
│   └── inf8239_u01/
│       └── models.py          # build_svm(): pipeline reutilizable
├── tests/
│   └── test_models.py         # pruebas de pytest
├── reports/
│   ├── svm_cv_results.csv     # tabla de GridSearchCV
│   └── svm_best.joblib        # mejor modelo entrenado
└── README.md
```

## Requisitos

Python 3 con `pandas`, `scikit-learn`, `matplotlib`, `joblib` y `pytest`. Registra las versiones usadas para poder reproducir los resultados.

## Flujo del laboratorio

### 1. Importar y cargar los datos
Carga el dataset con `load_breast_cancer(as_frame=True)`. Genera `X` (DataFrame de 569 filas y 30 predictores) e `y` (Series binaria: 0 = maligno, 1 = benigno), e imprime la forma de `X` y la distribución de clases.

### 2. Auditar antes de modelar
Construye una tabla `audit` con el tipo, los ausentes y los valores únicos de cada columna, cuenta los duplicados y confirma que el target no está dentro de `X`. El balance es de 212 malignos y 357 benignos (cerca de 37 % y 63 %), un desbalance moderado. Esta etapa no elimina filas ni columnas: cualquier eliminación posterior debe justificarse con un hallazgo concreto.

### 3. Reservar prueba
`train_test_split` con `test_size=0.20`, `random_state=42` y `stratify=y`. Se esperan 455 filas de entrenamiento y 114 de prueba, con proporciones de clase muy parecidas en ambos conjuntos. **No se ajusta `StandardScaler` antes de esta división.**

### 4. Crear una línea base
`DummyClassifier(strategy="most_frequent")` evaluado con F1 macro. Predice siempre "benigno", por lo que el F1 macro esperado ronda 0.39. Es el piso que cualquier modelo debe superar con claridad.

### 5. Construir la SVM correctamente
Un `Pipeline` con `StandardScaler` y `SVC` (kernel `rbf`, `C=1`, `gamma="scale"`, `probability=True`, `random_state=42`). Al ir dentro del pipeline, el escalador se ajusta solo con el entrenamiento.

### 6. Evaluar la configuración base
Reporte de clasificación, ROC-AUC y matriz de confusión sobre el conjunto de prueba. Con la clase 1 (benigno) como positiva:

- **Falso positivo:** un tumor maligno clasificado como benigno.
- **Falso negativo:** un tumor benigno clasificado como maligno.

Aquí el falso positivo es el error más costoso, porque puede retrasar un diagnóstico. Además de la exactitud, conviene revisar el recall de la clase maligna. Los hiperparámetros no deben elegirse mirando esta matriz repetidamente.

### 7. Buscar C y gamma dentro del pipeline
`GridSearchCV` con `StratifiedKFold` de 5 particiones, métrica `f1_macro` y la rejilla `model__C` en [0.1, 1, 10] y `model__gamma` en ["scale", 0.01, 0.1]. Son 9 combinaciones, 45 ajustes. El prefijo `model__` es necesario porque el `SVC` está dentro del pipeline. Solo usa datos de entrenamiento.

### 8. Comparar sin ocultar variación
Tabla de `cv_results_` ordenada por puntaje medio, con su desviación estándar y el tiempo de ajuste. Si dos combinaciones difieren menos que su desviación estándar, no se puede afirmar que una sea mejor. El mejor estimador se evalúa después en el conjunto de prueba y se compara con la SVM base.

### 9. Llevar código reutilizable a `src`
`build_svm(C=1.0, gamma="scale")` en `src/inf8239_u01/models.py` devuelve el pipeline sin ajustar y lanza `ValueError` si `C` no es positivo. Evita duplicar la construcción del modelo en el notebook.

### 10. Añadir pruebas
`tests/test_models.py` verifica tres cosas:

- El modelo devuelve una predicción por cada fila de prueba.
- `build_svm(C=0)` lanza `ValueError`.
- El pipeline contiene exactamente los pasos `["scale", "model"]`.

### 11. Guardar resultados y versionar
Crea `reports/` y guarda la tabla comparativa en `reports/svm_cv_results.csv` y el mejor pipeline en `reports/svm_best.joblib`, que se recarga con `joblib.load`. Revisa el tamaño del `.joblib` antes de subirlo al repositorio.

## Cómo ejecutar las pruebas

En PowerShell, desde la raíz del proyecto:

```powershell
$env:PYTHONPATH="src"
python -m pytest -q
```

Resultado esperado: todas las pruebas aprobadas.

## Errores frecuentes

| Situación | Corrección |
|---|---|
| El escalado ocurre antes del split | Elimina ese escalado y usa `Pipeline`. |
| `GridSearchCV` no reconoce `C` | Usa `model__C`, porque el estimador está dentro del pipeline. |
| La exactitud es alta pero la clase minoritaria falla | Revisa F1 macro, recall y la matriz de confusión. |
| Los resultados cambian entre ejecuciones | Fija `random_state` y registra las versiones de las librerías. |

## Evidencias a entregar

- [ ] Notebook ejecutado de inicio a fin.
- [ ] Línea base y SVM comparadas.
- [ ] Tabla de `GridSearchCV`.
- [ ] Matriz de confusión interpretada.
- [ ] CSV, modelo, pruebas y commit.