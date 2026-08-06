from pathlib import Path

from src.schemas import load_assumptions_registry
from src.sobol_analysis import build_sobol_parameter_names, run_sobol_analysis
from src.tornado_analysis import build_base_scenarios

REGISTRY_PATH = Path(__file__).resolve().parent.parent / "config" / "assumptions_registry.json"


def test_sobol_total_effect_at_least_main_effect_and_wacc_dominates():
    registry = load_assumptions_registry(REGISTRY_PATH)
    scenarios = build_base_scenarios(registry)

    for key, scenario in scenarios.items():
        param_names = build_sobol_parameter_names(key)
        main_effects, _interactions = run_sobol_analysis(registry, scenario, param_names)

        # ST (total effect: main effect + all interactions) must be >= S1
        # (main effect alone) for every parameter, up to small sampling
        # noise at N=512 base samples.
        for _, row in main_effects.iterrows():
            assert row["ST"] >= row["S1"] - 0.05, (key, row)

        # Consistent with the Krok 7 OAT tornado result via a different
        # method: cost of capital should still dominate total sensitivity.
        top_parameter = main_effects.iloc[0]["parameter"]
        assert top_parameter == scenario.wacc_parameter_name, (key, main_effects)
