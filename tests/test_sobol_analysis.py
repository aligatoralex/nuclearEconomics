from pathlib import Path

from src.schemas import load_assumptions_registry
from src.sobol_analysis import build_sobol_parameter_names, run_sobol_analysis
from src.tornado_analysis import build_base_scenarios

REGISTRY_PATH = (
    Path(__file__).resolve().parent.parent / "config" / "assumptions_registry.json"
)


def test_sobol_total_effect_at_least_main_effect_and_wacc_capex_dominate():
    registry = load_assumptions_registry(REGISTRY_PATH)
    scenarios = build_base_scenarios(registry)

    for key, scenario in scenarios.items():
        param_names = build_sobol_parameter_names(key)
        main_effects, _interactions = run_sobol_analysis(
            registry, scenario, param_names
        )

        # ST (total effect: main effect + all interactions) must be >= S1
        # (main effect alone) for every parameter, up to small sampling
        # noise at N=512 base samples.
        for _, row in main_effects.iterrows():
            assert row["ST"] >= row["S1"] - 0.05, (key, row)

        # Krok 9 gave CANDU EC6 a real, comparable Tier 2 CAPEX (was a
        # flat, unvaried placeholder through Krok 8) - CAPEX is now a real
        # Sobol dimension and can rival or even edge out WACC. F1 then wired
        # interest-during-construction in and added the per-technology
        # construction_years_* parameter as a further Sobol dimension: it is
        # now the clear #3 factor in the commercial scenarios (ST~0.06-0.07,
        # ahead of capacity_factor/fuel/decomm/D2O) but still well behind the
        # WACC/CAPEX pair - IDC scales with both WACC and overnight CAPEX, so
        # those two stay dominant. So we still assert WACC and CAPEX are
        # jointly the top 2 by ST, now clearly ahead of a third factor that
        # is construction (commercial) or capacity_factor (government).
        # A tighter seed-pinned regression on the exact ST values is being
        # added separately (F4), not here.
        top_2 = set(main_effects.head(2)["parameter"])
        expected_top_2 = {
            scenario.wacc_parameter_name,
            scenario.capex_per_kw_parameter_name,
        }
        assert top_2 == expected_top_2, (key, main_effects)

        third_place_st = main_effects.iloc[2]["ST"]
        assert main_effects.iloc[0]["ST"] >= 3 * third_place_st, (key, main_effects)
