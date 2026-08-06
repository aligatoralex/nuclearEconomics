from pathlib import Path

from src.schemas import load_assumptions_registry
from src.tornado_analysis import build_base_scenarios, run_oat_tornado

REGISTRY_PATH = Path(__file__).resolve().parent.parent / "config" / "assumptions_registry.json"


def test_wacc_ranks_in_top_3_for_all_scenarios():
    registry = load_assumptions_registry(REGISTRY_PATH)
    scenarios = build_base_scenarios(registry)

    # Cost of capital is expected to dominate LCOE sensitivity more than any
    # single technical parameter, consistent with the earlier model finding
    # "koszt kapitału ma większy wpływ niż wybór technologii" - check this
    # holds for every technology x financing combination, not just one.
    # (D2O_total_upfront_capex has the largest absolute USD range for CANDU
    # but is NOT asserted to rank #1 - a wide absolute range doesn't have to
    # translate into the largest LCOE swing, since decomm%/capacity_factor%
    # also compound nonlinearly through the discounted cash flow.)
    for key, scenario in scenarios.items():
        df = run_oat_tornado(registry, scenario)
        top3 = df.head(3)["parameter"].tolist()
        assert scenario.wacc_parameter_name in top3, (key, df)
