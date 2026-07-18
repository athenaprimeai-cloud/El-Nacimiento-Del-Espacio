"""
DOMAIN-E006 — M2 ordinal vs Cramér-rueda W∈{1,2,6,30} (issue #2 / protocolo v1.0).
MD-035: gcd only for null universe U_W; edges only ordinal |i-j|<=k.
Halves: restrict wheel universe U_W ∩ half, not only cardinality.
"""

from __future__ import annotations

import hashlib
import heapq
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

PROTOCOL_PATH = ROOT / "ATHENA_DOMAIN_E006" / "ATHENA_DOMAIN_E006_PROTOCOL.md"
SEALED_SHA = "12b9c1b7ec6930472efc2a774d484a90ea64e9db9f15270394c24e15161f9e5b"
N_DEFAULT = 100_000
B_DEFAULT = 2000
C = 1.0
WHEELS = (1, 2, 6, 30)
PRINCIPAL_W = 30


def protocol_sha256() -> str:
    return hashlib.sha256(PROTOCOL_PATH.read_bytes()).hexdigest()


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
    """
    MD-035 edges: (u,v) iff 0 < |u-v| <= k.
    No gcd / p|n / factors in edge construction.
    """
    s = sorted(set(int(v) for v in S))
    n = len(s)
    if n == 0:
        return [], 0
    deg = [0] * n
    edges = 0
    j = 0
    for i in range(n):
        if j < i:
            j = i
        while j + 1 < n and s[j + 1] - s[i] <= k:
            j += 1
        right = j - i
        left = 0
        t = i - 1
        while t >= 0 and s[i] - s[t] <= k:
            left += 1
            t -= 1
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


def wheel_universe(N: int, W: int, lo: int = 1, hi: int | None = None) -> List[int]:
    """
    U_W ∩ [lo, hi]: n with gcd(n, W)==1.
    MD-035: gcd only filters null sampling universe, never edges.
    """
    if hi is None:
        hi = N
    if W == 1:
        return list(range(lo, hi + 1))
    return [n for n in range(lo, hi + 1) if math.gcd(n, W) == 1]


def weighted_sample(
    universe: Sequence[int],
    m: int,
    seed: int,
    weights: Sequence[float] | None = None,
) -> List[int]:
    """Efraimidis–Spirakis weighted sample without replacement."""
    if m <= 0:
        return []
    if m >= len(universe):
        return list(universe)
    rng = random.Random(seed)
    heap: List[Tuple[float, int]] = []
    for i, x in enumerate(universe):
        w = weights[i] if weights is not None else weight(x)
        if w <= 0:
            continue
        u = max(rng.random(), 1e-300)
        key = u ** (1.0 / w)
        if len(heap) < m:
            heapq.heappush(heap, (key, x))
        elif key > heap[0][0]:
            heapq.heapreplace(heap, (key, x))
    return [x for _, x in heap]


def median(xs: Sequence[float]) -> float:
    if not xs:
        return 0.0
    ys = sorted(xs)
    return ys[len(ys) // 2]


def p_range_bilateral(M_P: float, M_nulls: Sequence[float]) -> Tuple[float, float, float]:
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


def curve_code(signals: Dict[int, float]) -> str:
    s1, s2, s6, s30 = signals[1], signals[2], signals[6], signals[30]
    if s1 > s2 > s6 > s30:
        return "CURVE_MONOTONE"
    if s1 >= s2 >= s6 >= s30 and not (s1 > s2 > s6 > s30):
        return "CURVE_WEAK"
    return "CURVE_NONMONOTONE"


def run_wheel(
    W: int,
    N: int,
    k: int,
    B: int,
    primes: Sequence[int],
    M_P: float,
    mid: int,
    P_L: Sequence[int],
    P_H: Sequence[int],
    seed_base: int,
) -> Dict:
    m = len(primes)
    m_L, m_H = len(P_L), len(P_H)
    M_PL, M_PH = M2(P_L, k), M2(P_H, k)

    # Full universe U_W
    U = wheel_universe(N, W, 1, N)
    assert len(U) >= m, f"U_W={W} too small: |U|={len(U)} < m={m}"
    w_U = [weight(x) for x in U]

    M_nulls: List[float] = []
    for s in range(B):
        sample = weighted_sample(U, m, seed=seed_base + s, weights=w_U)
        M_nulls.append(M2(sample, k))
    p_range, med, d_med = p_range_bilateral(M_P, M_nulls)
    central80 = in_central_80(M_P, M_nulls)
    senal = abs(M_P - med)

    # Halves: U_W ∩ half (not only cardinality)
    U_L = wheel_universe(N, W, 1, mid)
    U_H = wheel_universe(N, W, mid + 1, N)
    assert len(U_L) >= m_L, f"U_L W={W} |U_L|={len(U_L)} < m_L={m_L}"
    assert len(U_H) >= m_H, f"U_H W={W} |U_H|={len(U_H)} < m_H={m_H}"
    w_L = [weight(x) for x in U_L]
    w_H = [weight(x) for x in U_H]

    M_L: List[float] = []
    M_H: List[float] = []
    for s in range(B):
        M_L.append(M2(weighted_sample(U_L, m_L, seed=seed_base + 10_000 + s, weights=w_L), k))
        M_H.append(M2(weighted_sample(U_H, m_H, seed=seed_base + 20_000 + s, weights=w_H), k))
    p_L, med_L, _ = p_range_bilateral(M_PL, M_L)
    p_H, med_H, _ = p_range_bilateral(M_PH, M_H)
    hc = half_code(p_L, p_H)

    return {
        "W": W,
        "n_U": len(U),
        "n_U_L": len(U_L),
        "n_U_H": len(U_H),
        "median": round(med, 8),
        "p_range": p_range,
        "D_C1_med": round(d_med, 8),
        "senal": round(senal, 8),
        "in_central_80": central80,
        "threshold_2_D_med": round(2.0 * d_med, 8),
        "halves": {
            "M_P_L": round(M_PL, 8),
            "M_P_H": round(M_PH, 8),
            "med_L": round(med_L, 8),
            "med_H": round(med_H, 8),
            "p_range_L": p_L,
            "p_range_H": p_H,
            "half_code": hc,
            "universe": "U_W ∩ half (not cardinality-only)",
        },
    }


def run_campaign(N: int = N_DEFAULT, B: int = B_DEFAULT) -> Dict:
    sha = protocol_sha256()
    assert sha == SEALED_SHA, f"protocol SHA256 mismatch: {sha}"

    k = k_of_N(N)
    primes = sieve_primes(N)
    m = len(primes)
    M_P = M2(primes, k)
    mid = N // 2
    P_L = [p for p in primes if p <= mid]
    P_H = [p for p in primes if p > mid]

    # C2 / C3 once (same as E005)
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

    ulam = ulam_upto(N)
    m3 = min(len(ulam), m)
    if m3 == 0:
        M_C3, D_P_C3, note_c3 = 0.0, abs(M_P), "no Ulam"
    else:
        Ulam = ulam[:m3]
        if m3 < m:
            M_P_c3 = M2(random.Random(1).sample(primes, m3), k)
            note_c3 = f"Ulam {m3}<m; P subsampled"
        else:
            M_P_c3 = M_P
            note_c3 = "full m"
        M_C3 = M2(Ulam, k)
        D_P_C3 = abs(M_P_c3 - M_C3)

    wheels: Dict[str, Dict] = {}
    signals: Dict[int, float] = {}
    seed_bases = {1: 0, 2: 100_000, 6: 200_000, 30: 300_000}
    for W in WHEELS:
        rec = run_wheel(
            W, N, k, B, primes, M_P, mid, P_L, P_H, seed_base=seed_bases[W]
        )
        # attach C2/C3 vs this wheel's thr
        thr = rec["threshold_2_D_med"]
        rec["D_P_C2"] = round(D_P_C2, 8)
        rec["D_P_C3"] = round(D_P_C3, 8)
        rec["cond_C2"] = D_P_C2 > thr
        rec["cond_C3"] = D_P_C3 > thr
        wheels[f"W{W}"] = rec
        signals[W] = rec["senal"]

    cc = curve_code(signals)
    r30 = wheels["W30"]
    p30 = r30["p_range"]
    thr30 = r30["threshold_2_D_med"]
    hc30 = r30["halves"]["half_code"]
    central30 = r30["in_central_80"]

    cond_p = p30 <= 0.01
    cond_c2 = D_P_C2 > thr30
    cond_c3 = D_P_C3 > thr30
    cond_halves = hc30 == "HALF_BOTH_EXTREME"
    gray_p = (p30 > 0.01) and (p30 <= 0.10)

    if cond_p and cond_c2 and cond_c3 and cond_halves:
        h01 = HypothesisState.SOPORTADA_BAJO_CONTROL.value
        h00 = HypothesisState.MUERTA.value
        interp = "PERSISTE"
        verdict = "H01_MATERIAL_BEYOND_WHEEL_30"
    elif p30 > 0.10 or central30 or (
        hc30 == "HALF_BOTH_NULL" and not (cond_p and cond_c2 and cond_c3)
    ):
        h01 = HypothesisState.MUERTA.value
        h00 = HypothesisState.SOPORTADA_BAJO_CONTROL.value
        interp = "DESAPARECE"
        verdict = "MATERIAL_DISSOLVED_BY_WHEEL_30"
    elif gray_p:
        h01 = h00 = HypothesisState.NO_SABEMOS.value
        interp = "NO_SABEMOS"
        verdict = "NO_SABEMOS"
    else:
        h01 = h00 = HypothesisState.NO_SABEMOS.value
        interp = "NO_SABEMOS"
        verdict = "NO_SABEMOS"

    md035 = {
        "edges": "only 0 < |i-j| <= k in degrees_induced_ordinal",
        "gcd": "only constructs U_W for null sampling (and U_W ∩ half)",
        "halves": "wheel universe restricted per half, not cardinality-only",
        "sieve_Omega": "labels P and C2 only",
        "status": "PASS",
    }

    store = ProtocolStore(ROOT / "ATHENA_DOMAIN_E006" / "resultados" / "kernel")
    store.root.mkdir(parents=True, exist_ok=True)
    for f in store.root.glob("*.json"):
        f.write_text("{}\n", encoding="utf-8")
    q = create_question(
        "¿M2 ordinal discrimina P vs Cramér-rueda W=30 (E006, issue #2)?",
        domain="athena/domain-e006",
        store=store,
    )
    h = create_hypothesis(
        q.id,
        "H-ATH-D006-01: material beyond wheel-30 + C2/C3 + halves",
        predicts="p_range_30<=0.01 and C2/C3 and HALF_BOTH_EXTREME",
        weakens_if="gray band or HALF_SPLIT",
        dies_if="p_range_30>0.10 or central80 or HALF_BOTH_NULL",
        store=store,
    )
    death = None
    if h01 == HypothesisState.MUERTA.value:
        death = f"p30={p30:.6f} half={hc30} central80={central30}"
    record_result(
        h.id,
        control_description=(
            f"E006 v1.0 N={N} k={k} B={B} wheels={{1,2,6,30}} principal=30 "
            f"sha256={sha[:16]}"
        ),
        result_summary=f"M_P={M_P:.6f} p30={p30:.6f} {verdict} curve={cc}",
        new_state=h01,
        death_reason=death,
        store=store,
    )

    return {
        "campaign": "ATHENA_DOMAIN_E006",
        "protocol": "v1.0 PREREGISTERED",
        "issue": "https://gitlab.com/athena-group321329/athena/-/issues/2",
        "protocol_sha256": sha,
        "design": "direct_curve",
        "N": N,
        "k": k,
        "B": B,
        "m_pi_N": m,
        "M_P": round(M_P, 8),
        "principal_W": PRINCIPAL_W,
        "wheels": wheels,
        "signals": {str(w): signals[w] for w in WHEELS},
        "curve_code": cc,
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
        "conditions_W30": {
            "p_range_le_0.01": cond_p,
            "D_PC2_gt_thr": cond_c2,
            "D_PC3_gt_thr": cond_c3,
            "HALF_BOTH_EXTREME": cond_halves,
            "gray_band_0.01_to_0.10": gray_p,
        },
        "interpretation": interp,
        "verdict": verdict,
        "hypotheses": {"H-ATH-D006-01": h01, "H-ATH-D006-00": h00},
        "md035_audit": md035,
        "a_priori_prediction": "collapse on W=2; shrink to W=30; likely H-00",
        "no_claims": [
            "Not Hardy–Littlewood theorem",
            "Not Hilbert–Pólya",
            "Dissolved by wheel ≠ no structure in primes",
            "Only M2+ordinal vs these wheel nulls",
        ],
    }


def main() -> int:
    N = int(sys.argv[1]) if len(sys.argv) > 1 else N_DEFAULT
    B = int(sys.argv[2]) if len(sys.argv) > 2 else B_DEFAULT
    out = run_campaign(N=N, B=B)
    dest = ROOT / "ATHENA_DOMAIN_E006" / "resultados"
    dest.mkdir(parents=True, exist_ok=True)
    path = dest / "classification.json"
    path.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"\nWrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
