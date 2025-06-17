class ParametrosBateria:
    """Parámetros relacionados a la batería."""

    def __init__(self, potencia_carga=100, capacidad=300, soc_objetivo=100):
        self.potencia_carga = potencia_carga
        self.capacidad = capacidad
        self.soc_objetivo = soc_objetivo

    def actualizar(self, potencia=None, capacidad=None, soc_objetivo=None):
        """Actualiza los valores de la batería según se necesite."""
        if potencia is not None:
            self.potencia_carga = potencia
        if capacidad is not None:
            self.capacidad = capacidad
        if soc_objetivo is not None:
            self.soc_objetivo = soc_objetivo
