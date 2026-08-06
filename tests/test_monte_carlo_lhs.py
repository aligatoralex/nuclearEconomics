import numpy as np

from src.lcoe_core import calculate_lcoe
from src.monte_carlo_lhs import run_lhs_simulation

# Same fixture values as tests/test_lcoe_core.py, reused here as degenerate
# (min=mid=max) ranges so the LHS output has a known deterministic baseline
# to compare against.
CAPEX_USD = 5_000_000_000.0
OPEX_USD_PER_YEAR = 100_000_000.0
FUEL_USD_PER_YEAR = 50_000_000.0
DECOMM_USD = 750_000_000.0
WACC = 0.04
LIFETIME_YEARS = 60
CAPACITY_MW = 1100.0
CAPACITY_FACTOR = 0.90
N_SAMPLES = 1000


def test_lhs_degenerate_matches_deterministic_baseline():
    expected = calculate_lcoe(
        capex_usd=CAPEX_USD,
        opex_usd_per_year=OPEX_USD_PER_YEAR,
        fuel_usd_per_year=FUEL_USD_PER_YEAR,
        decomm_usd=DECOMM_USD,
        wacc=WACC,
        lifetime_years=LIFETIME_YEARS,
        capacity_mw=CAPACITY_MW,
        capacity_factor=CAPACITY_FACTOR,
    )

    results = run_lhs_simulation(
        capex_range=(CAPEX_USD, CAPEX_USD, CAPEX_USD),
        opex_range=(OPEX_USD_PER_YEAR, OPEX_USD_PER_YEAR, OPEX_USD_PER_YEAR),
        fuel_range=(FUEL_USD_PER_YEAR, FUEL_USD_PER_YEAR, FUEL_USD_PER_YEAR),
        decomm_range=(DECOMM_USD, DECOMM_USD, DECOMM_USD),
        wacc_range=(WACC, WACC, WACC),
        lifetime_years=LIFETIME_YEARS,
        capacity_mw=CAPACITY_MW,
        capacity_factor=CAPACITY_FACTOR,
        n_samples=N_SAMPLES,
        seed=42,
    )

    assert results.shape == (N_SAMPLES,)
    assert np.allclose(results, expected)
