import matplotlib.pyplot as plt
import modelo
from modelo import param_simulacion, param_economicos


def ahorro_co2(numero_autobuses):
    anterior = modelo.VERBOSE
    modelo.VERBOSE = False
    estacion = modelo.ejecutar_simulacion(max_autobuses=numero_autobuses, intervalo_llegada=0)
    modelo.VERBOSE = anterior
    emis_elec = estacion.energia_total_cargada * param_economicos.factor_co2_elec
    emis_gas = estacion.energia_total_gas * param_economicos.factor_co2_gas
    factor = 720 / param_simulacion.duracion
    ahorro = (emis_gas - emis_elec) * factor / 1000
    return ahorro


def main():
    max_autos = param_simulacion.max_autobuses
    valores = list(range(1, max_autos + 1))
    ahorros = [ahorro_co2(n) for n in valores]

    plt.figure(figsize=(8, 4))
    plt.plot(valores, ahorros, marker='o')
    plt.xlabel('Número de autobuses')
    plt.ylabel('Ahorro de CO2 (toneladas/mes)')
    plt.title('Ahorro de emisiones de CO2')
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()
