"""
DOMAIN-E003 — resistencia de identidad bajo ventanas admisibles (G_adm).
Protocolo v1.0 CONGELADO (rectangular + D_q + borde en FASE 2).
"""

from __future__ import annotations

import csv
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

PARTITIONS_CSV = ROOT / "artifacts" / "goldbach" / "goldbach_partitions_4_10000.csv"
Q = 0.5  # fractional spectral discrepancy D_q


def _load_g(n_max: int = 10000) -> List[float]:
    out: List[float] = []
    with PARTITIONS_CSV.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            n = int(row["N"])
            if n > n_max:
                break
            if n >= 4 and n % 2 == 0:
                out.append(float(row["partition_count"]))
    return out


def _fft_power(x: Sequence[float]) -> List[float]:
    n = len(x)
    if n < 4:
        return [0.0]
    n2 = 1
    while n2 < n:
        n2 *= 2
    a = [complex(float(v), 0.0) for v in x] + [0j] * (n2 - n)
    j = 0
    for i in range(1, n2):
        bit = n2 >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    length = 2
    while length <= n2:
        ang = -2.0 * math.pi / length
        wlen = complex(math.cos(ang), math.sin(ang))
        for i in range(0, n2, length):
            w = 1 + 0j
            half = length // 2
            for jj in range(half):
                u = a[i + jj]
                v = a[i + jj + half] * w
                a[i + jj] = u + v
                a[i + jj + half] = u - v
                w *= wlen
        length *= 2
    powers: List[float] = []
    for k in range(n // 2 + 1):
        k2 = int(round(k * n2 / n)) % n2
        c = a[k2]
        powers.append(c.real * c.real + c.imag * c.imag)
    return powers


def _normalized_spectrum(x: Sequence[float]) -> List[float]:
    powers = _fft_power(x)
    pos = powers[1:]  # exclude DC
    s = sum(pos)
    if s <= 0:
        return [0.0] * max(len(pos), 1)
    return [p / s for p in pos]


def D_q(s1: Sequence[float], s2: Sequence[float], q: float = Q) -> float:
    """Fractional spectral discrepancy D_q (not claimed to be a classical metric)."""
    m = min(len(s1), len(s2))
    if m == 0:
        return 0.0
    acc = 0.0
    for i in range(m):
        acc += abs(s1[i] - s2[i]) ** q
    return acc ** (1.0 / q)


def _residual_mean(g: Sequence[float]) -> List[float]:
    mu = sum(g) / len(g) if g else 0.0
    return [x - mu for x in g]


def window_intervals(n: int) -> List[Tuple[int, int]]:
    """
    Five rectangular windows: same length L = n//2, five start positions.
    One instrument, five fields of view.
    """
    L = max(n // 2, 4)
    m = max(n - L, 0)
    starts = [0, m // 4, (2 * m) // 4, (3 * m) // 4, m]
    # unique while preserving order
    seen = set()
    intervals: List[Tuple[int, int]] = []
    for a in starts:
        a = max(0, min(a, n - L))
        key = (a, a + L)
        if key not in seen:
            seen.add(key)
            intervals.append(key)
    return intervals


def delta_per_window(g: Sequence[float], a: int, b: int) -> float:
    """D_{1/2} between global residual restricted to I and local residual on I."""
    g_i = list(g[a:b])
    r_global = _residual_mean(g)
    r_restrict = r_global[a:b]
    r_local = _residual_mean(g_i)
    return D_q(_normalized_spectrum(r_restrict), _normalized_spectrum(r_local), Q)


def deltas_all_windows(g: Sequence[float]) -> List[float]:
    n = len(g)
    return [delta_per_window(g, a, b) for a, b in window_intervals(n)]


def median(xs: Sequence[float]) -> float:
    if not xs:
        return 0.0
    ys = sorted(xs)
    return ys[len(ys) // 2]


def block_bootstrap(g: List[float], block: int, rng: random.Random) -> List[float]:
    n = len(g)
    blocks = [g[i : i + block] for i in range(0, n - block + 1, block)]
    if not blocks:
        return g[:]
    out: List[float] = []
    while len(out) < n:
        out.extend(rng.choice(blocks))
    return out[:n]


def run_campaign(n_null: int = 100) -> Dict:
    g = _load_g(10000)
    n = len(g)
    intervals = window_intervals(n)
    d_by_w = deltas_all_windows(g)
    d_real = median(d_by_w)

    d_n1: List[float] = []
    for s in range(n_null):
        rng = random.Random(s)
        gg = g[:]
        rng.shuffle(gg)
        d_n1.append(median(deltas_all_windows(gg)))
    med_n1 = median(d_n1)
    p_n1 = sum(1 for d in d_n1 if d <= d_real) / n_null

    d_n2: List[float] = []
    for s in range(n_null):
        rng = random.Random(10_000 + s)
        gg = block_bootstrap(g, 50, rng)
        d_n2.append(median(deltas_all_windows(gg)))
    med_n2 = median(d_n2)
    p_n2 = sum(1 for d in d_n2 if d <= d_real) / n_null

    real_lt_n1 = d_real < med_n1
    real_lt_n2 = d_real < med_n2

    if p_n1 <= 0.05 and p_n2 <= 0.05 and real_lt_n1 and real_lt_n2:
        h01 = HypothesisState.SOPORTADA_BAJO_CONTROL.value
        h00 = HypothesisState.MUERTA.value
        interp = "PERSISTE"
        verdict = "H01_IDENTITY_RESISTANCE_DIFFERENTIAL"
        fase2 = "PENDIENTE_AUDITORIA_BORDE"
    elif p_n1 > 0.10 or p_n2 > 0.10 or (not real_lt_n1) or (not real_lt_n2):
        h01 = HypothesisState.MUERTA.value
        h00 = HypothesisState.SOPORTADA_BAJO_CONTROL.value
        interp = "DESAPARECE"
        verdict = "H00_NO_DIFFERENTIAL_IDENTITY_RESISTANCE"
        fase2 = "NO_EJECUTADA"
    else:
        h01 = h00 = HypothesisState.NO_SABEMOS.value
        interp = "NO_SABEMOS"
        verdict = "NO_SABEMOS"
        fase2 = "NO_EJECUTADA_ZONA_GRIS"

    store = ProtocolStore(ROOT / "ATHENA_DOMAIN_E003" / "resultados" / "kernel")
    store.root.mkdir(parents=True, exist_ok=True)
    for f in store.root.glob("*.json"):
        f.write_text("{}\n", encoding="utf-8")
    q = create_question(
        "¿Resistencia de identidad (D_1/2) al mover ventanas rectangulares es diferencial vs nulos?",
        domain="athena/domain-e003",
        store=store,
    )
    h = create_hypothesis(
        q.id,
        "H-ATH-D003-01: Δ_real < Δ_nulo bajo W1–W5 rectangulares y D_{1/2}",
        predicts="p_N1<=0.05 y p_N2<=0.05 y Δ_real < median Δ_nulo en ambos",
        weakens_if="zona gris entre umbrales",
        dies_if="p>0.10 o Δ_real >= median Δ_nulo",
        store=store,
    )
    death = None
    if h01 == HypothesisState.MUERTA.value:
        death = f"Δ_real={d_real:.6f}, p_N1={p_n1}, p_N2={p_n2}, med_N1={med_n1:.6f}, med_N2={med_n2:.6f}"
    record_result(
        h.id,
        control_description=(
            "DOMAIN-E003 v1.0 FASE1: rectangular W L=n/2 x5 positions; "
            f"D_q q=0.5 excl DC; N1 perm n={n_null}; N2 block50 n={n_null}"
        ),
        result_summary=(
            f"Δ_real={d_real:.6f}, p_N1={p_n1}, p_N2={p_n2}, "
            f"med_N1={med_n1:.6f}, med_N2={med_n2:.6f}, interp={interp}"
        ),
        new_state=h01,
        death_reason=death,
        store=store,
    )

    return {
        "campaign": "ATHENA_DOMAIN_E003",
        "protocol": "v1.0 CONGELADO",
        "phase": "FASE_1_rectangular",
        "instrument": {
            "name": "D_q fractional spectral discrepancy",
            "q": Q,
            "DC": "excluded",
            "not_claimed": "classical metric",
        },
        "windows": {
            "type": "rectangular",
            "L": n // 2,
            "n": n,
            "intervals": [{"id": f"W{i+1}", "a": a, "b": b} for i, (a, b) in enumerate(intervals)],
            "morphology": "same scale, five positions (one instrument)",
        },
        "Delta_by_window_real": {
            f"W{i+1}": round(v, 8) for i, v in enumerate(d_by_w)
        },
        "Delta_real": round(d_real, 8),
        "median_Delta_null_N1": round(med_n1, 8),
        "median_Delta_null_N2": round(med_n2, 8),
        "p_N1_permutation": p_n1,
        "p_N2_block_bootstrap": p_n2,
        "real_lt_median_null": {"N1": real_lt_n1, "N2": real_lt_n2},
        "phase2_edge_audit": fase2,
        "interpretation": interp,
        "verdict": verdict,
        "hypotheses": {"H-ATH-D003-01": h01, "H-ATH-D003-00": h00},
        "ficha": {
            "Objeto": "G(N) Goldbach, N even in [4,10000]",
            "R": "residual media",
            "G_adm": "W1–W5 rectangular L=n/2 five positions",
            "instrumento": "D_1/2 discrepancia espectral fraccionaria (excl. DC)",
            "Delta_real": round(d_real, 8),
            "median_Delta_nulo": {"N1": round(med_n1, 8), "N2": round(med_n2, 8)},
            "p_vs_nulos": {"p_N1": p_n1, "p_N2": p_n2},
            "FASE_2_borde": fase2,
            "Interpretacion": interp,
        },
        "no_claims": [
            "Not Riemann geometry",
            "Not an operator",
            "Not structure → primes",
            "D_q is not claimed as a classical metric",
            "Only this rectangular window family and this D_q vs these nulls",
            "Hann/Hamming only if phase-2 edge audit is opened",
        ],
        "mountain_step": "identity resistance when moving the lamp — one brick",
    }


def main() -> int:
    n_null = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    out = run_campaign(n_null=n_null)
    dest = ROOT / "ATHENA_DOMAIN_E003" / "resultados"
    dest.mkdir(parents=True, exist_ok=True)
    path = dest / "classification.json"
    path.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"\nWrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
