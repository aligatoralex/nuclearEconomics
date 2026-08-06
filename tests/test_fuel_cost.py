import pytest

from src.fuel_cost import (
    calculate_fuel_cost_usd_per_year,
    candu_natural_fuel_usd_per_mwh,
)


def test_calculate_fuel_cost_usd_per_year_ap1000_hand_calculated():
    # Independent hand calculation of the same formula:
    # capacity_mw * hours/year * capacity_factor * base_fuel_usd_per_mwh
    expected = 1150 * 8760 * 0.90 * 9
    result = calculate_fuel_cost_usd_per_year(
        capacity_mw=1150, capacity_factor=0.90, base_fuel_usd_per_mwh=9
    )
    assert result == pytest.approx(expected)


def test_candu_natural_fuel_cost_below_ap1000_when_ratio_above_one():
    ap1000_fuel_usd_per_mwh = 9.0
    candu_vs_pwr_fuel_cost_ratio = 1.68  # registry mid: CANDU cheaper per MWh
    candu_fuel_usd_per_mwh = candu_natural_fuel_usd_per_mwh(
        ap1000_fuel_usd_per_mwh, candu_vs_pwr_fuel_cost_ratio
    )
    assert candu_fuel_usd_per_mwh < ap1000_fuel_usd_per_mwh
