# PrimerRepo

Este repositorio contiene utilidades para simulación.

Las simulaciones por defecto abarcan 500 horas de operación.

## Gráfico de eficiencia operativa

Ejecuta el script `tiempos_intercambio.py` para visualizar el tiempo de
operación promedio por autobús. Cada vehículo efectúa una ruta de dos horas y
regresa con la batería al 20‑30 % de carga para un nuevo intercambio. El valor
incluye la espera en cola y el reemplazo de 4 minutos, expresado en minutos. El
script agrupa a todos los autobuses de la simulación para reflejar la cola:

```bash
python tiempos_intercambio.py
```

Se abrirá una ventana con la gráfica correspondiente.

## Gráficos de costos y consumos

El script `graficos_costos.py` genera tres gráficos:

1. Costo de operación con electricidad según el número de autobuses.
2. Comparación de costos usando electricidad y gas natural.
3. Consumo eléctrico en hora punta y fuera de punta.

Los valores se escalan a un mes de operación para evitar distorsiones cuando
la simulación se ejecuta por 500 horas.

Ejecuta:

```bash
python graficos_costos.py
```

## Ahorro de emisiones

Ejecuta `graficos_emisiones.py` para comparar las emisiones mensuales de CO₂
entre electricidad y gas natural. El script también muestra el ahorro mensual
obtenido al usar baterías en lugar de gas:

```bash
python graficos_emisiones.py
```

## Ejecutar las pruebas

Instala `pytest` y ejecuta las pruebas con:

```bash
pytest
```
