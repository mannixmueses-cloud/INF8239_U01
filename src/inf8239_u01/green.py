def pareto_flags(df, score="f1_macro", cost="fit_median_s"):
    """
    Marca qué filas de df están en la frontera de Pareto, considerando
    score a maximizar (por ejemplo F1 macro) y cost a minimizar (por
    ejemplo tiempo de ajuste).

    Parameters
    ----------
    df : pandas.DataFrame
        Tabla con al menos las columnas score y cost.
    score : str
        Nombre de la columna a maximizar.
    cost : str
        Nombre de la columna a minimizar.

    Returns
    -------
    list[bool]
        Una bandera por fila: True si esa fila no está dominada por
        ninguna otra (es decir, pertenece a la frontera de Pareto).
    """
    flags = []
    for _, row in df.iterrows():
        dominated = ((df[score] >= row[score]) & (df[cost] <= row[cost]) &
                     ((df[score] > row[score]) | (df[cost] < row[cost]))).any()
        flags.append(not bool(dominated))
    return flags