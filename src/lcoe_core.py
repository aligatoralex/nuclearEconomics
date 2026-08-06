def calculate_lcoe(
    capex_usd: float,
    opex_usd_per_year: float,
    fuel_usd_per_year: float,
    decomm_usd: float,
    wacc: float,
    lifetime_years: int,
    capacity_mw: float,
    capacity_factor: float,
) -> float:
    """Deterministic point-value LCOE (USD/MWh) via discounted cash flow.

    CAPEX is treated as an undiscounted overnight cost at t=0 (construction
    expenditure timing is handled separately by the IDC engine). OPEX and
    fuel are constant annual costs from t=1..lifetime_years; decommissioning
    is a single cost in the final operating year.
    """
    annual_generation_mwh = capacity_mw * 8760 * capacity_factor

    discounted_costs = capex_usd
    discounted_generation = 0.0
    for t in range(1, lifetime_years + 1):
        discount_factor = (1 + wacc) ** t
        discounted_costs += (opex_usd_per_year + fuel_usd_per_year) / discount_factor
        discounted_generation += annual_generation_mwh / discount_factor

    discounted_costs += decomm_usd / (1 + wacc) ** lifetime_years

    return discounted_costs / discounted_generation
