"""CLI mínima del núcleo — sin IA."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .auditor import audit_store
from .protocol import (
    HypothesisState,
    ProtocolError,
    ProtocolStore,
    create_hypothesis,
    create_question,
    get_hypothesis,
    list_hypotheses,
    record_result,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="ATHENA CORE PROTOCOL — árbitro de disciplina (sin IA)"
    )
    parser.add_argument(
        "--data",
        type=Path,
        default=None,
        help="Directorio de registro (default: data/athena_core)",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_q = sub.add_parser("question", help="Crear pregunta")
    p_q.add_argument("text")
    p_q.add_argument("--domain", default="unspecified")

    p_h = sub.add_parser("hypothesis", help="Crear hipótesis")
    p_h.add_argument("question_id")
    p_h.add_argument("statement")
    p_h.add_argument("--predicts", required=True)
    p_h.add_argument("--weakens-if", required=True)
    p_h.add_argument("--dies-if", required=True)

    p_r = sub.add_parser("result", help="Registrar resultado y estado")
    p_r.add_argument("hypothesis_id")
    p_r.add_argument("--control", required=True)
    p_r.add_argument("--summary", required=True)
    p_r.add_argument(
        "--state",
        required=True,
        choices=[s.value for s in HypothesisState if s != HypothesisState.OPEN],
    )
    p_r.add_argument("--death-reason", default=None)

    sub.add_parser("list", help="Listar hipótesis")
    p_g = sub.add_parser("get", help="Ver hipótesis")
    p_g.add_argument("hypothesis_id")
    sub.add_parser("audit", help="Correr auditor de disciplina (PASS/WARN/FAIL)")

    args = parser.parse_args(argv)
    store = ProtocolStore(args.data)

    try:
        if args.cmd == "audit":
            report = audit_store(store)
            print(json.dumps(report.to_dict(), indent=2, ensure_ascii=False))
            return 0 if report.verdict != "FAIL" else 2
        if args.cmd == "question":
            q = create_question(args.text, args.domain, store)
            print(json.dumps({"id": q.id, "text": q.text}, ensure_ascii=False))
        elif args.cmd == "hypothesis":
            h = create_hypothesis(
                args.question_id,
                args.statement,
                args.predicts,
                args.weakens_if,
                args.dies_if,
                store,
            )
            print(
                json.dumps(
                    {"id": h.id, "state": h.state, "predicts": h.predicts},
                    ensure_ascii=False,
                )
            )
        elif args.cmd == "result":
            h = record_result(
                args.hypothesis_id,
                args.control,
                args.summary,
                args.state,
                death_reason=args.death_reason,
                store=store,
            )
            print(
                json.dumps(
                    {
                        "id": h.id,
                        "state": h.state,
                        "control_id": h.control_id,
                        "death_reason": h.death_reason,
                    },
                    ensure_ascii=False,
                )
            )
        elif args.cmd == "list":
            rows = [
                {"id": h.id, "state": h.state, "statement": h.statement}
                for h in list_hypotheses(store)
            ]
            print(json.dumps(rows, indent=2, ensure_ascii=False))
        elif args.cmd == "get":
            h = get_hypothesis(args.hypothesis_id, store)
            print(json.dumps(h.__dict__, indent=2, ensure_ascii=False))
    except ProtocolError as e:
        print(json.dumps({"error": e.code, "message": str(e)}), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
