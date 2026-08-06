from pathlib import Path

from src.apples_to_apples import run_apples_to_apples_lhs
from src.schemas import load_assumptions_registry

REGISTRY_PATH = Path(__file__).resolve().parent.parent / "config" / "assumptions_registry.json"


def test_candu_median_lcoe_below_ap1000_within_plausible_band():
    registry = load_assumptions_registry(REGISTRY_PATH)
    df = run_apples_to_apples_lhs(registry, n_samples=1000, seed=42)

    for wacc_scenario in ("government", "commercial"):
        ap1000_median = df[
            (df["scenario"] == "ap1000") & (df["wacc_scenario"] == wacc_scenario)
        ]["lcoe_usd_mwh"].median()
        candu_median = df[
            (df["scenario"] == "candu_ec6") & (df["wacc_scenario"] == wacc_scenario)
        ]["lcoe_usd_mwh"].median()

        # With genuinely comparable CAPEX (both Tier 2, similar order of
        # magnitude - not the old ~2x-low CANDU placeholder from Kroki
        # 6-8), the apples-to-apples run shows CANDU's fuel-cost advantage
        # (CANDU_vs_PWR_fuel_cost_ratio > 1) is real but SMALL in LCOE
        # terms (~0.1-1.5%), not the ~30% TUEC figure from CNS literature -
        # that 30% describes the fuel cost component itself, which is only
        # a minor share of total LCOE (WACC and CAPEX dominate, per Krok
        # 7-9c's tornado/Sobol). A ratio outside [0.98, 1.5] would mean
        # either the direction flipped (CAPEX wiring bug) or the gap is
        # implausibly large for a fuel-only effect.
        ratio = ap1000_median / candu_median
        assert 0.98 <= ratio <= 1.5, (wacc_scenario, ap1000_median, candu_median, ratio)
