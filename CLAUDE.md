# CLAUDE.md

Technical conventions for this repo. No domain knowledge here — see
`config/assumptions_registry.json` and its schema for that.

## Stack

- Python 3.11+
- numpy, scipy, pandas — numerical core
- SALib — Latin Hypercube Sampling / Sobol sensitivity analysis
- pydantic — input validation
- plotly — visualization
- pytest — testing

## Core conventions

1. **Separation of concerns**: all numerical/simulation logic lives in
   `src/`. Everything in `viz/` reads exclusively from `data/output/*.csv`
   and never performs its own calculations.
2. **Tiered input validation**: every input parameter is assigned a
   credibility tier (1/2/3) and must pass a pydantic schema before it is
   used in a simulation. No parameter enters `src/` code as a bare literal.

## Commands

```bash
pytest              # run tests
ruff check .         # lint
ruff format .        # format
```
