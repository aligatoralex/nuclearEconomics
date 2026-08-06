from pathlib import Path

import kaleido
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

CHROMIUM_PATH = "/opt/pw-browsers/chromium"
DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "output"

TIER_COLORS = {1: "#9e9e9e", 2: "#f2c744", 3: "#e05a47"}
S1_COLOR = "#c9d6e3"  # neutral reference shade, not tier-coded (S1 is a reference value, not the headline metric)
WACC_SCENARIOS = ["government", "commercial"]


def _sobol_bar_traces(subset: pd.DataFrame) -> list[go.Bar]:
    subset = subset.sort_values("ST")  # ascending so largest ST plots at top
    st_trace = go.Bar(
        y=subset["parameter"],
        x=subset["ST"],
        orientation="h",
        name="ST",
        marker_color=[TIER_COLORS[t] for t in subset["tier"]],
        showlegend=False,
        hovertemplate="%{y}<br>ST %{x:.3f}<extra></extra>",
    )
    s1_trace = go.Bar(
        y=subset["parameter"],
        x=subset["S1"],
        orientation="h",
        name="S1",
        marker_color=S1_COLOR,
        showlegend=False,
        hovertemplate="%{y}<br>S1 %{x:.3f}<extra></extra>",
    )
    return [st_trace, s1_trace]


def make_sobol_figure(df: pd.DataFrame, title: str) -> go.Figure:
    fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=[f"WACC: {w}" for w in WACC_SCENARIOS],
        shared_yaxes=False,
    )
    for col, wacc_scenario in enumerate(WACC_SCENARIOS, start=1):
        subset = df[df["wacc_scenario"] == wacc_scenario]
        for trace in _sobol_bar_traces(subset):
            fig.add_trace(trace, row=1, col=col)

    # Manual legend entries: tier color coding for ST bars, plus the S1
    # reference shade (bars themselves have per-bar colors, not a single
    # traced series, so they don't auto-legend).
    for tier, color in TIER_COLORS.items():
        fig.add_trace(
            go.Bar(x=[None], y=[None], marker_color=color, name=f"ST, Tier {tier}", showlegend=True)
        )
    fig.add_trace(
        go.Bar(x=[None], y=[None], marker_color=S1_COLOR, name="S1 (main effect)", showlegend=True)
    )

    fig.update_layout(
        template="plotly_white",
        title=title,
        barmode="group",
        xaxis_title="Sobol index",
        xaxis2_title="Sobol index",
    )
    return fig


def main() -> None:
    technologies = [
        ("ap1000", "AP1000"),
        ("candu_ec6", "CANDU EC6"),
    ]
    for tech_key, tech_label in technologies:
        df = pd.read_csv(DATA_DIR / f"step8_sobol_{tech_key}.csv")
        fig = make_sobol_figure(
            df, f"Krok 8: Sobol S1 vs ST - {tech_label} (colored by tier, illustrative)"
        )
        png_path = DATA_DIR / f"step8_sobol_{tech_key}.png"
        kaleido.write_fig_sync(
            fig,
            path=str(png_path),
            opts={"width": 1400, "height": 600, "scale": 2},
            kopts={"path": CHROMIUM_PATH},
        )
        print(f"Wrote {png_path}")


if __name__ == "__main__":
    main()
