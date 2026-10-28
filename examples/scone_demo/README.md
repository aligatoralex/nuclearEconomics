# SCONE demo

Minimal, runnable demo of [SCONE](https://github.com/CambridgeNuclear/SCONE)
(MIT, Cambridge) – the open-source Monte Carlo code from
`docs/serpent_alternatives.md`.

## What it does
`inf_u235` is an eigenvalue calculation (5000 neutrons/cycle, 30 inactive +
100 active cycles) in an infinite medium (reflective box) of a toy
multigroup U-235 library (`XS/URRa_2_1_XSS`, taken from SCONE's own test
inputs). It uses delta tracking (`transportOperatorDT`).

## Run
```bash
./run_demo.sh
```
Builds SCONE (pinned commit `a4a02bfb24`, no MPI/OpenMP/tests; first build takes a few minutes; needs network, `git`, `python3`, `gfortran`, `cmake`, LAPACK/BLAS) and runs
the input. Reference result from this session's build: **k-eff ≈ 1.6314 ± 0.00005**,
about 15 s on one core. A clean run of `run_demo.sh` (OpenMP off) gave 1.63135 ± 0.00004.

## Limits
- This is **not** an SNR-300 model. The cross sections are a toy data set used
  for SCONE tests; a real SFR/MOX core needs ACE (continuous-energy) libraries
  (`$SCONE_ACE`, e.g. ENDF/B) and the core geometry, which this repo does not have.
- SCONE's authors say it prioritises modifiability over speed; for production
  work see OpenMC in `docs/serpent_alternatives.md`.
- Per CLAUDE.md, nothing here feeds the economics model; any future use of
  results must go through `src/` and the assumptions registry.

## Licence
`inf_u235` and `XS/URRa_2_1_XSS` are copied from SCONE (MIT, © Cambridge Nuclear); see `LICENCE` in the SCONE repository.
