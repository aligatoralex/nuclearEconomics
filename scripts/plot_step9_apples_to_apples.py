from pathlib import Path

import kaleido
import pandas as pd
import plotly.express as px

CHROMIUM_PATH = "/opt/pw-browsers/chromium"
CSV_PATH = Path(__file__).resolve().parent.parent / "data" / "output" / "step9_apples_to_apples_lcoe.csv"
PNG_PATH = Path(__file__).resolve().parent.parent / "data" / "output" / "step9_apples_to_apples_lcoe.png"


def main() -> None:
    df = pd.read_csv(CSV_PATH)
    fig = px.box(
        df,
        x="wacc_scenario",
        y="lcoe_usd_mwh",
        color="scenario",
        template="plotly_white",
        points=False,
        title=(
            "Krok 9: AP1000 vs CANDU EC6, CAPEX porownywalny (oba Tier 2) - "
            "roznica LCOE wynika z fuel cost i WACC, nie z artefaktu CAPEX"
        ),
        labels={"lcoe_usd_mwh": "LCOE (USD/MWh)", "wacc_scenario": "WACC", "scenario": "Technologia"},
    )
    fig.add_annotation(
        text="CAPEX porownywalny (oba Tier 2) - roznica LCOE wynika z fuel cost i WACC, nie z artefaktu CAPEX",
        xref="paper",
        yref="paper",
        x=0.5,
        y=-0.18,
        showarrow=False,
        font={"size": 12, "color": "#555555"},
    )
    fig.update_layout(margin={"b": 100})

    kaleido.write_fig_sync(
        fig,
        path=str(PNG_PATH),
        opts={"width": 1400, "height": 750, "scale": 2},
        kopts={"path": CHROMIUM_PATH},
    )
    print(f"Wrote {PNG_PATH}")


if __name__ == "__main__":
    main()
