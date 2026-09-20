# U01.LAB00 · Preparación y validación del entorno profesional

**Estudiante:** Manicaotex Mueses  
**Asignatura:** INF-8239 Ciencia de Datos II  
**Unidad:** 01 - Modelos avanzados, reducción dimensional y Green AI  
**Código:** U01.LAB00  
**Sistema operativo utilizado:** Windows 10 de 64 bits  

## 1. Propósito de la práctica

Esta práctica documenta la preparación y validación de un entorno profesional y reproducible para desarrollar los ejercicios de la asignatura. Se instalaron y comprobaron Python, Git, Visual Studio Code y Jupyter; además, se creó un proyecto organizado, un entorno virtual, una prueba unitaria y el primer commit del repositorio.

> **Resultado esperado:** disponer de un proyecto funcional en Windows 10, con las dependencias aisladas en `.venv`, las pruebas aprobadas y el historial inicial de Git disponible.

## 2. Herramientas requeridas

- Windows 10 de 64 bits.
- Python 3.11 o superior.
- Git.
- Visual Studio Code.
- Extensiones de VS Code: Python, Jupyter, Pylance y Ruff.
- Cuenta de GitHub, si se publicará el repositorio.

Se recomienda guardar el proyecto en una carpeta local y evitar usar Google Drive como ruta obligatoria.

## 3. Verificación de Python y pip

Después de instalar Python desde [python.org](https://www.python.org/), marcando la opción **Add python.exe to PATH**, se abrió una nueva terminal de PowerShell y se ejecutaron los comandos siguientes:

```powershell
python --version
python -m pip --version
```

El resultado debe mostrar Python 3.11 o una versión superior, junto con la ubicación de `pip` asociada al mismo intérprete.

## 4. Instalación y configuración de Git

Una vez instalado Git, se comprobó su versión:

```powershell
git --version
```

Luego se configuró la identidad que aparecerá en los commits:

```powershell
git config --global user.name "Manicaotex Mueses Ruiz"
git config --global user.email "mannixmueses@gmail.com"
git config --global --list
```


## 5. Preparación de Visual Studio Code

En Visual Studio Code se abrió **Extensions** mediante `Ctrl+Shift+X` y se instalaron las extensiones siguientes:

- Python, publicada por Microsoft.
- Jupyter, publicada por Microsoft.
- Pylance, publicada por Microsoft.
- Ruff.

## 6. Creación de la estructura del proyecto

En PowerShell se accedió a la carpeta elegida para guardar el curso y se ejecutaron estos comandos:

```powershell
mkdir INF8239_U01
cd INF8239_U01
mkdir data, notebooks, reports, src, tests
```

Para abrir la carpeta completa en Visual Studio Code se puede utilizar:

```powershell
code .
```

La estructura inicial esperada es:

```text
INF8239_U01/
├── data/
├── notebooks/
├── reports/
├── src/
└── tests/
```

## 7. Creación y activación del entorno virtual

Desde la raíz del proyecto se creó el entorno virtual:

```powershell
python -m venv .venv
```

Para activarlo en PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Si PowerShell bloquea temporalmente el script de activación, se ejecuta lo siguiente únicamente para la sesión actual:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Como alternativa, desde el Símbolo del sistema (`cmd`) se puede activar con:

```bat
.venv\Scripts\activate.bat
```

Cuando el entorno está activo, la terminal muestra `(.venv)` al inicio de la línea.

## 8. Creación e instalación de `requirements.txt`

En la raíz del proyecto se creó el archivo `requirements.txt` con este contenido:

```text
numpy>=1.26
pandas>=2.2
scikit-learn>=1.4
matplotlib>=3.8
seaborn>=0.13
joblib>=1.3
pytest>=8.0
```

Después se actualizaron `pip` y las dependencias:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Para verificar los paquetes instalados:

```powershell
python -m pip list
```

## 9. Creación del módulo de Python

Se creó la carpeta del paquete:

```powershell
mkdir src\inf8239_u01
```

Dentro de `src/inf8239_u01/` se creó un archivo vacío llamado `__init__.py` y otro llamado `environment.py`.

Contenido de `src/inf8239_u01/environment.py`:

```python
def environment_message() -> str:
    return "Entorno INF-8239 listo"
```

La estructura correspondiente es:

```text
src/
└── inf8239_u01/
    ├── __init__.py
    └── environment.py
```

## 10. Creación y ejecución de la primera prueba

En `tests/test_environment.py` se agregó:

```python
from inf8239_u01.environment import environment_message


def test_environment_message():
    assert environment_message() == "Entorno INF-8239 listo"
```

En PowerShell se indicó que los módulos del proyecto están dentro de `src` y se ejecutó `pytest`:

```powershell
$env:PYTHONPATH = "src"
python -m pytest -q
```

Resultado esperado:

```text
1 passed
```

## 11. Verificación de Jupyter

En Visual Studio Code se realizaron estos pasos:

1. Abrir la paleta de comandos con `Ctrl+Shift+P`.
2. Ejecutar **Python: Select Interpreter**.
3. Elegir el intérprete ubicado en `.venv`.
4. Crear el archivo `notebooks/00_verificacion.ipynb`.
5. Pulsar **Select Kernel** en la esquina superior derecha del notebook.
6. Seleccionar **Python Environments** y luego el intérprete `.venv`.

En una celda del notebook se ejecutó:

```python
import sys
import platform

print(sys.executable)
print(sys.version)
print(platform.platform())

assert ".venv" in sys.executable.lower()
```

La ruta presentada por `sys.executable` debe contener `.venv`. La información de `platform.platform()` debe identificar el sistema como Windows 10.

Si **Select Kernel** no aparece, se puede:

1. Confirmar que la extensión Jupyter está instalada y habilitada.
2. Cerrar y volver a abrir el archivo `.ipynb`.
3. Ejecutar `Ctrl+Shift+P` y buscar **Notebook: Select Notebook Kernel**.
4. Reiniciar Visual Studio Code si la opción todavía no está disponible.

## 12. Preparación del repositorio Git

En la raíz del proyecto se creó `.gitignore` con el contenido siguiente:

```gitignore
.venv/
__pycache__/
.pytest_cache/
.ipynb_checkpoints/
*.joblib
data/raw/*
!data/raw/.gitkeep
```

Luego se inicializó el repositorio y se realizó el primer commit:

```powershell
git init
git add .
git commit -m "chore: create INF-8239 reproducible environment"
git status
git log --oneline
```

El resultado esperado de `git status` es `working tree clean`, mientras que `git log --oneline` debe mostrar el primer commit.