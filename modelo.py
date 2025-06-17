import simpy
import random

from parametros import (
    ParametrosBateria,
    ParametrosEstacion,
    ParametrosOperacionBus,
    ParametrosEconomicos,
    ParametrosSimulacion,
)


param_bateria = ParametrosBateria()
param_estacion = ParametrosEstacion()
param_operacion = ParametrosOperacionBus()
param_economicos = ParametrosEconomicos()
param_simulacion = ParametrosSimulacion()

# Controla la verbosidad de la simulación
VERBOSE = True

# Función para formatear horas decimales a formato hh:mm
def formato_hora(horas_decimales):
    horas, minutos = divmod(horas_decimales * 60, 60)
    return f"{int(horas):02}:{int(minutos):02}"

def calcular_soc_inicial(hora_actual):
    """Calcula el SoC inicial basado en la hora actual."""
    if 7 <= hora_actual < 9 or 18 <= hora_actual < 20:  # Hora punta de autobuses
        soc_inicial = random.uniform(10, 20)  # SoC entre 10% y 20%
    else:  # Fuera de hora punta de autobuses
        soc_inicial = random.uniform(30, 40)  # SoC entre 30% y 40%
    return soc_inicial


class EstacionIntercambio:
    def __init__(self, env, capacidad_estacion):
        self.env = env
        self.estaciones = simpy.Resource(env, capacity=capacidad_estacion)
        self.baterias_disponibles = param_estacion.baterias_iniciales  # Baterías previamente cargadas
        self.tiempo_espera_total = 0  # Tiempo total de espera acumulado
        self.energia_total_cargada = 0  # Energía total consumida para cargar baterías
        self.costo_total_electrico = 0  # Costo total de carga eléctrica
        self.costo_total_petroleo = 0  # Costo total si se usara petróleo
        self.energia_punta_autobuses = 0  # Energía consumida en hora punta por autobuses
        self.energia_fuera_punta_autobuses = 0  # Energía consumida fuera de hora punta por autobuses
        self.energia_punta_electrica = 0  # Energía consumida en hora punta de electricidad

        # Costo de cargar las baterías iniciales
        self.cargar_baterias_iniciales()

    def cargar_baterias_iniciales(self):
        for _ in range(param_estacion.baterias_iniciales):
            hora_actual = 0  # Asumimos que se cargaron antes del inicio de la simulación
            capacidad_carga = param_bateria.capacidad
            if param_economicos.horas_punta[0] <= hora_actual < param_economicos.horas_punta[1]:  # Hora punta eléctrica
                costo_carga = capacidad_carga * param_economicos.costo_punta
            else:  # Hora fuera de punta
                costo_carga = capacidad_carga * param_economicos.costo_normal

            self.energia_total_cargada += capacidad_carga
            self.costo_total_electrico += costo_carga

    def reemplazar_bateria(self, autobuses_id, soc_inicial, hora_actual):
        inicio_espera = self.env.now
        while self.baterias_disponibles <= 0:  # Si no hay baterías disponibles
            if VERBOSE:
                print(f"Autobús {autobuses_id} espera porque no hay baterías disponibles en {formato_hora(self.env.now)}")
            yield self.env.timeout(1)  # Espera 1 hora antes de intentar nuevamente

        # Registra el tiempo total de espera acumulado
        tiempo_espera = self.env.now - inicio_espera
        self.tiempo_espera_total += tiempo_espera

        # Proceso de reemplazo
        self.baterias_disponibles -= 1
        capacidad_requerida = (param_bateria.soc_objetivo - soc_inicial) / 100 * param_bateria.capacidad
        tiempo_reemplazo = 4 / 60  # 4 minutos en horas
        hora_final = self.env.now + tiempo_reemplazo  # Hora después del intercambio
        if VERBOSE:
            print(
                f"Autobús {autobuses_id} reemplaza su batería en {formato_hora(self.env.now)} "
                f"(SoC inicial: {soc_inicial:.2f}%). Hora final: {formato_hora(hora_final)}"
            )
        yield self.env.timeout(tiempo_reemplazo)

        # Clasificar consumo de energía según hora punta de autobuses
        if 7 <= hora_actual < 9 or 18 <= hora_actual < 20:
            self.energia_punta_autobuses += capacidad_requerida
        else:
            self.energia_fuera_punta_autobuses += capacidad_requerida

        # Clasificar consumo según hora punta de electricidad
        if param_economicos.horas_punta[0] <= hora_actual < param_economicos.horas_punta[1]:  # Hora punta eléctrica
            self.energia_punta_electrica += capacidad_requerida

        # Costo si se usara petróleo
        costo_petroleo = (1 - soc_inicial / 100) * param_economicos.costo_petroleo_completo
        self.costo_total_petroleo += costo_petroleo

    def cargar_bateria(self):
        while True:
            # Hora actual en la simulación
            hora_actual = int(self.env.now % 24)
            if self.baterias_disponibles < param_estacion.total_baterias:
                with self.estaciones.request() as req:
                    yield req  # Adquiere un cargador disponible
                    capacidad_carga = param_bateria.capacidad
                    tiempo_carga = capacidad_carga / param_bateria.potencia_carga

                    if param_economicos.horas_punta[0] <= hora_actual < param_economicos.horas_punta[1]:  # Hora punta eléctrica
                        costo_carga = capacidad_carga * param_economicos.costo_punta
                        if VERBOSE:
                            print(
                                f"Se está cargando una batería en hora punta (Hora actual: {hora_actual})"
                            )
                    else:  # Hora fuera de punta
                        costo_carga = capacidad_carga * param_economicos.costo_normal
                        if VERBOSE:
                            print(
                                f"Se está cargando una batería fuera de hora punta (Hora actual: {hora_actual})"
                            )

                    yield self.env.timeout(tiempo_carga)
                    self.baterias_disponibles += 1
                    self.energia_total_cargada += capacidad_carga
                    self.costo_total_electrico += costo_carga
            else:
                yield self.env.timeout(1)  # Espera 1 hora antes de verificar nuevamente


# Procesos para simular la llegada de autobuses
def llegada_autobuses(env, estacion, max_autobuses, intervalo=0.25):
    """Genera la llegada de autobuses en intervalos dados."""
    yield env.timeout(5)  # Los autobuses comienzan a llegar a las 5:00 AM
    autobuses_id = 0
    while autobuses_id < max_autobuses:
        yield env.timeout(intervalo)
        autobuses_id += 1
        hora_actual = int(env.now % 24)
        soc_inicial = calcular_soc_inicial(hora_actual)
        if VERBOSE:
            print(
                f"Autobús {autobuses_id} llega a la estación en {formato_hora(env.now)} "
                f"(Hora actual: {hora_actual}, SoC inicial: {soc_inicial:.2f}%)"
            )
        env.process(proceso_autobus(env, estacion, autobuses_id, soc_inicial, hora_actual))


# Proceso para simular el flujo del autobús
def proceso_autobus(env, estacion, autobuses_id, soc_inicial, hora_actual):
    llegada = env.now
    with estacion.estaciones.request() as req:
        yield req
        tiempo_espera = env.now - llegada
        estacion.tiempo_espera_total += tiempo_espera
        if VERBOSE:
            print(
                f"Autobús {autobuses_id} entra a la estación en {formato_hora(env.now)} "
                f"tras esperar {formato_hora(tiempo_espera)}"
            )
        yield env.process(estacion.reemplazar_bateria(autobuses_id, soc_inicial, hora_actual))


# Configuración de la simulación
def ejecutar_simulacion(
    max_autobuses=param_simulacion.max_autobuses,
    duracion=param_simulacion.duracion,
    intervalo_llegada=0.25,
):
    """Ejecuta la simulación y devuelve la estación resultante."""
    random.seed(param_simulacion.semilla)
    env = simpy.Environment()
    estacion = EstacionIntercambio(env, param_estacion.capacidad_estacion)

    env.process(
        llegada_autobuses(env, estacion, max_autobuses=max_autobuses, intervalo=intervalo_llegada)
    )
    env.process(estacion.cargar_bateria())

    env.run(until=duracion)
    return estacion


def imprimir_resultados(estacion):
    """Muestra por pantalla los resultados de la simulación."""
    print(
        f"\nConsumo total de energía en hora punta de autobuses: {estacion.energia_punta_autobuses:.2f} kWh"
    )
    print(
        f"Consumo total de energía fuera de hora punta de autobuses: {estacion.energia_fuera_punta_autobuses:.2f} kWh"
    )
    print(
        f"Consumo total de energía en hora punta de electricidad: {estacion.energia_punta_electrica:.2f} kWh"
    )
    print(f"Tiempo total de espera acumulado: {formato_hora(estacion.tiempo_espera_total)}")
    print(f"Costo total de operación (eléctrico): S/. {estacion.costo_total_electrico:.2f}")
    print(f"\nCosto total usando electricidad: S/. {estacion.costo_total_electrico:.2f}")
    print(f"Costo total usando petróleo: S/. {estacion.costo_total_petroleo:.2f}")

    if estacion.costo_total_electrico < estacion.costo_total_petroleo:
        print("Es más barato operar con electricidad.")
    else:
        print("Es más barato operar con petróleo.")


if __name__ == "__main__":
    estacion = ejecutar_simulacion()
    imprimir_resultados(estacion)


