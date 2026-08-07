from pathlib import Path

from src.apples_to_apples import run_apples_to_apples_lhs
from src.schemas import load_assumptions_registry

REGISTRY_PATH = (
    Path(__file__).resolve().parent.parent / "config" / "assumptions_registry.json"
)


def test_candu_median_lcoe_near_parity_within_plausible_band():
    registry = load_assumptions_registry(REGISTRY_PATH)
    df = run_apples_to_apples_lhs(registry, n_samples=1000, seed=42)

    for wacc_scenario in ("government", "commercial"):
        ap1000_median = df[
            (df["scenario"] == "ap1000") & (df["wacc_scenario"] == wacc_scenario)
        ]["lcoe_usd_mwh"].median()
        candu_median = df[
            (df["scenario"] == "candu_ec6") & (df["wacc_scenario"] == wacc_scenario)
        ]["lcoe_usd_mwh"].median()

        # AP1000 and CANDU sit at near-parity once CAPEX is genuinely
        # comparable (both Tier 2, similar order of magnitude - not the old
        # ~2x-low CANDU placeholder from Kroki 6-8). Three effects now pull
        # in competing directions: CANDU's cheaper fuel-cost structure and
        # (since F1 wired interest-during-construction in) its shorter build
        # (construction_years 5/6/8 vs AP1000 6/7/9, less accrued IDC) push
        # CANDU DOWN, while F5 gave CANDU its own, honestly lower capacity
        # factor (capacity_factor_CANDU_EC6_pct mid 87 vs the large_LWR mid
        # 91 it used to borrow), which spreads CANDU's fixed CAPEX/decomm
        # over fewer MWh and pushes CANDU UP. The CF penalty slightly
        # outweighs the fuel+IDC edge, so CANDU now lands marginally ABOVE
        # AP1000 rather than just below: median ratio ap1000/candu ~0.978
        # (gov) / ~0.989 (commercial). The gap is tiny either way (fuel is a
        # minor share of LCOE; WACC and CAPEX dominate per the Sobol
        # analysis) - the point of this test is that the two technologies
        # are within a few percent of each other. A ratio outside
        # [0.95, 1.05] would mean the gap grew implausibly large in either
        # direction (a CAPEX/IDC/CF wiring bug).
        ratio = ap1000_median / candu_median
        assert 0.95 <= ratio <= 1.05, (
            wacc_scenario,
            ap1000_median,
            candu_median,
            ratio,
        )
