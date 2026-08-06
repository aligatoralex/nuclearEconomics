def calculate_fuel_cost_usd_per_year(
    capacity_mw: float, capacity_factor: float, base_fuel_usd_per_mwh: float
) -> float:
    """Annual fuel cost (USD/year) from capacity, capacity factor, and a
    per-MWh fuel cost figure."""
    return capacity_mw * 8760 * capacity_factor * base_fuel_usd_per_mwh


def candu_natural_fuel_usd_per_mwh(
    ap1000_fuel_usd_per_mwh: float, candu_vs_pwr_fuel_cost_ratio: float
) -> float:
    """CANDU natural-uranium fuel cost per MWh, derived from AP1000's own
    fuel cost divided by the CANDU/PWR cost ratio. Not an independent
    assumptions registry entry: its value doesn't come from its own
    source, it's a pure function of two Tier 1 registry parameters
    (ap1000_fuel_usd_per_mwh, CANDU_vs_PWR_fuel_cost_ratio) - see the
    registry v3 commit for why a "derived" entry doesn't fit the
    AssumptionEntry schema.
    """
    return ap1000_fuel_usd_per_mwh / candu_vs_pwr_fuel_cost_ratio
