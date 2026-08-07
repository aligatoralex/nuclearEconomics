from pathlib import Path

import kaleido
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from src.schemas import load_assumptions_registry
from src.sobol_analysis import build_sobol_parameter_names, run_sobol_analysis
from src.tornado_analysis import build_base_scenarios, run_oat_tornado

CHROMIUM_PATH = "/opt/pw-browsers/chromium"
REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data" / "output"
NEW_DIR = DATA_DIR / "step9c_tornado_sobol_updated"
# Frozen pre-CAPEX Krok 7/8 baseline (the "before" reference), quarantined so
# re-running the analysis modules can't overwrite it.
OLD_DIR = DATA_DIR / "step7_8_pre_capex_baseline"

TECHNOLOGIES = [("ap1000", "AP1000"), ("candu_ec6", "CANDU EC6")]
OLD_COLOR = "#b0b0b0"
NEW_COLOR = "#3f6fb4"


def _generate_new_results(registry, scenarios) -> None:
    """Runs tornado + Sobol with the now-CAPEX-wired code and writes them
    to data/output/step9c_tornado_sobol_updated/ - explicitly NOT to the
    step7_8_pre_capex_baseline/ frozen CSVs, which stay untouched as the
    Krok 7/8 "before" reference (already reviewed/committed).
    """
    NEW_DIR.mkdir(parents=True, exist_ok=True)
    for tech_key, _label in TECHNOLOGIES:
        tornado_frames = []
        sobol_frames = []
        for wacc_kind in ("government", "commercial"):
            key = f"{tech_key}_{wacc_kind}"
            scenario = scenarios[key]

            tornado_df = run_oat_tornado(registry, scenario)
            tornado_df["wacc_scenario"] = wacc_kind
            tornado_frames.append(tornado_df)

            sobol_params = build_sobol_parameter_names(key)
            main_effects, _interactions = run_sobol_analysis(
                registry, scenario, sobol_params
            )
            main_effects["wacc_scenario"] = wacc_kind
            sobol_frames.append(main_effects)

        pd.concat(tornado_frames, ignore_index=True).to_csv(
            NEW_DIR / f"tornado_{tech_key}.csv", index=False
        )
        pd.concat(sobol_frames, ignore_index=True).to_csv(
            NEW_DIR / f"sobol_{tech_key}.csv", index=False
        )
    print(f"Wrote new tornado/Sobol results to {NEW_DIR}")


def _old_vs_new(
    old_df: pd.DataFrame, new_df: pd.DataFrame, value_col: str
) -> pd.DataFrame:
    """Averages value_col across wacc_scenario per parameter, for old
    (Krok 7/8, on disk unchanged) and new (this script's output), and
    joins them - parameters only present in new (the CAPEX-per-kW bars,
    which didn't exist before Krok 9b) get old=0.
    """
    old_avg = old_df.groupby("parameter")[value_col].mean().rename("old")
    new_avg = new_df.groupby("parameter")[value_col].mean().rename("new")
    comparison = pd.concat([old_avg, new_avg], axis=1).fillna(0.0)
    return comparison.sort_values("new", ascending=False)


def _comparison_traces(comparison: pd.DataFrame) -> list[go.Bar]:
    comparison = comparison.sort_values("new")  # ascending so largest plots at top
    return [
        go.Bar(
            y=comparison.index,
            x=comparison["old"],
            orientation="h",
            name="stary (Krok 7-8)",
            marker_color=OLD_COLOR,
            showlegend=False,
        ),
        go.Bar(
            y=comparison.index,
            x=comparison["new"],
            orientation="h",
            name="nowy (Krok 9c)",
            marker_color=NEW_COLOR,
            showlegend=False,
        ),
    ]


def _build_comparison_figure() -> go.Figure:
    fig = make_subplots(
        rows=2,
        cols=2,
        subplot_titles=[
            "Tornado range - AP1000",
            "Tornado range - CANDU EC6",
            "Sobol ST - AP1000",
            "Sobol ST - CANDU EC6",
        ],
        vertical_spacing=0.15,
    )

    for col, (tech_key, _label) in enumerate(TECHNOLOGIES, start=1):
        old_tornado = pd.read_csv(OLD_DIR / f"step7_tornado_{tech_key}.csv")
        new_tornado = pd.read_csv(NEW_DIR / f"tornado_{tech_key}.csv")
        tornado_comparison = _old_vs_new(old_tornado, new_tornado, "range")
        for trace in _comparison_traces(tornado_comparison):
            fig.add_trace(trace, row=1, col=col)

        old_sobol = pd.read_csv(OLD_DIR / f"step8_sobol_{tech_key}.csv")
        new_sobol = pd.read_csv(NEW_DIR / f"sobol_{tech_key}.csv")
        sobol_comparison = _old_vs_new(old_sobol, new_sobol, "ST")
        for trace in _comparison_traces(sobol_comparison):
            fig.add_trace(trace, row=2, col=col)

    # Manual legend (bars don't auto-legend with showlegend=False per-trace above).
    fig.add_trace(
        go.Bar(
            x=[None],
            y=[None],
            marker_color=OLD_COLOR,
            name="stary (Krok 7-8, CANDU CAPEX niedoszacowany)",
            showlegend=True,
        )
    )
    fig.add_trace(
        go.Bar(
            x=[None],
            y=[None],
            marker_color=NEW_COLOR,
            name="nowy (Krok 9c, CAPEX porownywalny)",
            showlegend=True,
        )
    )

    fig.update_layout(
        template="plotly_white",
        title="Krok 9c: ranking czynnikow niepewnosci - przed i po realnym CAPEX CANDU EC6 (usrednione WACC gov/comm)",
        barmode="group",
        height=900,
        width=1500,
    )
    return fig


def main() -> None:
    repo_root = REPO_ROOT
    registry = load_assumptions_registry(
        repo_root / "config" / "assumptions_registry.json"
    )
    scenarios = build_base_scenarios(registry)

    _generate_new_results(registry, scenarios)

    fig = _build_comparison_figure()
    png_path = DATA_DIR / "step9c_tornado_sobol_comparison.png"
    kaleido.write_fig_sync(
        fig,
        path=str(png_path),
        opts={"width": 1500, "height": 900, "scale": 2},
        kopts={"path": CHROMIUM_PATH},
    )
    print(f"Wrote {png_path}")


if __name__ == "__main__":
    main()
