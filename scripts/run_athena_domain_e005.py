"""
DOMAIN-E005 — M2 ordinal vs Cramér (prerregistro issue #1 / protocolo v1.1).
No ejecutar antes de sello git + sha256 en GitLab issue #1.
"""

from __future__ import annotations

import hashlib
import json
import math
import random
import sys
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from athena_core.protocol import (
    HypothesisState,
    ProtocolStore,
    create_hypothesis,
    create_question,
    record_result,
)

PROTOCOL_PATH = ROOT / "ATHENA_DOMAIN_E005" / "ATHENA_DOMAIN_E005_PROTOCOL.md"
N_DEFAULT = 100_000
B_DEFAULT = 2000
C = 1.0


def protocol_sha256() -> str:
    data = PROTOCOL_PATH.read_bytes()
    return hashlib.sha256(data).hexdigest()


def k_of_N(N: int, c: float = C) -> int:
    return max(1, int(round(c * math.log(N))))


def sieve_primes(n: int) -> List[int]:
    if n < 2:
        return []
    is_p = bytearray(b"\x01") * (n + 1)
    is_p[0] = is_p[1] = 0
    r = int(n**0.5)
    for i in range(2, r + 1):
        if is_p[i]:
            start = i * i
            step = i
            is_p[start : n + 1 : step] = b"\x00" * (((n - start) // step) + 1)
    return [i for i in range(2, n + 1) if is_p[i]]


def big_omega_list(n: int) -> List[int]:
    spf = list(range(n + 1))
    r = int(n**0.5)
    for i in range(2, r + 1):
        if spf[i] == i:
            for j in range(i * i, n + 1, i):
                if spf[j] == j:
                    spf[j] = i
    big = [0] * (n + 1)
    for x in range(2, n + 1):
        y, c = x, 0
        while y > 1:
            p = spf[y]
            while y % p == 0:
                y //= p
                c += 1
        big[x] = c
    return big


def semiprimes_all(n: int) -> List[int]:
    big = big_omega_list(n)
    return [x for x in range(4, n + 1) if big[x] == 2]


def ulam_upto(n: int) -> List[int]:
    if n < 1:
        return []
    from collections import Counter

    seq = [1, 2]
    ways: Counter = Counter({3: 1})
    while True:
        found = None
        x = seq[-1] + 1
        while x <= n:
            if ways.get(x, 0) == 1:
                found = x
                break
            x += 1
        if found is None:
            break
        for s in seq:
            ways[s + found] += 1
        seq.append(found)
    return [u for u in seq if 1 <= u <= n]


def degrees_induced_ordinal(S: Sequence[int], k: int) -> Tuple[List[int], int]:
    s = sorted(set(int(v) for v in S))
    n = len(s)
    if n == 0:
        return [], 0
    deg = [0] * n
    edges = 0
    for i in range(n):
        t = i + 1
        while t < n and s[t] - s[i] <= k:
            t += 1
        right = t - i - 1
        t = i - 1
        while t >= 0 and s[i] - s[t] <= k:
            t -= 1
        left = i - t - 1
        deg[i] = left + right
        edges += right
    return deg, edges


def M2(S: Sequence[int], k: int) -> float:
    deg, edges = degrees_induced_ordinal(S, k)
    n = len(deg)
    if n == 0:
        return 0.0
    return (sum(d * d for d in deg) + 2 * edges) / n


def weight(n: int) -> float:
    if n <= 2:
        return 1.0
    return 1.0 / math.log(n)


def cramer_sample(universe: Sequence[int], m: int, seed: int) -> List[int]:
    """Weighted sample without replacement, w_n = 1/ln n (Efraimidis–Spirakis)."""
    if m <= 0:
        return []
    if m >= len(universe):
        return list(universe)
    rng = random.Random(seed)
    scored: List[Tuple[float, int]] = []
    for x in universe:
        w = weight(x)
        if w <= 0:
            continue
        u = rng.random()
        # avoid u=0
        u = max(u, 1e-300)
        key = u ** (1.0 / w)
        scored.append((key, x))
    scored.sort(key=lambda t: t[0], reverse=True)
    return [x for _, x in scored[:m]]


def median(xs: Sequence[float]) -> float:
    if not xs:
        return 0.0
    ys = sorted(xs)
    return ys[len(ys) // 2]


def mean_std(xs: Sequence[float]) -> Tuple[float, float]:
    if not xs:
        return 0.0, 0.0
    mu = sum(xs) / len(xs)
    if len(xs) < 2:
        return mu, 0.0
    var = sum((x - mu) ** 2 for x in xs) / (len(xs) - 1)
    return mu, math.sqrt(var)


def p_range_bilateral(M_P: float, M_nulls: Sequence[float]) -> Tuple[float, float, float]:
    """Returns p_range, median_null, D_C1_med."""
    B = len(M_nulls)
    if B == 0:
        return 1.0, 0.0, 0.0
    med = median(M_nulls)
    dev_p = abs(M_P - med)
    count = sum(1 for v in M_nulls if abs(v - med) >= dev_p - 1e-15)
    p = (1 + count) / (B + 1)
    d_med = median([abs(v - med) for v in M_nulls])
    return p, med, d_med


def in_central_80(M_P: float, M_nulls: Sequence[float]) -> bool:
    ys = sorted(M_nulls)
    if len(ys) < 5:
        return True
    lo = ys[int(0.10 * (len(ys) - 1))]
    hi = ys[int(0.90 * (len(ys) - 1))]
    return lo <= M_P <= hi


def half_code(p_L: float, p_H: float) -> str:
    if p_L <= 0.05 and p_H <= 0.05:
        return "HALF_BOTH_EXTREME"
    if p_L > 0.10 and p_H > 0.10:
        return "HALF_BOTH_NULL"
    return "HALF_SPLIT"


def run_campaign(N: int = N_DEFAULT, B: int = B_DEFAULT) -> Dict:
    k = k_of_N(N)
    sha = protocol_sha256()
    primes = sieve_primes(N)
    m = len(primes)
    universe = list(range(1, N + 1))
    M_P = M2(primes, k)

    # C1 Cramér
    M_c1: List[float] = []
    for s in range(B):
        c1 = cramer_sample(universe, m, seed=s)
        M_c1.append(M2(c1, k))
    p_range, med_c1, D_c1_med = p_range_bilateral(M_P, M_c1)
    mu_c1, sig_c1 = mean_std(M_c1)
    z_desc = (M_P - mu_c1) / sig_c1 if sig_c1 > 1e-15 else 0.0
    thr = 2.0 * D_c1_med
    central80 = in_central_80(M_P, M_c1)

    # C2 sample semiprimes ≤ N
    semi_all = semiprimes_all(N)
    rng0 = random.Random(0)
    if len(semi_all) >= m:
        c2 = rng0.sample(semi_all, m)
        note_c2 = "sample m of all semiprimes ≤ N"
        M_P_c2 = M_P
    else:
        c2 = semi_all
        M_P_c2 = M2(rng0.sample(primes, len(c2)), k) if c2 else 0.0
        note_c2 = f"only {len(semi_all)} semiprimes; P subsampled"
    M_C2 = M2(c2, k)
    D_P_C2 = abs(M_P_c2 - M_C2)

    # C3 Ulam
    ulam = ulam_upto(N)
    m3 = min(len(ulam), m)
    if m3 == 0:
        M_C3, D_P_C3, note_c3 = 0.0, abs(M_P), "no Ulam"
    else:
        U = ulam[:m3]
        if m3 < m:
            M_P_c3 = M2(random.Random(1).sample(primes, m3), k)
            note_c3 = f"Ulam {m3}<m; P subsampled"
        else:
            M_P_c3 = M_P
            note_c3 = "full m"
        M_C3 = M2(U, k)
        D_P_C3 = abs(M_P_c3 - M_C3)

    # Halves
    mid = N // 2
    V_L = list(range(1, mid + 1))
    V_H = list(range(mid + 1, N + 1))
    P_L = [p for p in primes if p <= mid]
    P_H = [p for p in primes if p > mid]
    m_L, m_H = len(P_L), len(P_H)
    M_PL, M_PH = M2(P_L, k), M2(P_H, k)

    M_c1_L: List[float] = []
    M_c1_H: List[float] = []
    for s in range(B):
        M_c1_L.append(M2(cramer_sample(V_L, m_L, seed=10_000 + s), k))
        M_c1_H.append(M2(cramer_sample(V_H, m_H, seed=20_000 + s), k))
    p_L, med_L, _ = p_range_bilateral(M_PL, M_c1_L)
    p_H, med_H, _ = p_range_bilateral(M_PH, M_c1_H)
    hc = half_code(p_L, p_H)

    cond_p = p_range <= 0.01
    cond_c2 = D_P_C2 > thr
    cond_c3 = D_P_C3 > thr
    cond_halves = hc == "HALF_BOTH_EXTREME"

    if cond_p and cond_c2 and cond_c3 and cond_halves:
        h01 = HypothesisState.SOPORTADA_BAJO_CONTROL.value
        h00 = HypothesisState.MUERTA.value
        interp = "PERSISTE"
        verdict = "H01_MATERIAL_BEYOND_CRAMER"
    elif p_range > 0.10 or central80 or (
        hc == "HALF_BOTH_NULL" and not (cond_p and cond_c2 and cond_c3)
    ):
        h01 = HypothesisState.MUERTA.value
        h00 = HypothesisState.SOPORTADA_BAJO_CONTROL.value
        interp = "DESAPARECE"
        verdict = "MATERIAL_DISSOLVED_BY_CRAMER"
    else:
        # also dissolve if clearly null globally even if halves mixed
        if p_range > 0.10 or central80:
            h01 = HypothesisState.MUERTA.value
            h00 = HypothesisState.SOPORTADA_BAJO_CONTROL.value
            interp = "DESAPARECE"
            verdict = "MATERIAL_DISSOLVED_BY_CRAMER"
        else:
            h01 = h00 = HypothesisState.NO_SABEMOS.value
            interp = "NO_SABEMOS"
            verdict = "NO_SABEMOS"

    store = ProtocolStore(ROOT / "ATHENA_DOMAIN_E005" / "resultados" / "kernel")
    store.root.mkdir(parents=True, exist_ok=True)
    for f in store.root.glob("*.json"):
        f.write_text("{}\n", encoding="utf-8")
    q = create_question(
        "¿M2 ordinal discrimina P vs Cramér (E005 v1.1, issue #1)?",
        domain="athena/domain-e005",
        store=store,
    )
    h = create_hypothesis(
        q.id,
        "H-ATH-D005-01: material M2 beyond Cramér + C2/C3 + both halves",
        predicts="p_range<=0.01 and C2/C3 and HALF_BOTH_EXTREME",
        weakens_if="HALF_SPLIT or gray band",
        dies_if="p_range>0.10 or central80 or HALF_BOTH_NULL without H01",
        store=store,
    )
    death = None
    if h01 == HypothesisState.MUERTA.value:
        death = f"p_range={p_range:.6f}, half={hc}, central80={central80}"
    record_result(
        h.id,
        control_description=(
            f"E005 v1.1 N={N} k={k} B={B} Cramér weighted; C2 sample; halves; sha256={sha[:16]}"
        ),
        result_summary=f"M_P={M_P:.6f} p_range={p_range:.6f} {verdict}",
        new_state=h01,
        death_reason=death,
        store=store,
    )

    return {
        "campaign": "ATHENA_DOMAIN_E005",
        "protocol": "v1.1 PREREGISTERED",
        "issue": "https://gitlab.com/athena-group321329/athena/-/issues/1",
        "protocol_sha256": sha,
        "N": N,
        "k": k,
        "c": C,
        "B": B,
        "m_pi_N": m,
        "M_P": round(M_P, 8),
        "C1_Cramer": {
            "median": round(med_c1, 8),
            "mu": round(mu_c1, 8),
            "sigma": round(sig_c1, 8),
            "p_range": p_range,
            "D_C1_med": round(D_c1_med, 8),
            "z_descriptive_not_verdict": round(z_desc, 6),
            "in_central_80": central80,
        },
        "C2_semiprimes_sample": {
            "M": round(M_C2, 8),
            "D_P_C2": round(D_P_C2, 8),
            "note": note_c2,
            "n_semi_all": len(semi_all),
        },
        "C3_ulam": {
            "M": round(M_C3, 8),
            "D_P_C3": round(D_P_C3, 8),
            "note": note_c3,
            "m3": m3,
        },
        "threshold_2_D_C1_med": round(thr, 8),
        "halves": {
            "mid": mid,
            "m_L": m_L,
            "m_H": m_H,
            "M_P_L": round(M_PL, 8),
            "M_P_H": round(M_PH, 8),
            "med_C1_L": round(med_L, 8),
            "med_C1_H": round(med_H, 8),
            "p_range_L": p_L,
            "p_range_H": p_H,
            "half_code": hc,
        },
        "conditions": {
            "p_range_le_0.01": cond_p,
            "D_PC2_gt_thr": cond_c2,
            "D_PC3_gt_thr": cond_c3,
            "HALF_BOTH_EXTREME": cond_halves,
        },
        "interpretation": interp,
        "verdict": verdict,
        "hypotheses": {"H-ATH-D005-01": h01, "H-ATH-D005-00": h00},
        "md035_audit": "ordinal edges only",
        "no_claims": [
            "Not Hilbert–Pólya",
            "Not primes→spectrum theorem",
            "Dissolved by Cramér ≠ no structure in primes",
            "Only M2+ordinal under this seal",
        ],
    }


def main() -> int:
    N = int(sys.argv[1]) if len(sys.argv) > 1 else N_DEFAULT
    B = int(sys.argv[2]) if len(sys.argv) > 2 else B_DEFAULT
    out = run_campaign(N=N, B=B)
    dest = ROOT / "ATHENA_DOMAIN_E005" / "resultados"
    dest.mkdir(parents=True, exist_ok=True)
    path = dest / "classification.json"
    path.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"\nWrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
