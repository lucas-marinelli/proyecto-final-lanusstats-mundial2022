# Proyecto Final · Curso de Introducción al Análisis de Datos en el Fútbol con Python

**Curso:** [LanusStats](https://www.youtube.com/@LanusStats) · Director: Federico Rábanos
**Alumno:** Lucas Marinelli · [@datafutbol_ar](https://instagram.com/datafutbol_ar)
**Fecha de entrega:** 15 de junio de 2026 · **Aprobado:** 20 de junio de 2026

![Status](https://img.shields.io/badge/status-aprobado-brightgreen)
![Python](https://img.shields.io/badge/python-3.12-blue)
![Stack](https://img.shields.io/badge/stack-pandas%20%7C%20mplsoccer%20%7C%20statsbombpy-orange)
![License](https://img.shields.io/badge/license-MIT-blue)

---

## De qué se trata

Análisis del **Mundial 2022** con datos abiertos de **StatsBomb**, hecho como
proyecto final del curso de Federico Rábanos.

**Partido principal elegido:** *Argentina 1–2 Arabia Saudita* (debut Mundial 2022).
La final está hipersaturada de análisis — el debut casi nadie lo analizó y permite
una narrativa más fuerte: *"el equipo que dominó 6 de 8 métricas y aun así perdió 1–2"*.

**Jugador analizado:** Lionel Messi (juega los dos partidos del proyecto, ARG-SAU
debut y ARG-FRA final, lo cual permite contrastar al mismo jugador en distintos
contextos del torneo).

---

## Dos versiones

Este repo tiene **dos versiones** del proyecto, en carpetas paralelas:

| Carpeta | Versión | Estado |
|---|---|---|
| [`Proyecto_Final_Lucas_Marinelli/`](Proyecto_Final_Lucas_Marinelli/) | **V0** — lo que entregué al curso | ✅ aprobado por Federico Rábanos |
| [`Proyecto_Final_Lucas_Marinelli_V1.0/`](Proyecto_Final_Lucas_Marinelli_V1.0/) | **V1.0** — con las 5 correcciones del feedback | ✅ portfolio mejorado |

> 💡 La V1.0 mantiene la V0 intacta y agrega las correcciones en archivos
> separados. Ver el [`CHANGELOG`](Proyecto_Final_Lucas_Marinelli_V1.0/CHANGELOG.md)
> para el detalle de cada corrección aplicada.

---

## Stack técnico

| Categoría | Librerías |
|---|---|
| Datos | `statsbombpy` (open data del Mundial 2022) |
| Procesamiento | `pandas` · `numpy` · `pyarrow` |
| Visualización | `matplotlib` · `mplsoccer` (Pitch, VerticalPitch, PyPizza) |
| Estadística | `scipy.stats` |
| Helpers | `tqdm` |

Ver `requirements.txt` para la lista exacta.

---

## Cómo correrlo

### 1. Cloná el repo

```bash
git clone https://github.com/lucas-marinelli/proyecto-final-lanusstats-mundial2022.git
cd proyecto-final-lanusstats-mundial2022
```

### 2. Creá un entorno virtual e instalá las dependencias

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Configurá StatsBomb (gratis, registro rápido)

`statsbombpy` lee de los free open data de StatsBomb por default. No requiere API key
para el Mundial 2022.

### 4. Correr el setup inicial (una sola vez)

Abrí Jupyter y corré `Proyecto_Final_Lucas_Marinelli/00_setup.ipynb` una vez.
Esto descarga y cachea los 64 partidos del Mundial 2022 en `data/*.parquet`
(requiere internet). Las próximas veces todo lee del cache local.

### 5. Empezar por el notebook MAESTRO

`Proyecto_Final_Lucas_Marinelli/proyecto_final.ipynb` es el informe ejecutivo
con el índice y los hallazgos de cada punto. Recomiendo arrancar por ahí.

---

## Hallazgos destacados

### Partido ARG vs SAU

| Métrica | Argentina | Arabia Saudita |
|---|---:|---:|
| Goles | **1** | **2** ← ganó |
| Tiros | 15 | 3 |
| xG | 2.49 | 0.15 |
| Pases progresivos | 130 | 52 |
| Posesión | 63.9% | 36.1% |

> **Lección:** Argentina dominó 6 de 8 métricas pero perdió. La eficiencia
> decide partidos más que el dominio.

### Top 3 jugadores del Mundial 2022 (rankings propios)

| Ranking | Top 1 | Top 2 | Top 3 |
|---|---|---|---|
| Más tiros totales | Messi (32) | Mbappé (31) | Giroud (17) |
| Más pases completados | Rodri (644) | Otamendi (528) | De Paul (475) |
| Más recuperaciones | Amrabat (44) | Hakimi (43) | Modrić (39) |
| **Más pases progresivos** (propio) | Rodri (175) | Gvardiol (168) | Otamendi (155) |

### PyPizza de Messi en el Mundial 2022 (vs jugadores ofensivos del torneo)

En la **V1.0** las métricas están normalizadas per 90 minutos. Messi sigue siendo
top pero ya no es P100 en todo — aparecen matices:

- P99 en Goles/90 · **P100** en xG/90 · P99 en Tiros/90
- P65 en xG por tiro → tira desde más lejos que el promedio
- **P100** en Faltas recibidas/90 → el más fouleado del torneo
- P50 en Pases progresivos/90 → no es su rol principal vs volantes

---

## Identidad visual

Cada gráfico está hecho con la identidad de mi proyecto personal
[@datafutbol_ar](https://instagram.com/datafutbol_ar):

- **Combo C:** navy `#0E2A47` + celeste `#75AADB` + dorado `#C9A227`
- **Paleta semáforo CVD-safe** (Wong 2011) para evitar problemas de daltonismo
- **Formato 1080×1350 / 1080×1620 px** para carrusel Instagram

---

## Feedback de Federico Rábanos (20/6/2026)

Federico me devolvió 5 correcciones puntuales muy valiosas. Las apliqué todas
en la V1.0. Resumen:

| # | Corrección | Aplicada en |
|---|---|---|
| 1 | "Mapa de pases" = Pass Network, no mapa literal | `pass_network.py` + `punto_3_v1.ipynb` |
| 2 | Mostrar TODOS los pases del jugador (no solo progresivos) | `punto_4_v1.ipynb` |
| 3 | PyPizza: normalizar per 90 min, filtrar por muestra mínima | `punto_extra_v1.ipynb` |
| 4 | Shot maps con menos espacio entre ellos | `punto_5_v1.ipynb` |
| 5 | Leyendas que no estiren la imagen ni tapen datos | `punto_4_v1.ipynb` + `punto_5_v1.ipynb` |

Ver el [`CHANGELOG`](Proyecto_Final_Lucas_Marinelli_V1.0/CHANGELOG.md) completo
con el detalle técnico de cada corrección.

---

## Sobre mí

Vengo del rubro de **electromedicina y automatización** (16 años en OFIMED,
La Plata). Mi primer acercamiento al fútbol como disciplina fue un curso de
videoanálisis en la UP con Mati Conde. Terminé hace poco la **Carrera de Data
Analytics de Coderhouse** ([repo aquí](https://github.com/lucas-marinelli/proyecto-final-data-analytics))
y este curso de LanusStats fue mi siguiente paso lógico.

[@datafutbol_ar](https://instagram.com/datafutbol_ar) es mi vehículo editorial
para construir portfolio público como analista de fútbol en español, con foco
sudamericano y estética profesional. Próximo paso: aplicar el módulo Pass Network
a partidos del Mundial 2026 en vivo.

---

## Créditos y licencia

- **Datos:** [StatsBomb Open Data](https://github.com/statsbomb/open-data) (uso no comercial, fines educativos).
- **Librería de visualización:** [mplsoccer](https://mplsoccer.readthedocs.io/) de Andrew Rowlinson.
- **Inspiración técnica:** [LanusStats](https://github.com/lanusstats) de Federico Rábanos.
- **Código del proyecto:** [MIT License](LICENSE).

---

## Contacto

- **GitHub:** [lucas-marinelli](https://github.com/lucas-marinelli)
- **LinkedIn:** [linkedin.com/in/lucasmarinelli-data](https://linkedin.com/in/lucasmarinelli-data)
- **Instagram:** [@datafutbol_ar](https://instagram.com/datafutbol_ar)
- **Email:** lucasmarinelli_12@hotmail.com
