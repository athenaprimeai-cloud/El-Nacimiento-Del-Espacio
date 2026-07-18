from __future__ import annotations

import hashlib
import json
import weakref
from contextvars import ContextVar
from dataclasses import asdict, dataclass, field
from decimal import Decimal, InvalidOperation
from threading import RLock

from .authorization import (
    ExecutionAuthorization,
    issue_evidence_provenance,
    require_validated_evidence_provenance,
)


class InvalidRealEvidence(RuntimeError):
    """Raised when probative evidence lacks valid provenance."""


def _decimal(value: str) -> Decimal:
    try:
        result = Decimal(value)
    except InvalidOperation as exc:
        raise InvalidRealEvidence(f"invalid decimal bound: {value!r}") from exc
    if not result.is_finite():
        raise InvalidRealEvidence("ball bounds must be finite")
    return result


def _sha256(value: str) -> bool:
    return len(value) == 64 and all(char in "0123456789abcdef" for char in value)


def _digest(payload: dict) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


@dataclass(frozen=True)
class RealBallRecord:
    lower: str
    upper: str

    def __post_init__(self) -> None:
        if _decimal(self.lower) > _decimal(self.upper):
            raise InvalidRealEvidence("real ball bounds are reversed")


@dataclass(frozen=True)
class ComplexBallRecord:
    real_lower: str
    real_upper: str
    imag_lower: str
    imag_upper: str

    def __post_init__(self) -> None:
        if _decimal(self.real_lower) > _decimal(self.real_upper):
            raise InvalidRealEvidence("complex ball real bounds are reversed")
        if _decimal(self.imag_lower) > _decimal(self.imag_upper):
            raise InvalidRealEvidence("complex ball imaginary bounds are reversed")


@dataclass(frozen=True)
class _ConstructionPermit:
    capability: object
    probative: bool
    provenance: tuple[str, str, str, str]


_CONSTRUCTION_PERMIT: ContextVar[_ConstructionPermit | None] = ContextVar(
    "h2_real_evidence_construction_permit",
    default=None,
)


def _create_issuance_registry():
    records: dict[int, tuple[weakref.ReferenceType, object, tuple[str, str, str, str], str]] = {}
    lock = RLock()

    def register(evidence: "_EvidenceBase", capability: object) -> None:
        identity = id(evidence)

        def discard(reference: weakref.ReferenceType) -> None:
            with lock:
                current = records.get(identity)
                if current is not None and current[0] is reference:
                    records.pop(identity, None)

        reference = weakref.ref(evidence, discard)
        record = (reference, capability, _provenance(evidence), evidence.digest)
        with lock:
            records[identity] = record

    def require(evidence: "_EvidenceBase") -> None:
        with lock:
            record = records.get(id(evidence))
        if record is None or record[0]() is not evidence:
            raise InvalidRealEvidence(
                "probative evidence was not emitted by a validated factory"
            )
        if record[1] is not evidence._capability:
            raise InvalidRealEvidence("probative issuance capability mismatch")
        if record[2] != _provenance(evidence) or record[3] != evidence.digest:
            raise InvalidRealEvidence("probative issuance record no longer matches evidence")

    return register, require


_register_probative_issuance, _require_registered_probative_issuance = (
    _create_issuance_registry()
)


@dataclass(frozen=True)
class _EvidenceBase:
    precision_bits: int
    backend_id: str
    authorization_digest: str
    runtime_code_digest: str
    review_chain_digest: str
    probative: bool
    parent_evidence_hashes: tuple[str, ...]
    digest: str
    _capability: object = field(default=None, init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        permit = _CONSTRUCTION_PERMIT.get()
        if permit is None:
            raise InvalidRealEvidence("real evidence requires an active factory issuance")
        actual_provenance = (
            self.backend_id,
            self.authorization_digest,
            self.runtime_code_digest,
            self.review_chain_digest,
        )
        if self.probative is not permit.probative or actual_provenance != permit.provenance:
            raise InvalidRealEvidence("evidence does not match its factory issuance permit")
        object.__setattr__(self, "_capability", permit.capability)
        if self.precision_bits < 1 or not self.backend_id:
            raise InvalidRealEvidence("evidence precision and backend id are required")
        for value in (
            self.authorization_digest,
            self.runtime_code_digest,
            self.review_chain_digest,
            self.digest,
            *self.parent_evidence_hashes,
        ):
            if not _sha256(value):
                raise InvalidRealEvidence("evidence contains an invalid sha256")


@dataclass(frozen=True)
class RealCompletedL3PointEvidence(_EvidenceBase):
    value: ComplexBallRecord
    segment_id: str = ""


@dataclass(frozen=True)
class RealSegmentImageEvidence(_EvidenceBase):
    value: ComplexBallRecord
    segment_id: str
    mechanism: str
    entire_segment_covered: bool


@dataclass(frozen=True)
class RealHalfPlaneEvidence(_EvidenceBase):
    segment: RealSegmentImageEvidence
    rotation_real: str
    rotation_imag: str
    rotated_real_lower: str

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.parent_evidence_hashes != (self.segment.digest,):
            raise InvalidRealEvidence("half-plane parent identity mismatch")
        if _decimal(self.rotated_real_lower) <= 0:
            raise InvalidRealEvidence("half-plane separation must be strict")


@dataclass(frozen=True)
class RealArgumentIncrementEvidence(_EvidenceBase):
    half_plane: RealHalfPlaneEvidence
    delta_ball: RealBallRecord

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.parent_evidence_hashes != (self.half_plane.digest,):
            raise InvalidRealEvidence("argument increment parent identity mismatch")


@dataclass(frozen=True)
class RealWindingEvidence(_EvidenceBase):
    increments: tuple[RealArgumentIncrementEvidence, ...]
    winding_ball: RealBallRecord
    winding_number: int

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.winding_number < 0:
            raise InvalidRealEvidence("winding number must be nonnegative")
        if self.parent_evidence_hashes != tuple(item.digest for item in self.increments):
            raise InvalidRealEvidence("winding parent identity mismatch")


_REAL_EVIDENCE_TYPES = (
    RealCompletedL3PointEvidence,
    RealSegmentImageEvidence,
    RealHalfPlaneEvidence,
    RealArgumentIncrementEvidence,
    RealWindingEvidence,
)


def _provenance(evidence: _EvidenceBase) -> tuple[str, str, str, str]:
    return (
        evidence.backend_id,
        evidence.authorization_digest,
        evidence.runtime_code_digest,
        evidence.review_chain_digest,
    )


def _expected_digest(evidence: _EvidenceBase) -> str:
    base = {
        "precision_bits": evidence.precision_bits,
        "backend_id": evidence.backend_id,
        "authorization_digest": evidence.authorization_digest,
        "runtime_code_digest": evidence.runtime_code_digest,
        "review_chain_digest": evidence.review_chain_digest,
        "probative": evidence.probative,
        "parent_evidence_hashes": evidence.parent_evidence_hashes,
    }
    if isinstance(evidence, RealCompletedL3PointEvidence):
        payload = {
            "value": asdict(evidence.value),
            "segment_id": evidence.segment_id,
        }
    elif isinstance(evidence, RealSegmentImageEvidence):
        payload = {
            "value": asdict(evidence.value),
            "segment_id": evidence.segment_id,
            "mechanism": evidence.mechanism,
        }
    elif isinstance(evidence, RealHalfPlaneEvidence):
        payload = {
            "segment": evidence.segment.digest,
            "rotation_real": evidence.rotation_real,
            "rotation_imag": evidence.rotation_imag,
            "rotated_real_lower": evidence.rotated_real_lower,
        }
    elif isinstance(evidence, RealArgumentIncrementEvidence):
        payload = {
            "half_plane": evidence.half_plane.digest,
            "delta": asdict(evidence.delta_ball),
        }
    elif isinstance(evidence, RealWindingEvidence):
        payload = {
            "increments": tuple(item.digest for item in evidence.increments),
            "winding_ball": asdict(evidence.winding_ball),
            "winding_number": evidence.winding_number,
        }
    else:
        raise InvalidRealEvidence("unsupported real evidence type")
    return _digest({**base, **payload})


def _require_evidence_chain(
    evidence: _EvidenceBase,
    *,
    expected_provenance: tuple[str, str, str, str],
    expected_probative: bool,
    active: set[int] | None = None,
) -> None:
    if not isinstance(evidence, _REAL_EVIDENCE_TYPES):
        raise InvalidRealEvidence("unsupported parent evidence type")
    if evidence.probative is not expected_probative:
        raise InvalidRealEvidence("parent evidence has incompatible probative status")
    if _provenance(evidence) != expected_provenance:
        raise InvalidRealEvidence("parent evidence has different sealed provenance")
    if expected_probative:
        _require_registered_probative_issuance(evidence)
    if evidence.digest != _expected_digest(evidence):
        raise InvalidRealEvidence("evidence digest does not match its content")

    current_active = active if active is not None else set()
    identity = id(evidence)
    if identity in current_active:
        raise InvalidRealEvidence("evidence ancestry contains a cycle")
    current_active.add(identity)
    try:
        if isinstance(evidence, (RealCompletedL3PointEvidence, RealSegmentImageEvidence)):
            if evidence.parent_evidence_hashes:
                raise InvalidRealEvidence("root evidence cannot declare parents")
            if isinstance(evidence, RealSegmentImageEvidence) and (
                evidence.mechanism != "whole_rectangular_complex_ball"
                or evidence.entire_segment_covered is not True
            ):
                raise InvalidRealEvidence("segment evidence is not a whole-segment enclosure")
            return

        if isinstance(evidence, RealHalfPlaneEvidence):
            parents = (evidence.segment,)
        elif isinstance(evidence, RealArgumentIncrementEvidence):
            parents = (evidence.half_plane,)
        else:
            parents = evidence.increments

        if evidence.parent_evidence_hashes != tuple(parent.digest for parent in parents):
            raise InvalidRealEvidence("evidence parent hashes do not match its ancestry")
        for parent in parents:
            _require_evidence_chain(
                parent,
                expected_provenance=expected_provenance,
                expected_probative=expected_probative,
                active=current_active,
            )
    finally:
        current_active.remove(identity)


def require_probative_evidence_chain(evidence: _EvidenceBase) -> _EvidenceBase:
    if not isinstance(evidence, _REAL_EVIDENCE_TYPES) or evidence.probative is not True:
        raise InvalidRealEvidence(
            "probative evidence requires a fully validated ancestry"
        )
    _require_evidence_chain(
        evidence,
        expected_provenance=_provenance(evidence),
        expected_probative=True,
    )
    return evidence


class RealEvidenceFactory:
    def __init__(self, backend_id: str, authorization_digest: str, runtime_code_digest: str):
        if not backend_id or not _sha256(authorization_digest) or not _sha256(runtime_code_digest):
            raise InvalidRealEvidence("factory provenance is invalid")
        self.backend_id = backend_id
        self.authorization_digest = authorization_digest
        self.runtime_code_digest = runtime_code_digest
        self.review_chain_digest = "0" * 64
        self.probative = False
        self._validated_provenance = None
        self._issuer_capability = object()

    @classmethod
    def from_authorization(
        cls,
        authorization: ExecutionAuthorization,
        *,
        backend_id: str,
    ) -> "RealEvidenceFactory":
        provenance = issue_evidence_provenance(
            authorization,
            backend_id=backend_id,
        )
        factory = cls(
            provenance.backend_id,
            provenance.authorization_digest,
            provenance.runtime_code_digest,
        )
        factory.review_chain_digest = provenance.review_chain_digest
        factory.probative = True
        factory._validated_provenance = provenance
        return factory

    def _require_owned(self, evidence: _EvidenceBase) -> None:
        if self._validated_provenance is None:
            expected_provenance = (
                self.backend_id,
                self.authorization_digest,
                self.runtime_code_digest,
                "0" * 64,
            )
            expected_probative = False
        else:
            provenance = require_validated_evidence_provenance(
                self._validated_provenance
            )
            expected_provenance = (
                provenance.backend_id,
                provenance.authorization_digest,
                provenance.runtime_code_digest,
                provenance.review_chain_digest,
            )
            expected_probative = True
        _require_evidence_chain(
            evidence,
            expected_provenance=expected_provenance,
            expected_probative=expected_probative,
        )

    def _issuance_identity(self) -> tuple[tuple[str, str, str, str], bool]:
        if self._validated_provenance is None:
            return (
                (
                    self.backend_id,
                    self.authorization_digest,
                    self.runtime_code_digest,
                    "0" * 64,
                ),
                False,
            )
        provenance = require_validated_evidence_provenance(
            self._validated_provenance
        )
        return (
            (
                provenance.backend_id,
                provenance.authorization_digest,
                provenance.runtime_code_digest,
                provenance.review_chain_digest,
            ),
            True,
        )

    def _construct(self, evidence_type, **values):
        provenance, probative = self._issuance_identity()
        permit = _ConstructionPermit(
            capability=self._issuer_capability,
            probative=probative,
            provenance=provenance,
        )
        token = _CONSTRUCTION_PERMIT.set(permit)
        try:
            evidence = evidence_type(**values)
        finally:
            _CONSTRUCTION_PERMIT.reset(token)
        if probative:
            _register_probative_issuance(evidence, self._issuer_capability)
        return evidence

    def _common(self, precision_bits: int, parents: tuple[str, ...], payload: dict) -> dict:
        if self._validated_provenance is None:
            backend_id = self.backend_id
            authorization_digest = self.authorization_digest
            runtime_code_digest = self.runtime_code_digest
            review_chain_digest = "0" * 64
            probative = False
        else:
            provenance = require_validated_evidence_provenance(
                self._validated_provenance
            )
            backend_id = provenance.backend_id
            authorization_digest = provenance.authorization_digest
            runtime_code_digest = provenance.runtime_code_digest
            review_chain_digest = provenance.review_chain_digest
            probative = True
        base = {
            "precision_bits": precision_bits,
            "backend_id": backend_id,
            "authorization_digest": authorization_digest,
            "runtime_code_digest": runtime_code_digest,
            "review_chain_digest": review_chain_digest,
            "probative": probative,
            "parent_evidence_hashes": parents,
        }
        return {**base, "digest": _digest({**base, **payload})}

    def completed_l3_point(self, value: ComplexBallRecord, *, precision_bits: int,
                           segment_id: str = "") -> RealCompletedL3PointEvidence:
        common = self._common(precision_bits, (), {"value": asdict(value), "segment_id": segment_id})
        return self._construct(
            RealCompletedL3PointEvidence,
            value=value,
            segment_id=segment_id,
            **common,
        )

    def segment_image(self, *, value: ComplexBallRecord, segment_id: str,
                      precision_bits: int) -> RealSegmentImageEvidence:
        if not segment_id:
            raise InvalidRealEvidence("segment id is required")
        payload = {"value": asdict(value), "segment_id": segment_id,
                   "mechanism": "whole_rectangular_complex_ball"}
        common = self._common(precision_bits, (), payload)
        return self._construct(
            RealSegmentImageEvidence,
            value=value, segment_id=segment_id,
            mechanism="whole_rectangular_complex_ball",
            entire_segment_covered=True, **common,
        )

    def half_plane(self, *, segment: RealSegmentImageEvidence,
                   rotation_real: str, rotation_imag: str,
                   rotated_real_lower: str,
                   claimed_parent_hash: str | None = None) -> RealHalfPlaneEvidence:
        self._require_owned(segment)
        parent = claimed_parent_hash or segment.digest
        common = self._common(
            segment.precision_bits, (parent,),
            {"segment": segment.digest, "rotation_real": rotation_real,
             "rotation_imag": rotation_imag, "rotated_real_lower": rotated_real_lower},
        )
        return self._construct(
            RealHalfPlaneEvidence,
            segment=segment, rotation_real=rotation_real,
            rotation_imag=rotation_imag,
            rotated_real_lower=rotated_real_lower, **common,
        )

    def argument_increment(self, half_plane: RealHalfPlaneEvidence,
                           lower: str, upper: str) -> RealArgumentIncrementEvidence:
        self._require_owned(half_plane)
        delta = RealBallRecord(lower, upper)
        common = self._common(
            half_plane.precision_bits, (half_plane.digest,),
            {"half_plane": half_plane.digest, "delta": asdict(delta)},
        )
        return self._construct(
            RealArgumentIncrementEvidence,
            half_plane=half_plane,
            delta_ball=delta,
            **common,
        )

    def winding(self, increments: tuple[RealArgumentIncrementEvidence, ...],
                winding_ball: RealBallRecord, winding_number: int) -> RealWindingEvidence:
        if not increments:
            raise InvalidRealEvidence("winding requires increments")
        for increment in increments:
            self._require_owned(increment)
        if len({item.precision_bits for item in increments}) != 1:
            raise InvalidRealEvidence("winding increments use mixed precision")
        parents = tuple(item.digest for item in increments)
        precision = increments[0].precision_bits
        common = self._common(
            precision, parents,
            {"increments": parents, "winding_ball": asdict(winding_ball),
             "winding_number": winding_number},
        )
        return self._construct(
            RealWindingEvidence,
            increments=increments, winding_ball=winding_ball,
            winding_number=winding_number, **common,
        )
