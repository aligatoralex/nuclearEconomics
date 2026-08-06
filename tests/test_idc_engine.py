import pytest

from src.idc_engine import (
    beta_expenditure_profile,
    calculate_idc,
    calculate_idc_simplified_compound,
)

CAPEX_USD = 5_000_000_000.0
CONSTRUCTION_YEARS = 8
WACC = 0.08


def test_idc_scurve_exceeds_simplified_compound_markup():
    # Compounding (1+r)^tau is convex in tau. The symmetric beta(2,2)
    # profile has the same mean expenditure timing (mid-construction) as
    # the simplified method assumes, so by Jensen's inequality the
    # period-by-period S-curve IDC must be >= the simplified compound
    # markup, and strictly greater for any non-degenerate spread — this
    # is exactly the effect the previous (simplified) model was missing.
    idc_scurve = calculate_idc(CAPEX_USD, CONSTRUCTION_YEARS, WACC)
    idc_simplified = calculate_idc_simplified_compound(
        CAPEX_USD, CONSTRUCTION_YEARS, WACC
    )

    assert idc_scurve > idc_simplified

    profile = beta_expenditure_profile(CONSTRUCTION_YEARS)
    assert sum(profile) == pytest.approx(1.0)
