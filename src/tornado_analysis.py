from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from src.fuel_cost import (
    calculate_fuel_cost_usd_per_year,
    candu_natural_fuel_usd_per_mwh,
)
from src.lcoe_core import calculate_lcoe
from src.schemas import AssumptionEntry

DECOMM_PARAM = "decommissioning_pct_capex_large_LWR"
CAPACITY_FACTOR_PARAM = "capacity_factor_large_LWR_pct"
D2O_CAPEX_PARAM = "D2O_total_upfront_capex_usd_per_1000MWe"
FUEL_PARAM = "ap1000_fuel_usd_per_mwh"
CANDU_PWR_RATIO_PARAM = "CANDU_vs_PWR_fuel_cost_ratio"


@dataclass
class BaseScenario:
    """Point-value inputs calculate_lcoe needs, plus which registry
    parameters this scenario's OAT tornado should vary.

    fuel_usd_per_year is derived from the registry (see
    build_base_scenarios). capex_usd/opex_usd_per_year/lifetime_years
    aren't covered by the registry and stay as fixed placeholders (see
    build_base_scenarios) - not tier-sourced data.
    """

    name: str
    capex_usd: float
    fuel_usd_per_year: float
    opex_usd_per_year: float
    lifetime_years: int
    capacity_mw: float
    wacc_parameter_name: str
    applicable_parameter_names: list[str]


def build_base_scenarios(registry: list[AssumptionEntry]) -> dict[str, BaseScenario]:
    """Builds the four base scenarios (ap1000/candu_ec6 x government/
    commercial WACC). fuel_usd_per_year is derived from the registry
    (ap1000_fuel_usd_per_mwh, CANDU_vs_PWR_fuel_cost_ratio) via
    src/fuel_cost.py, replacing the Krok 6 hardcoded placeholders
    (60M/50M). This can't be a module-level constant like DECOMM_PARAM
    etc. since it depends on registry contents, not just its keys.
    CAPEX/OPEX/lifetime/capacity_mw still aren't covered by the registry
    and stay as constants here (same figures as Krok 6/7b).
    """
    registry_by_name = {e.parameter: e for e in registry}
    capacity_factor = registry_by_name[CAPACITY_FACTOR_PARAM].value_or_range.mid / 100

    ap1000_fuel_usd_per_mwh = registry_by_name[FUEL_PARAM].value_or_range.mid
    ap1000_fuel_usd_per_year = calculate_fuel_cost_usd_per_year(
        capacity_mw=1150.0,
        capacity_factor=capacity_factor,
        base_fuel_usd_per_mwh=ap1000_fuel_usd_per_mwh,
    )

    candu_ratio = registry_by_name[CANDU_PWR_RATIO_PARAM].value_or_range.mid
    candu_fuel_usd_per_mwh = candu_natural_fuel_usd_per_mwh(
        ap1000_fuel_usd_per_mwh, candu_ratio
    )
    candu_fuel_usd_per_year = calculate_fuel_cost_usd_per_year(
        capacity_mw=1000.0,
        capacity_factor=capacity_factor,
        base_fuel_usd_per_mwh=candu_fuel_usd_per_mwh,
    )

    common = {"opex_usd_per_year": 100_000_000.0, "lifetime_years": 60}
    ap1000_applicable = {
        "WACC_government_pct": [
            "WACC_government_pct",
            DECOMM_PARAM,
            CAPACITY_FACTOR_PARAM,
        ],
        "WACC_commercial_pct": [
            "WACC_commercial_pct",
            DECOMM_PARAM,
            CAPACITY_FACTOR_PARAM,
        ],
    }
    candu_applicable = {
        "WACC_government_pct": [
            "WACC_government_pct",
            DECOMM_PARAM,
            CAPACITY_FACTOR_PARAM,
            D2O_CAPEX_PARAM,
        ],
        "WACC_commercial_pct": [
            "WACC_commercial_pct",
            DECOMM_PARAM,
            CAPACITY_FACTOR_PARAM,
            D2O_CAPEX_PARAM,
        ],
    }

    scenarios = {}
    for wacc_kind, wacc_param in [
        ("government", "WACC_government_pct"),
        ("commercial", "WACC_commercial_pct"),
    ]:
        scenarios[f"ap1000_{wacc_kind}"] = BaseScenario(
            name="ap1000",
            capex_usd=15_525_000_000.0,
            fuel_usd_per_year=ap1000_fuel_usd_per_year,
            capacity_mw=1150.0,
            wacc_parameter_name=wacc_param,
            applicable_parameter_names=ap1000_applicable[wacc_param],
            **common,
        )
        scenarios[f"candu_ec6_{wacc_kind}"] = BaseScenario(
            name="candu_ec6",
            capex_usd=5_000_000_000.0,
            fuel_usd_per_year=candu_fuel_usd_per_year,
            capacity_mw=1000.0,
            wacc_parameter_name=wacc_param,
            applicable_parameter_names=candu_applicable[wacc_param],
            **common,
        )
    return scenarios


def _lcoe_at_bound(
    base_scenario: BaseScenario,
    registry_by_name: dict[str, AssumptionEntry],
    varying_parameter_name: str,
    bound: str,
    target_fn: Callable[..., float],
) -> float:
    """Computes LCOE with exactly one registry parameter set to its min or
    max bound, and every other applicable registry parameter held at mid.

    decomm_usd and capex_usd are DERIVED from decommissioning % and D2O
    add-on respectively, rather than being free inputs themselves - so
    varying D2O_total_upfront_capex_usd_per_1000MWe changes the CAPEX that
    decomm % is applied to (decomm % itself stays at mid unless it's the
    parameter being varied), which is the intended OAT behavior for a
    derived quantity, not an extra hidden factor.
    """

    def value(param_name: str, mid_fallback: float) -> float:
        if varying_parameter_name == param_name:
            return getattr(registry_by_name[param_name].value_or_range, bound)
        return mid_fallback

    d2o_mid = registry_by_name[D2O_CAPEX_PARAM].value_or_range.mid
    d2o_add_on = (
        value(D2O_CAPEX_PARAM, d2o_mid)
        if D2O_CAPEX_PARAM in base_scenario.applicable_parameter_names
        else 0.0
    )
    capex_usd = base_scenario.capex_usd + d2o_add_on

    decomm_pct_mid = registry_by_name[DECOMM_PARAM].value_or_range.mid
    decomm_pct = value(DECOMM_PARAM, decomm_pct_mid)
    decomm_usd = capex_usd * decomm_pct / 100

    capacity_factor_mid = registry_by_name[CAPACITY_FACTOR_PARAM].value_or_range.mid
    capacity_factor = value(CAPACITY_FACTOR_PARAM, capacity_factor_mid) / 100

    wacc_mid = registry_by_name[base_scenario.wacc_parameter_name].value_or_range.mid
    wacc = value(base_scenario.wacc_parameter_name, wacc_mid) / 100

    return target_fn(
        capex_usd=capex_usd,
        opex_usd_per_year=base_scenario.opex_usd_per_year,
        fuel_usd_per_year=base_scenario.fuel_usd_per_year,
        decomm_usd=decomm_usd,
        wacc=wacc,
        lifetime_years=base_scenario.lifetime_years,
        capacity_mw=base_scenario.capacity_mw,
        capacity_factor=capacity_factor,
    )


def run_oat_tornado(
    registry: list[AssumptionEntry],
    base_scenario: BaseScenario,
    target_fn: Callable[..., float] = calculate_lcoe,
) -> pd.DataFrame:
    """One-at-a-time tornado: for each registry parameter applicable to
    base_scenario, computes LCOE at that parameter's min and max (all
    other applicable parameters held at mid). Returns a DataFrame sorted
    by range descending: parameter, lcoe_at_min, lcoe_at_max, range, tier.
    """
    registry_by_name = {entry.parameter: entry for entry in registry}

    rows = []
    for name in base_scenario.applicable_parameter_names:
        lcoe_at_min = _lcoe_at_bound(
            base_scenario, registry_by_name, name, "min", target_fn
        )
        lcoe_at_max = _lcoe_at_bound(
            base_scenario, registry_by_name, name, "max", target_fn
        )
        rows.append(
            {
                "parameter": name,
                "lcoe_at_min": lcoe_at_min,
                "lcoe_at_max": lcoe_at_max,
                "range": abs(lcoe_at_max - lcoe_at_min),
                "tier": registry_by_name[name].tier,
            }
        )

    return (
        pd.DataFrame(rows).sort_values("range", ascending=False).reset_index(drop=True)
    )


if __name__ == "__main__":
    from src.schemas import load_assumptions_registry

    repo_root = Path(__file__).resolve().parent.parent
    registry = load_assumptions_registry(
        repo_root / "config" / "assumptions_registry.json"
    )
    scenarios = build_base_scenarios(registry)

    for tech_name in ("ap1000", "candu_ec6"):
        government_df = run_oat_tornado(registry, scenarios[f"{tech_name}_government"])
        government_df["wacc_scenario"] = "government"
        commercial_df = run_oat_tornado(registry, scenarios[f"{tech_name}_commercial"])
        commercial_df["wacc_scenario"] = "commercial"

        combined = pd.concat([government_df, commercial_df], ignore_index=True)
        output_path = repo_root / "data" / "output" / f"step7_tornado_{tech_name}.csv"
        combined.to_csv(output_path, index=False)
        print(f"Wrote {len(combined)} rows to {output_path}")
