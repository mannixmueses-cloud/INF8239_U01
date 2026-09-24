"""Descarga y almacenamiento reproducible de datasets de UCI."""

from pathlib import Path

import pandas as pd
from ucimlrepo import fetch_ucirepo


def download_uci_dataset(
    dataset_id: int = 545,
    destination: str = "data/raw/rice.csv"
) -> Path:
    """Descarga un dataset de UCI y lo guarda como CSV."""

    if not isinstance(dataset_id, int) or dataset_id <= 0:
        raise ValueError("dataset_id debe ser un entero positivo")

    dataset = fetch_ucirepo(id=dataset_id)

    features = dataset.data.features.copy()
    targets = dataset.data.targets.copy()

    if features.empty:
        raise ValueError("El dataset no contiene predictores")

    if targets.empty:
        raise ValueError("El dataset no contiene target")

    frame = pd.concat(
        [
            features.reset_index(drop=True),
            targets.reset_index(drop=True)
        ],
        axis=1
    )

    if frame.empty:
        raise ValueError("El dataset descargado está vacío")

    path = Path(destination)
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, index=False)

    return path