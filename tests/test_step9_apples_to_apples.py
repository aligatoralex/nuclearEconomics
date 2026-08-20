from pathlib import Path

import pytest

from src.apples_to_apples import run_apples_to_apples_lhs
from src.schemas import load_assumptions_registry

REGISTRY_PATH = (
    Path(__file__).resolve().parent.parent / "config" / "assumptions_registry.json"
)


@pytest.fixture(scope="module")
def apples_df():
    """Single deterministic LHS run shared by every test in this module, so
    the regression test below adds coverage WITHOUT paying for a second
    (slow) run_apples_to_apples_lhs call."""
    registry = load_assumptions_registry(REGISTRY_PATH)
    return run_apples_to_apples_lhs(registry, n_samples=1000, seed=42)


def _series(df, scenario, wacc_scenario):
    return df[(df["scenario"] == scenario) & (df["wacc_scenario"] == wacc_scenario)][
        "lcoe_usd_mwh"
    ].reset_index(drop=True)


# Seed-pinned ground truth (P2, re-pinned after the B1-B5 critical-review
# backlog landed). These numbers are captured from
# run_apples_to_apples_lhs(registry, n_samples=1000, seed=42) against the
# CURRENT registry + model: D2O annual makeup wired into CANDU OPEX (B2),
# research-updated construction/CF/decomm ranges (B1), OPEX now a
# per-technology sampled dimension instead of an identical flat 100M
# placeholder (B3), lifetime_years/capacity_mw registry-sourced (B4). The
# run is fully deterministic, so we can pin exact-ish values.
#
# Per (wacc_scenario): the AP1000 and CANDU EC6 median LCOE, and the
# positionally-paired difference (candu - ap1000, common random numbers
# within the wacc run) - its median and the probability CANDU is cheaper.
#
# TOLERANCES (chosen deliberately):
#   * median LCOE       -> abs=0.5 USD/MWh. Medians sit at ~103-202, so 0.5
#     is <0.5% - tight enough that un-wiring IDC (which moves medians by
#     several USD/MWh) or changing a registry mid trips it, loose enough to
#     absorb BLAS/lib float noise (which is < 1e-3 here).
#   * paired diff median -> abs=0.5 USD/MWh, same reasoning; the gap itself
#     is only ~3 USD/MWh so 0.5 still catches a real directional shift.
#   * P(CANDU cheaper)  -> abs=0.02. It is a fraction of 1000 paired draws;
#     0.02 = ~20 rows flipping, far above float noise but well below the
#     change a real wiring bug would cause.
# If a DELIBERATE model change moves these, re-capture and update the
# numbers here - the test is meant to FAIL loudly on an unintended shift.
EXPECTED = {
    "government": {
        "ap1000_median": 102.8256,
        "candu_median": 105.5165,
        "diff_median": 3.1982,
        "p_candu_cheaper": 0.3620,
    },
    "commercial": {
        "ap1000_median": 201.8563,
        "candu_median": 197.6668,
        "diff_median": -2.8694,
        "p_candu_cheaper": 0.5560,
    },
}


def test_candu_median_lcoe_near_parity_within_plausible_band(apples_df):
    """Directional guard (kept alongside the pinned regression below): the
    two technologies stay within a few percent of each other."""
    for wacc_scenario in ("government", "commercial"):
        ap1000_median = _series(apples_df, "ap1000", wacc_scenario).median()
        candu_median = _series(apples_df, "candu_ec6", wacc_scenario).median()

        # AP1000 and CANDU sit at near-parity once CAPEX is genuinely
        # comparable (both Tier 2, similar order of magnitude - not the old
        # ~2x-low CANDU placeholder from Kroki 6-8). Several effects now pull
        # in competing directions: CANDU's cheaper fuel-cost structure and
        # its shorter construction range push CANDU DOWN, while its lower
        # capacity factor (mid 87 vs AP1000's 91) and wider, research-backed
        # decommissioning % (B1: 10/15/22 vs AP1000's 8/12/16) push CANDU UP.
        # B1 also widened AP1000's construction-time range upward (realized
        # builds run 8-10.5 years, not 6-9) - more accrued IDC pushes AP1000
        # UP too. Net result flips sign by WACC scenario: median ratio
        # ap1000/candu ~0.974 (gov, CANDU slightly pricier) / ~1.021
        # (commercial, CANDU now slightly cheaper). The gap stays small
        # either way (fuel/decomm/OPEX are minor shares of LCOE; WACC and
        # CAPEX dominate per the Sobol analysis) - the point of this test is
        # that the two technologies are within a few percent of each other.
        # A ratio outside [0.95, 1.05] would mean the gap grew implausibly
        # large in either direction (a CAPEX/IDC/CF/OPEX wiring bug).
        ratio = ap1000_median / candu_median
        assert 0.95 <= ratio <= 1.05, (
            wacc_scenario,
            ap1000_median,
            candu_median,
            ratio,
        )


def test_apples_to_apples_medians_and_paired_diff_pinned(apples_df):
    """Seed-pinned regression (F4). Reuses the module-scoped LHS frame (no
    extra run). Pins the exact current medians and the paired difference so
    a modeling change that stays inside the loose [0.95, 1.05] band checked
    above still trips here. See EXPECTED and the tolerance rationale above."""
    for wacc_scenario in ("government", "commercial"):
        exp = EXPECTED[wacc_scenario]
        ap1000_series = _series(apples_df, "ap1000", wacc_scenario)
        candu_series = _series(apples_df, "candu_ec6", wacc_scenario)
        ap1000_median = ap1000_series.median()
        candu_median = candu_series.median()
        # candu - ap1000, positional pairing (common random numbers).
        diff = candu_series - ap1000_series

        assert ap1000_median == pytest.approx(exp["ap1000_median"], abs=0.5), (
            wacc_scenario,
            ap1000_median,
        )
        assert candu_median == pytest.approx(exp["candu_median"], abs=0.5), (
            wacc_scenario,
            candu_median,
        )
        assert diff.median() == pytest.approx(exp["diff_median"], abs=0.5), (
            wacc_scenario,
            diff.median(),
        )
        p_candu_cheaper = float((diff < 0).mean())
        assert p_candu_cheaper == pytest.approx(exp["p_candu_cheaper"], abs=0.02), (
            wacc_scenario,
            p_candu_cheaper,
        )
