class ParametrosSimulacion:
    """Parámetros generales de la simulación."""

    def __init__(self, duracion=500, max_autobuses=30, semilla=42):
        self.duracion = duracion
        self.max_autobuses = max_autobuses
        self.semilla = semilla

    def actualizar(self, duracion=None, max_autobuses=None, semilla=None):
        """Permite actualizar los parámetros de simulación."""
        if duracion is not None:
            self.duracion = duracion
        if max_autobuses is not None:
            self.max_autobuses = max_autobuses
        if semilla is not None:
            self.semilla = semilla
