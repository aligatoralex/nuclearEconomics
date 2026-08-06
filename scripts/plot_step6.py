from pathlib import Path

import kaleido
import pandas as pd
import plotly.express as px

# kaleido v1 wants its own Chrome by default; point it at the environment's
# pre-installed Chromium instead of downloading a new one.
CHROMIUM_PATH = "/opt/pw-browsers/chromium"

CSV_PATH = Path(__file__).resolve().parent.parent / "data" / "output" / "step6_lhs_results.csv"
PNG_PATH = Path(__file__).resolve().parent.parent / "data" / "output" / "step6_lcoe_distributions.png"


def main() -> None:
    df = pd.read_csv(CSV_PATH)
    fig = px.histogram(
        df,
        x="lcoe_usd_mwh",
        color="scenario",
        facet_col="wacc_scenario",
        barmode="overlay",
        opacity=0.6,
        nbins=40,
        template="plotly_white",
        title="Krok 6: LCOE distribution by scenario and WACC (N=1000 LHS, illustrative placeholder data)",
        labels={"lcoe_usd_mwh": "LCOE (USD/MWh)", "wacc_scenario": "WACC"},
    )
    kaleido.write_fig_sync(
        fig,
        path=str(PNG_PATH),
        opts={"width": 1400, "height": 700, "scale": 2},
        kopts={"path": CHROMIUM_PATH},
    )
    print(f"Wrote {PNG_PATH}")


if __name__ == "__main__":
    main()
