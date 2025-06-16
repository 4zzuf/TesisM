class ParametrosOperacionBus:
    """Parámetros de operación del autobús."""

    def __init__(self, costo_operacion_hora=50, penalizacion_espera=10):
        self.costo_operacion_hora = costo_operacion_hora
        self.penalizacion_espera = penalizacion_espera

    def actualizar(self, costo=None, penalizacion=None):
        """Permite modificar el costo de operación o la penalización."""
        if costo is not None:
            self.costo_operacion_hora = costo
        if penalizacion is not None:
            self.penalizacion_espera = penalizacion
