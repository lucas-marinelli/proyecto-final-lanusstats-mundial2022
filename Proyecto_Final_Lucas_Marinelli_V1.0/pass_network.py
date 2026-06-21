"""
Modulo de Pass Network - utilidad reusable para datos StatsBomb.

El Pass Network es la visualizacion estandar de "estructura de equipo"
en football analytics. Muestra:
- Nodos = jugadores en su posicion promedio
- Lineas entre nodos = pases entre ese par de jugadores
- Grosor de linea = cantidad de pases
- Tamano de nodo = participacion del jugador

Convencion: se calcula HASTA EL PRIMER CAMBIO porque despues la
estructura del equipo cambia.

Uso tipico:
    from pass_network import calcular_pass_network, dibujar_pass_network
    posiciones, conexiones = calcular_pass_network(ev, 'Argentina')
    dibujar_pass_network(posiciones, conexiones, 'Argentina', ax=ax)

Inspirado en el tutorial oficial de mplsoccer:
    https://mplsoccer.readthedocs.io/en/latest/gallery/pass_plots/plot_pass_network.html
"""
from __future__ import annotations
import numpy as np
import pandas as pd


def _extraer_coord(loc, idx):
    """Extrae componente idx (0=x, 1=y) de un location StatsBomb (puede ser np.ndarray)."""
    if isinstance(loc, (list, tuple, np.ndarray)) and len(loc) > idx:
        return loc[idx]
    return np.nan


def calcular_pass_network(ev: pd.DataFrame,
                           equipo: str,
                           min_pases_conexion: int = 3) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Calcula los nodos y conexiones del Pass Network de un equipo.

    Parametros
    ----------
    ev : DataFrame de eventos del partido (1 partido completo, ambos equipos)
    equipo : nombre del equipo
    min_pases_conexion : minimo de pases entre 2 jugadores para que la conexion
                        cuente como linea. Default 3.

    Devuelve
    --------
    posiciones : DataFrame con columnas (player, x_avg, y_avg, n_pases)
    conexiones : DataFrame con columnas (pasador, receptor, n_pases)
    """
    # === 1. Identificar primer cambio del equipo ===
    sustituciones = ev[(ev["type"] == "Substitution") & (ev["team"] == equipo)]
    if not sustituciones.empty:
        primer_cambio_min = sustituciones["minute"].min()
    else:
        primer_cambio_min = 200  # no hubo cambios, uso todo el partido

    # === 2. Filtrar eventos hasta el primer cambio + del equipo ===
    ev_pre = ev[(ev["minute"] < primer_cambio_min) & (ev["team"] == equipo)].copy()

    # === 3. Extraer coordenadas si no estan ===
    if "x" not in ev_pre.columns:
        ev_pre["x"] = ev_pre["location"].apply(lambda loc: _extraer_coord(loc, 0))
        ev_pre["y"] = ev_pre["location"].apply(lambda loc: _extraer_coord(loc, 1))

    # === 4. Posiciones promedio + cantidad de eventos por jugador ===
    pos_por_jugador = (ev_pre.dropna(subset=["x", "y"])
                       .groupby("player")
                       .agg(x_avg=("x", "mean"),
                            y_avg=("y", "mean"),
                            n_eventos=("type", "count"))
                       .reset_index())

    # === 5. Filtrar solo pases completados con receptor identificado ===
    pases = ev_pre[(ev_pre["type"] == "Pass") &
                   (ev_pre["pass_outcome"].isna()) &
                   (ev_pre["pass_recipient"].notna())].copy()

    # Cantidad total de pases por pasador (para tamano del nodo)
    n_pases_jugador = (pases.groupby("player").size()
                       .rename("n_pases").reset_index())
    posiciones = pos_por_jugador.merge(n_pases_jugador, on="player", how="left")
    posiciones["n_pases"] = posiciones["n_pases"].fillna(0).astype(int)

    # === 6. Conexiones pasador <-> receptor (no dirigidas) ===
    # Normalizo el par para que (A,B) y (B,A) se sumen juntos
    pares = pases[["player", "pass_recipient"]].copy()
    pares.columns = ["pasador", "receptor"]
    pares["par_norm"] = pares.apply(
        lambda r: tuple(sorted([r["pasador"], r["receptor"]])), axis=1
    )
    conex = (pares.groupby("par_norm").size().rename("n_pases").reset_index())
    conex["pasador"] = conex["par_norm"].apply(lambda t: t[0])
    conex["receptor"] = conex["par_norm"].apply(lambda t: t[1])
    conex = conex[["pasador", "receptor", "n_pases"]]

    # Filtrar conexiones con pocos pases
    conex = conex[conex["n_pases"] >= min_pases_conexion]

    # Quedarme solo con jugadores que tienen al menos algun pase
    posiciones = posiciones[posiciones["n_pases"] > 0]

    return posiciones, conex


def dibujar_pass_network(posiciones: pd.DataFrame,
                          conexiones: pd.DataFrame,
                          equipo: str,
                          ax,
                          pitch,
                          color_nodo: str,
                          color_linea: str,
                          color_texto: str = "white"):
    """Dibuja el Pass Network en un eje matplotlib ya con pitch.

    Parametros
    ----------
    posiciones, conexiones : output de calcular_pass_network()
    equipo : nombre del equipo (para titulos)
    ax : matplotlib Axes con un pitch ya dibujado
    pitch : objeto mplsoccer.Pitch o VerticalPitch ya dibujado
    color_nodo, color_linea : colores
    color_texto : color del nombre de los jugadores
    """
    # === 1. Dibujar conexiones (lineas) primero (van debajo) ===
    pos_dict = posiciones.set_index("player")[["x_avg", "y_avg"]].to_dict("index")

    if not conexiones.empty:
        max_conex = conexiones["n_pases"].max()
        for _, row in conexiones.iterrows():
            if row["pasador"] not in pos_dict or row["receptor"] not in pos_dict:
                continue
            p1 = pos_dict[row["pasador"]]
            p2 = pos_dict[row["receptor"]]
            # Grosor proporcional a la cantidad de pases
            grosor = 1 + (row["n_pases"] / max_conex) * 6
            alpha_ln = 0.35 + (row["n_pases"] / max_conex) * 0.55
            pitch.lines(p1["x_avg"], p1["y_avg"], p2["x_avg"], p2["y_avg"],
                        ax=ax, lw=grosor, color=color_linea,
                        alpha=alpha_ln, zorder=2)

    # === 2. Dibujar nodos (circulos) ===
    if not posiciones.empty:
        max_pases = posiciones["n_pases"].max()
        sizes = 200 + (posiciones["n_pases"] / max_pases) * 800
        pitch.scatter(posiciones["x_avg"], posiciones["y_avg"], s=sizes,
                      ax=ax, color=color_nodo, edgecolors=color_texto,
                      linewidth=1.5, alpha=0.95, zorder=4)

        # === 3. Etiquetas con nombres bonitos (apellido conocido) ===
        # Importa nombre_bonito del modulo en V0 (centralizado)
        try:
            from nombres_bonitos import nombre_bonito
        except ImportError:
            # Fallback si el modulo no esta disponible
            def nombre_bonito(p, formato="apellido"):
                partes = p.split()
                return partes[-1] if len(partes) >= 1 else p

        for _, row in posiciones.iterrows():
            etiqueta = nombre_bonito(row["player"], formato="apellido")
            ax.text(row["x_avg"], row["y_avg"] + 4, etiqueta,
                    ha="center", va="center", color=color_texto,
                    fontsize=8, weight="bold", zorder=5)
