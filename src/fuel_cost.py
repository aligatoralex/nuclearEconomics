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


def candu_seu_fuel_usd_per_mwh(
    candu_natural_fuel_usd_per_mwh_value: float,
    fuel_cycle_cost_reduction_pct_seu_vs_natural: float,
) -> float:
    """CANDU slightly-enriched-uranium (SEU) fuel cost per MWh, derived from
    the natural-uranium CANDU fuel cost reduced by the SEU fuel-cycle cost
    saving (fuel_cycle_cost_reduction_pct_CANDU_SEU_vs_natural, Tier 1).
    Same physical plant/CAPEX/OPEX/decomm as CANDU-natural - only the fuel
    cycle differs (B5: reactivating the Krok 6 SEU variant on top of the
    current, CAPEX-comparable model).
    """
    return candu_natural_fuel_usd_per_mwh_value * (
        1 - fuel_cycle_cost_reduction_pct_seu_vs_natural / 100
    )
