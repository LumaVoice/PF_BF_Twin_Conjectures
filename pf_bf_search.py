#!/usr/bin/env python3
"""
pf_bf_search.py

Brute-force search helpers for two conjectures:

PF (Permutation–Factorial):  nPr = c!
BF (Binomial–Factorial):     C(n, r) = c!

- Nonnegative integers are allowed for n, r, c.
- We classify solutions as:
  * trivial (PF): r in {0, n-1, n} OR (r == 1 and n is a factorial)
  * trivial (BF): r in {0, n} OR (r in {1, n-1} and n is a factorial)
  * PF_F3: the infinite family (n, r, c) = (t!, t! - t, t! - 1) for t >= 3
  * exceptional: anything that is a solution but not covered by the above

This script lets you scan ranges and write CSVs for GitHub reproducibility.
"""

import argparse
import math
import csv
from dataclasses import dataclass
from typing import List, Tuple, Optional

# ---------- factorial cache ----------

facts: List[int] = [1, 1]  # 0! = 1, 1! = 1

def extend_factorials_until_ge(x: int) -> None:
    while facts[-1] < x:
        facts.append(facts[-1] * len(facts))

def factorial_index_of(x: int) -> Tuple[bool, Optional[int]]:
    """Return (True, k) if x == k! for some k >= 0, else (False, None)."""
    if x < 1:
        return (False, None)
    extend_factorials_until_ge(x)
    lo, hi = 0, len(facts) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        v = facts[mid]
        if v == x:
            return (True, mid)
        if v < x:
            lo = mid + 1
        else:
            hi = mid - 1
    return (False, None)

def is_factorial(x: int) -> Tuple[bool, Optional[int]]:
    return factorial_index_of(x)

def n_is_factorial(n: int) -> Tuple[bool, Optional[int]]:
    return factorial_index_of(n)

# ---------- data models ----------

@dataclass
class PFRecord:
    n: int
    r: int
    c: int
    cls: str  # 'trivial' | 'PF_F3' | 'exceptional'

@dataclass
class BFRecord:
    n: int
    r: int
    c: int
    cls: str  # 'trivial' | 'exceptional'

# ---------- classification helpers ----------

def is_pf_trivial(n: int, r: int, c: int) -> bool:
    if r == 0 or r == n - 1 or r == n:
        return True
    if r == 1:
        ok, _ = n_is_factorial(n)
        if ok:
            return True
    return False

def is_pf_F3(n: int, r: int, c: int) -> bool:
    ok, t = n_is_factorial(n)
    if not ok or t is None or t < 3:
        return False
    return (r == n - t) and (c == n - 1)

def is_bf_trivial(n: int, r: int, c: int) -> bool:
    if r == 0 or r == n:
        return True
    if r == 1 or r == n - 1:
        ok, _ = n_is_factorial(n)
        if ok:
            return True
    return False

# ---------- search functions ----------

def search_pf(n_max: int, include_trivial: bool = True, include_pf_f3: bool = True) -> List[PFRecord]:
    out: List[PFRecord] = []
    for n in range(0, n_max + 1):
        prod = 1  # nP0
        for r in range(0, n + 1):
            if r > 0:
                prod *= (n - (r - 1))
            ok, c = is_factorial(prod)
            if not ok or c is None:
                continue
            if is_pf_trivial(n, r, c):
                if include_trivial:
                    out.append(PFRecord(n, r, c, 'trivial'))
                continue
            if is_pf_F3(n, r, c):
                if include_pf_f3:
                    out.append(PFRecord(n, r, c, 'PF_F3'))
                continue
            out.append(PFRecord(n, r, c, 'exceptional'))
    return out

def search_bf(n_max: int, include_trivial: bool = True) -> List[BFRecord]:
    out: List[BFRecord] = []
    for n in range(0, n_max + 1):
        for r in range(0, n + 1):
            val = math.comb(n, r)
            ok, c = is_factorial(val)
            if not ok or c is None:
                continue
            if is_bf_trivial(n, r, c):
                if include_trivial:
                    out.append(BFRecord(n, r, c, 'trivial'))
                continue
            out.append(BFRecord(n, r, c, 'exceptional'))
    return out

# ---------- CSV writers ----------

def write_pf_csv(rows: List[PFRecord], path: str) -> None:
    with open(path, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['n', 'r', 'c', 'class'])
        for rec in rows:
            w.writerow([rec.n, rec.r, rec.c, rec.cls])

def write_bf_csv(rows: List[BFRecord], path: str) -> None:
    with open(path, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['n', 'r', 'c', 'class'])
        for rec in rows:
            w.writerow([rec.n, rec.r, rec.c, rec.cls])

# ---------- CLI ----------

def main():
    ap = argparse.ArgumentParser(description="Search PF (nPr=c!) and BF (C(n,r)=c!) solutions.")
    ap.add_argument('--mode', choices=['pf','bf','both'], default='both')
    ap.add_argument('--nmax', type=int, default=500)
    ap.add_argument('--no-trivial', action='store_true')
    ap.add_argument('--no-pf-f3', action='store_true')
    ap.add_argument('--outdir', type=str, default='.')
    args = ap.parse_args()

    include_trivial = not args.no_trivial
    include_pf_f3 = not args.no_pf_f3

    import os
    os.makedirs(args.outdir, exist_ok=True)

    if args.mode in ('pf','both'):
        pf_rows = search_pf(args.nmax, include_trivial=include_trivial, include_pf_f3=include_pf_f3)
        pf_csv = os.path.join(args.outdir, f'pf_solutions_nmax{args.nmax}.csv')
        write_pf_csv(pf_rows, pf_csv)
        print(f"[PF] wrote {len(pf_rows)} rows -> {pf_csv}")

    if args.mode in ('bf','both'):
        bf_rows = search_bf(args.nmax, include_trivial=include_trivial)
        bf_csv = os.path.join(args.outdir, f'bf_solutions_nmax{args.nmax}.csv')
        write_bf_csv(bf_rows, bf_csv)
        print(f"[BF] wrote {len(bf_rows)} rows -> {bf_csv}")

if __name__ == '__main__':
    main()
