from __future__ import annotations

import json
import hashlib
from dataclasses import dataclass, field
from pathlib import Path
from types import MappingProxyType
from typing import Mapping


PROTOCOL_006B_SHA256 = "4f110d0926067e9e1eb44cbbfe78ee1acc93f85f526176c81d98446eafd492cb"
SPEC_006E2_SHA256 = "4b14ba44d08d80941a4ab69776c41479453f0f08661ffec9fcb304204f1212c5"
PLAN_006E3_SHA256 = "4b7a277e939fab39ac6a9ce95cfe771944964a90a37dab12d005908ab849e931"
RUNTIME_CODE_FILES = (
    "athena_azr/h2_zero_certifier/__init__.py",
    "athena_azr/h2_zero_certifier/argument_principle.py",
    "athena_azr/h2_zero_certifier/authorization.py",
    "athena_azr/h2_zero_certifier/backend.py",
    "athena_azr/h2_zero_certifier/ball_argument.py",
    "athena_azr/h2_zero_certifier/argument_increment.py",
    "athena_azr/h2_zero_certifier/boundary_certifier.py",
    "athena_azr/h2_zero_certifier/chi3_function.py",
    "athena_azr/h2_zero_certifier/completed_l3.py",
    "athena_azr/h2_zero_certifier/config.py",
    "athena_azr/h2_zero_certifier/contour.py",
    "athena_azr/h2_zero_certifier/l3_argument_count.py",
    "athena_azr/h2_zero_certifier/l3_certifier.py",
    "athena_azr/h2_zero_certifier/l3_isolator.py",
    "athena_azr/h2_zero_certifier/models.py",
    "athena_azr/h2_zero_certifier/pipeline.py",
    "athena_azr/h2_zero_certifier/python_flint_backend.py",
    "athena_azr/h2_zero_certifier/serialization.py",
    "athena_azr/h2_zero_certifier/validation.py",
    "athena_azr/h2_zero_certifier/winding_certifier.py",
    "athena_azr/h2_zero_certifier/zeta_certifier.py",
    "scripts/run_h2_zero_certification.py",
)
SYNTHETIC_TEST_ONLY_FILES = (
    "athena_azr/h2_zero_certifier/argument_principle.py",
)
PROBATIVE_RUNTIME_CODE_FILES = tuple(
    name for name in RUNTIME_CODE_FILES if name not in SYNTHETIC_TEST_ONLY_FILES
) + (
    "athena_azr/h2_zero_certifier/real_evidence.py",
    "athena_azr/h2_zero_certifier/rigorous_ball_runtime.py",
    "athena_azr/h2_zero_certifier/real_completed_l3.py",
    "athena_azr/h2_zero_certifier/real_segment_enclosure.py",
    "athena_azr/h2_zero_certifier/real_argument.py",
)
REVIEW_DOCUMENT_FILES = MappingProxyType({
    "plan_006e7_sha256": "docs/experimentos/experimento-006e7-c03b-l3-real-backend-inert-tdd-plan.md",
    "report_006e8_sha256": "docs/experimentos/experimento-006e8-c03b-l3-real-backend-inert-code-report.md",
    "review_006e9_sha256": "docs/experimentos/experimento-006e9-c03b-l3-real-backend-inert-independent-review.md",
    "corrections_006e10_sha256": "docs/experimentos/experimento-006e10-c03b-l3-inert-backend-corrections.md",
})
_FIELDS = {
    "experiment_id",
    "execution_authorized",
    "max_height",
    "requested_heights",
    "protocol_006b_sha256",
    "plan_006c_sha256",
    "spec_006e2_sha256",
    "plan_006e3_sha256",
    "approved_code_hashes",
    "output_directory",
    *REVIEW_DOCUMENT_FILES,
}
G5B_006F_AUTHORIZATION_FILENAME = "G5B-006F-AUTHORIZATION.json"
G5B_006F_AUTHORIZATION_FIELDS = frozenset(
    {
        "authorization_id",
        "phase_id",
        "authorized_runtime",
        "authorized_backend_versions",
        "authorized_code_hashes",
        "authorized_protocol_hashes",
        "authorized_functions",
        "authorized_heights",
        "authorized_artifact_directory",
        "network_policy",
        "dependency_policy",
        "execution_scope",
        "forbidden_scope",
        "issued_by",
        "issued_at",
    }
)


class ExecutionNotAuthorized(RuntimeError):
    """Raised before any real numerical backend or output can be used."""


_VALIDATED_AUTHORIZATION_TOKEN = object()
_VALIDATED_EVIDENCE_PROVENANCE_TOKEN = object()


@dataclass(frozen=True)
class ExecutionAuthorization:
    experiment_id: str
    execution_authorized: bool
    max_height: int
    requested_heights: tuple[int, ...]
    protocol_006b_sha256: str
    plan_006c_sha256: str
    spec_006e2_sha256: str
    plan_006e3_sha256: str
    approved_code_hashes: Mapping[str, str]
    review_chain_hashes: Mapping[str, str]
    output_directory: Path
    source_digest: str
    _validation_token: object = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._validation_token is not _VALIDATED_AUTHORIZATION_TOKEN:
            raise ExecutionNotAuthorized(
                "execution authorization must be issued by the validated 006F parser"
            )
        object.__setattr__(
            self, "approved_code_hashes", MappingProxyType(dict(self.approved_code_hashes))
        )
        object.__setattr__(
            self, "review_chain_hashes", MappingProxyType(dict(self.review_chain_hashes))
        )


@dataclass(frozen=True)
class ValidatedEvidenceProvenance:
    backend_id: str
    authorization_digest: str
    runtime_code_digest: str
    review_chain_digest: str
    _validation_token: object = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._validation_token is not _VALIDATED_EVIDENCE_PROVENANCE_TOKEN:
            raise ExecutionNotAuthorized(
                "evidence provenance must come from a validated authorization"
            )
        if not self.backend_id or not all(
            _is_sha256(value) for value in (
                self.authorization_digest,
                self.runtime_code_digest,
                self.review_chain_digest,
            )
        ):
            raise ExecutionNotAuthorized("validated evidence provenance is malformed")


def _is_sha256(value: object) -> bool:
    return isinstance(value, str) and len(value) == 64 and all(
        character in "0123456789abcdef" for character in value
    )


def _mapping_digest(values: Mapping[str, str]) -> str:
    encoded = json.dumps(
        dict(sorted(values.items())),
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def validate_g5b_006f_authorization_schema(payload: Mapping[str, object]) -> Mapping[str, object]:
    if not isinstance(payload, Mapping) or set(payload) != G5B_006F_AUTHORIZATION_FIELDS:
        raise ExecutionNotAuthorized("G5B-006F authorization schema mismatch")
    if payload["phase_id"] != "006F":
        raise ExecutionNotAuthorized("G5B-006F phase mismatch")
    if payload["authorized_functions"] != ["zeta", "L3"]:
        raise ExecutionNotAuthorized("G5B-006F function scope mismatch")
    if payload["authorized_heights"] != [143, 200, 300, 500]:
        raise ExecutionNotAuthorized("G5B-006F height scope mismatch")
    if payload["network_policy"] != "forbidden":
        raise ExecutionNotAuthorized("G5B-006F network policy must be forbidden")
    if payload["dependency_policy"] != "no_installation_during_execution":
        raise ExecutionNotAuthorized("G5B-006F dependency policy mismatch")
    for mapping_name in (
        "authorized_runtime",
        "authorized_backend_versions",
        "authorized_code_hashes",
        "authorized_protocol_hashes",
        "execution_scope",
    ):
        if not isinstance(payload[mapping_name], Mapping) or not payload[mapping_name]:
            raise ExecutionNotAuthorized(f"{mapping_name} must be a nonempty mapping")
    for list_name in ("forbidden_scope",):
        if not isinstance(payload[list_name], list) or not payload[list_name]:
            raise ExecutionNotAuthorized(f"{list_name} must be a nonempty list")
    for text_name in ("authorization_id", "authorized_artifact_directory", "issued_by", "issued_at"):
        if not isinstance(payload[text_name], str) or not payload[text_name]:
            raise ExecutionNotAuthorized(f"{text_name} must be nonempty")
    normalized = dict(payload)
    normalized["execution_authorized"] = False
    return MappingProxyType(normalized)


def canonical_authorization_schema_json(payload: Mapping[str, object]) -> str:
    validate_g5b_006f_authorization_schema(payload)
    return json.dumps(
        dict(payload),
        sort_keys=True,
        separators=(",", ":"),
    ) + "\n"


def issue_evidence_provenance(
    authorization: ExecutionAuthorization,
    *,
    backend_id: str,
) -> ValidatedEvidenceProvenance:
    if (
        not isinstance(authorization, ExecutionAuthorization)
        or authorization._validation_token is not _VALIDATED_AUTHORIZATION_TOKEN
        or not authorization.execution_authorized
    ):
        raise ExecutionNotAuthorized(
            "probative evidence requires a parser-validated authorization"
        )
    return ValidatedEvidenceProvenance(
        backend_id=backend_id,
        authorization_digest=authorization.source_digest,
        runtime_code_digest=_mapping_digest(authorization.approved_code_hashes),
        review_chain_digest=_mapping_digest(authorization.review_chain_hashes),
        _validation_token=_VALIDATED_EVIDENCE_PROVENANCE_TOKEN,
    )


def require_validated_evidence_provenance(
    provenance: object,
) -> ValidatedEvidenceProvenance:
    if (
        not isinstance(provenance, ValidatedEvidenceProvenance)
        or provenance._validation_token is not _VALIDATED_EVIDENCE_PROVENANCE_TOKEN
    ):
        raise ExecutionNotAuthorized("evidence provenance is not validated")
    return provenance


def require_execution_authorization(
    path: Path,
    *,
    expected_protocol_hash: str = PROTOCOL_006B_SHA256,
    expected_plan_hash: str,
    expected_spec_hash: str = SPEC_006E2_SHA256,
    expected_inert_plan_hash: str = PLAN_006E3_SHA256,
    expected_review_hashes: Mapping[str, str],
    expected_output_dir: Path,
    code_root: Path,
    required_code_files: tuple[str, ...] = (),
) -> ExecutionAuthorization:
    try:
        raw_payload = path.read_bytes()
        payload = json.loads(raw_payload.decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ExecutionNotAuthorized("missing or invalid 006F authorization") from exc

    if not isinstance(payload, dict) or set(payload) != _FIELDS:
        raise ExecutionNotAuthorized("authorization schema mismatch")
    if payload["experiment_id"] != "G5B-006F" or payload["execution_authorized"] is not True:
        raise ExecutionNotAuthorized("real execution is not authorized")
    if payload["max_height"] != 500 or payload["requested_heights"] != [143, 200, 300, 500]:
        raise ExecutionNotAuthorized("authorization scope mismatch")
    if payload["protocol_006b_sha256"] != expected_protocol_hash:
        raise ExecutionNotAuthorized("006B hash mismatch")
    if payload["plan_006c_sha256"] != expected_plan_hash:
        raise ExecutionNotAuthorized("006C hash mismatch")
    if payload["spec_006e2_sha256"] != expected_spec_hash:
        raise ExecutionNotAuthorized("006E2 hash mismatch")
    if payload["plan_006e3_sha256"] != expected_inert_plan_hash:
        raise ExecutionNotAuthorized("006E3 hash mismatch")
    if set(expected_review_hashes) != set(REVIEW_DOCUMENT_FILES):
        raise ExecutionNotAuthorized("post-006E7 review hash inventory mismatch")
    for field_name, expected_hash in expected_review_hashes.items():
        if not _is_sha256(expected_hash) or payload[field_name] != expected_hash:
            raise ExecutionNotAuthorized(f"{field_name} mismatch")

    expected_output = expected_output_dir.resolve()
    authorized_output = Path(payload["output_directory"]).resolve()
    if authorized_output != expected_output:
        raise ExecutionNotAuthorized("output directory mismatch")

    hashes = payload["approved_code_hashes"]
    if not isinstance(hashes, dict) or not hashes:
        raise ExecutionNotAuthorized("approved code hashes are required")
    if not all(isinstance(name, str) and name and _is_sha256(value) for name, value in hashes.items()):
        raise ExecutionNotAuthorized("invalid approved code hash")
    if required_code_files and set(hashes) != set(required_code_files):
        raise ExecutionNotAuthorized("approved code hash inventory is incomplete or contains extras")

    root = code_root.resolve()
    for relative_name, expected_hash in hashes.items():
        relative_path = Path(relative_name)
        if relative_path.is_absolute():
            raise ExecutionNotAuthorized("approved code path must be relative")
        target = (root / relative_path).resolve()
        if not target.is_relative_to(root) or not target.is_file():
            raise ExecutionNotAuthorized("approved code path is missing or escapes code root")
        actual_hash = hashlib.sha256(target.read_bytes()).hexdigest()
        if actual_hash != expected_hash:
            raise ExecutionNotAuthorized(f"approved code hash mismatch: {relative_name}")

    return ExecutionAuthorization(
        experiment_id=payload["experiment_id"],
        execution_authorized=True,
        max_height=500,
        requested_heights=(143, 200, 300, 500),
        protocol_006b_sha256=payload["protocol_006b_sha256"],
        plan_006c_sha256=payload["plan_006c_sha256"],
        spec_006e2_sha256=payload["spec_006e2_sha256"],
        plan_006e3_sha256=payload["plan_006e3_sha256"],
        approved_code_hashes=hashes,
        review_chain_hashes={
            field_name: payload[field_name] for field_name in REVIEW_DOCUMENT_FILES
        },
        output_directory=authorized_output,
        source_digest=hashlib.sha256(raw_payload).hexdigest(),
        _validation_token=_VALIDATED_AUTHORIZATION_TOKEN,
    )


def compute_review_document_hashes(code_root: Path) -> Mapping[str, str]:
    root = code_root.resolve()
    hashes: dict[str, str] = {}
    for field_name, relative_name in REVIEW_DOCUMENT_FILES.items():
        target = (root / relative_name).resolve()
        if not target.is_relative_to(root) or not target.is_file():
            raise ExecutionNotAuthorized(
                f"required review document is missing: {relative_name}"
            )
        hashes[field_name] = hashlib.sha256(target.read_bytes()).hexdigest()
    return MappingProxyType(hashes)
