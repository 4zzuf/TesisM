import matplotlib.pyplot as plt

import modelo

from modelo import param_simulacion

TIEMPO_REEMPLAZO = 4 / 60  # Tiempo fijo del intercambio en horas

def tiempo_promedio_para_autobuses(numero_autobuses):
    """Calcula el tiempo promedio de permanencia por autobús en minutos."""
    # Desactivar la verbosidad durante las simulaciones
    anterior = modelo.VERBOSE
    modelo.VERBOSE = False
    estacion = modelo.ejecutar_simulacion(
        max_autobuses=numero_autobuses, intervalo_llegada=0
    )
    modelo.VERBOSE = anterior
    if estacion.intercambios_realizados == 0:
        return 0
    tiempo_total = (
        estacion.tiempo_espera_total
        + estacion.intercambios_realizados * TIEMPO_REEMPLAZO
    )
    return (tiempo_total / estacion.intercambios_realizados) * 60

def main():
    max_autos = param_simulacion.max_autobuses
    valores = list(range(1, max_autos + 1))
    tiempos = [tiempo_promedio_para_autobuses(n) for n in valores]

    plt.figure(figsize=(8, 4))
    plt.plot(valores, tiempos, marker='o')
    plt.xlabel('Número de autobuses')
    plt.ylabel('Tiempo promedio de operación (minutos)')
    plt.title('Eficiencia operativa de la estación')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()
