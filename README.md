# PrimerRepo

Este repositorio contiene utilidades para simulación.

## Gráfico de eficiencia operativa

Ejecuta el script `tiempos_intercambio.py` para visualizar el tiempo de
operación promedio por autobús. El valor incluye la espera en cola y el
intercambio de la batería (4 minutos) y se expresa en minutos. El script
agrupa a todos los autobuses de la simulación para reflejar la cola:

```bash
python tiempos_intercambio.py
```

Se abrirá una ventana con la gráfica correspondiente.

## Gráficos de costos y consumos

El script `graficos_costos.py` genera tres gráficos:

1. Costo de operación con electricidad según el número de autobuses.
2. Comparación de costos usando electricidad y gas natural.
3. Consumo eléctrico en hora punta y fuera de punta.

Ejecuta:

```bash
python graficos_costos.py
```

## Ejecutar las pruebas

Instala `pytest` y ejecuta las pruebas con:

```bash
pytest
```
