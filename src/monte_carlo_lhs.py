import numpy as np
from SALib.sample import latin
from scipy.stats import triang

from src.lcoe_core import calculate_lcoe

_PARAM_NAMES = ["capex_usd", "opex_usd_per_year", "fuel_usd_per_year", "decomm_usd", "wacc"]


def _triangular_samples(unit_samples: np.ndarray, low: float, mid: float, high: float) -> np.ndarray:
    """Maps unit-hypercube LHS draws to a triangular(low, mid, high) distribution.

    Degenerate ranges (high == low) skip scipy.stats.triang entirely, since
    its scale=high-low would be 0 and its ppf would divide by zero.
    """
    if high == low:
        return np.full_like(unit_samples, low)
    shape = (mid - low) / (high - low)
    return triang.ppf(unit_samples, shape, loc=low, scale=high - low)


def run_lhs_simulation(
    capex_range: tuple[float, float, float],
    opex_range: tuple[float, float, float],
    fuel_range: tuple[float, float, float],
    decomm_range: tuple[float, float, float],
    wacc_range: tuple[float, float, float],
    lifetime_years: int,
    capacity_mw: float,
    capacity_factor: float,
    n_samples: int = 1000,
    seed: int | None = None,
) -> np.ndarray:
    """Propagates uncertainty in CAPEX/OPEX/fuel/decomm/WACC through
    calculate_lcoe via Latin Hypercube Sampling.

    Each *_range is (min, mid, max), sampled as a triangular distribution.
    lifetime_years/capacity_mw/capacity_factor stay point values, matching
    the deterministic core's signature from lcoe_core.calculate_lcoe.
    Returns an array of n_samples LCOE values (USD/MWh).
    """
    problem = {
        "num_vars": len(_PARAM_NAMES),
        "names": _PARAM_NAMES,
        "bounds": [[0, 1]] * len(_PARAM_NAMES),
    }
    unit_samples = latin.sample(problem, n_samples, seed=seed)

    capex_samples = _triangular_samples(unit_samples[:, 0], *capex_range)
    opex_samples = _triangular_samples(unit_samples[:, 1], *opex_range)
    fuel_samples = _triangular_samples(unit_samples[:, 2], *fuel_range)
    decomm_samples = _triangular_samples(unit_samples[:, 3], *decomm_range)
    wacc_samples = _triangular_samples(unit_samples[:, 4], *wacc_range)

    results = np.empty(n_samples)
    for i in range(n_samples):
        results[i] = calculate_lcoe(
            capex_usd=capex_samples[i],
            opex_usd_per_year=opex_samples[i],
            fuel_usd_per_year=fuel_samples[i],
            decomm_usd=decomm_samples[i],
            wacc=wacc_samples[i],
            lifetime_years=lifetime_years,
            capacity_mw=capacity_mw,
            capacity_factor=capacity_factor,
        )
    return results
