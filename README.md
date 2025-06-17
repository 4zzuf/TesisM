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

## Ejecutar las pruebas

Instala `pytest` y ejecuta las pruebas con:

```bash
pytest
```
