"""
META-E004 — ¿economía↔diversidad generaliza o era el generador E002b?
Selector v0.1 congelado; solo cambia el dominio de candidatos.
"""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Set

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from athena_core.domain_generators import payload as domain_payload
from athena_core.protocol import ProtocolError, ProtocolStore, create_hypothesis, create_question, get_hypothesis
from athena_core.selector import _tokens, select_challenges

DOMAINS = ("math_struct", "engineering", "creative")


def _clusters(hyp_ids: List[str], store: ProtocolStore) -> int:
    sigs: Set[str] = set()
    for hid in hyp_ids:
        h = get_hypothesis(hid, store)
        toks = sorted(_tokens((h.statement or "") + " " + (h.predicts or "")))
        sigs.add("|".join(toks[:5]) if toks else hid)
    return len(sigs)


def run_domain_seed(domain: str, seed: int, n_cand: int = 100) -> Dict[str, Any]:
    d = Path(tempfile.mkdtemp(prefix=f"e004_{domain}_s{seed}_"))
    store = ProtocolStore(d)
    q = create_question(
        f"META-E004 domain={domain} seed={seed}",
        domain=domain,
        store=store,
    )
    latent_by_hyp: Dict[str, str] = {}
    open_ids: List[str] = []
    for i in range(n_cand):
        p = domain_payload(domain, i, n_cand, seed)
        lat = p.get("latent_class", "noise")
        try:
            h = create_hypothesis(
                q.id,
                p["statement"],
                p["predicts"],
                p["weakens_if"],
                p["dies_if"],
                store=store,
            )
            open_ids.append(h.id)
            latent_by_hyp[h.id] = lat
        except ProtocolError:
            pass

    sel = select_challenges(store=store, only_open=True)
    a_ids = [s.hypothesis_id for s in sel.ranked if s.group == "A"]
    excluded = [hid for hid in open_ids if hid not in set(a_ids)]

    hv_all = [hid for hid in open_ids if latent_by_hyp.get(hid) == "high_value"]
    hv_a = [hid for hid in a_ids if latent_by_hyp.get(hid) == "high_value"]
    hv_ex = [hid for hid in excluded if latent_by_hyp.get(hid) == "high_value"]
    n_hv = len(hv_all)
    fn_rate = (len(hv_ex) / n_hv) if n_hv else 0.0
    cov_hv = (len(hv_a) / n_hv) if n_hv else 0.0

    cl_all = _clusters(open_ids, store)
    cl_a = _clusters(a_ids, store) if a_ids else 0
    div_drop = 1.0 - (cl_a / cl_all) if cl_all else 0.0
    eco = 1.0 - (len(a_ids) / len(open_ids)) if open_ids else 0.0

    pattern_div = bool(div_drop >= 0.55 or fn_rate >= 0.50 or cov_hv < 0.35)
    # when no high_value, don't use cov/fn alone as diversity pattern from zeros
    if n_hv == 0:
        pattern_div = bool(div_drop >= 0.55)
    pattern_ok = bool(
        n_hv > 0 and fn_rate < 0.40 and cov_hv >= 0.50 and div_drop < 0.50
    )

    return {
        "domain": domain,
        "seed": seed,
        "n_open": len(open_ids),
        "n_a": len(a_ids),
        "eco": round(eco, 4),
        "n_high_value": n_hv,
        "hv_in_a": len(hv_a),
        "hv_excluded": len(hv_ex),
        "fn_rate": round(fn_rate, 4),
        "cov_hv": round(cov_hv, 4),
        "div_drop": round(div_drop, 4),
        "pattern_diversity": pattern_div,
        "pattern_coverage_ok": pattern_ok,
        "reversibility": True,
    }


def classify_domain(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    n = len(rows)
    mean = lambda k: sum(r[k] for r in rows) / n
    n_div = sum(1 for r in rows if r["pattern_diversity"])
    n_ok = sum(1 for r in rows if r["pattern_coverage_ok"])
    # majority of seeds
    if n_div >= (n // 2 + 1):
        state = "diversidad_comprimida"
    elif n_ok >= (n // 2 + 1):
        state = "cobertura_ok"
    else:
        state = "mixto_NO_SABEMOS"
    return {
        "domain": rows[0]["domain"],
        "mean_eco": round(mean("eco"), 4),
        "mean_div_drop": round(mean("div_drop"), 4),
        "mean_fn_rate": round(mean("fn_rate"), 4),
        "mean_cov_hv": round(mean("cov_hv"), 4),
        "n_seeds_diversity": n_div,
        "n_seeds_coverage_ok": n_ok,
        "state": state,
        "seeds": rows,
    }


def main() -> int:
    n_rep = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    n_cand = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    by_domain = {}
    for dom in DOMAINS:
        rows = [run_domain_seed(dom, s, n_cand) for s in range(n_rep)]
        by_domain[dom] = classify_domain(rows)

    states = [by_domain[d]["state"] for d in DOMAINS]
    n_div = sum(1 for s in states if s == "diversidad_comprimida")
    n_ok = sum(1 for s in states if s == "cobertura_ok")

    if n_div >= 2:
        h01, h00 = "SOPORTADA_BAJO_CONTROL", "DEBILITADA"
        verdict = "H01_TRANSVERSAL_DIVERSITY_COST"
    elif n_ok >= 2:
        h01, h00 = "DEBILITADA", "SOPORTADA_BAJO_CONTROL"
        verdict = "H00_CONTEXTUAL_E002b"
    else:
        h01, h00 = "NO_SABEMOS", "NO_SABEMOS"
        verdict = "NO_SABEMOS_MIXED"

    table = []
    for d in DOMAINS:
        b = by_domain[d]
        eco_s = "+" if b["mean_eco"] >= 0.5 else "0"
        div_s = "-" if b["mean_div_drop"] >= 0.55 else ("0" if b["mean_div_drop"] < 0.4 else "~")
        table.append(
            {
                "domain": d,
                "economia": eco_s,
                "diversidad": div_s,
                "mean_eco": b["mean_eco"],
                "mean_div_drop": b["mean_div_drop"],
                "mean_fn": b["mean_fn_rate"],
                "state": b["state"],
            }
        )

    out = {
        "campaign": "META-E004",
        "protocol": "v1.0 CONGELADO",
        "selector": "v0.1 frozen",
        "n_rep_per_domain": n_rep,
        "n_candidates": n_cand,
        "domains": by_domain,
        "table": table,
        "hypotheses": {"H-META-E004-01": h01, "H-META-E004-00": h00},
        "verdict": verdict,
        "evidence_profile": {
            "E-M1": "fuerte",
            "E-M2": "fuerte" if all(t["mean_eco"] >= 0.5 for t in table) else "moderada",
            "E-M3": "ver por dominio",
            "E-M4": (
                "contraria_a_especificidad"
                if n_div >= 2
                else ("apoyo_a_especificidad" if n_ok >= 2 else "insuficiente")
            ),
            "E-M5": "no evaluada",
        },
        "reading": (
            "If H01: diversity cost looks structural to selection mechanism. "
            "If H00: E002b cost was contextual to that generator. "
            "Neither rewrites E001 economy under E002b domain."
        ),
        "claim_limit": "Synthetic multi-domain generators; not real math domains.",
    }
    dest = ROOT / "META-E004" / "resultados"
    dest.mkdir(parents=True, exist_ok=True)
    path = dest / "classification.json"
    path.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({k: out[k] for k in (
        "campaign", "verdict", "hypotheses", "table", "evidence_profile", "claim_limit"
    )}, indent=2, ensure_ascii=False))
    print(f"\nWrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
