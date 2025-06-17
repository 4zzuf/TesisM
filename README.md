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

El script `graficos_costos.py` genera cuatro gráficos:

1. Costo de operación con electricidad según el número de autobuses.
2. Comparación de costos usando electricidad y gas natural.
3. Consumo eléctrico en hora punta y fuera de punta.
4. Costo de operación por hora para ambas tecnologías.

El último gráfico presenta dos barras con el costo promedio por hora al operar
con gas natural frente a electricidad.

Los valores se escalan a un mes de operación para evitar distorsiones cuando
la simulación se ejecuta por 500 horas.

Es posible notar que el costo eléctrico disminuye ligeramente al pasar de
cuatro a cinco autobuses porque el incremento de la cola reduce la cantidad de
ciclos de carga que la estación puede completar por hora. A partir de unos diez
vehículos la capacidad de los cargadores queda saturada y los costos totales se
mantienen casi constantes.

Ejecuta:

```bash
python graficos_costos.py
```

## Ahorro de emisiones

Ejecuta `graficos_emisiones.py` para comparar las emisiones mensuales con
electricidad y gas natural. El gráfico incluye las emisiones de cada tecnología
y una barra adicional con el ahorro total de CO₂:

```bash
python graficos_emisiones.py
```

## Ejecutar las pruebas

Instala `pytest` y ejecuta las pruebas con:

```bash
pytest
```
