import shutil
from pathlib import Path

import kagglehub

# Ruta al directorio raíz del proyecto (src/inf8239_u01/data.py -> raíz)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

ADULT_CENSUS_SLUG = "uciml/adult-census-income"


def download_kaggle_dataset(dataset_slug: str, dest_dir: Path = RAW_DATA_DIR) -> Path:
    """
    Descarga un dataset público de Kaggle y deja el CSV directamente en dest_dir.

    Parameters
    ----------
    dataset_slug : str
        Identificador del dataset en Kaggle, formato "usuario/nombre-dataset".
    dest_dir : Path
        Carpeta donde quedará el archivo .csv. Por defecto, data/raw en la
        raíz del proyecto.

    Returns
    -------
    Path
        Ruta al archivo .csv dentro de dest_dir.
    """
    cache_path = Path(kagglehub.dataset_download(dataset_slug))
    dest_dir.mkdir(parents=True, exist_ok=True)

    csv_source = next(cache_path.glob("*.csv"))
    csv_dest = dest_dir / csv_source.name
    shutil.copy2(csv_source, csv_dest)

    return csv_dest


def get_adult_census_data() -> Path:
    """
    Descarga (si hace falta) el dataset Adult Census Income y devuelve
    la ruta al CSV en data/raw.

    Returns
    -------
    Path
        Ruta al archivo .csv.
    """
    return download_kaggle_dataset(ADULT_CENSUS_SLUG)