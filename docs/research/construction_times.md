# Construction times — AP1000 vs CANDU EC6 (research note)

Scope: verify/refine `construction_years_AP1000` and `construction_years_CANDU_EC6`
in `config/assumptions_registry.json`. Read-only research; no registry or `src/`
files were modified by this note. All durations below are **first concrete →
commercial operation (COD)**, matching the parameter's intended meaning
(the model uses `construction_years` to size the IDC S-curve in
`src/idc_engine.calculate_idc`, i.e. the interest-bearing build window).

## 1. Source table

| Project | Unit | Country | First concrete | Commercial operation | Duration | Source | Confidence |
|---|---|---|---|---|---|---|---|
| Vogtle 3&4 | Unit 3 | USA (FOAK Western) | 2013-03-12/15 | 2023-07-31 | **10.4 yr** | [NucNet — first concrete](https://www.nucnet.org/news/new-milestone-in-us-as-first-concrete-is-poured-at-vogtle-3); [MEAG Power — Vogtle 3 COD](https://www.meagpower.org/vogtle-3-cod/) | High (hard dates, official) |
| Vogtle 3&4 | Unit 4 | USA (FOAK Western) | 2013-11-21 | 2024-04-29 | **10.4 yr** | [Southern Co. — final concrete placement](https://www.southerncompany.com/newsroom/clean-energy/final-major-concrete-placement-completed-vogtle-unit-3.html); [Georgia Power — Unit 4 COD](https://www.georgiapower.com/news-hub/press-releases/vogtle-unit-4-enters-commercial-operation.html) | High |
| Sanmen | Unit 1 | China (FOAK, first AP1000 worldwide) | 2009-04-19 | 2018-09-21 | **9.4 yr** | [World Nuclear News — first AP1000 in commercial operation](https://www.world-nuclear-news.org/Articles/First-AP1000-reactor-enters-commercial-operation); [CNNC](https://en.cnnc.com.cn/2018-09/21/c_1026695.htm) | High |
| Sanmen | Unit 2 | China | 2009-12-15 | 2018-11-05 | **8.9 yr** | [NucNet — Sanmen-2 commercial operation](https://www.nucnet.org/news/china-s-sanmen-2-ap1000-begins-commercial-operation); [World Nuclear News](https://www.world-nuclear-news.org/articles/sanmen-2-ap1000-enters-commercial-operation) | High |
| Haiyang | Unit 1 | China | 2009-09-24 | 2018-10-22 | **9.1 yr** | [NEI — first concrete at Haiyang](https://www.neimagazine.com/news/first-concrete-at-china-s-haiyang/); [NucNet — Haiyang-1 commercial operation](https://www.nucnet.org/news/china-s-haiyang-1-becomes-second-westinghouse-ap1000-to-begin-commercial-operation) | High |
| Haiyang | Unit 2 | China | 2010-06-20 | 2019-01-09 | **8.6 yr** (fastest AP1000 built to date) | [PRNewswire — record-time first concrete pour](https://www.prnewswire.com/news-releases/first-concrete-pour-for-haiyang-unit-2-completed-in-record-time-97151039.html); [NucNet — Haiyang-2 commercial operation](https://www.nucnet.org/news/haiyang-2-becomes-fourth-westinghouse-ap1000-reactor-to-begin-commercial-operation-in-china) | High |
| Westinghouse vendor claim | NOAK, generic | — | — | — | **"36 months first concrete → fuel load"** (not COD; company/NOAK marketing claim, never achieved in any completed build) | [Search synthesis of AP1000 design-basis / NOAK claim documents, incl. NucNet "AP1000 reactor is proven technology that has reached NOAK status"](https://www.nucnet.org/news/ap1000-reactor-is-proven-technology-that-has-reached-noak-status-8-2-2022) | **Low** as a COD predictor — it is a sub-milestone target (fuel load, not COD), and no AP1000 build (China or US) has ever come close to it end-to-end |
| EJ1 Poland | Block 1, AP1000 | Poland | planned 2028 | planned 2036 | **8 yr** (official government/PEJ planning schedule) | [Polish press synthesis — PEJ/Westinghouse-Bechtel schedule](https://www.trojmiasto.pl/biznes/Jadrowy-przelom-juz-w-tym-roku-Rzad-zapowiada-final-umowy-z-Westinghouse-i-Bechtel-n223141.html), corroborated by multiple PL energy-press sources (wnp.pl, energetyka24.com) | Medium — official planning date, but pre-construction and thus can still slip; not yet a contractual/EPC-committed schedule |
| Qinshan Phase III | Unit 1 | China (CANDU-6) | 1998-06-08 | 2002-12-31 | **4.6 yr** (fastest CANDU-6 built to date, ahead of schedule) | [World Nuclear News — Chinese Candu reactor sets operating records](https://www.world-nuclear-news.org/articles/chinese-candu-reactor-sets-operating-records); [IAEA INIS — Qinshan Phase III case study](https://inis.iaea.org/records/twbec-97n42) | High |
| Qinshan Phase III | Unit 2 | China (CANDU-6) | 1998-09-25 | 2003-07-24 | **4.8 yr** | same as above | High |
| Cernavodă | Unit 1 | Romania (CANDU-6) | 1982-07 | 1996-12 | **~14.4 yr** (communist-era funding suspension, not representative of technical build time) | [World Nuclear Association — Romania country profile](https://world-nuclear.org/information-library/country-profiles/countries-o-s/romania) | High as a fact, but **not representative** — extreme political/financing outlier |
| Cernavodă | Unit 2 | Romania (CANDU-6) | 1983-07 | 2007-10-05 | **~24.3 yr** (construction physically halted for over a decade, then resumed with EU financing) | [NucNet — Cernavoda-2 commercial operation](https://www.nucnet.org/news/romania-s-cernavoda-2-begins-commercial-operation); WNA Romania profile | High as a fact, **excluded from range-setting** — this is a financing-halt outlier, not a construction-duration data point |
| AtkinsRéalis vendor claim | EC6, generic | — | — | — | **"5–6 years first concrete → grid synchronization"**; company states their fastest-ever build was **4 yr 11 mo** (China) | [Polish press synthesis, inzynieria.com — AtkinsRéalis EJ2 statements](https://inzynieria.com/energetyka/elektrownie_atomowe/wiadomosci/100693,to-ma-zmienic-polska-energetyke-na-dekady-jest-nowy-harmonogram) | Medium-High — this vendor claim is *corroborated* by the real Qinshan Unit 1 precedent (4.6 yr), unlike the Westinghouse NOAK claim which has no matching real build |
| EJ2 Poland | Block 1, tech TBD | Poland | planned 2032 | planned 2040 | **8 yr** (official, but **tech-neutral** — reactor vendor not yet selected as of this writing; competitive dialogue concludes 2027) | [inzynieria.com — EJ2 schedule](https://inzynieria.com/energetyka/elektrownie_atomowe/wiadomosci/100693,to-ma-zmienic-polska-energetyke-na-dekady-jest-nowy-harmonogram) | Medium — generic government planning figure, not CANDU-specific, and pre-selection |

Note on "first concrete" vs. "construction start": for Vogtle, Sanmen, Haiyang,
and Qinshan the dates above are the nuclear-island basemat first-concrete pour
(the standard IAEA PRIS "construction start" milestone), which is also what
`src/idc_engine.calculate_idc` implicitly assumes as t=0 for the IDC S-curve.
Cernavodă historical dates are civil-works construction start (less precisely
documented at the day level; sourced to month/year only), which is adequate
for this note's purpose (they are excluded from the recommended range anyway).

## 2. Proposed min/mid/max

### `construction_years_AP1000`

| | current | proposed | driver |
|---|---|---|---|
| min | 6 | **8** | Fastest real AP1000 build to date is Haiyang 2 at 8.6 yr. The current min=6 is closer to the Westinghouse 36-month NOAK claim, which is a fuel-load target (not COD) that **no completed AP1000 build — Chinese fleet or US — has ever approached**. Recommend anchoring the floor to the best *realized* precedent instead of an unachieved marketing target, rounded down slightly (8.6 → 8) to leave a small margin for a hypothetical best-case NOAK/fleet effect not yet observed anywhere.
| mid | 7 | **9** | Average of the four completed Chinese units (9.4, 8.9, 9.1, 8.6 → mean 9.0 yr). This also lines up closely with Poland's own official EJ1 planning assumption (8 yr, but pre-construction and typically optimistic at this stage) and is well below the realized Western FOAK figure.
| max | 9 | **10.5** | Vogtle 3/4 realized duration (10.4 yr each), the only Western/OECD AP1000 precedent and the most relevant analogue for regulatory/labor/supply-chain conditions closer to Poland's than China's fleet-construction environment. Rounded up slightly for margin.

Net effect: the proposed range (8 / 9 / 10.5) is narrower and shifted upward
relative to the current (6 / 7 / 9) registry entry. The current range's low
end is not supported by any completed build; its high end (9) is *below* both
realized Vogtle units (10.4 yr each).

### `construction_years_CANDU_EC6`

| | current | proposed | driver |
|---|---|---|---|
| min | 5 | **5** (unchanged) | Matches AtkinsRéalis's own stated "5–6 years first concrete → grid sync" and is corroborated by the fastest real CANDU-6 build (Qinshan Unit 1, 4.6 yr to COD, i.e. even faster than the vendor's own current standard claim). This is materially better-evidenced than the AP1000 min, because here the vendor claim and a completed real build actually agree.
| mid | 6 | **6.5** | Midpoint of the vendor's own "5–6 yr to grid sync" range, plus a small allowance for grid-sync → COD lag (Qinshan's grid-sync-to-COD gaps were on the order of weeks to a few months). Keeps CANDU's central estimate meaningfully below AP1000's (6.5 vs 9), consistent with both the Qinshan precedent and the vendor's own comparative marketing claim, while not simply repeating the vendor's number unadjusted.
| max | 8 | **9** | The only forward-looking, Poland-specific anchor available for the *upper* end is EJ2's official (tech-neutral) government schedule: first concrete 2032 → COD 2040 = 8 yr. Since this figure is not CANDU-specific (technology not yet selected) and a real FOAK-in-new-country build could run longer, a modest buffer above it (9 yr) is proposed. Cernavodă's 14.4 yr and 24.3 yr durations are **explicitly excluded** from this range — both were financing/political halts, not construction-technology-driven delays, and using them would conflate two different failure modes.

## 3. Tier and `requires_confirmation`

Both parameters: **recommend keeping Tier 2, `requires_confirmation: true`.**

- The underlying historical durations (Vogtle, Sanmen, Haiyang, Qinshan,
  Cernavodă) are themselves hard, well-documented facts — Tier-1 grade as
  historical data points. But the *parameter* being estimated is a
  forward-looking construction duration for a **hypothetical new build in
  Poland**, which requires judgment about how much of China's fleet-effect
  speed or Vogtle's Western-FOAK delay risk transfers to a first-of-a-kind
  Polish project. That extrapolation step is what keeps this Tier 2 rather
  than Tier 1.
- `requires_confirmation` should stay `true` for both until either (a) PEJ/
  Westinghouse-Bechtel publish an EPC-contract-level schedule for EJ1 (the
  current 2028/2036 dates are a planning assumption, not yet a signed
  construction schedule), or (b) AtkinsRéalis/the EJ2 process publishes a
  CANDU-specific (not tech-neutral) schedule for Poland — expected only after
  the 2027 technology selection concludes competitive dialogue.

## 4. Hard facts vs. extrapolation — explicit flags

**Hard facts (verifiable dates from primary/trade-press sources):**
- All six completed AP1000 first-concrete and COD dates (Vogtle 3, Vogtle 4,
  Sanmen 1, Sanmen 2, Haiyang 1, Haiyang 2).
- Both Qinshan Phase III CANDU-6 first-concrete and COD dates.
- Both Cernavodă CANDU-6 dates (month-level precision).
- The headline EJ1 (2028/2036) and EJ2 (2032/2040) planning dates as currently
  published by the Polish nuclear program.
- The Westinghouse "36 months first concrete → fuel load" and AtkinsRéalis
  "5–6 years first concrete → grid synchronization" / "fastest build 4 yr 11
  mo" claims, as **stated vendor claims** — the claims themselves are
  verifiable as claims, but their applicability to a future Polish build is
  not a fact.

**Extrapolation / judgment (this note's contribution, not sourced facts):**
- The proposed min/mid/max values themselves — these are this note's
  synthesis of the above facts into a Poland-relevant triangular range, not
  numbers published by any single source.
- The assumption that Poland's regulatory/labor/supply-chain environment for
  a FOAK build sits closer to the Vogtle (Western FOAK) experience than to
  the Chinese fleet-construction experience, for AP1000's max.
- The decision to exclude Cernavodă's realized durations from the CANDU range
  as non-representative political/financing outliers, rather than blending
  them in numerically.
- The decision to treat EJ2's 8-year tech-neutral government schedule as a
  soft ceiling anchor for CANDU specifically, despite it not being
  CANDU-committed.

## Sources (consolidated)

- [NucNet — first concrete poured at Vogtle-3](https://www.nucnet.org/news/new-milestone-in-us-as-first-concrete-is-poured-at-vogtle-3)
- [MEAG Power — Vogtle 3 commercial operation date](https://www.meagpower.org/vogtle-3-cod/)
- [Southern Company — final major concrete placement, Vogtle Unit 3](https://www.southerncompany.com/newsroom/clean-energy/final-major-concrete-placement-completed-vogtle-unit-3.html)
- [Georgia Power — Vogtle Unit 4 enters commercial operation](https://www.georgiapower.com/news-hub/press-releases/vogtle-unit-4-enters-commercial-operation.html)
- [World Nuclear News — First AP1000 reactor enters commercial operation (Sanmen 1)](https://www.world-nuclear-news.org/Articles/First-AP1000-reactor-enters-commercial-operation)
- [CNNC — First AP1000 reactor enters commercial operation](https://en.cnnc.com.cn/2018-09/21/c_1026695.htm)
- [NucNet — China's Sanmen-2 AP1000 begins commercial operation](https://www.nucnet.org/news/china-s-sanmen-2-ap1000-begins-commercial-operation)
- [World Nuclear News — Sanmen 2 AP1000 enters commercial operation](https://www.world-nuclear-news.org/articles/sanmen-2-ap1000-enters-commercial-operation)
- [Nuclear Engineering International — First concrete at China's Haiyang](https://www.neimagazine.com/news/first-concrete-at-china-s-haiyang/)
- [NucNet — China's Haiyang-1 becomes second Westinghouse AP1000 to begin commercial operation](https://www.nucnet.org/news/china-s-haiyang-1-becomes-second-westinghouse-ap1000-to-begin-commercial-operation)
- [PRNewswire — First concrete pour for Haiyang Unit 2 completed in record time](https://www.prnewswire.com/news-releases/first-concrete-pour-for-haiyang-unit-2-completed-in-record-time-97151039.html)
- [NucNet — Haiyang-2 becomes fourth Westinghouse AP1000 reactor to begin commercial operation in China](https://www.nucnet.org/news/haiyang-2-becomes-fourth-westinghouse-ap1000-reactor-to-begin-commercial-operation-in-china)
- [NucNet — AP1000 reactor is "proven technology that has reached NOAK status"](https://www.nucnet.org/news/ap1000-reactor-is-proven-technology-that-has-reached-noak-status-8-2-2022)
- [Trojmiasto.pl — EJ1 Poland schedule (PEJ/Westinghouse-Bechtel)](https://www.trojmiasto.pl/biznes/Jadrowy-przelom-juz-w-tym-roku-Rzad-zapowiada-final-umowy-z-Westinghouse-i-Bechtel-n223141.html)
- [World Nuclear News — Chinese Candu reactor sets operating records (Qinshan III)](https://www.world-nuclear-news.org/articles/chinese-candu-reactor-sets-operating-records)
- [IAEA INIS — Successful completion of the Qinshan Phase III nuclear power plant](https://inis.iaea.org/records/twbec-97n42)
- [World Nuclear Association — Nuclear Power in Romania (Cernavodă)](https://world-nuclear.org/information-library/country-profiles/countries-o-s/romania)
- [NucNet — Romania's Cernavodă-2 begins commercial operation](https://www.nucnet.org/news/romania-s-cernavoda-2-begins-commercial-operation)
- [inzynieria.com — EJ1/EJ2 Poland schedule and AtkinsRéalis EC6 statements](https://inzynieria.com/energetyka/elektrownie_atomowe/wiadomosci/100693,to-ma-zmienic-polska-energetyke-na-dekady-jest-nowy-harmonogram)

*Note: `config/assumptions_registry.json` already documents the CANDU EC6 CAPEX
offer for EJ2 (AtkinsRéalis, February 2026, 4×EC6, PLN 117–130 bn) — see
entry `CANDU_EC6_CAPEX_usd_per_kW`. That offer's own construction-schedule
claims were not separately quoted with a duration figure in the material
reviewed for this note beyond the generic AtkinsRéalis "5–6 years" statement
above; if a schedule specific to the February 2026 EJ2 offer becomes
available it should supersede the generic vendor claim used here.*
