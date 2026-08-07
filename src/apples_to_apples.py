from pathlib import Path

import numpy as np
import pandas as pd
from SALib.sample import latin
from scipy.stats import triang

from src.schemas import AssumptionEntry
from src.sobol_analysis import build_sobol_parameter_names, lcoe_from_values
from src.tornado_analysis import build_base_scenarios


def _triangular_samples(
    unit_samples: np.ndarray, low: float, mid: float, high: float
) -> np.ndarray:
    """Same technique as monte_carlo_lhs.py's helper - a new, self-contained
    copy rather than an import, because monte_carlo_lhs.run_lhs_simulation's
    fixed 5-argument signature can't express derived quantities (CAPEX+D2O,
    CANDU fuel via ratio) the way this module needs.
    """
    if high == low:
        return np.full_like(unit_samples, low)
    shape = (mid - low) / (high - low)
    return triang.ppf(unit_samples, shape, loc=low, scale=high - low)


def run_apples_to_apples_lhs(
    registry: list[AssumptionEntry],
    n_samples: int = 1000,
    seed: int = 42,
) -> pd.DataFrame:
    """Full LHS comparison of AP1000 vs CANDU EC6 with comparable, Tier 2
    CAPEX (Krok 9a/9b). WACC stays a point value per financing scenario
    (two separate runs), matching the convention from Kroki 6-8.

    Uses PAIRED sampling (common random numbers) for the one parameter
    both technologies still genuinely share: the base
    ap1000_fuel_usd_per_mwh figure (AP1000 uses it directly; CANDU's fuel
    is derived from it via CANDU_vs_PWR_fuel_cost_ratio). A single LHS
    draw of that figure feeds both technologies per row, so the fuel
    comparison isn't drowned in independent-sampling noise. Capacity
    factor and decommissioning % are now technology-specific registry
    parameters (F5: capacity_factor_CANDU_EC6_pct /
    decommissioning_pct_capex_CANDU vs the large_LWR ones), so they no
    longer overlap between the two param sets and are sampled
    independently - which is correct, since the two technologies have
    different documented CF and decommissioning profiles. The remaining
    technology-specific parameters (CAPEX, D2O, fuel ratio) are likewise
    sampled independently. With CAPEX now comparable between the two
    technologies (Krok 9a), the true gap is much smaller than it looked
    in Kroki 6-8 (where CANDU's CAPEX was an unfair ~2x-low placeholder).

    Returns a long-format DataFrame: scenario, wacc_scenario, lcoe_usd_mwh.
    """
    registry_by_name = {entry.parameter: entry for entry in registry}
    base_scenarios = build_base_scenarios(registry)

    rows = []
    for wacc_kind in ("government", "commercial"):
        ap1000_scenario = base_scenarios[f"ap1000_{wacc_kind}"]
        candu_scenario = base_scenarios[f"candu_ec6_{wacc_kind}"]

        ap1000_params = [
            p
            for p in build_sobol_parameter_names(f"ap1000_{wacc_kind}")
            if p != ap1000_scenario.wacc_parameter_name
        ]
        candu_params = [
            p
            for p in build_sobol_parameter_names(f"candu_ec6_{wacc_kind}")
            if p != candu_scenario.wacc_parameter_name
        ]
        union_params = sorted(set(ap1000_params) | set(candu_params))

        problem = {
            "num_vars": len(union_params),
            "names": union_params,
            "bounds": [[0, 1]] * len(union_params),
        }
        unit_samples = latin.sample(problem, n_samples, seed=seed)

        sampled = {}
        for j, name in enumerate(union_params):
            value_range = registry_by_name[name].value_or_range
            sampled[name] = _triangular_samples(
                unit_samples[:, j], value_range.min, value_range.mid, value_range.max
            )

        ap1000_wacc = registry_by_name[
            ap1000_scenario.wacc_parameter_name
        ].value_or_range.mid
        candu_wacc = registry_by_name[
            candu_scenario.wacc_parameter_name
        ].value_or_range.mid

        for i in range(n_samples):
            row_values = {name: sampled[name][i] for name in union_params}

            ap1000_values = {p: row_values[p] for p in ap1000_params}
            ap1000_values[ap1000_scenario.wacc_parameter_name] = ap1000_wacc
            rows.append(
                {
                    "scenario": "ap1000",
                    "wacc_scenario": wacc_kind,
                    "lcoe_usd_mwh": lcoe_from_values(ap1000_scenario, ap1000_values),
                }
            )

            candu_values = {p: row_values[p] for p in candu_params}
            candu_values[candu_scenario.wacc_parameter_name] = candu_wacc
            rows.append(
                {
                    "scenario": "candu_ec6",
                    "wacc_scenario": wacc_kind,
                    "lcoe_usd_mwh": lcoe_from_values(candu_scenario, candu_values),
                }
            )

    return pd.DataFrame(rows)


if __name__ == "__main__":
    from src.schemas import load_assumptions_registry

    repo_root = Path(__file__).resolve().parent.parent
    registry = load_assumptions_registry(
        repo_root / "config" / "assumptions_registry.json"
    )

    df = run_apples_to_apples_lhs(registry)
    output_path = repo_root / "data" / "output" / "step9_apples_to_apples_lcoe.csv"
    df.to_csv(output_path, index=False)
    print(f"Wrote {len(df)} rows to {output_path}")
