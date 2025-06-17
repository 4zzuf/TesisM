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


class Bateria:
    """Representa una batería individual."""

    def __init__(self, capacidad_inicial):
        self.capacidad = capacidad_inicial


class EstacionIntercambio:
    def __init__(self, env, capacidad_estacion):
        self.env = env
        self.estaciones = simpy.Resource(env, capacity=capacidad_estacion)

        # Listas de baterías según su estado
        self.baterias_disponibles = []  # Totalmente cargadas
        self.baterias_descargadas = []  # Necesitan recarga
        self.baterias_en_uso = []  # Se encuentran en los autobuses

        self.tiempo_espera_total = 0
        self.energia_total_cargada = 0
        self.costo_total_electrico = 0
        self.energia_punta_autobuses = 0
        self.energia_fuera_punta_autobuses = 0
        self.energia_punta_electrica = 0

        # Crear todas las baterías y realizar la carga inicial
        self._inicializar_baterias()

    def _inicializar_baterias(self):
        """Genera las baterías y aplica la primera carga."""
        for i in range(param_estacion.total_baterias):
            bateria = Bateria(param_bateria.capacidad)
            if i < param_estacion.baterias_iniciales:
                self._cargar_bateria_inicial(bateria)
                self.baterias_disponibles.append(bateria)
            else:
                # Asumimos que el resto está en uso al iniciar la simulación
                self.baterias_en_uso.append(bateria)

    def _cargar_bateria_inicial(self, bateria):
        """Carga una batería al comienzo de la simulación."""
        hora_actual = 0
        capacidad_carga = bateria.capacidad
        if param_economicos.horas_punta[0] <= hora_actual < param_economicos.horas_punta[1]:
            costo_carga = capacidad_carga * param_economicos.costo_punta
        else:
            costo_carga = capacidad_carga * param_economicos.costo_normal
        self.energia_total_cargada += capacidad_carga
        self.costo_total_electrico += costo_carga


    def reemplazar_bateria(self, autobuses_id, soc_inicial, hora_actual):
        inicio_espera = self.env.now
        while not self.baterias_disponibles:
            print(
                f"Autobús {autobuses_id} espera porque no hay baterías disponibles en {formato_hora(self.env.now)}"
            )
            yield self.env.timeout(1)

        # Registra el tiempo total de espera acumulado
        tiempo_espera = self.env.now - inicio_espera
        self.tiempo_espera_total += tiempo_espera

        # Batería usada que retorna el autobús
        if self.baterias_en_uso:
            bateria_descargada = self.baterias_en_uso.pop(0)
        else:
            bateria_descargada = Bateria(param_bateria.capacidad)
        self.baterias_descargadas.append(bateria_descargada)

        # Batería cargada que se entrega al autobús
        bateria_entregada = self.baterias_disponibles.pop(0)
        self.baterias_en_uso.append(bateria_entregada)

        capacidad_requerida = (
            (param_bateria.soc_objetivo - soc_inicial) / 100 * bateria_descargada.capacidad
        )
        tiempo_reemplazo = 0.083  # 5 minutos en horas
        hora_final = self.env.now + tiempo_reemplazo
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


    def cargar_bateria(self):
        while True:
            hora_actual = int(self.env.now % 24)
            if self.baterias_descargadas:
                with self.estaciones.request() as req:
                    yield req
                    bateria = self.baterias_descargadas.pop(0)
                    capacidad_carga = bateria.capacidad
                    tiempo_carga = capacidad_carga / param_bateria.potencia_carga

                    if param_economicos.horas_punta[0] <= hora_actual < param_economicos.horas_punta[1]:
                        costo_carga = capacidad_carga * param_economicos.costo_punta
                        print(f"Se está cargando una batería en hora punta (Hora actual: {hora_actual})")
                    else:
                        costo_carga = capacidad_carga * param_economicos.costo_normal
                        print(f"Se está cargando una batería fuera de hora punta (Hora actual: {hora_actual})")

                    yield self.env.timeout(tiempo_carga)
                    self.energia_total_cargada += capacidad_carga
                    self.costo_total_electrico += costo_carga
                    self.baterias_disponibles.append(bateria)
            else:
                yield self.env.timeout(1)


# Procesos para simular la llegada de autobuses
def llegada_autobuses(env, estacion, max_autobuses):
    yield env.timeout(5)  # Los autobuses comienzan a llegar a las 5:00 AM
    autobuses_id = 0
    while autobuses_id < max_autobuses:
        yield env.timeout(0.25)  # Intervalo de 15 minutos entre llegadas
        autobuses_id += 1
        hora_actual = int(env.now % 24)
        soc_inicial = calcular_soc_inicial(hora_actual)
        print(f"Autobús {autobuses_id} llega a la estación en {formato_hora(env.now)} "
              f"(Hora actual: {hora_actual}, SoC inicial: {soc_inicial:.2f}%)")
        env.process(proceso_autobus(env, estacion, autobuses_id, soc_inicial, hora_actual))


# Proceso para simular el flujo del autobús
def proceso_autobus(env, estacion, autobuses_id, soc_inicial, hora_actual):
    llegada = env.now
    with estacion.estaciones.request() as req:
        yield req
        tiempo_espera = env.now - llegada
        estacion.tiempo_espera_total += tiempo_espera
        print(f"Autobús {autobuses_id} entra a la estación en {formato_hora(env.now)} "
              f"tras esperar {formato_hora(tiempo_espera)}")
        yield env.process(estacion.reemplazar_bateria(autobuses_id, soc_inicial, hora_actual))


# Configuración de la simulación
random.seed(param_simulacion.semilla)
env = simpy.Environment()
estacion = EstacionIntercambio(env, param_estacion.capacidad_estacion)

# Procesos: Llegada de autobuses y carga de baterías
env.process(llegada_autobuses(env, estacion, max_autobuses=param_simulacion.max_autobuses))
env.process(estacion.cargar_bateria())  # Proceso continuo de carga de baterías

# Ejecutar la simulación
env.run(until=param_simulacion.duracion)  # Simula por la duración indicada

# Resultados
print(f"\nConsumo total de energía en hora punta de autobuses: {estacion.energia_punta_autobuses:.2f} kWh")
print(f"Consumo total de energía fuera de hora punta de autobuses: {estacion.energia_fuera_punta_autobuses:.2f} kWh")
print(f"Consumo total de energía en hora punta de electricidad: {estacion.energia_punta_electrica:.2f} kWh")
print(f"Tiempo total de espera acumulado: {formato_hora(estacion.tiempo_espera_total)}")
print(f"Costo total de operación (eléctrico): S/. {estacion.costo_total_electrico:.2f}")


