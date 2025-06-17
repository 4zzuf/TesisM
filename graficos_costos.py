import matplotlib.pyplot as plt
import modelo
from modelo import param_simulacion

TIEMPO_REEMPLAZO = 4 / 60  # Tiempo de intercambio de la batería en horas

def datos_para_autobuses(numero_autobuses):
    """Devuelve costos y consumos para la cantidad dada de autobuses."""
    anterior = modelo.VERBOSE
    modelo.VERBOSE = False
    estacion = modelo.ejecutar_simulacion(max_autobuses=numero_autobuses)
    modelo.VERBOSE = anterior
    factor = 720 / param_simulacion.duracion
    costo_electrico = estacion.costo_total_electrico * factor
    costo_gas = estacion.costo_total_gas * factor
    energia_punta = estacion.energia_punta_electrica * factor
    energia_fuera = (estacion.energia_total_cargada - estacion.energia_punta_electrica) * factor
    return costo_electrico, costo_gas, energia_punta, energia_fuera

def main():
    max_autos = param_simulacion.max_autobuses
    valores = list(range(1, max_autos + 1))
    resultados = [datos_para_autobuses(n) for n in valores]
    costos_elec, costos_gas, energias_punta, energias_fuera = zip(*resultados)

    # Gráfico de costo eléctrico
    plt.figure(figsize=(8, 4))
    plt.plot(valores, costos_elec, marker='o')
    plt.xlabel('Número de autobuses')
    plt.ylabel('Costo eléctrico (S/.)')
    plt.title('Costo de operación con electricidad')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Costo por hora de operación usando el máximo de autobuses
    anterior = modelo.VERBOSE
    modelo.VERBOSE = False
    estacion = modelo.ejecutar_simulacion()
    modelo.VERBOSE = anterior
    costo_e_hora = estacion.costo_total_electrico / param_simulacion.duracion
    costo_g_hora = estacion.costo_total_gas / param_simulacion.duracion

    plt.figure(figsize=(6, 4))
    etiquetas = ['Electricidad/hora', 'Gas natural/hora']
    valores_bar = [costo_e_hora, costo_g_hora]
    plt.bar(etiquetas, valores_bar, color=['tab:blue', 'tab:orange'])
    plt.ylabel('Costo (S/./h)')
    plt.title('Costo promedio por hora de operación')
    plt.tight_layout()
    plt.show()

    # Comparación de electricidad vs gas
    plt.figure(figsize=(8, 4))
    plt.plot(valores, costos_elec, marker='o', label='Electricidad')
    plt.plot(valores, costos_gas, marker='s', label='Gas natural')
    plt.xlabel('Número de autobuses')
    plt.ylabel('Costo (S/.)')
    plt.title('Comparación de costos de operación')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Consumo en hora punta vs fuera de punta
    plt.figure(figsize=(8, 4))
    plt.plot(valores, energias_punta, marker='o', label='Hora punta')
    plt.plot(valores, energias_fuera, marker='s', label='Fuera de punta')
    plt.xlabel('Número de autobuses')
    plt.ylabel('Consumo eléctrico (kWh)')
    plt.title('Consumo en hora punta y fuera de punta')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()
