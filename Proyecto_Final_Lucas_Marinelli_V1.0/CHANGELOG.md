# CHANGELOG · V1.0

**Fecha:** 20 jun 2026 (mismo día que recibí el feedback de Federico)
**Versión anterior entregada:** V0 (en la carpeta `../Proyecto_Final_Lucas_Marinelli/`)
**Feedback documentado en:** `G:\Mi unidad\DATAFUTBOL_AR\memory\context\lanusstats_feedback.md`

---

## Qué cambió respecto a V0

### ✅ Aplicado del feedback de Federico (4 de 5 correcciones)

| # | Corrección | Archivo V1.0 | Cómo lo resolví |
|---|---|---|---|
| **1** | "Mapa de pases" debería ser Pass Network, no mapa literal | `pass_network.py` + `punto_3_v1.ipynb` | Creé un módulo reusable que calcula nodos (jugadores en posición promedio hasta primer cambio) + conexiones (pases entre par, min 3). Lo apliqué a ambos equipos. |
| **2** | En el mapa de acciones de Messi mostrar TODOS los pases, no solo los progresivos | `punto_4_v1.ipynb` | Agregué capa de fondo con todos los pases completados (alpha 0.20) + capa resaltada con pases progresivos (alpha 0.75). Ahora se ve la circulación completa + énfasis en lo decisivo. |
| **4** | Shot maps del Dashboard A con mucho espacio en el medio | `punto_5_v1.ipynb` | Bajé `wspace=0.10 → 0.02` + reduje paddings internos del pitch (`pad_*=0.5`). Ahora los dos shot maps se leen como una pieza comparativa. |
| **5** | Leyenda de Messi que estiraba la imagen | `punto_4_v1.ipynb` | Cambié la leyenda de `bbox_to_anchor=(1, 1.13)` (afuera) a `loc='upper right'` (adentro del axes). El pitch ya no se distorsiona. |
| **3** | PyPizza con filtro de 10 tiros era poco robusto | `punto_extra_v1.ipynb` | Cambié el filtro a `minutos >= 270 + top P80 de muestra` y normalicé todas las métricas per 90 min. Grupo de comparación pasó de 23 a ~50 jugadores. |

### Resultado: 5 de 5 correcciones aplicadas en V1.0 ✅

---

## Estructura de la V1.0

```
Proyecto_Final_Lucas_Marinelli_V1.0/
├── CHANGELOG.md              ← este archivo
├── pass_network.py           ← módulo reusable nuevo
├── punto_3_v1.ipynb          ← agrega Pass Network
├── punto_4_v1.ipynb          ← pases todos de Messi + leyenda interna
├── punto_5_v1.ipynb          ← shot maps con menos espacio
├── punto_extra_v1.ipynb      ← PyPizza per 90 con grupo ampliado
└── outputs_v1/               ← visualizaciones nuevas
    ├── punto3_pass_network_argentina.png
    ├── punto3_pass_network_arabia.png
    ├── punto4_acciones_messi_v1.png
    ├── punto5_dashboard_partido_v1.png
    └── punto_extra_pizza_messi_v1.png
```

---

## Lo que NO se tocó

- **Puntos 1, 2, 6 y MAESTRO** quedan exactos a V0. Federico no los observó.
- **README.md** se queda en V0 (V1.0 es un agregado, no reemplaza la entrega).
- **outputs/** original en V0 queda intacto.
- **Módulos `helpers.py` y `pases_progresivos.py`** los reutilizo importando desde la carpeta de V0 (no duplico código).

---

## Cómo correr la V1.0

Los notebooks V1.0 importan helpers desde la carpeta V0:

```python
import sys
from pathlib import Path
V0_PATH = Path('..').resolve() / 'Proyecto_Final_Lucas_Marinelli'
sys.path.insert(0, str(V0_PATH))
from helpers import *
from pases_progresivos import agregar_pases_progresivos
```

Esto requiere que la carpeta V0 esté **al lado** de la V1.0 (que es como está acomodada).

Para correr cada notebook:
1. Abrir en VSCode
2. Restart Kernel
3. Run All

El cache de `data/` de V0 se reusa automáticamente — no hace falta volver a bajar partidos.

---

## Lecciones generales que me llevo

| # | Lección |
|---|---|
| 1 | "Mapa de pases" en football analytics = Pass Network. El literal es secundario. |
| 2 | Normalizar por tiempo (per 90) es la regla para comparar jugadores entre sí. |
| 3 | Siempre poner un piso de minutos jugados para descartar muestras chicas. |
| 4 | Leyendas siempre dentro del axes salvo casos con grilla dedicada. |
| 5 | Cuidar el wspace/hspace de gridspec: chico = relacionados, grande = no relacionados. |
| 6 | Cuando una consigna dice "pases" sin adjetivo, son TODOS. Los progresivos son subset. |

---

## Próximos pasos

- Aplicar el módulo `pass_network.py` a partidos del Mundial 2026 que arranca este mes — pieza editorial directa para @datafutbol_ar.
- En cualquier futuro PyPizza, recordar siempre normalizar per 90 min.
- Mantener este patrón "V0 entregado + V1.0 con feedback aplicado" para futuros cursos. Es buena práctica de portfolio: muestra que recibo feedback y itero.
