"""
DOMAIN-E007 — réplica de E006: único cambio N=50000.
Replicación, no descubrimiento.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROTOCOL_PATH = ROOT / "ATHENA_DOMAIN_E007" / "ATHENA_DOMAIN_E007_PROTOCOL.md"
N_E007 = 50_000
B_DEFAULT = 2000
E006_SHA = "12b9c1b7ec6930472efc2a774d484a90ea64e9db9f15270394c24e15161f9e5b"


def protocol_sha256() -> str:
    return hashlib.sha256(PROTOCOL_PATH.read_bytes()).hexdigest()


def load_e006():
    path = ROOT / "scripts" / "run_athena_domain_e006.py"
    spec = importlib.util.spec_from_file_location("athena_e006", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def replica_verdict(class_w30: str, sig: dict) -> str:
    try:
        s1, s2, s6, s30 = sig["1"], sig["2"], sig["6"], sig["30"]
    except KeyError:
        return "AMBIGUA"
    order_ok = s1 > s2 > s6 > s30
    if class_w30 == "PERSISTE" and order_ok:
        return "REPRODUCIDA"
    if class_w30 == "PERSISTE" and not order_ok:
        return "SENAL_SIN_CURVA"
    if class_w30 in ("DESAPARECE", "NO_SABEMOS"):
        return "NO_REPRODUCIDA"
    return "AMBIGUA"


def main() -> int:
    e006 = load_e006()
    N = int(sys.argv[1]) if len(sys.argv) > 1 else N_E007
    B = int(sys.argv[2]) if len(sys.argv) > 2 else B_DEFAULT

    out6 = e006.run_campaign(N=N, B=B)

    interp = out6.get("interpretation", "")
    if interp == "PERSISTE":
        class_w30 = "PERSISTE"
    elif interp == "DESAPARECE":
        class_w30 = "DESAPARECE"
    else:
        class_w30 = "NO_SABEMOS"

    sig = {str(k): float(v) for k, v in out6.get("signals", {}).items()}
    rv = replica_verdict(class_w30, sig)
    order_ok = (
        all(k in sig for k in ("1", "2", "6", "30"))
        and sig["1"] > sig["2"] > sig["6"] > sig["30"]
    )

    out = {
        "campaign": "ATHENA_DOMAIN_E007",
        "protocol": "v1.0 CONGELADO",
        "kind": "replication_not_discovery",
        "protocol_sha256": protocol_sha256(),
        "parent_E006_protocol_sha256": E006_SHA,
        "N_E006_reference": 100_000,
        "N_E007": N,
        "k": out6.get("k"),
        "B": B,
        "only_changed_variable": "N",
        "M_P": out6.get("M_P"),
        "signals": sig,
        "curve_order_S1_gt_S2_gt_S6_gt_S30": order_ok,
        "class_W30": class_w30,
        "E006_pipeline_verdict": out6.get("verdict"),
        "E006_pipeline_interpretation": interp,
        "wheels": out6.get("wheels"),
        "conditions_W30": out6.get("conditions_W30"),
        "curve_code_E006_style": out6.get("curve_code"),
        "replica_verdict": rv,
        "anti_retrospective_rule": "E007 does not rewrite E006",
        "E006_status": "unchanged",
        "md035_audit": out6.get("md035_audit"),
        "no_claims": [
            "Not a stronger signal hunt",
            "Not a theory",
            "NO_REPRODUCIDA does not falsify E006 retrospectively",
            "REPRODUCIDA does not promote E006 to theory",
        ],
        "full_E006_style_output": {
            "verdict": out6.get("verdict"),
            "hypotheses": out6.get("hypotheses"),
            "C2_semiprimes_sample": out6.get("C2_semiprimes_sample"),
            "C3_ulam": out6.get("C3_ulam"),
        },
    }

    dest = ROOT / "ATHENA_DOMAIN_E007" / "resultados"
    dest.mkdir(parents=True, exist_ok=True)
    path = dest / "classification.json"
    path.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"\nWrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
