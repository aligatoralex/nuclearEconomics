from pathlib import Path

import pytest

from src.schemas import load_assumptions_registry
from src.sobol_analysis import build_sobol_parameter_names, run_sobol_analysis
from src.tornado_analysis import build_base_scenarios

REGISTRY_PATH = (
    Path(__file__).resolve().parent.parent / "config" / "assumptions_registry.json"
)

# Seed-pinned ground truth (F4). Captured from run_sobol_analysis at the
# default n_base_samples=512, seed=42 against the CURRENT registry + model
# (IDC wired in, per-technology construction_years_* and CANDU-specific
# CAPEX/CF params). Saltelli sampling + SALib analyze are deterministic at a
# fixed seed, so the exact S1/ST values are stable and worth pinning.
#
# For each build_base_scenarios() key: the top ~3 parameters by ST, each
# with its expected (S1, ST). Pinning magnitudes (not just ordering) is what
# catches numeric drift the existing property assertions miss.
#
# TOLERANCE: abs=0.03 on both S1 and ST. Sobol indices live in [0, 1]; the
# S1_conf/ST_conf bootstrap confidence half-widths at N=512 are ~0.01-0.05,
# so 0.03 is inside the sampling-noise floor for a fixed seed yet an order
# of magnitude smaller than the shift a real change causes (e.g. un-wiring
# IDC drops construction_years' ST from ~0.06-0.07 to ~0, and reshuffles the
# WACC/CAPEX split by >0.05). Tight enough to bite, loose enough to survive
# BLAS/platform float noise.
# If a DELIBERATE model change moves these, re-capture and update below.
EXPECTED_SOBOL = {
    "ap1000_government": {
        "WACC_government_pct": (0.6712, 0.6804),
        "AP1000_CAPEX_usd_per_kW": (0.2699, 0.2792),
        "capacity_factor_large_LWR_pct": (0.0241, 0.0241),
    },
    "ap1000_commercial": {
        "WACC_commercial_pct": (0.5770, 0.5872),
        "AP1000_CAPEX_usd_per_kW": (0.3257, 0.3349),
        "construction_years_AP1000": (0.0585, 0.0601),
    },
    "candu_ec6_government": {
        "WACC_government_pct": (0.7640, 0.7746),
        "CANDU_EC6_CAPEX_usd_per_kW": (0.1417, 0.1440),
        "capacity_factor_CANDU_EC6_pct": (0.0608, 0.0606),
    },
    "candu_ec6_commercial": {
        "WACC_commercial_pct": (0.6651, 0.6805),
        "CANDU_EC6_CAPEX_usd_per_kW": (0.1752, 0.1784),
        "construction_years_CANDU_EC6": (0.0657, 0.0717),
    },
}


@pytest.fixture(scope="module")
def sobol_main_effects():
    """Run the (slow, ~40s) Sobol suite ONCE for every scenario and share the
    resulting main-effect frames across tests, so the pinned regression test
    below adds coverage without re-running any Saltelli sampling.

    Returns {scenario_key: (BaseScenario, main_effects_df)}.
    """
    registry = load_assumptions_registry(REGISTRY_PATH)
    scenarios = build_base_scenarios(registry)
    out = {}
    for key, scenario in scenarios.items():
        param_names = build_sobol_parameter_names(key)
        main_effects, _interactions = run_sobol_analysis(
            registry, scenario, param_names
        )
        out[key] = (scenario, main_effects)
    return out


def test_sobol_total_effect_at_least_main_effect_and_wacc_capex_dominate(
    sobol_main_effects,
):
    for key, (scenario, main_effects) in sobol_main_effects.items():
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


def test_sobol_top_parameter_indices_pinned(sobol_main_effects):
    """Seed-pinned regression (F4). Reuses the module-scoped main-effect
    frames (no extra Sobol run). Pins the exact S1/ST magnitudes of the top
    parameters so numeric drift the ordering/relative assertions above cannot
    see is caught. See EXPECTED_SOBOL and the tolerance rationale above."""
    for key, (_scenario, main_effects) in sobol_main_effects.items():
        st_by_param = dict(zip(main_effects["parameter"], main_effects["ST"]))
        s1_by_param = dict(zip(main_effects["parameter"], main_effects["S1"]))
        for param, (exp_s1, exp_st) in EXPECTED_SOBOL[key].items():
            assert param in st_by_param, (key, param, main_effects)
            assert st_by_param[param] == pytest.approx(exp_st, abs=0.03), (
                key,
                param,
                st_by_param[param],
            )
            assert s1_by_param[param] == pytest.approx(exp_s1, abs=0.03), (
                key,
                param,
                s1_by_param[param],
            )
