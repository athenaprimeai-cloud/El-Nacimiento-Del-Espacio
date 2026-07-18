"""
META-E002b — zona excluida del Selector.
¿Compresión de ruido o de diversidad?
"""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Set

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from athena_core.explorer import explore_pressure
from athena_core.protocol import ProtocolStore, get_hypothesis
from athena_core.selector import _tokens, select_challenges


def _clusters(hyp_ids: List[str], store: ProtocolStore) -> int:
    """Rough diversity: number of distinct token-set signatures."""
    sigs: Set[str] = set()
    for hid in hyp_ids:
        h = get_hypothesis(hid, store)
        toks = sorted(_tokens((h.statement or "") + " " + (h.predicts or "")))
        # bucket by first 5 tokens
        sigs.add("|".join(toks[:5]) if toks else hid)
    return len(sigs)


def run_seed(seed: int, n_cand: int = 100) -> Dict[str, Any]:
    d = Path(tempfile.mkdtemp(prefix=f"e002b_s{seed}_"))
    store = ProtocolStore(d)
    exp = explore_pressure(
        f"META-E002b seed={seed}: ¿compresión ruido o diversidad?",
        n_candidates=n_cand,
        store=store,
        seed=seed,
    )
    sel = select_challenges(store=store, only_open=True)
    open_ids = [a.hypothesis_id for a in exp.attempts if a.accepted and a.hypothesis_id]
    a_ids = [s.hypothesis_id for s in sel.ranked if s.group == "A"]
    excluded = [hid for hid in open_ids if hid not in set(a_ids)]

    latent = exp.latent_by_hyp
    rare_all = [hid for hid in open_ids if latent.get(hid) == "rare_valuable"]
    rare_in_a = [hid for hid in a_ids if latent.get(hid) == "rare_valuable"]
    rare_ex = [hid for hid in excluded if latent.get(hid) == "rare_valuable"]
    common_all = [hid for hid in open_ids if latent.get(hid) == "common_ok"]
    common_in_a = [hid for hid in a_ids if latent.get(hid) == "common_ok"]

    n_rare = len(rare_all)
    fn_rate = (len(rare_ex) / n_rare) if n_rare else 0.0
    cov_rare_a = (len(rare_in_a) / n_rare) if n_rare else 0.0

    cl_all = _clusters(open_ids, store)
    cl_a = _clusters(a_ids, store) if a_ids else 0
    div_drop = 1.0 - (cl_a / cl_all) if cl_all else 0.0

    budget_m1 = len(open_ids)
    budget_m2 = len(a_ids)
    eco = 1.0 - (budget_m2 / budget_m1) if budget_m1 else 0.0

    # Reversibility: excluded IDs and scores still in store
    rev = all(get_hypothesis(hid, store) is not None for hid in excluded) and all(
        any(s.hypothesis_id == hid for s in sel.ranked) for hid in open_ids
    )

    return {
        "seed": seed,
        "n_open": len(open_ids),
        "n_group_a": len(a_ids),
        "n_excluded": len(excluded),
        "eco": round(eco, 4),
        "n_rare": n_rare,
        "rare_in_a": len(rare_in_a),
        "rare_excluded": len(rare_ex),
        "fn_rate": round(fn_rate, 4),
        "cov_rare_a": round(cov_rare_a, 4),
        "common_in_a": len(common_in_a),
        "n_common": len(common_all),
        "div_drop": round(div_drop, 4),
        "clusters_all": cl_all,
        "clusters_a": cl_a,
        "reversibility_ids_intact": rev,
        "pattern_00": bool(fn_rate >= 0.50 or cov_rare_a < 0.35 or div_drop >= 0.55),
        "pattern_01": bool(fn_rate < 0.40 and cov_rare_a >= 0.50 and div_drop < 0.50),
    }


def classify(replicas: List[Dict[str, Any]]) -> Dict[str, Any]:
    n = len(replicas)
    mean = lambda k: sum(r[k] for r in replicas) / n

    mean_fn = mean("fn_rate")
    mean_cov = mean("cov_rare_a")
    mean_div = mean("div_drop")
    mean_eco = mean("eco")
    n_00 = sum(1 for r in replicas if r["pattern_00"])
    n_01 = sum(1 for r in replicas if r["pattern_01"])
    rev_all = all(r["reversibility_ids_intact"] for r in replicas)

    # Protocol death rules
    if n_00 >= 7 and mean_fn >= 0.60:
        h01, h00 = "MUERTA", "SOPORTADA_BAJO_CONTROL"
        verdict = "H00_DIVERSITY_COMPRESSION"
    elif n_00 >= 7:
        h01, h00 = "DEBILITADA", "SOPORTADA_BAJO_CONTROL"
        verdict = "H00_DIVERSITY_COMPRESSION_MODERATE"
    elif n_01 >= 7 and mean_fn < 0.40 and mean_cov >= 0.50:
        h01, h00 = "SOPORTADA_BAJO_CONTROL", "MUERTA"
        verdict = "H01_NOISE_COMPRESSION"
    else:
        h01, h00 = "NO_SABEMOS", "NO_SABEMOS"
        verdict = "NO_SABEMOS"

    # Validity map (not a medal) — driven by diversity compression / FN
    if mean_div >= 0.55 or mean_fn >= 0.50 or n_00 >= 7:
        validity = {
            "aceptado": [
                "solo si se acepta pérdida fuerte de diversidad de candidatos OPEN",
            ],
            "limitado": [
                "exploración inicial con alta redundancia",
                "requiere control oculto / muestreo de excluidos",
            ],
            "no_recomendado": [
                "búsqueda abierta de estructuras raras o baja frecuencia",
                "dominios donde la diversidad de caminos es el activo",
            ],
        }
    elif mean_fn < 0.35 and mean_eco >= 0.5 and mean_div < 0.4:
        validity = {
            "aceptado": [
                "problemas con alta redundancia",
                "candidatos con señales claras (common_ok)",
            ],
            "limitado": ["mezclas rare/common sin control oculto"],
            "no_recomendado": [],
        }
    else:
        validity = {
            "aceptado": [],
            "limitado": ["uso solo con monitoreo de zona excluida"],
            "no_recomendado": [],
        }

    return {
        "campaign": "META-E002b",
        "protocol": "v1.0 CONGELADO",
        "n_rep": n,
        "replicas": replicas,
        "aggregate": {
            "mean_eco": round(mean_eco, 4),
            "mean_fn_rate": round(mean_fn, 4),
            "mean_cov_rare_a": round(mean_cov, 4),
            "mean_div_drop": round(mean_div, 4),
            "n_seeds_pattern_00": n_00,
            "n_seeds_pattern_01": n_01,
            "reversibility_all": rev_all,
        },
        "hypotheses": {
            "H-META-E002b-01": h01,
            "H-META-E002b-00": h00,
        },
        "verdict": verdict,
        "evidence_profile": {
            "E-M1": "fuerte" if rev_all else "contraria",
            "E-M2": "fuerte" if mean_eco >= 0.5 else "moderada",
            # E-M3: cost of selection = FN on rare + diversity collapse
            "E-M3": (
                "contraria"
                if (mean_fn >= 0.5 or mean_div >= 0.55 or n_00 >= 7)
                else ("moderada" if mean_fn >= 0.35 or mean_div >= 0.4 else "insuficiente")
            ),
            "E-M4": "no evaluada",
            "E-M5": "no evaluada",
        },
        "validity_map": validity,
        "local_vs_global": (
            "E-M2 may stay strong while E-M3 shows cost of blindness to rare_valuable"
        ),
        "claim_limit": (
            "Synthetic latent labels; not real math value. "
            "Measures compression type under this generator."
        ),
    }


def main() -> int:
    n_rep = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    n_cand = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    reps = [run_seed(s, n_cand) for s in range(n_rep)]
    out = classify(reps)
    dest = ROOT / "META-E002b" / "resultados"
    dest.mkdir(parents=True, exist_ok=True)
    path = dest / "classification.json"
    path.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"\nWrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
