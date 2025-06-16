class ParametrosEconomicos:
    """Parámetros económicos que pueden modificarse."""

    def __init__(self, costo_punta=0.28, costo_normal=0.238, costo_petroleo_completo=300, horas_punta=(18, 23)):
        self.costo_punta = costo_punta
        self.costo_normal = costo_normal
        self.costo_petroleo_completo = costo_petroleo_completo
        self.horas_punta = horas_punta

    def actualizar(self, punta=None, normal=None, petroleo=None, horas=None):
        """Actualiza los costos o las horas punta."""
        if punta is not None:
            self.costo_punta = punta
        if normal is not None:
            self.costo_normal = normal
        if petroleo is not None:
            self.costo_petroleo_completo = petroleo
        if horas is not None:
            self.horas_punta = horas
