# PF/BF Twin Conjectures — Code & Logs

This repo contains the Python code used in the preprint **“Permutation–Factorial and Binomial–Factorial Twin Conjectures.”**  
It reproduces the computational searches for:
- **PF**: `nP_r = c!` (permutations vs factorials)
- **BF**: `C(n,r) = c!` (binomial coefficients vs factorials)

**Preprint (Zenodo)**: https://doi.org/10.5281/zenodo.16909910

---

## Contents
- `pf_bf_search.py` — brute-force scanners and CSV writers for PF/BF; small factorial cache; classification helpers.

## Quick start
```bash
# (Optional) create a venv
python3 -m venv .venv && source .venv/bin/activate

# Run both PF and BF up to n=2000 and write CSVs to ./out
python3 pf_bf_search.py --mode both --nmax 2000 --outdir out
```

This will create:
- `out/pf_solutions_nmax2000.csv`
- `out/bf_solutions_nmax2000.csv`

## Command-line options
```
--mode {pf,bf,both}   # which family to scan (default: both)
--nmax INT            # max n to scan (default: 500)
--no-trivial          # omit 'trivial' solutions from CSV
--no-pf-f3            # omit the PF infinite family (t!, t!-t, t!-1) with t>=3
--outdir PATH         # output directory (default: ".")
```

## Classification (as used in CSV)
- **PF / trivial**: `r in {0, n-1, n}` OR `(r==1 and n is factorial)`
- **PF_F3**: the infinite family `(n, r, c) = (t!, t! - t, t! - 1)` for `t ≥ 3`
- **PF / exceptional**: any PF solution not covered above
- **BF / trivial**: `r in {0, n}` OR `(r in {1, n-1} and n is factorial)`
- **BF / exceptional**: any BF solution not trivial

## Reproducibility notes
- Integer arithmetic only; no external deps.
- Factorials are cached incrementally; lookups are `O(log k)` via binary search.
- PF uses an in-place product to maintain `nP_r` in `O(1)` per step.

## Cite
If you use this code, please cite the preprint (Zenodo DOI above). 
