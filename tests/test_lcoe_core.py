import pytest

from src.lcoe_core import calculate_lcoe

# Illustrative round-number example (NOT sourced/validated AP1000 data —
# chosen purely so the LCOE can be independently verified via the
# closed-form level-annuity formula below). Real Tier 1/2/3 data enters
# through the assumptions registry, not through test fixtures.
CAPEX_USD = 5_000_000_000.0
OPEX_USD_PER_YEAR = 100_000_000.0
FUEL_USD_PER_YEAR = 50_000_000.0
DECOMM_USD = 750_000_000.0
WACC = 0.04
LIFETIME_YEARS = 60
CAPACITY_MW = 1100.0
CAPACITY_FACTOR = 0.90


def test_calculate_lcoe_matches_hand_calculated_ap1000_example():
    # Closed-form level-annuity present value, computed independently of
    # calculate_lcoe's year-by-year loop:
    #   AF = (1 - (1+WACC)^-L) / WACC
    #   LCOE = [CAPEX + (OPEX+Fuel)*AF + Decomm*(1+WACC)^-L] / [E*AF]
    discount_factor_final_year = (1 + WACC) ** -LIFETIME_YEARS
    annuity_factor = (1 - discount_factor_final_year) / WACC
    annual_generation_mwh = CAPACITY_MW * 8760 * CAPACITY_FACTOR

    numerator = (
        CAPEX_USD
        + (OPEX_USD_PER_YEAR + FUEL_USD_PER_YEAR) * annuity_factor
        + DECOMM_USD * discount_factor_final_year
    )
    denominator = annual_generation_mwh * annuity_factor
    expected_lcoe = numerator / denominator

    result = calculate_lcoe(
        capex_usd=CAPEX_USD,
        opex_usd_per_year=OPEX_USD_PER_YEAR,
        fuel_usd_per_year=FUEL_USD_PER_YEAR,
        decomm_usd=DECOMM_USD,
        wacc=WACC,
        lifetime_years=LIFETIME_YEARS,
        capacity_mw=CAPACITY_MW,
        capacity_factor=CAPACITY_FACTOR,
    )

    assert result == pytest.approx(expected_lcoe, rel=1e-9)
