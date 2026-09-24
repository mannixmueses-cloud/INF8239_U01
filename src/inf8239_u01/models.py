"""Construcción de modelos para la Unidad 01 de INF-8239."""

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC


def build_svm(C=1.0, gamma="scale"):
    """Construye un pipeline de escalado y clasificación SVM.

    Parameters
    ----------
    C : float
        Parámetro de regularización. Debe ser positivo.
    gamma : str or float
        Coeficiente del kernel RBF.

    Returns
    -------
    sklearn.pipeline.Pipeline
        Pipeline con StandardScaler y SVC.
    """
    if C <= 0:
        raise ValueError("C debe ser positivo")

    return Pipeline([
        ("scale", StandardScaler()),
        (
            "model",
            SVC(
                C=C,
                gamma=gamma,
                kernel="rbf",
                probability=True,
                random_state=42
            )
        )
    ])