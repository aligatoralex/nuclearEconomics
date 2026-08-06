from pathlib import Path

import kaleido
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

CHROMIUM_PATH = "/opt/pw-browsers/chromium"
DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "output"

TIER_COLORS = {1: "#9e9e9e", 2: "#f2c744", 3: "#e05a47"}
WACC_SCENARIOS = ["government", "commercial"]


def _tornado_bar_trace(subset: pd.DataFrame) -> go.Bar:
    subset = subset.sort_values("range")  # ascending so largest range plots at top
    return go.Bar(
        y=subset["parameter"],
        x=subset["range"],
        base=subset["lcoe_at_min"],
        orientation="h",
        marker_color=[TIER_COLORS[t] for t in subset["tier"]],
        showlegend=False,
        hovertemplate="%{y}<br>LCOE %{base:.1f} - %{x:.1f} USD/MWh<extra></extra>",
    )


def make_tornado_figure(df: pd.DataFrame, title: str) -> go.Figure:
    fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=[f"WACC: {w}" for w in WACC_SCENARIOS],
        shared_yaxes=False,
    )
    for col, wacc_scenario in enumerate(WACC_SCENARIOS, start=1):
        subset = df[df["wacc_scenario"] == wacc_scenario]
        fig.add_trace(_tornado_bar_trace(subset), row=1, col=col)

    # Manual legend entries for the tier color coding (bars themselves have
    # per-bar colors, not a single traced series, so they don't auto-legend).
    for tier, color in TIER_COLORS.items():
        fig.add_trace(
            go.Bar(x=[None], y=[None], marker_color=color, name=f"Tier {tier}", showlegend=True)
        )

    fig.update_layout(
        template="plotly_white",
        title=title,
        barmode="overlay",
        xaxis_title="LCOE (USD/MWh)",
        xaxis2_title="LCOE (USD/MWh)",
    )
    return fig


def main() -> None:
    technologies = [
        ("ap1000", "AP1000"),
        ("candu_ec6", "CANDU EC6"),
    ]
    for tech_key, tech_label in technologies:
        df = pd.read_csv(DATA_DIR / f"step7_tornado_{tech_key}.csv")
        fig = make_tornado_figure(
            df, f"Krok 7: OAT tornado - {tech_label} (colored by tier, illustrative)"
        )
        png_path = DATA_DIR / f"step7_tornado_{tech_key}.png"
        kaleido.write_fig_sync(
            fig,
            path=str(png_path),
            opts={"width": 1400, "height": 600, "scale": 2},
            kopts={"path": CHROMIUM_PATH},
        )
        print(f"Wrote {png_path}")


if __name__ == "__main__":
    main()
