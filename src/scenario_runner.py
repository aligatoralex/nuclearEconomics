from dataclasses import dataclass
from pathlib import Path

import pandas as pd
import yaml

from src.monte_carlo_lhs import run_lhs_simulation

DEFAULT_SCENARIOS_PATH = Path(__file__).resolve().parent.parent / "config" / "scenarios_step6.yaml"
CAPEX_FUEL_UNCERTAINTY_PCT = 0.20


@dataclass
class Scenario:
    name: str
    capex_usd: float
    fuel_usd_per_year: float
    opex_usd_per_year: float
    decomm_usd: float
    wacc_scenarios: list[float]
    lifetime_years: int
    capacity_mw: float
    capacity_factor: float


def load_scenarios_step6(path: Path = DEFAULT_SCENARIOS_PATH) -> list[Scenario]:
    with open(path) as f:
        raw = yaml.safe_load(f)
    return [Scenario(name=name, **fields) for name, fields in raw["scenarios"].items()]


def _pct_range(mid: float, pct: float = CAPEX_FUEL_UNCERTAINTY_PCT) -> tuple[float, float, float]:
    return (mid * (1 - pct), mid, mid * (1 + pct))


def run_all_scenarios(n_samples: int = 1000, seed: int = 42) -> pd.DataFrame:
    """Runs each Krok 6 scenario at each of its WACC points through the
    Krok 5 LHS sampler (CAPEX and fuel are the only sampled/uncertain
    parameters here, +/-20% triangular; OPEX/decomm/WACC stay point values).
    Returns a long-format DataFrame: scenario, wacc_scenario, lcoe_usd_mwh.
    """
    scenarios = load_scenarios_step6()
    rows = []
    for scenario in scenarios:
        for wacc in scenario.wacc_scenarios:
            results = run_lhs_simulation(
                capex_range=_pct_range(scenario.capex_usd),
                opex_range=(scenario.opex_usd_per_year,) * 3,
                fuel_range=_pct_range(scenario.fuel_usd_per_year),
                decomm_range=(scenario.decomm_usd,) * 3,
                wacc_range=(wacc, wacc, wacc),
                lifetime_years=scenario.lifetime_years,
                capacity_mw=scenario.capacity_mw,
                capacity_factor=scenario.capacity_factor,
                n_samples=n_samples,
                seed=seed,
            )
            for lcoe in results:
                rows.append(
                    {"scenario": scenario.name, "wacc_scenario": wacc, "lcoe_usd_mwh": lcoe}
                )
    return pd.DataFrame(rows)


if __name__ == "__main__":
    output_path = Path(__file__).resolve().parent.parent / "data" / "output" / "step6_lhs_results.csv"
    df = run_all_scenarios()
    df.to_csv(output_path, index=False)
    print(f"Wrote {len(df)} rows to {output_path}")
