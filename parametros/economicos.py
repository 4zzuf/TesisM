class ParametrosEconomicos:
    """Parámetros económicos y ambientales."""

    def __init__(
        self,
        costo_punta=0.28,
        costo_normal=0.238,
        costo_gas_kwh=0.12,
        horas_punta=(18, 23),
        factor_co2_gas=0.25,
        factor_co2_elec=0.15,
    ):
        self.costo_punta = costo_punta
        self.costo_normal = costo_normal
        self.costo_gas_kwh = costo_gas_kwh
        self.horas_punta = horas_punta
        self.factor_co2_gas = factor_co2_gas
        self.factor_co2_elec = factor_co2_elec

    def actualizar(
        self,
        punta=None,
        normal=None,
        gas_kwh=None,
        horas=None,
        factor_gas=None,
        factor_elec=None,
    ):
        """Actualiza costos, horas o factores de emisión."""
        if punta is not None:
            self.costo_punta = punta
        if normal is not None:
            self.costo_normal = normal
        if gas_kwh is not None:
            self.costo_gas_kwh = gas_kwh
        if horas is not None:
            self.horas_punta = horas
        if factor_gas is not None:
            self.factor_co2_gas = factor_gas
        if factor_elec is not None:
            self.factor_co2_elec = factor_elec
