# Ficha del dataset


## Formular antes de buscar

- **Dominio:** Salud pública / detección temprana de diabetes.
- **Unidad de análisis:** Una paciente (mujer de al menos 21 años, de herencia Pima).
- **Decisión:** ✏️ Priorizar qué pacientes deben recibir pruebas confirmatorias de diabetes y seguimiento clínico.
- **Target:** `Outcome` (0 = prueba negativa, 1 = prueba positiva para diabetes).
- **Tipo de tarea:** Clasificación binaria.
- **Error más costoso:** ✏️ Falso negativo: no detectar a una paciente con diabetes y retrasar su diagnóstico y tratamiento. El falso positivo solo implica una prueba adicional.
- **Usuario:** ✏️ Personal clínico de atención primaria.

---

## Candidatos

### Candidato A: Pima Indians Diabetes Database

- **URL de la ficha:** https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database
- **URL de descarga:** botón *Download* de la ficha (requiere cuenta de Kaggle) o `kaggle datasets download -d uciml/pima-indians-diabetes-database`
- **Autor / publicador:** UCI Machine Learning (Kaggle). Origen: National Institute of Diabetes and Digestive and Kidney Diseases.
- **Cita original:** Smith, J.W., Everhart, J.E., Dickson, W.C., Knowler, W.C., & Johannes, R.S. (1988). Using the ADAP learning algorithm to forecast the onset of diabetes mellitus. Proceedings of the Symposium on Computer Applications and Medical Care, 261–265. IEEE Computer Society Press.
- **Fecha:** Publicado en Kaggle en octubre de 2016.
- **Licencia:** CC0: Public Domain.
- **Tamaño:** 768 filas, 9 columnas (< 100 KB).
- **Diccionario:** Sí, descrito en la ficha (embarazos, glucosa, IMC, insulina, edad, etc.).

### Candidato B: Adult Census Income

- **URL de la ficha (Kaggle):** https://www.kaggle.com/datasets/uciml/adult-census-income
- **URL de la ficha original (documentación y diccionario):** https://archive.ics.uci.edu/dataset/2/adult
- **URL de descarga:** botón *Download* en Kaggle, `kaggle datasets download -d uciml/adult-census-income`, o `fetch_ucirepo(id=2)` desde UCI.
- **Autores:** Becker, B. & Kohavi, R. (1996). Extracción de Barry Becker a partir del censo de EE. UU. de 1994.
- **Fecha:** Publicado en Kaggle en octubre de 2016 (dataset original de 1996).
- **DOI:** 10.24432/C5XW20
- **Licencia:** CC BY 4.0 según la ficha de UCI (no verificada en la copia de Kaggle).
- **Tamaño:** ✏️ ~32 500 filas y 15 columnas en el archivo de Kaggle (verificar al descargar), unos pocos MB.
- **Diccionario:** Sí. Variables demográficas y laborales: edad, tipo de empleo, educación, estado civil, ocupación, horas por semana, etc.

### Comparación

| Criterio | Candidato A (Pima) | Candidato B (Adult Census) |
|---|---|---|
| Procedencia | NIDDK (EE. UU.), publicado por UCI Machine Learning en Kaggle | Censo de EE. UU. de 1994, repositorio UCI |
| Licencia | CC0 (dominio público) | CC BY 4.0 (UCI), atribución obligatoria |
| Filas/columnas | 768 / 9 | ✏️ ~32 500 / 15 (verificar) |
| Target y clases | `Outcome`: 0 (500) y 1 (268) | `income`: <=50K y >50K (desbalanceado, ~80 % / 20 %) |
| Ausentes | No declarados, pero varias columnas usan 0 como valor faltante (verificar) | Sí: valores "?" en variables como tipo de empleo, ocupación y país de origen (verificar) |
| Riesgo de fuga | Bajo: mediciones diagnósticas previas al resultado | Bajo-medio: `education` y `education-num` son redundantes; `fnlwgt` es un peso muestral del censo, no una característica de la persona |

---

## Criterios de aceptación

| Criterio | Candidato A | Candidato B |
|---|---|---|
| Al menos 500 filas | ✅ 768 | ✅ Decenas de miles |
| Target observable y mínimo dos clases | ✅ Binario | ✅ Binario |
| Uso académico permitido | ✅ CC0 | ✅ CC BY 4.0 |
| Variables disponibles al momento de predecir | ✅ | ✅ Son datos demográficos y laborales |
| Tamaño compatible con CPU/Colab gratuito | ✅ | ✅ Unos pocos MB |
| No repetir dataset con otro estudiante | ✏️ Pendiente de confirmar | ✏️ Pendiente de confirmar |

