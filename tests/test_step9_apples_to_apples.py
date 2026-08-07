from pathlib import Path

from src.apples_to_apples import run_apples_to_apples_lhs
from src.schemas import load_assumptions_registry

REGISTRY_PATH = (
    Path(__file__).resolve().parent.parent / "config" / "assumptions_registry.json"
)


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
        # 6-8), CANDU sits slightly below AP1000. Two effects stack in the
        # same direction: CANDU's fuel-cost structure, and (since F1 wired
        # interest-during-construction in) its shorter build - CANDU EC6
        # construction_years 5/6/8 vs AP1000 6/7/9, on a slightly lower
        # overnight CAPEX, so CANDU accrues less IDC. Before IDC the median
        # ratio was ~1.011 (gov) / ~1.000 (commercial, essentially a tie);
        # adding IDC WIDENS CANDU's edge to ~1.025 (gov) / ~1.034
        # (commercial) - direction unchanged (CANDU cheaper), magnitude up,
        # and commercial goes from a tie to a clear ~3% CANDU advantage.
        # This is still small next to the ~30% TUEC fuel-only figure from
        # CNS literature (fuel is a minor share of LCOE; WACC and CAPEX
        # dominate per the Sobol analysis). A ratio outside [1.0, 1.15]
        # would mean either the direction flipped (a CAPEX/IDC wiring bug)
        # or the gap grew implausibly large.
        ratio = ap1000_median / candu_median
        assert 1.0 <= ratio <= 1.15, (wacc_scenario, ap1000_median, candu_median, ratio)
