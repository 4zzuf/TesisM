import modelo
from modelo import param_simulacion

TIEMPO_REEMPLAZO = 4 / 60  # Tiempo fijo del intercambio en horas

def tiempo_promedio_para_autobuses(numero_autobuses):
    """Calcula el tiempo promedio de intercambio por autobús en minutos."""
    # Desactivar la verbosidad durante las simulaciones
    anterior = modelo.VERBOSE
    modelo.VERBOSE = False
    estacion = modelo.ejecutar_simulacion(max_autobuses=numero_autobuses)
    modelo.VERBOSE = anterior
    if estacion.intercambios_realizados == 0:
        return 0
    tiempo_total = (
        estacion.tiempo_espera_total
        + estacion.intercambios_realizados * TIEMPO_REEMPLAZO
    )
    return (tiempo_total / estacion.intercambios_realizados) * 60

def main():
    # Importar matplotlib solo cuando se ejecuta directamente para
    # evitar dependencias innecesarias al utilizar este módulo desde
    # otros scripts o durante las pruebas.
    import matplotlib.pyplot as plt

    max_autos = param_simulacion.max_autobuses
    valores = list(range(1, max_autos + 1))
    tiempos = [tiempo_promedio_para_autobuses(n) for n in valores]

    plt.figure(figsize=(8, 4))
    plt.plot(valores, tiempos, marker='o')
    plt.xlabel('Número de autobuses')
    plt.ylabel('Tiempo promedio de intercambio (minutos)')
    plt.title('Tiempo promedio de intercambio por número de autobuses')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()
