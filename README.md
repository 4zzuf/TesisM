# PrimerRepo

Este repositorio contiene utilidades para simulación.

## Gráfico de tiempo de intercambio

Ejecuta el script `tiempos_intercambio.py` para generar un gráfico que muestra
el tiempo promedio de intercambio según cuántos autobuses llegan a la estación.
Cada intercambio dura 4 minutos más el tiempo de espera de los autobuses cuando
las estaciones de carga están ocupadas. El script agrupa a todos los autobuses
de la simulación para reflejar esta cola:

```bash
python tiempos_intercambio.py
```

Se abrirá una ventana con la gráfica correspondiente.

## Ejecutar las pruebas

Instala `pytest` y ejecuta las pruebas con:

```bash
pytest
```
