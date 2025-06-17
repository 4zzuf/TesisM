import matplotlib.pyplot as plt
import modelo
from modelo import param_simulacion, param_economicos


def main():
    """Muestra un gráfico comparando emisiones y el ahorro total de CO2."""
    anterior = modelo.VERBOSE
    modelo.VERBOSE = False
    estacion = modelo.ejecutar_simulacion()
    modelo.VERBOSE = anterior

    factor = 720 / param_simulacion.duracion
    emis_elec = (
        estacion.energia_total_cargada * param_economicos.factor_co2_elec * factor / 1000
    )
    emis_gas = (
        estacion.energia_total_gas * param_economicos.factor_co2_gas * factor / 1000
    )
    ahorro = emis_gas - emis_elec

    plt.figure(figsize=(6, 4))
    etiquetas = ['Electricidad', 'Gas natural', 'Ahorro de CO2']
    valores = [emis_elec, emis_gas, ahorro]
    plt.bar(etiquetas, valores, color=['tab:blue', 'tab:orange', 'tab:green'])
    plt.ylabel('Toneladas de CO2 por mes')
    plt.title('Comparación de emisiones mensuales')
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()
