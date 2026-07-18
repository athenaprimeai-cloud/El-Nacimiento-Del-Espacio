"""
ATHENA DOMAIN-E001 — firma ~1/6 en residuo Goldbach vs nulos.
Protocolo v1.0 CONGELADO.
"""

from __future__ import annotations

import json
import math
import random
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from athena_core.protocol import (
    HypothesisState,
    ProtocolStore,
    create_hypothesis,
    create_question,
    record_result,
)

PARTITIONS_CSV = (
    ROOT / "artifacts" / "goldbach" / "goldbach_partitions_4_10000.csv"
)


def _g_counts(n_max: int) -> List[float]:
    """Load partition counts from frozen artifact (G4 window)."""
    import csv

    if not PARTITIONS_CSV.exists():
        raise FileNotFoundError(f"Missing {PARTITIONS_CSV}")
    out: List[float] = []
    with PARTITIONS_CSV.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            n = int(row["N"])
            if n > n_max:
                break
            if n >= 4 and n % 2 == 0:
                out.append(float(row["partition_count"]))
    if len(out) < 10:
        raise ValueError("too few partition rows loaded")
    return out


def _residual(g: List[float]) -> List[float]:
    mu = sum(g) / len(g)
    return [x - mu for x in g]


def _fft_complex(a: List[complex]) -> List[complex]:
    """Cooley–Tukey radix-2 FFT; pads to next power of 2."""
    n = len(a)
    n2 = 1
    while n2 < n:
        n2 *= 2
    if n2 != n:
        a = a + [0j] * (n2 - n)
        n = n2
    # bit-reverse
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    length = 2
    while length <= n:
        ang = -2.0 * math.pi / length
        wlen = complex(math.cos(ang), math.sin(ang))
        for i in range(0, n, length):
            w = 1 + 0j
            half = length // 2
            for j in range(half):
                u = a[i + j]
                v = a[i + j + half] * w
                a[i + j] = u + v
                a[i + j + half] = u - v
                w *= wlen
        length *= 2
    return a


def _fft_power(x: List[float]) -> List[float]:
    """Power spectrum for k=0..n//2 using radix-2 FFT on original length n.

    Uses zero-pad FFT of length n2; frequencies mapped back to original n bins
    by evaluating nearest bin to k/n in the padded grid.
    Protocol uses frequency ~1/6 on the sample grid of length n.
    """
    n = len(x)
    try:
        import numpy as np

        spec = np.fft.rfft(np.asarray(x, dtype=float))
        return [float(abs(c) ** 2) for c in spec]
    except ImportError:
        # Pad to power of 2 for speed; still report n_orig bins via interpolation of bins
        n2 = 1
        while n2 < n:
            n2 *= 2
        a = [complex(float(v), 0.0) for v in x] + [0j] * (n2 - n)
        spec = _fft_complex(a)
        # rfft-like: k=0..n//2 but use padded spectrum scaled
        # For statistic we need powers on original frequency grid k/n
        powers = []
        for k in range(n // 2 + 1):
            # nearest bin in padded spectrum: freq k/n = k2/n2 => k2 = k*n2/n
            k2 = int(round(k * n2 / n)) % n2
            c = spec[k2]
            powers.append(float(c.real * c.real + c.imag * c.imag))
        return powers


def _freq_for_bin(k: int, n: int) -> float:
    # frequency in cycles per sample (even-N index)
    return k / n


def _bin_nearest_sixth(n: int) -> int:
    target = 1.0 / 6.0
    best_k = 1
    best_d = 1e9
    for k in range(1, n // 2 + 1):
        f = _freq_for_bin(k, n)
        d = abs(f - target)
        if d < best_d:
            best_d = d
            best_k = k
    return best_k


def _statistic_T(powers: List[float], k_star: int) -> float:
    # exclude DC
    pos = powers[1:]
    if not pos:
        return 0.0
    med = sorted(pos)[len(pos) // 2]
    if med <= 0:
        med = 1e-30
    return powers[k_star] / med


def _top5_contains(powers: List[float], k_star: int) -> bool:
    # rank among positive freqs (exclude DC)
    scored = [(powers[k], k) for k in range(1, len(powers))]
    scored.sort(reverse=True)
    top = {k for _, k in scored[:5]}
    return k_star in top


def run_campaign(n_max: int = 10000, n_null: int = 100) -> Dict[str, Any]:
    g = _g_counts(n_max)
    r = _residual(g)
    n = len(r)
    powers = _fft_power(r)
    k_star = _bin_nearest_sixth(n)
    f_star = _freq_for_bin(k_star, n)
    t0 = _statistic_T(powers, k_star)

    # N1 permutation
    t_n1 = []
    rng = random.Random(0)
    for s in range(n_null):
        rr = r[:]
        rng.seed(s)
        rng.shuffle(rr)
        p = _fft_power(rr)
        t_n1.append(_statistic_T(p, k_star))
    p_n1 = sum(1 for t in t_n1 if t >= t0) / n_null

    # N2 gaussian i.i.d. same variance
    var = sum(x * x for x in r) / len(r)
    sd = math.sqrt(var) if var > 0 else 1.0
    t_n2 = []
    for s in range(n_null):
        rng.seed(10_000 + s)
        rr = [rng.gauss(0.0, sd) for _ in range(n)]
        p = _fft_power(rr)
        t_n2.append(_statistic_T(p, k_star))
    p_n2 = sum(1 for t in t_n2 if t >= t0) / n_null

    # N3 subwindows
    half = n // 2
    r1, r2 = r[:half], r[half:]
    p1, p2 = _fft_power(r1), _fft_power(r2)
    k1, k2 = _bin_nearest_sixth(len(r1)), _bin_nearest_sixth(len(r2))
    n3_ok = _top5_contains(p1, k1) and _top5_contains(p2, k2)

    # Verdict per protocol
    if p_n1 <= 0.01 and p_n2 <= 0.01 and n3_ok:
        h01, h00 = (
            HypothesisState.SOPORTADA_BAJO_CONTROL.value,
            HypothesisState.MUERTA.value,
        )
        verdict = "H01_SIGNAL_EXTREME_VS_NULLS"
    elif p_n1 > 0.05 or p_n2 > 0.05 or not n3_ok:
        h01, h00 = (
            HypothesisState.MUERTA.value,
            HypothesisState.SOPORTADA_BAJO_CONTROL.value,
        )
        verdict = "H00_COMPATIBLE_WITH_NULL_OR_UNSTABLE"
    else:
        h01 = h00 = HypothesisState.NO_SABEMOS.value
        verdict = "NO_SABEMOS"

    # Register in kernel
    store = ProtocolStore(ROOT / "ATHENA_DOMAIN_E001" / "resultados" / "kernel")
    # clean previous if any
    for f in store.root.glob("*.json"):
        if f.name != "audit_log.jsonl":
            f.write_text("{}\n", encoding="utf-8")
    q = create_question(
        "¿La firma espectral ~1/6 del residuo Goldbach es extrema vs nulos?",
        domain="athena/domain-e001",
        store=store,
    )
    h = create_hypothesis(
        q.id,
        "H-ATH-D001-01: pico ~1/6 del residuo G(N)-mean es extremo vs permutación y Gauss i.i.d., y estable en subventanas",
        predicts="p_N1<=0.01 y p_N2<=0.01 y top-5 en ambas subventanas",
        weakens_if="0.01 < p <= 0.05 o N3 mixto",
        dies_if="p_N1>0.05 o p_N2>0.05 o falla N3",
        store=store,
    )
    death_reason = None
    state = h01
    if h01 == HypothesisState.MUERTA.value:
        death_reason = f"p_N1={p_n1}, p_N2={p_n2}, n3_ok={n3_ok}"
    record_result(
        h.id,
        control_description=(
            f"DOMAIN-E001 v1.0: Nmax={n_max}, residual mean-centered, "
            f"T=P_1/6 / median(P), N1/N2 n={n_null}, N3 half-windows"
        ),
        result_summary=(
            f"T0={t0:.4g}, f*={f_star:.6f}, k*={k_star}, "
            f"p_N1={p_n1}, p_N2={p_n2}, n3_ok={n3_ok}, verdict={verdict}"
        ),
        new_state=state,
        death_reason=death_reason,
        store=store,
    )

    return {
        "campaign": "ATHENA_DOMAIN_E001",
        "protocol": "v1.0 CONGELADO",
        "n_max": n_max,
        "n_samples": n,
        "k_star": k_star,
        "f_star": f_star,
        "T0": t0,
        "p_N1_permutation": p_n1,
        "p_N2_gaussian": p_n2,
        "n3_top5_both_halves": n3_ok,
        "verdict": verdict,
        "hypotheses": {
            "H-ATH-D001-01": h01,
            "H-ATH-D001-00": h00,
        },
        "kernel_hypothesis_id": h.id,
        "no_claims": [
            "Not a proof of prime distribution",
            "Not fundamental structure → primes",
            "Only: 1/6 signature extremity vs declared nulls on this window",
        ],
        "mountain": "primes / deep structure — one step, not the summit",
    }


def main() -> int:
    n_max = int(sys.argv[1]) if len(sys.argv) > 1 else 10000
    n_null = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    out = run_campaign(n_max=n_max, n_null=n_null)
    dest = ROOT / "ATHENA_DOMAIN_E001" / "resultados"
    dest.mkdir(parents=True, exist_ok=True)
    path = dest / "classification.json"
    path.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"\nWrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
