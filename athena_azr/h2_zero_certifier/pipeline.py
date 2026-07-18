from __future__ import annotations

from pathlib import Path
from typing import Callable

from .authorization import (
    ExecutionNotAuthorized,
    G5B_006F_AUTHORIZATION_FILENAME,
    PLAN_006E3_SHA256,
    PROTOCOL_006B_SHA256,
    PROBATIVE_RUNTIME_CODE_FILES,
    SPEC_006E2_SHA256,
    compute_review_document_hashes,
    require_execution_authorization,
    validate_g5b_006f_authorization_schema,
)
from .real_evidence import (
    InvalidRealEvidence,
    RealArgumentIncrementEvidence,
    RealCompletedL3PointEvidence,
    RealHalfPlaneEvidence,
    RealSegmentImageEvidence,
    RealWindingEvidence,
    require_probative_evidence_chain,
)


OUTPUT_RELATIVE_PATH = Path(
    "artifacts/goldbach_cesaro/c03b_h2_zero_certification"
)

PROBATIVE_EVIDENCE_TYPES = (
    RealCompletedL3PointEvidence,
    RealSegmentImageEvidence,
    RealHalfPlaneEvidence,
    RealArgumentIncrementEvidence,
    RealWindingEvidence,
)


def require_probative_evidence(value):
    if not isinstance(value, PROBATIVE_EVIDENCE_TYPES) or value.probative is not True:
        raise InvalidRealEvidence(
            "probative pipeline requires evidence bound to validated authorization"
        )
    return require_probative_evidence_chain(value)


def expected_output_path(code_root: Path) -> Path:
    return code_root.resolve() / OUTPUT_RELATIVE_PATH


def recognize_documentary_006f_authorization(path: Path):
    if path.name != G5B_006F_AUTHORIZATION_FILENAME:
        raise ExecutionNotAuthorized("documentary 006F authorization filename mismatch")
    import json

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ExecutionNotAuthorized("documentary 006F authorization is unreadable") from exc
    return validate_g5b_006f_authorization_schema(payload)


def run_certification_pipeline(
    *,
    authorization_path: Path,
    output_dir: Path,
    backend_factory: Callable[[], object],
    expected_plan_hash: str,
    code_root: Path | None = None,
) -> None:
    resolved_code_root = code_root or Path(__file__).resolve().parents[2]
    if output_dir.resolve() != expected_output_path(resolved_code_root):
        raise ExecutionNotAuthorized("output directory is not the preregistered H2 path")
    authorization = require_execution_authorization(
        authorization_path,
        expected_protocol_hash=PROTOCOL_006B_SHA256,
        expected_plan_hash=expected_plan_hash,
        expected_spec_hash=SPEC_006E2_SHA256,
        expected_inert_plan_hash=PLAN_006E3_SHA256,
        expected_review_hashes=compute_review_document_hashes(resolved_code_root),
        expected_output_dir=output_dir,
        code_root=resolved_code_root,
        required_code_files=PROBATIVE_RUNTIME_CODE_FILES,
    )

    if output_dir.exists() and any(output_dir.iterdir()):
        raise FileExistsError("certification output directory must be absent or empty")

    backend = backend_factory()
    initialize = getattr(backend, "initialize", None)
    if initialize is None:
        raise TypeError("backend does not expose initialize()")
    initialize(authorization=authorization)

    raise NotImplementedError("real certification pipeline is reserved for 006F")
