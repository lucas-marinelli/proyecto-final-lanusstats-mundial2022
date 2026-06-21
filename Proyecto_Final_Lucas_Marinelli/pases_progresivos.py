"""
Modulo de pases progresivos - utilidad reusable para datos StatsBomb.

Definicion: un pase progresivo es un pase completado que avanza >=10 metros
hacia el arco rival (configurable por umbral_metros).

Uso tipico:
    from pases_progresivos import agregar_pases_progresivos
    pases = ev[ev["type"] == "Pass"]
    pases = agregar_pases_progresivos(pases)
    n_prog = pases["es_progresivo"].sum()

NOTA: statsbombpy devuelve `location` y `pass_end_location` como np.ndarray.
Por eso el isinstance acepta list, tuple Y np.ndarray.
"""
from __future__ import annotations
import numpy as np
import pandas as pd


def _extraer_coord(loc, idx):
    """Extrae el componente `idx` (0=x, 1=y) de un location de StatsBomb.

    StatsBomb puede devolver location como list, tuple o np.ndarray segun
    cargador. Tambien puede ser NaN cuando no hay coordenadas.
    """
    if isinstance(loc, (list, tuple, np.ndarray)) and len(loc) > idx:
        return loc[idx]
    return np.nan


def agregar_pases_progresivos(pases_df: pd.DataFrame,
                               umbral_metros: float = 10.0) -> pd.DataFrame:
    """Agrega columnas progresivas a un DataFrame de pases StatsBomb.

    Columnas nuevas:
        - x, y, x_end, y_end : coordenadas del pase
        - avance_x           : metros que avanzo (positivo = hacia adelante)
        - es_completado      : pase llego al destinatario
        - es_progresivo      : completado Y avance_x >= umbral_metros
    """
    df = pases_df.copy()

    if "x" not in df.columns:
        df["x"] = df["location"].apply(lambda loc: _extraer_coord(loc, 0))
        df["y"] = df["location"].apply(lambda loc: _extraer_coord(loc, 1))

    df["x_end"] = df["pass_end_location"].apply(lambda loc: _extraer_coord(loc, 0))
    df["y_end"] = df["pass_end_location"].apply(lambda loc: _extraer_coord(loc, 1))

    df["avance_x"]      = df["x_end"] - df["x"]
    df["es_completado"] = df["pass_outcome"].isna()
    df["es_progresivo"] = df["es_completado"] & (df["avance_x"] >= umbral_metros)

    return df
