"""
DOMAIN-E002 — conservación de entropía espectral bajo representaciones R.
Protocolo v1.0 CONGELADO.
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


def _fft_power(x: List[float]) -> List[float]:
    n = len(x)
    n2 = 1
    while n2 < n:
        n2 *= 2
    a = [complex(float(v), 0.0) for v in x] + [0j] * (n2 - n)
    # bit-reverse Cooley-Tukey
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
    powers = []
    for k in range(n // 2 + 1):
        k2 = int(round(k * n2 / n)) % n2
        c = a[k2]
        powers.append(c.real * c.real + c.imag * c.imag)
    return powers


def _spectral_entropy(r: List[float]) -> float:
    powers = _fft_power(r)
    pos = powers[1:]  # exclude DC
    s = sum(pos)
    if s <= 0:
        return 1.0
    K = len(pos)
    ent = 0.0
    for pk in pos:
        p = pk / s
        if p > 0:
            ent -= p * math.log(p)
    return ent / math.log(K) if K > 1 else 0.0


def _residual_mean(g: Sequence[float]) -> List[float]:
    mu = sum(g) / len(g)
    return [x - mu for x in g]


def _residual_linear(g: Sequence[float]) -> List[float]:
    n = len(g)
    # t = 0..n-1
    st = sn = stt = stx = 0.0
    for t, y in enumerate(g):
        st += t
        sn += 1
        stt += t * t
        stx += t * y
    den = sn * stt - st * st
    if abs(den) < 1e-12:
        return _residual_mean(list(g))
    b = (sn * stx - st * sum(g)) / den
    a = (sum(g) - b * st) / sn
    return [y - (a + b * t) for t, y in enumerate(g)]


def _residual_log_mean(g: Sequence[float]) -> List[float]:
    lg = [math.log(1.0 + x) for x in g]
    return _residual_mean(lg)


def family_R(g: List[float]) -> Dict[str, float]:
    """P under each legitimate representation T in R."""
    n = len(g)
    half = n // 2
    out = {
        "T0_mean": _spectral_entropy(_residual_mean(g)),
        "T1_half_low": _spectral_entropy(_residual_mean(g[:half])),
        "T2_half_high": _spectral_entropy(_residual_mean(g[half:])),
        "T3_linear": _spectral_entropy(_residual_linear(g)),
        "T4_log_mean": _spectral_entropy(_residual_log_mean(g)),
    }
    return out


def delta_stability(p_by_t: Dict[str, float]) -> float:
    vals = list(p_by_t.values())
    med = sorted(vals)[len(vals) // 2]
    return max(abs(v - med) for v in vals)


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
    import random

    g = _load_g(10000)
    p0 = family_R(g)
    d0 = delta_stability(p0)

    # N1 permutation
    d_n1 = []
    for s in range(n_null):
        rng = random.Random(s)
        gg = g[:]
        rng.shuffle(gg)
        d_n1.append(delta_stability(family_R(gg)))
    p_n1 = sum(1 for d in d_n1 if d <= d0) / n_null

    # N2 block bootstrap
    d_n2 = []
    for s in range(n_null):
        rng = random.Random(10_000 + s)
        gg = block_bootstrap(g, 50, rng)
        d_n2.append(delta_stability(family_R(gg)))
    p_n2 = sum(1 for d in d_n2 if d <= d0) / n_null

    # combine: use max of empirical p (stricter for H01)
    p_emp = max(p_n1, p_n2)

    if d0 <= 0.08 and p_emp <= 0.05:
        h01 = HypothesisState.SOPORTADA_BAJO_CONTROL.value
        h00 = HypothesisState.MUERTA.value
        interp = "PERSISTE"
        verdict = "H01_CONSERVATION_DIFFERENTIAL"
    elif p_emp > 0.10 or d0 > 0.15:
        h01 = HypothesisState.MUERTA.value
        h00 = HypothesisState.SOPORTADA_BAJO_CONTROL.value
        interp = "DESAPARECE"
        verdict = "H00_NO_DIFFERENTIAL_CONSERVATION"
    else:
        h01 = h00 = HypothesisState.NO_SABEMOS.value
        interp = "NO_SABEMOS"
        verdict = "NO_SABEMOS"

    store = ProtocolStore(ROOT / "ATHENA_DOMAIN_E002" / "resultados" / "kernel")
    for f in store.root.glob("*.json"):
        f.write_text("{}\n", encoding="utf-8")
    q = create_question(
        "¿Entropía espectral del residual Goldbach se conserva bajo R y es diferencial vs nulos?",
        domain="athena/domain-e002",
        store=store,
    )
    h = create_hypothesis(
        q.id,
        "H-ATH-D002-01: P=entropía espectral estable bajo R (T0–T4) y extrema vs permutación/bloques",
        predicts="Δ0<=0.08 y p_emp<=0.05",
        weakens_if="zona gris entre umbrales",
        dies_if="p_emp>0.10 o Δ0>0.15",
        store=store,
    )
    death = None
    if h01 == HypothesisState.MUERTA.value:
        death = f"Δ0={d0:.4f}, p_N1={p_n1}, p_N2={p_n2}"
    record_result(
        h.id,
        control_description=(
            "DOMAIN-E002 v1.0: P spectral entropy; R={T0..T4}; "
            f"N1 perm n={n_null}; N2 block50 n={n_null}"
        ),
        result_summary=(
            f"Δ0={d0:.4f}, p_N1={p_n1}, p_N2={p_n2}, interp={interp}, P_by_T={p0}"
        ),
        new_state=h01,
        death_reason=death,
        store=store,
    )

    return {
        "campaign": "ATHENA_DOMAIN_E002",
        "protocol": "v1.0 CONGELADO",
        "P": "normalized spectral entropy of residual (excl. DC)",
        "family_R": list(p0.keys()),
        "P_by_T": {k: round(v, 6) for k, v in p0.items()},
        "Delta_0": round(d0, 6),
        "p_N1_permutation": p_n1,
        "p_N2_block_bootstrap": p_n2,
        "interpretation": interp,
        "verdict": verdict,
        "hypotheses": {"H-ATH-D002-01": h01, "H-ATH-D002-00": h00},
        "ficha": {
            "Propiedad_P": "entropía espectral normalizada",
            "Familia_T": "T0 mean, T1 half-low, T2 half-high, T3 linear, T4 log-mean",
            "Rango": "N even in [4,10000]",
            "Nulos": "N1 permutation, N2 block bootstrap B=50",
            "Estabilidad_Delta0": round(d0, 6),
            "p_vs_nulos": {"p_N1": p_n1, "p_N2": p_n2},
            "Interpretacion": interp,
        },
        "no_claims": [
            "Not Riemann geometry",
            "Not an operator",
            "Not structure → primes",
            "Only this P under this R vs these nulls",
        ],
        "mountain_step": "conservation under change of light — one brick",
    }


def main() -> int:
    n_null = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    out = run_campaign(n_null=n_null)
    dest = ROOT / "ATHENA_DOMAIN_E002" / "resultados"
    dest.mkdir(parents=True, exist_ok=True)
    path = dest / "classification.json"
    path.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"\nWrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
