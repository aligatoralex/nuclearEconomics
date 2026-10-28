#!/usr/bin/env bash
# Build SCONE (no MPI, no tests) in a separate dir and run the demo input.
# Requires: network access, git, python3, gfortran, cmake, LAPACK/BLAS.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
work="${SCONE_WORK:-$here/.scone}"
mkdir -p "$work/build"
# Pinned commit, so the reference k-eff in README.md is reproducible.
sha=a4a02bfb24a664bbc98a5027e70f10c36edec859
if [ ! -d "$work/scone" ]; then
  git init -q "$work/scone"
  git -C "$work/scone" fetch -q --depth 1 https://github.com/CambridgeNuclear/scone "$sha"
  git -C "$work/scone" checkout -q FETCH_HEAD
fi
cd "$work/build"
cmake "$work/scone" -DCMAKE_BUILD_TYPE=Release -DMPI=OFF -DBUILD_TESTS=OFF -DOPENMP=OFF >/dev/null
make -j"$(nproc)" >/dev/null
cd "$here"
"$work/build/scone.out" inf_u235 | tee "$work/run.log" | tail -n 8
python3 -I parse_keff.py "$work/run.log"
