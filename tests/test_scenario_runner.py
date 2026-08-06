from src.scenario_runner import run_all_scenarios

N_SAMPLES = 1000
SEED = 42


def _median_lcoe(df, scenario, wacc_scenario):
    subset = df[(df["scenario"] == scenario) & (df["wacc_scenario"] == wacc_scenario)]
    return subset["lcoe_usd_mwh"].median()


def test_candu_seu_median_lcoe_below_candu_natural():
    df = run_all_scenarios(n_samples=N_SAMPLES, seed=SEED)

    for wacc in (0.04, 0.08):
        seu_median = _median_lcoe(df, "candu_seu", wacc)
        natural_median = _median_lcoe(df, "candu_natural", wacc)
        # SEU fuel cost is 27.5% lower than natural (fuel_cycle_cost_reduction_pct
        # from this session); CAPEX/OPEX/decomm are otherwise identical, so SEU's
        # LCOE must come out lower.
        assert seu_median < natural_median


def test_candu_median_lcoe_increases_with_wacc():
    df = run_all_scenarios(n_samples=N_SAMPLES, seed=SEED)

    for scenario in ("candu_natural", "candu_seu"):
        low_wacc_median = _median_lcoe(df, scenario, 0.04)
        high_wacc_median = _median_lcoe(df, scenario, 0.08)
        # Higher cost of capital must increase discounted LCOE, all else equal.
        assert high_wacc_median > low_wacc_median
