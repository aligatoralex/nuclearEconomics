import datetime
import html
from pathlib import Path

import kaleido
import pandas as pd
import plotly.graph_objects as go

from src.schemas import load_assumptions_registry

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data" / "output"
OUTPUT_PATH = REPO_ROOT / "reports" / "step10_results_dashboard.html"
CHROMIUM_PATH = "/opt/pw-browsers/chromium"

# The 4 declared color roles. Tier badges (green/yellow/red) are a
# separate, conventional traffic-light set used only in the registry
# table - "tier1=green" isn't one of these 4 roles, so it's kept out of
# them rather than silently folded in (see plan/commit notes).
COLOR_AP1000 = "#4C6FE7"
COLOR_CANDU = "#E2574C"
COLOR_WARNING = "#F2B134"
COLOR_NEUTRAL = "#6B7280"
TIER_BADGE_COLORS = {1: "#2E9E5B", 2: COLOR_WARNING, 3: "#C0392B"}

CANDU_CAPEX_PARAM = "CANDU_EC6_CAPEX_usd_per_kW"


def _fig_to_inline_svg(fig: go.Figure, width: int, height: int) -> str:
    """Renders a Plotly figure to an inline SVG string at generation time
    (via kaleido) instead of shipping Plotly.js + live JSON for
    client-side rendering. Verified during development that the
    cdnjs.cloudflare.com CDN is unreachable in this sandboxed environment
    (ERR_TUNNEL_CONNECTION_FAILED) - a professor opening this file
    offline or behind a restrictive network would hit the same blank-chart
    failure. Pre-rendered SVG has zero runtime network dependency, which
    is a strictly safer reading of "self-contained, no live API calls".
    """
    svg_bytes = kaleido.calc_fig_sync(
        fig,
        opts={"format": "svg", "width": width, "height": height, "scale": 1},
        kopts={"path": CHROMIUM_PATH},
    )
    return svg_bytes.decode("utf-8")


def _load_apples_to_apples_stats() -> dict:
    df = pd.read_csv(DATA_DIR / "step9_apples_to_apples_lcoe.csv")
    stats = {}
    for scenario in ("ap1000", "candu_ec6"):
        for wacc_scenario in ("government", "commercial"):
            subset = df[(df["scenario"] == scenario) & (df["wacc_scenario"] == wacc_scenario)][
                "lcoe_usd_mwh"
            ]
            stats[f"{scenario}_{wacc_scenario}"] = {
                "p10": subset.quantile(0.10),
                "mid": subset.median(),
                "p90": subset.quantile(0.90),
            }
    return stats


def _load_sobol_rankings() -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    ap1000_df = pd.read_csv(DATA_DIR / "step9c_tornado_sobol_updated" / "sobol_ap1000.csv")
    candu_df = pd.read_csv(DATA_DIR / "step9c_tornado_sobol_updated" / "sobol_candu_ec6.csv")

    ap1000_gov = ap1000_df[ap1000_df["wacc_scenario"] == "government"].sort_values(
        "ST", ascending=False
    )
    candu_gov = candu_df[candu_df["wacc_scenario"] == "government"].sort_values(
        "ST", ascending=False
    )

    combined = pd.concat([ap1000_df, candu_df], ignore_index=True)
    top_row = combined.sort_values("ST", ascending=False).iloc[0]
    dominant_factor = {"parameter": top_row["parameter"], "ST": float(top_row["ST"])}

    return ap1000_gov, candu_gov, dominant_factor


def _build_kpi_cards(stats: dict, dominant_factor: dict) -> str:
    ap1000 = stats["ap1000_government"]
    candu = stats["candu_ec6_government"]
    diff_pct = (candu["mid"] - ap1000["mid"]) / ap1000["mid"] * 100

    return f"""
    <div class="kpi-card" style="border-top-color:{COLOR_AP1000}">
      <div class="kpi-label">AP1000 LCOE (WACC rzadowy)</div>
      <div class="kpi-value">{ap1000["mid"]:.1f} <span class="kpi-unit">USD/MWh</span></div>
      <div class="kpi-sub">P10-P90: {ap1000["p10"]:.0f} - {ap1000["p90"]:.0f}</div>
    </div>
    <div class="kpi-card" style="border-top-color:{COLOR_CANDU}">
      <div class="kpi-label">CANDU EC6 LCOE (WACC rzadowy)</div>
      <div class="kpi-value">{candu["mid"]:.1f} <span class="kpi-unit">USD/MWh</span></div>
      <div class="kpi-sub">P10-P90: {candu["p10"]:.0f} - {candu["p90"]:.0f}</div>
    </div>
    <div class="kpi-card" style="border-top-color:{COLOR_NEUTRAL}">
      <div class="kpi-label">Roznica CANDU vs AP1000</div>
      <div class="kpi-value">{diff_pct:+.1f}<span class="kpi-unit">%</span></div>
      <div class="kpi-sub">Marginalna przy porownywalnym CAPEX - Krok 9b</div>
    </div>
    <div class="kpi-card" style="border-top-color:{COLOR_WARNING}">
      <div class="kpi-label">Dominujacy czynnik niepewnosci</div>
      <div class="kpi-value" style="font-size:1.4rem">{dominant_factor["parameter"]}</div>
      <div class="kpi-sub">Sobol ST = {dominant_factor["ST"]:.2f}</div>
    </div>
    """


def _build_ranking_svg(ap1000_gov: pd.DataFrame, candu_gov: pd.DataFrame) -> str:
    ap1000_sorted = ap1000_gov.sort_values("ST")
    candu_sorted = candu_gov.sort_values("ST")

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            orientation="h",
            x=ap1000_sorted["ST"],
            y=["AP1000: " + p for p in ap1000_sorted["parameter"]],
            marker_color=COLOR_AP1000,
            name="AP1000",
        )
    )
    fig.add_trace(
        go.Bar(
            orientation="h",
            x=candu_sorted["ST"],
            y=["CANDU: " + p for p in candu_sorted["parameter"]],
            marker_color=COLOR_CANDU,
            name="CANDU EC6",
        )
    )
    fig.update_layout(
        title={"text": "Sobol ST, WACC rzadowy (Krok 9c)", "font": {"size": 14}},
        margin={"l": 230, "r": 10, "t": 40, "b": 30},
        xaxis_title="Sobol ST",
        showlegend=False,
        font={"size": 11},
        template="plotly_white",
    )
    return _fig_to_inline_svg(fig, width=900, height=470)


def _build_boxplot_svg() -> str:
    df = pd.read_csv(DATA_DIR / "step9_apples_to_apples_lcoe.csv")
    fig = go.Figure()
    for scenario, color, label in [
        ("ap1000", COLOR_AP1000, "AP1000"),
        ("candu_ec6", COLOR_CANDU, "CANDU EC6"),
    ]:
        subset = df[df["scenario"] == scenario]
        fig.add_trace(
            go.Box(
                x=subset["wacc_scenario"],
                y=subset["lcoe_usd_mwh"],
                name=label,
                marker_color=color,
                boxpoints=False,
            )
        )
    fig.update_layout(
        title={"text": "LCOE apples-to-apples, N=1000 (Krok 9b)", "font": {"size": 14}},
        margin={"l": 50, "r": 10, "t": 40, "b": 30},
        yaxis_title="LCOE (USD/MWh)",
        boxmode="group",
        legend={"orientation": "h", "y": -0.15},
        font={"size": 11},
        template="plotly_white",
    )
    return _fig_to_inline_svg(fig, width=900, height=470)


def _format_number(value: float) -> str:
    if abs(value) >= 1_000_000:
        millions = value / 1_000_000
        return f"{millions:g}M"
    if abs(value) == int(value):
        return f"{int(value):,}"
    return f"{value:g}"


def _build_registry_table_rows(registry) -> str:
    rows = []
    for entry in registry:
        badge_color = TIER_BADGE_COLORS[entry.tier]
        confirmation_icon = "&#9888;" if entry.requires_confirmation else "&#10003;"
        confirmation_title = (
            "Wymaga potwierdzenia" if entry.requires_confirmation else "Potwierdzone / silne zrodlo"
        )
        source_escaped = html.escape(entry.source)
        extra_badge = ""
        if entry.parameter == CANDU_CAPEX_PARAM:
            extra_badge = (
                '<span class="offer-badge">Tier 2 &mdash; oferta przedprzetargowa '
                "AtkinsR&eacute;alis, luty 2026, nie kontrakt</span>"
            )
        value_range = (
            f"{_format_number(entry.value_or_range.min)} / "
            f"{_format_number(entry.value_or_range.mid)} / "
            f"{_format_number(entry.value_or_range.max)}"
        )
        rows.append(
            f"""
            <tr>
              <td>{html.escape(entry.parameter)}{extra_badge}</td>
              <td>{value_range}</td>
              <td><span class="tier-badge" style="background:{badge_color}">Tier {entry.tier}</span></td>
              <td><span title="{confirmation_title}">{confirmation_icon}</span></td>
              <td class="source-cell" title="{source_escaped}">{source_escaped}</td>
            </tr>
            """
        )
    return "".join(rows)


def build_dashboard_html() -> str:
    registry = load_assumptions_registry(REPO_ROOT / "config" / "assumptions_registry.json")
    stats = _load_apples_to_apples_stats()
    ap1000_gov, candu_gov, dominant_factor = _load_sobol_rankings()

    kpi_html = _build_kpi_cards(stats, dominant_factor)
    ranking_svg = _build_ranking_svg(ap1000_gov, candu_gov)
    boxplot_svg = _build_boxplot_svg()
    table_rows_html = _build_registry_table_rows(registry)

    generated_at = datetime.datetime.now(tz=datetime.UTC).date().isoformat()

    return f"""<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<title>LCOE AP1000 vs CANDU EC6 &mdash; Krok 9/10</title>
<style>
  :root {{
    --color-ap1000: {COLOR_AP1000};
    --color-candu: {COLOR_CANDU};
    --color-warning: {COLOR_WARNING};
    --color-neutral: {COLOR_NEUTRAL};
    --bg-page: #fafafa;
    --text-primary: #1a1a1a;
    --border-color: #ddd;
    --border-color-soft: #f0f0f0;
    /* Chart panels stay white in both themes - the SVGs are pre-rendered
       with a white plot background at generation time, so the panel
       itself must match rather than go dark around a white chart. */
    --card-bg: #ffffff;
  }}
  @media (prefers-color-scheme: dark) {{
    :root {{
      --bg-page: #16181d;
      --text-primary: #e8e8ea;
      --border-color: #3a3d44;
      --border-color-soft: #2a2d33;
    }}
  }}
  :root[data-theme="dark"] {{
    --bg-page: #16181d;
    --text-primary: #e8e8ea;
    --border-color: #3a3d44;
    --border-color-soft: #2a2d33;
  }}
  :root[data-theme="light"] {{
    --bg-page: #fafafa;
    --text-primary: #1a1a1a;
    --border-color: #ddd;
    --border-color-soft: #f0f0f0;
  }}
  * {{ box-sizing: border-box; }}
  html, body {{
    margin: 0; padding: 0; height: 100vh; width: 100vw; overflow: hidden;
    font-family: -apple-system, "Segoe UI", Roboto, sans-serif;
    color: var(--text-primary); background: var(--bg-page);
  }}
  .dashboard {{
    display: grid;
    grid-template-rows: 5vh 15vh 51vh 27vh;
    height: 100vh; width: 100vw;
    padding: 6px 16px; gap: 6px;
  }}
  h1 {{ margin: 0; font-size: 1.1rem; color: var(--color-neutral); font-weight: 600; }}
  .kpi-row {{ display: flex; gap: 10px; }}
  .kpi-card {{
    flex: 1; background: var(--card-bg); color: #1a1a1a; border-top: 4px solid; border-radius: 6px;
    padding: 10px 14px; box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    display: flex; flex-direction: column; justify-content: center;
  }}
  .kpi-label {{ font-size: 0.72rem; color: var(--color-neutral); text-transform: uppercase; letter-spacing: 0.03em; }}
  .kpi-value {{ font-size: 1.9rem; font-weight: 700; line-height: 1.15; }}
  .kpi-unit {{ font-size: 1rem; font-weight: 400; color: var(--color-neutral); }}
  .kpi-sub {{ font-size: 0.75rem; color: var(--color-neutral); margin-top: 2px; }}
  .chart-row {{ display: flex; gap: 10px; min-height: 0; }}
  .chart-panel {{
    flex: 1; background: var(--card-bg); border-radius: 6px; box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    padding: 4px; display: flex; flex-direction: column; min-height: 0;
  }}
  .chart-panel svg {{ width: 100%; height: auto; max-height: 100%; }}
  .chart-svg-wrap {{ flex: 1; min-height: 0; display: flex; align-items: center; justify-content: center; }}
  .chart-source {{ font-size: 0.65rem; color: var(--color-neutral); padding: 2px 8px; }}
  .table-panel {{
    background: var(--card-bg); color: #1a1a1a; border-radius: 6px; box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    padding: 8px 14px; display: flex; flex-direction: column; min-height: 0;
  }}
  .table-panel h2 {{ margin: 0 0 4px 0; font-size: 0.85rem; color: var(--color-neutral); }}
  .table-scroll {{ overflow-y: auto; flex: 1; min-height: 0; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 0.72rem; }}
  thead th {{
    position: sticky; top: 0; background: var(--card-bg); text-align: left;
    padding: 3px 8px; border-bottom: 1px solid var(--border-color); color: var(--color-neutral);
  }}
  tbody td {{ padding: 3px 8px; border-bottom: 1px solid var(--border-color-soft); vertical-align: top; }}
  .source-cell {{
    max-width: 320px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    cursor: help;
  }}
  .tier-badge {{
    color: white; border-radius: 3px; padding: 1px 6px; font-size: 0.68rem; font-weight: 600;
  }}
  .offer-badge {{
    display: inline-block; margin-left: 6px; background: var(--color-warning);
    color: #3a2c00; border-radius: 3px; padding: 1px 6px; font-size: 0.62rem; font-weight: 600;
  }}
</style>
</head>
<body>
<div class="dashboard">
  <h1>LCOE AP1000 vs CANDU EC6 &mdash; wyniki Krok 9 (dane zamrozone {generated_at})</h1>

  <div class="kpi-row">
    {kpi_html}
  </div>

  <div class="chart-row">
    <div class="chart-panel">
      <div class="chart-svg-wrap">{ranking_svg}</div>
      <div class="chart-source">Zrodlo: data/output/step9c_tornado_sobol_updated/sobol_*.csv (Krok 9c, {generated_at})</div>
    </div>
    <div class="chart-panel">
      <div class="chart-svg-wrap">{boxplot_svg}</div>
      <div class="chart-source">Zrodlo: data/output/step9_apples_to_apples_lcoe.csv (Krok 9b, {generated_at})</div>
    </div>
  </div>

  <div class="table-panel">
    <h2>Rejestr zalozen (config/assumptions_registry.json, {len(registry)} parametrow)</h2>
    <div class="table-scroll">
      <table>
        <thead>
          <tr><th>Parametr</th><th>Min / Mid / Max</th><th>Tier</th><th>Potw.</th><th>Zrodlo</th></tr>
        </thead>
        <tbody>
          {table_rows_html}
        </tbody>
      </table>
    </div>
  </div>
</div>
</body>
</html>
"""


def main() -> None:
    html_content = build_dashboard_html()
    OUTPUT_PATH.write_text(html_content)
    print(f"Wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
