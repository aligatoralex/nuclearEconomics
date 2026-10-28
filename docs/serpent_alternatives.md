# Serpent and fast open-source alternatives

Research note, 2026-10-28. Claims marked **[unverified]** come from general
knowledge, not from sources checked in this session; confirm before relying on them.

## 1. Serpent in brief

- 3D continuous-energy Monte Carlo reactor-physics and burnup code, developed by
  VTT (Finland) since 2004. Neutron, photon and coupled transport; ACE cross sections;
  built-in depletion; homogenized group-constant generation for nodal codes
  (e.g. VTT's Ants, part of the Kraken framework).
- **Not open source.** Licences: single-user research (via OECD/NEA Data Bank or
  RSICC, non-commercial), academic group licence (VTT), and negotiated commercial
  licence (VTT). Export-controlled.
- Consequence for this repo: it cannot be redistributed or run in CI, and results
  cannot be reproduced by third parties without their own licence.

Sources: [serpent.vtt.fi](https://serpent.vtt.fi/), [Serpent distribution](https://serpent.vtt.fi/serpent/users.htm),
[NEA Data Bank NEA-1923](https://databank.io.oecd-nea.org/codes/serpent).

## 2. Candidates

| Code | Type | Licence | Fit as Serpent replacement | Speed / ease of setup |
|---|---|---|---|---|
| [OpenMC](https://github.com/openmc-dev/openmc) | 3D CE Monte Carlo + depletion | MIT | **Best match** – same physics class, Python API, depletion chains | `conda install openmc` (conda-forge, linux-64/macOS) or `docker run openmc/openmc`; Monte Carlo is still slower than Serpent per case (see below) |
| [SCONE](https://github.com/CambridgeNuclear/SCONE) | 3D CE Monte Carlo | MIT | Teaching/prototyping; authors prioritise modifiability over performance | Needs source build (Fortran) **[unverified]**; not for production |
| [OpenMOC](https://github.com/mit-crpg/OpenMOC) | 2D/3D deterministic, method of characteristics | MIT **[unverified]** | Lattice/assembly calculations, Python interface | Much faster than MC for 2D lattices; needs multigroup XS |
| [DRAGON5](https://merlin.polymtl.ca/downloads/Version5.pdf) | Deterministic lattice code (collision probability) | Open source (Polytechnique Montréal) | Lattice + burnup, homogenization | Fast; steeper learning curve, needs NJOY-processed libraries |
| [NECP-X](https://necp-x.xjtu.edu.cn/info/1083/1023.htm) | Deterministic (Xi'an Jiaotong) | Not confirmed open | Compared with OpenMC on BEAVRS (<0.6% power deviation) | Availability unclear – skip |
| NJOY | Cross-section processing | Open source | Not a solver; prerequisite for deterministic codes | – |
| MOOSE Griffin / Cardinal (OpenMC+MOOSE) | Multiphysics | Griffin licensed via INL **[unverified]**; Cardinal open **[unverified]** | Overkill for an economics model | Heavy setup |

Not covered by the searches (so not assessed): MPACT, PyNE, EQL0D, OpenMC-ONIX details.

## 3. Evidence on OpenMC vs Serpent

- Depletion comparisons with matched inputs agree closely; differences trace to
  fission Q-value handling, power normalisation and default settings. One forum report
  got k within 60 pcm after aligning fission energy release; a micro-reactor study
  saw ≤300 pcm to 100 GWd/MT.
- Serpent defaults to critical-spectrum depletion; OpenMC applies no spectrum
  modification, so inputs must be matched explicitly.
- OpenMC currently supports only surface tracking (Serpent uses delta tracking by
  default) and runs longer per case in user reports.
- Sources: [OpenMC V&V slides](https://conferences.iaea.org/event/302/contributions/25303/attachments/13355/20811/openmc_vv.pdf),
  [Discourse: depletion assumptions](https://openmc.discourse.group/t/depletion-assumptions/1137),
  [Discourse: normalization](https://openmc.discourse.group/t/about-constant-power-normalization-during-eigenvalue-calculation-and-depletion-and-photo-fission-contribution-to-the-eigenvalue/4535),
  [GPU portability paper](https://arxiv.org/pdf/2403.12345),
  [OpenMC/OpenMC-ONIX/DRAGON VERA comparison](https://atomindonesia.brin.go.id/index.php/aij/article/view/1191).

## 4. Recommendations for this repo

1. **Reference neutronics: OpenMC.** MIT-licensed, pip/conda installable, scriptable
   from Python (fits the numpy/pandas stack), has pincell depletion examples.
2. **Make it fast with OpenMC's `IndependentOperator` (added in 0.13.1).** Run a
   single transport calculation to get one-group cross sections (`MicroXS`), then
   deplete with no further transport. This is orders of magnitude cheaper than
   coupled transport-depletion and adequate for burnup/fuel-cycle inputs to
   economics.
3. **If 2D lattice-level speed matters,** use a deterministic route
   (OpenMOC or DRAGON5 with NJOY libraries) – at the cost of more setup.
4. **Per CLAUDE.md,** keep all of this in `src/`, expose outputs as
   `data/output/*.csv`, and register any neutronics-derived parameter (burnup, enrichment,
   cycle length) in `config/assumptions_registry.json` with a credibility tier.
   Tier-2 or lower is appropriate until a benchmark against a Serpent reference
   (published or licensed) is reproduced.
5. **Validation plan:** reproduce one published Serpent benchmark case (e.g. pincell
   k∞ and burnup curve) in OpenMC, with fission Q-values and normalisation
   aligned, before using results as inputs.

## 5. Open questions

- Which reactor types/fuel cycles does the model need (LWR, SFR, MSR)? Fast-spectrum
  and MSR cases need different depletion chains.
- CPU budget and target runtime per case.
- Whether a licensed Serpent reference is available for validation.
