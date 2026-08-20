from pathlib import Path

import numpy as np
import pandas as pd
from SALib.analyze import sobol as sobol_analyze
from SALib.sample import sobol as sobol_sample

from src.fuel_cost import (
    calculate_fuel_cost_usd_per_year,
    candu_natural_fuel_usd_per_mwh,
    candu_seu_fuel_usd_per_mwh,
)
from src.idc_engine import calculate_idc
from src.lcoe_core import calculate_lcoe
from src.schemas import AssumptionEntry
from src.tornado_analysis import (
    AP1000_CAPEX_PARAM,
    CANDU_CAPACITY_FACTOR_PARAM,
    CANDU_CAPEX_PARAM,
    CANDU_DECOMM_PARAM,
    CANDU_PWR_RATIO_PARAM,
    CAPACITY_FACTOR_PARAM,
    CONSTRUCTION_AP1000_PARAM,
    CONSTRUCTION_CANDU_PARAM,
    D2O_CAPEX_PARAM,
    D2O_OPEX_PARAM,
    DECOMM_PARAM,
    FUEL_PARAM,
    SEU_REDUCTION_PARAM,
    BaseScenario,
)


def build_sobol_parameter_names(scenario_key: str) -> list[str]:
    """Which registry parameters to vary simultaneously for a given
    build_base_scenarios() key. Unlike Krok 7's OAT tornado (which
    deliberately excluded fuel cost to keep scope tight), Sobol adds
    ap1000_fuel_usd_per_mwh (and, for CANDU, CANDU_vs_PWR_fuel_cost_ratio)
    as real dimensions - variance-based analysis is exactly the tool for
    catching interactions between them and the other parameters. Krok 9b
    adds the CAPEX-per-kW parameter too, now that both technologies have
    real, comparable Tier 2 CAPEX figures.
    """
    wacc_param = (
        "WACC_government_pct" if "government" in scenario_key else "WACC_commercial_pct"
    )
    if scenario_key.startswith("ap1000"):
        return [
            wacc_param,
            DECOMM_PARAM,
            CAPACITY_FACTOR_PARAM,
            FUEL_PARAM,
            AP1000_CAPEX_PARAM,
            CONSTRUCTION_AP1000_PARAM,
        ]
    names = [
        wacc_param,
        CANDU_DECOMM_PARAM,
        CANDU_CAPACITY_FACTOR_PARAM,
        D2O_CAPEX_PARAM,
        D2O_OPEX_PARAM,
        FUEL_PARAM,
        CANDU_PWR_RATIO_PARAM,
        CANDU_CAPEX_PARAM,
        CONSTRUCTION_CANDU_PARAM,
    ]
    # B5: CANDU-SEU adds the SEU-vs-natural fuel-cycle cost reduction as a
    # further sampled dimension on top of the CANDU-natural parameter set.
    if scenario_key.startswith("candu_ec6_seu"):
        names.append(SEU_REDUCTION_PARAM)
    return names


def lcoe_from_values(base_scenario: BaseScenario, values: dict[str, float]) -> float:
    """Computes LCOE from a full row of simultaneously-sampled parameter
    values. Mirrors tornado_analysis._lcoe_at_bound's derived-quantity
    logic (capex_per_kw * capacity_mw * 1000 + D2O add-on, decomm % of capex,
    fuel from calculate_fuel_cost_usd_per_year), but for many varying
    parameters at once instead of one-at-a-time. Public (no leading
    underscore): reused directly by src/apples_to_apples.py.
    """
    capex_per_kw = values[base_scenario.capex_per_kw_parameter_name]
    base_capex_usd = capex_per_kw * base_scenario.capacity_mw * 1000  # USD/kW -> USD/MW
    d2o_add_on = values.get(D2O_CAPEX_PARAM, 0.0)
    capex_usd = base_capex_usd + d2o_add_on

    # D2O annual makeup losses (CANDU only) add to OPEX.
    opex_usd_per_year = base_scenario.opex_usd_per_year + values.get(D2O_OPEX_PARAM, 0.0)

    # Decommissioning stays a % of the OVERNIGHT capex (base + D2O), not of
    # the IDC-inflated capital booked at t=0.
    decomm_usd = capex_usd * values[base_scenario.decomm_parameter_name] / 100
    capacity_factor = values[base_scenario.capacity_factor_parameter_name] / 100
    wacc = values[base_scenario.wacc_parameter_name] / 100

    # Interest during construction on the real physical expenditure (overnight
    # capex incl. D2O), booked into capital at t=0.
    construction_years_value = values[base_scenario.construction_years_parameter_name]
    cy = max(1, round(float(construction_years_value)))
    idc = calculate_idc(capex_usd, cy, wacc)
    capex_effective = capex_usd + idc

    if CANDU_PWR_RATIO_PARAM in values:
        fuel_usd_per_mwh = candu_natural_fuel_usd_per_mwh(
            values[FUEL_PARAM], values[CANDU_PWR_RATIO_PARAM]
        )
        if SEU_REDUCTION_PARAM in values:
            fuel_usd_per_mwh = candu_seu_fuel_usd_per_mwh(
                fuel_usd_per_mwh, values[SEU_REDUCTION_PARAM]
            )
    else:
        fuel_usd_per_mwh = values[FUEL_PARAM]
    fuel_usd_per_year = calculate_fuel_cost_usd_per_year(
        base_scenario.capacity_mw, capacity_factor, fuel_usd_per_mwh
    )

    return calculate_lcoe(
        capex_usd=capex_effective,
        opex_usd_per_year=opex_usd_per_year,
        fuel_usd_per_year=fuel_usd_per_year,
        decomm_usd=decomm_usd,
        wacc=wacc,
        lifetime_years=base_scenario.lifetime_years,
        capacity_mw=base_scenario.capacity_mw,
        capacity_factor=capacity_factor,
    )


def run_sobol_analysis(
    registry: list[AssumptionEntry],
    base_scenario: BaseScenario,
    sobol_parameter_names: list[str],
    n_base_samples: int = 512,
    seed: int = 42,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Variance-based (Sobol) sensitivity analysis: samples
    sobol_parameter_names via Saltelli sampling over their registry
    min/max bounds, evaluates LCOE for each sample, and decomposes output
    variance into first-order (S1, main effect) and total-order (ST, main
    effect + all interactions) indices, plus pairwise interactions (S2).
    """
    registry_by_name = {entry.parameter: entry for entry in registry}
    problem = {
        "num_vars": len(sobol_parameter_names),
        "names": sobol_parameter_names,
        "bounds": [
            [
                registry_by_name[name].value_or_range.min,
                registry_by_name[name].value_or_range.max,
            ]
            for name in sobol_parameter_names
        ],
    }
    param_values = sobol_sample.sample(problem, n_base_samples, seed=seed)

    y = np.empty(param_values.shape[0])
    for i, row in enumerate(param_values):
        values = dict(zip(sobol_parameter_names, row, strict=True))
        y[i] = lcoe_from_values(base_scenario, values)

    sensitivity_indices = sobol_analyze.analyze(problem, y, seed=seed)

    main_effects = (
        pd.DataFrame(
            {
                "parameter": sobol_parameter_names,
                "S1": sensitivity_indices["S1"],
                "S1_conf": sensitivity_indices["S1_conf"],
                "ST": sensitivity_indices["ST"],
                "ST_conf": sensitivity_indices["ST_conf"],
                "tier": [registry_by_name[name].tier for name in sobol_parameter_names],
            }
        )
        .sort_values("ST", ascending=False)
        .reset_index(drop=True)
    )

    interaction_rows = []
    num_params = len(sobol_parameter_names)
    for i in range(num_params):
        for j in range(i + 1, num_params):
            interaction_rows.append(
                {
                    "parameter_1": sobol_parameter_names[i],
                    "parameter_2": sobol_parameter_names[j],
                    "S2": sensitivity_indices["S2"][i][j],
                    "S2_conf": sensitivity_indices["S2_conf"][i][j],
                }
            )
    interactions = (
        pd.DataFrame(interaction_rows)
        .sort_values("S2", key=abs, ascending=False)
        .reset_index(drop=True)
    )

    return main_effects, interactions


if __name__ == "__main__":
    from src.schemas import load_assumptions_registry
    from src.tornado_analysis import build_base_scenarios

    repo_root = Path(__file__).resolve().parent.parent
    registry = load_assumptions_registry(
        repo_root / "config" / "assumptions_registry.json"
    )
    scenarios = build_base_scenarios(registry)

    for tech_name in ("ap1000", "candu_ec6", "candu_ec6_seu"):
        main_frames = []
        interaction_frames = []
        for wacc_kind in ("government", "commercial"):
            key = f"{tech_name}_{wacc_kind}"
            param_names = build_sobol_parameter_names(key)
            main_effects, interactions = run_sobol_analysis(
                registry, scenarios[key], param_names
            )
            main_effects["wacc_scenario"] = wacc_kind
            interactions["wacc_scenario"] = wacc_kind
            main_frames.append(main_effects)
            interaction_frames.append(interactions)

        # Standalone re-run output goes to distinct *_current_* paths so it
        # cannot clobber the frozen pre-CAPEX baseline in
        # data/output/step7_8_pre_capex_baseline/.
        main_combined = pd.concat(main_frames, ignore_index=True)
        main_path = (
            repo_root / "data" / "output" / f"step8_sobol_current_{tech_name}.csv"
        )
        main_combined.to_csv(main_path, index=False)
        print(f"Wrote {len(main_combined)} rows to {main_path}")

        interactions_combined = pd.concat(interaction_frames, ignore_index=True)
        interactions_path = (
            repo_root
            / "data"
            / "output"
            / f"step8_sobol_interactions_current_{tech_name}.csv"
        )
        interactions_combined.to_csv(interactions_path, index=False)
        print(f"Wrote {len(interactions_combined)} rows to {interactions_path}")
