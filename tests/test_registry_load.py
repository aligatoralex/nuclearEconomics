from pathlib import Path

from src.schemas import load_assumptions_registry

REGISTRY_PATH = (
    Path(__file__).resolve().parent.parent / "config" / "assumptions_registry.json"
)

# Weakest-sourced entries in the registry (NEA explicitly advises against
# the %-of-CAPEX decommissioning method it's derived from; D2O inventory
# is a linear extrapolation, not a direct measurement at this scale) -
# priorytet do potwierdzenia u prelegenta Szkoły ITC PW.
PRIORITY_CONFIRMATION_PARAMETERS = {
    "decommissioning_pct_capex_large_LWR",
    "decommissioning_pct_capex_SMR",
    "D2O_inventory_tonnes_per_1000MWe_EC6",
}


def test_registry_loads_all_entries_valid():
    entries = load_assumptions_registry(REGISTRY_PATH)

    assert len(entries) == 22
    for entry in entries:
        if entry.tier == 3:
            assert entry.requires_confirmation is True


def test_priority_confirmation_parameters_require_confirmation():
    entries = load_assumptions_registry(REGISTRY_PATH)
    entries_by_name = {entry.parameter: entry for entry in entries}

    for name in PRIORITY_CONFIRMATION_PARAMETERS:
        assert entries_by_name[name].requires_confirmation is True


def test_candu_ec6_capex_upgraded_to_tier2_real_offer():
    entries = load_assumptions_registry(REGISTRY_PATH)
    entries_by_name = {entry.parameter: entry for entry in entries}

    ap1000_capex = entries_by_name["AP1000_CAPEX_usd_per_kW"]
    assert ap1000_capex.tier == 2
    assert (
        ap1000_capex.value_or_range.min,
        ap1000_capex.value_or_range.mid,
        ap1000_capex.value_or_range.max,
    ) == (
        9500,
        12000,
        13500,
    )

    candu_capex = entries_by_name["CANDU_EC6_CAPEX_usd_per_kW"]
    assert candu_capex.tier == 2
    assert (
        candu_capex.value_or_range.min,
        candu_capex.value_or_range.mid,
        candu_capex.value_or_range.max,
    ) == (
        10100,
        11500,
        12900,
    )
