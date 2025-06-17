import matplotlib.pyplot as plt
import modelo
from modelo import param_simulacion, param_economicos


def emisiones(numero_autobuses):
    anterior = modelo.VERBOSE
    modelo.VERBOSE = False
    estacion = modelo.ejecutar_simulacion(max_autobuses=numero_autobuses)
    modelo.VERBOSE = anterior
    factor = 720 / param_simulacion.duracion
    emis_elec = (
        estacion.energia_total_cargada * param_economicos.factor_co2_elec * factor / 1000
    )
    emis_gas = (
        estacion.energia_total_gas * param_economicos.factor_co2_gas * factor / 1000
    )
    return emis_elec, emis_gas


def main():
    max_autos = param_simulacion.max_autobuses
    valores = list(range(1, max_autos + 1))
    emisiones_por_bus = [emisiones(n) for n in valores]
    emis_elec, emis_gas = zip(*emisiones_por_bus)
    ahorros = [g - e for e, g in zip(emis_elec, emis_gas)]

    # Emisiones mensuales
    plt.figure(figsize=(8, 4))
    plt.plot(valores, emis_elec, marker='o', label='Electricidad')
    plt.plot(valores, emis_gas, marker='s', label='Gas natural')
    plt.xlabel('Número de autobuses')
    plt.ylabel('Emisiones (toneladas/mes)')
    plt.title('Emisiones de CO2 por tipo de energía')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Ahorro de emisiones
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
