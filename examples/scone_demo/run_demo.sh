#!/usr/bin/env bash
# Build SCONE (no MPI, no tests) in a separate dir and run the demo input.
# Requires: gfortran, cmake, LAPACK/BLAS, git.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
work="${SCONE_WORK:-$here/.scone}"
mkdir -p "$work/build"
[ -d "$work/scone" ] || GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 https://github.com/CambridgeNuclear/scone "$work/scone"
cd "$work/build"
cmake "$work/scone" -DCMAKE_BUILD_TYPE=Release -DMPI=OFF -DBUILD_TESTS=OFF >/dev/null
make -j"$(nproc)" >/dev/null
cd "$here"
"$work/build/scone.out" inf_u235 | tee "$work/run.log" | tail -n 8
python3 -I parse_keff.py "$work/run.log"
