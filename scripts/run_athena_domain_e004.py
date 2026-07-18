"""
DOMAIN-E004 — material espectral no aritmético vs controles (quirúrgico).
Protocolo v1.0 CONGELADO · MD-034 / MD-035 / MD-036.
"""

from __future__ import annotations

import json
import math
import random
import sys
from pathlib import Path
from typing import Dict, List, Sequence, Set, Tuple

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from athena_core.protocol import (
    HypothesisState,
    ProtocolStore,
    create_hypothesis,
    create_question,
    record_result,
)

N_DEFAULT = 10000
K_DEFAULT = 10
N_C1 = 100


def sieve_primes(n: int) -> List[int]:
    if n < 2:
        return []
    is_p = bytearray(b"\x01") * (n + 1)
    is_p[0] = is_p[1] = 0
    for i in range(2, int(n**0.5) + 1):
        if is_p[i]:
            step = i
            start = i * i
            is_p[start : n + 1 : step] = b"\x00" * (((n - start) // step) + 1)
    return [i for i in range(2, n + 1) if is_p[i]]


def big_omega_list(n: int) -> List[int]:
    """Ω(x) = total number of prime factors with multiplicity; spf sieve."""
    spf = list(range(n + 1))
    for i in range(2, int(n**0.5) + 1):
        if spf[i] == i:
            for j in range(i * i, n + 1, i):
                if spf[j] == j:
                    spf[j] = i
    big_omega = [0] * (n + 1)
    for x in range(2, n + 1):
        y = x
        c = 0
        while y > 1:
            p = spf[y]
            while y % p == 0:
                y //= p
                c += 1
        big_omega[x] = c
    return big_omega


def semiprimes_upto(n: int, m: int) -> List[int]:
    """First m integers ≤ n with Ω(x)=2 (exactly two prime factors with mult.)."""
    big_omega = big_omega_list(n)
    out = [x for x in range(4, n + 1) if big_omega[x] == 2]
    return out[:m]


def ulam_upto(n: int) -> List[int]:
    """Ulam sequence: 1, 2, then next = least integer > last with unique sum of two distinct earlier."""
    if n < 1:
        return []
    seq = [1, 2]
    # sums multiplicity of pairs of distinct earlier terms
    from collections import Counter

    ways: Counter = Counter()
    ways[1 + 2] = 1
    candidates_beyond = 3
    while True:
        # find next Ulam ≤ n
        found = None
        x = max(seq[-1] + 1, candidates_beyond)
        while x <= n:
            if ways.get(x, 0) == 1:
                found = x
                break
            x += 1
        if found is None:
            break
        # add found
        for s in seq:
            ways[s + found] += 1
        seq.append(found)
        candidates_beyond = found + 1
    return [u for u in seq if u <= n]


def degrees_induced_ordinal(S: Sequence[int], k: int) -> Tuple[List[int], int]:
    """
    Induced subgraph of ordinal neighborhood |i-j|≤k on vertex set S (sorted).
    Returns (deg list aligned with S, edge_count).
    MD-035: edges only from ordinal proximity, not arithmetic of primes.
    """
    s = sorted(set(int(v) for v in S))
    n = len(s)
    if n == 0:
        return [], 0
    deg = [0] * n
    edges = 0
    j = 0
    for i in range(n):
        while j < n and s[j] - s[i] <= k:
            j += 1
        # neighbors of s[i] are indices i+1 .. j-1 with 0 < diff ≤ k (auto)
        # also previous: use two pointers left
        # count right neighbors
        right = 0
        t = i + 1
        while t < n and s[t] - s[i] <= k:
            right += 1
            t += 1
        left = 0
        t = i - 1
        while t >= 0 and s[i] - s[t] <= k:
            left += 1
            t -= 1
        deg[i] = left + right
        edges += right  # count each edge once
    return deg, edges


def M2(S: Sequence[int], k: int) -> float:
    """Second spectral moment of combinatorial Laplacian of induced G[S]."""
    deg, edges = degrees_induced_ordinal(S, k)
    n = len(deg)
    if n == 0:
        return 0.0
    sum_deg2 = sum(d * d for d in deg)
    # sum λ_i^2 = sum deg^2 + 2|E|
    return (sum_deg2 + 2 * edges) / n


def mean_std(xs: Sequence[float]) -> Tuple[float, float]:
    if not xs:
        return 0.0, 0.0
    mu = sum(xs) / len(xs)
    if len(xs) < 2:
        return mu, 0.0
    var = sum((x - mu) ** 2 for x in xs) / (len(xs) - 1)
    return mu, math.sqrt(var)


def run_campaign(N: int = N_DEFAULT, k: int = K_DEFAULT, n_c1: int = N_C1) -> Dict:
    primes = sieve_primes(N)
    m = len(primes)
    M_P = M2(primes, k)

    # C1 replicas
    M_c1: List[float] = []
    universe = list(range(1, N + 1))
    for s in range(n_c1):
        rng = random.Random(s)
        c1 = rng.sample(universe, m)
        M_c1.append(M2(c1, k))
    mu_c1, sig_c1 = mean_std(M_c1)
    abs_dev_p = abs(M_P - mu_c1)
    p_c1 = sum(1 for v in M_c1 if abs(v - mu_c1) >= abs_dev_p - 1e-15) / n_c1
    z_p = (M_P - mu_c1) / sig_c1 if sig_c1 > 1e-15 else 0.0
    D_c1_med = sorted(abs(v - mu_c1) for v in M_c1)[n_c1 // 2]

    # C2 semiprimes
    semi = semiprimes_upto(N, m)
    m2 = len(semi)
    if m2 < m:
        rng = random.Random(0)
        P_cmp = rng.sample(primes, m2)
        M_P_c2 = M2(P_cmp, k)
        note_c2 = f"semiprimes only {m2}<m={m}; P subsampled to {m2}"
    else:
        M_P_c2 = M_P
        note_c2 = "full m"
        P_cmp = primes
    M_C2 = M2(semi, k)
    D_P_C2 = abs(M_P_c2 - M_C2)

    # C3 Ulam
    ulam = ulam_upto(N)
    m3 = min(len(ulam), m)
    if m3 == 0:
        M_C3 = 0.0
        M_P_c3 = M_P
        D_P_C3 = abs(M_P - M_C3)
        note_c3 = "no Ulam"
    else:
        U = ulam[:m3] if len(ulam) >= m3 else ulam
        if m3 < m:
            rng = random.Random(1)
            P_u = rng.sample(primes, m3)
            M_P_c3 = M2(P_u, k)
            note_c3 = f"Ulam only {m3}<m={m}; P subsampled to {m3}"
        else:
            M_P_c3 = M_P
            note_c3 = "full m"
        M_C3 = M2(U, k)
        D_P_C3 = abs(M_P_c3 - M_C3)

    thr = 2.0 * D_c1_med
    cond_c1 = p_c1 <= 0.05
    cond_c2 = D_P_C2 > thr
    cond_c3 = D_P_C3 > thr

    if cond_c1 and cond_c2 and cond_c3:
        h01 = HypothesisState.SOPORTADA_BAJO_CONTROL.value
        h00 = HypothesisState.MUERTA.value
        interp = "PERSISTE"
        verdict = "H01_SPECTRAL_MATERIAL_VS_CONTROLS"
    elif (
        p_c1 > 0.10
        or (D_P_C2 <= thr and D_P_C3 <= thr)
        or (abs(z_p) < 2.0 and p_c1 > 0.05)
    ):
        h01 = HypothesisState.MUERTA.value
        h00 = HypothesisState.SOPORTADA_BAJO_CONTROL.value
        interp = "DESAPARECE"
        verdict = "H00_NO_SPECTRAL_MATERIAL_UNDER_CONTROL"
    else:
        h01 = h00 = HypothesisState.NO_SABEMOS.value
        interp = "NO_SABEMOS"
        verdict = "NO_SABEMOS"

    store = ProtocolStore(ROOT / "ATHENA_DOMAIN_E004" / "resultados" / "kernel")
    store.root.mkdir(parents=True, exist_ok=True)
    for f in store.root.glob("*.json"):
        f.write_text("{}\n", encoding="utf-8")
    q = create_question(
        "¿M_2 del Laplaciano inducido (grafo ordinal) discrimina primos vs controles?",
        domain="athena/domain-e004",
        store=store,
    )
    h = create_hypothesis(
        q.id,
        "H-ATH-D004-01: firma M_2 estable vs C1/C2/C3 bajo grafo ordinal k=10",
        predicts="p_C1<=0.05 y D(P,C2),D(P,C3)>2*D_C1_med",
        weakens_if="zona gris",
        dies_if="p_C1>0.10 o no separación de impostores",
        store=store,
    )
    death = None
    if h01 == HypothesisState.MUERTA.value:
        death = (
            f"M_P={M_P:.6f}, p_C1={p_c1}, z={z_p:.3f}, "
            f"D_PC2={D_P_C2:.6f}, D_PC3={D_P_C3:.6f}, thr={thr:.6f}"
        )
    record_result(
        h.id,
        control_description=(
            f"E004 v1.0: ordinal k={k}, N={N}, M=M2 Laplacian; "
            f"C1 n={n_c1}; C2 semiprimes; C3 Ulam; MD-035 edges ordinal only"
        ),
        result_summary=(
            f"M_P={M_P:.6f}, μ_C1={mu_c1:.6f}, p_C1={p_c1}, interp={interp}"
        ),
        new_state=h01,
        death_reason=death,
        store=store,
    )

    return {
        "campaign": "ATHENA_DOMAIN_E004",
        "protocol": "v1.0 CONGELADO",
        "MD_anchors": ["MD-034", "MD-035", "MD-036"],
        "N": N,
        "k": k,
        "graph": "ordinal neighborhood 0<|i-j|<=k (no arithmetic edges)",
        "metric": "M2 second spectral moment of induced Laplacian",
        "m_pi_N": m,
        "M_P": round(M_P, 8),
        "C1": {
            "mu": round(mu_c1, 8),
            "sigma": round(sig_c1, 8),
            "p_C1": p_c1,
            "z_P": round(z_p, 6),
            "D_C1_med": round(D_c1_med, 8),
            "n_replicas": n_c1,
        },
        "C2_semiprimes": {
            "M": round(M_C2, 8),
            "D_P_C2": round(D_P_C2, 8),
            "note": note_c2,
            "m2": m2,
        },
        "C3_ulam": {
            "M": round(M_C3, 8),
            "D_P_C3": round(D_P_C3, 8),
            "note": note_c3,
            "m3": m3,
        },
        "threshold_2_D_C1_med": round(thr, 8),
        "conditions": {
            "p_C1_le_0.05": cond_c1,
            "D_PC2_gt_thr": cond_c2,
            "D_PC3_gt_thr": cond_c3,
        },
        "interpretation": interp,
        "verdict": verdict,
        "hypotheses": {"H-ATH-D004-01": h01, "H-ATH-D004-00": h00},
        "md035_audit": "E defined only by ordinal |i-j|<=k; no p|n, gcd, factor",
        "ficha": {
            "N_k": f"{N}, {k}",
            "G": "vecindad ordinal",
            "M": "M_2 Laplaciano inducido",
            "m": m,
            "M_P": round(M_P, 8),
            "mu_C1_sigma": f"{mu_c1:.6f} ± {sig_c1:.6f}",
            "z_P_p_C1": f"{z_p:.4f}, {p_c1}",
            "M_C2_D": f"{M_C2:.6f}, {D_P_C2:.6f}",
            "M_C3_D": f"{M_C3:.6f}, {D_P_C3:.6f}",
            "D_C1_med": round(D_c1_med, 8),
            "Interpretacion": interp,
            "MD035_audit": "OK",
        },
        "no_claims": [
            "Not primes → spectrum as theorem",
            "Not Hilbert–Pólya / Hamiltonian / GUE",
            "Not Riemann",
            "Only M2 on ordinal induced graphs vs these controls at this N",
        ],
        "mountain_step": "material for a wall — one brick, not the cathedral",
    }


def main() -> int:
    N = int(sys.argv[1]) if len(sys.argv) > 1 else N_DEFAULT
    k = int(sys.argv[2]) if len(sys.argv) > 2 else K_DEFAULT
    out = run_campaign(N=N, k=k)
    dest = ROOT / "ATHENA_DOMAIN_E004" / "resultados"
    dest.mkdir(parents=True, exist_ok=True)
    path = dest / "classification.json"
    path.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"\nWrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
