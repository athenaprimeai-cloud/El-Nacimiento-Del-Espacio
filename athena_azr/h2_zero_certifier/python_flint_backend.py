from __future__ import annotations

import hashlib
import json
import sys
from contextlib import contextmanager
from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation
from types import MappingProxyType, ModuleType
from typing import Any, Iterator, Mapping

from .authorization import ExecutionAuthorization, ExecutionNotAuthorized
from .chi3_function import CHI3_METADATA, validate_chi3_metadata
from .winding_certifier import parse_canonical_exact_endpoint


FLINT_REAL_IMPORT_ATTEMPTED = False

EXPECTED_PYTHON_FLINT_VERSION = "0.8.0"
EXPECTED_FLINT_NATIVE_VERSION = "3.3.1"
CRITICAL_HASH_FIELDS = (
    "python_executable_sha256",
    "libflint_sha256",
    "arb_extension_sha256",
    "acb_extension_sha256",
    "dirichlet_extension_sha256",
)
FAILURE_STATES = (
    "authorization_missing",
    "runtime_missing",
    "runtime_mismatch",
    "backend_version_mismatch",
    "runtime_hash_mismatch",
    "character_metadata_mismatch",
    "effective_precision_below_request",
    "precision_context_not_restored",
    "precision_context_unavailable",
    "noncanonical_exact_input",
    "float_input_forbidden",
    "whole_box_semantics_missing",
    "nonfinite_ball",
    "origin_not_excluded",
    "principal_log_branch_not_certified",
    "native_L_semantics_unavailable",
    "hurwitz_control_unavailable",
    "parent_evidence_mismatch",
    "scope_or_semantic_leak",
)


class RealBackendFailure(RuntimeError):
    """Deterministic closed failure for the L3 real-backend adapter."""

    def __init__(self, state: str, message: str | None = None) -> None:
        if state not in FAILURE_STATES:
            state = "scope_or_semantic_leak"
        self.state = state
        super().__init__(message or state)


def _is_sha256(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def _canonicalize(value: Any) -> Any:
    if hasattr(value, "evidence_payload"):
        return _canonicalize(value.evidence_payload())
    if isinstance(value, Mapping):
        return {str(key): _canonicalize(value[key]) for key in sorted(value)}
    if isinstance(value, tuple):
        return [_canonicalize(item) for item in value]
    if isinstance(value, list):
        return [_canonicalize(item) for item in value]
    if isinstance(value, (str, int, bool)) or value is None:
        return value
    if isinstance(value, Decimal):
        return str(value)
    raise RealBackendFailure(
        "scope_or_semantic_leak",
        "evidence payload cannot depend on Python object repr",
    )


def _canonical_json(payload: Mapping[str, Any]) -> str:
    return (
        json.dumps(
            _canonicalize(payload),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
        + "\n"
    )


def _digest_payload(payload: Mapping[str, Any]) -> str:
    return hashlib.sha256(_canonical_json(payload).encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class BackendOperationEvidence:
    operation_id: str
    operation: str
    backend_id: str
    runtime_seal_id: str
    precision_bits: int
    input_digest: str
    output_digest: str
    parent_evidence_hashes: tuple[str, ...]
    whole_box: bool
    finite: bool
    zero_relation: str
    branch_relation: str
    status: str
    details: Mapping[str, Any] = field(default_factory=dict)
    digest: str = ""

    def __post_init__(self) -> None:
        if self.precision_bits < 1 or not self.operation_id or not self.operation:
            raise RealBackendFailure("scope_or_semantic_leak", "operation evidence is malformed")
        if not _is_sha256(self.runtime_seal_id):
            raise RealBackendFailure("runtime_hash_mismatch", "runtime seal id is malformed")
        for value in (self.input_digest, self.output_digest, *self.parent_evidence_hashes):
            if not _is_sha256(value):
                raise RealBackendFailure("parent_evidence_mismatch", "evidence hash is malformed")
        if self.digest and not _is_sha256(self.digest):
            raise RealBackendFailure("parent_evidence_mismatch", "evidence digest is malformed")
        object.__setattr__(self, "details", MappingProxyType(dict(self.details)))
        if not self.digest:
            object.__setattr__(self, "digest", self.expected_digest())

    def payload_without_digest(self) -> Mapping[str, Any]:
        return {
            "backend_id": self.backend_id,
            "branch_relation": self.branch_relation,
            "details": dict(self.details),
            "finite": self.finite,
            "input_digest": self.input_digest,
            "operation": self.operation,
            "operation_id": self.operation_id,
            "output_digest": self.output_digest,
            "parent_evidence_hashes": self.parent_evidence_hashes,
            "precision_bits": self.precision_bits,
            "runtime_seal_id": self.runtime_seal_id,
            "status": self.status,
            "whole_box": self.whole_box,
            "zero_relation": self.zero_relation,
        }

    def expected_digest(self) -> str:
        return _digest_payload(self.payload_without_digest())

    def canonical_json(self) -> str:
        return _canonical_json({**self.payload_without_digest(), "digest": self.digest})


@dataclass(frozen=True)
class BackendBall:
    value: Any
    evidence: BackendOperationEvidence


@dataclass(frozen=True)
class BackendCharacter:
    raw: Any
    metadata: Mapping[str, str]
    evidence: BackendOperationEvidence

    def __post_init__(self) -> None:
        object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))


def _ctx_precision(ctx: object) -> int | None:
    for name in ("precision_bits", "prec"):
        value = getattr(ctx, name, None)
        if isinstance(value, int):
            return value
    return None


def _positive_decimal(value: object) -> bool:
    try:
        return Decimal(str(value)) > 0
    except (InvalidOperation, ValueError):
        return False


class PythonFlintBackend:
    """Lazy python-flint adapter with fake-runtime tests and closed real gates."""

    HURWITZ_CHANNEL_IS_CONTROL_ONLY = True
    NATIVE_AND_HURWITZ_INDEPENDENT = False

    def __init__(
        self,
        *,
        backend_id: str = "python-flint-l3-adapter",
        runtime: ModuleType | object | None = None,
        runtime_seal: Mapping[str, str] | None = None,
        expected_binary_hashes: Mapping[str, str] | None = None,
        fake_runtime: bool = False,
    ) -> None:
        self.backend_id = backend_id
        self._flint: ModuleType | object | None = runtime
        self._fake_runtime = fake_runtime
        self._runtime_seal = dict(runtime_seal or {})
        self._expected_binary_hashes = dict(expected_binary_hashes or {})
        self._runtime_seal_id: str | None = None
        self._operation_index = 0

    @classmethod
    def from_fake_runtime(
        cls,
        runtime: object,
        *,
        runtime_seal: Mapping[str, str],
        expected_binary_hashes: Mapping[str, str],
        backend_id: str = "python-flint-l3-adapter-fake-only",
    ) -> "PythonFlintBackend":
        return cls(
            backend_id=backend_id,
            runtime=runtime,
            runtime_seal=runtime_seal,
            expected_binary_hashes=expected_binary_hashes,
            fake_runtime=True,
        )

    @property
    def initialized(self) -> bool:
        return self._flint is not None

    @property
    def runtime_seal_id(self) -> str:
        if self._runtime_seal_id is None:
            if not self._runtime_seal:
                raise RealBackendFailure("runtime_missing", "runtime seal is missing")
            self._runtime_seal_id = _digest_payload(dict(self._runtime_seal))
        return self._runtime_seal_id

    def initialize(self, *, authorization: ExecutionAuthorization) -> None:
        global FLINT_REAL_IMPORT_ATTEMPTED
        if not isinstance(authorization, ExecutionAuthorization) or not authorization.execution_authorized:
            raise ExecutionNotAuthorized("FLINT initialization requires valid 006F authorization")
        FLINT_REAL_IMPORT_ATTEMPTED = True
        import flint  # type: ignore[import-not-found]  # lazy by design

        self._flint = flint
        self._fake_runtime = False

    def _require_runtime(self) -> ModuleType | object:
        if self._flint is None:
            raise ExecutionNotAuthorized("real FLINT mathematics requires 006F")
        return self._flint

    def metadata(self) -> Mapping[str, str]:
        runtime = self._require_runtime()
        if self._runtime_seal:
            return MappingProxyType(
                {
                    "python_flint": self._runtime_seal.get(
                        "python_flint_distribution_version", "unknown"
                    ),
                    "flint_module": self._runtime_seal.get("flint_module_version", "unknown"),
                    "FLINT_native": self._runtime_seal.get("FLINT_native_version", "unknown"),
                }
            )
        return {"python_flint": str(getattr(runtime, "__version__", "unknown"))}

    def validate_runtime_seal(self) -> Mapping[str, str]:
        runtime = self._require_runtime()
        seal = dict(self._runtime_seal)
        if not seal:
            raise RealBackendFailure("runtime_missing", "runtime seal is missing")
        expected_versions = {
            "python_flint_distribution_version": EXPECTED_PYTHON_FLINT_VERSION,
            "flint_module_version": EXPECTED_PYTHON_FLINT_VERSION,
            "FLINT_native_version": EXPECTED_FLINT_NATIVE_VERSION,
        }
        for key, expected in expected_versions.items():
            if seal.get(key) != expected:
                raise RealBackendFailure("backend_version_mismatch", f"{key} mismatch")
        runtime_version = getattr(runtime, "__version__", EXPECTED_PYTHON_FLINT_VERSION)
        if str(runtime_version) != seal["flint_module_version"]:
            raise RealBackendFailure("runtime_mismatch", "runtime module version mismatch")
        for key in CRITICAL_HASH_FIELDS:
            actual = seal.get(key)
            if not _is_sha256(actual):
                raise RealBackendFailure("runtime_hash_mismatch", f"{key} missing or invalid")
            expected_hash = self._expected_binary_hashes.get(key)
            if expected_hash is not None and actual != expected_hash:
                raise RealBackendFailure("runtime_hash_mismatch", f"{key} mismatch")
        self._runtime_seal_id = _digest_payload(seal)
        return MappingProxyType(seal)

    @contextmanager
    def precision_context(self, precision_bits: int) -> Iterator[Mapping[str, int]]:
        runtime = self._require_runtime()
        self.validate_runtime_seal()
        ctx = getattr(runtime, "ctx", None)
        workprec = getattr(ctx, "workprec", None)
        if ctx is None or not callable(workprec):
            raise RealBackendFailure("precision_context_unavailable")
        previous = _ctx_precision(ctx)
        manager = workprec(precision_bits)
        if not hasattr(manager, "__enter__") or not hasattr(manager, "__exit__"):
            raise RealBackendFailure("precision_context_unavailable")
        manager.__enter__()
        try:
            effective = _ctx_precision(ctx)
            if effective is None:
                raise RealBackendFailure("precision_context_unavailable")
            if effective < precision_bits:
                raise RealBackendFailure("effective_precision_below_request")
            yield {
                "previous_precision_bits": previous if previous is not None else -1,
                "requested_precision_bits": precision_bits,
                "effective_precision_bits": effective,
            }
        finally:
            exc_info = sys.exc_info()
            manager.__exit__(*exc_info)
            restored = _ctx_precision(ctx)
            if previous is not None and restored != previous:
                raise RealBackendFailure("precision_context_not_restored")

    def _next_operation_id(self, operation: str) -> str:
        self._operation_index += 1
        return f"006H16-{self._operation_index:04d}-{operation}"

    def _validate_parent(self, parent: BackendBall | BackendCharacter) -> str:
        evidence = parent.evidence
        if evidence.digest != evidence.expected_digest():
            raise RealBackendFailure("parent_evidence_mismatch")
        return evidence.digest

    def _parent_hashes(self, *parents: object) -> tuple[str, ...]:
        hashes: list[str] = []
        for parent in parents:
            if isinstance(parent, (BackendBall, BackendCharacter)):
                hashes.append(self._validate_parent(parent))
        return tuple(hashes)

    def _evidence(
        self,
        *,
        operation: str,
        precision_bits: int,
        inputs: Mapping[str, Any],
        output: Mapping[str, Any],
        parents: tuple[BackendBall | BackendCharacter, ...] = (),
        whole_box: bool = False,
        finite: bool = True,
        zero_relation: str = "not_evaluated",
        branch_relation: str = "not_evaluated",
        status: str = "pass",
        details: Mapping[str, Any] | None = None,
    ) -> BackendOperationEvidence:
        return BackendOperationEvidence(
            operation_id=self._next_operation_id(operation),
            operation=operation,
            backend_id=self.backend_id,
            runtime_seal_id=self.runtime_seal_id,
            precision_bits=precision_bits,
            input_digest=_digest_payload(inputs),
            output_digest=_digest_payload(output),
            parent_evidence_hashes=self._parent_hashes(*parents),
            whole_box=whole_box,
            finite=finite,
            zero_relation=zero_relation,
            branch_relation=branch_relation,
            status=status,
            details=dict(details or {}),
        )

    def _is_finite_value(self, value: object) -> bool:
        runtime = self._require_runtime()
        checker = getattr(runtime, "is_finite", None)
        if callable(checker):
            return bool(checker(value))
        return bool(getattr(value, "finite", False))

    def _wrap_ball(
        self,
        *,
        operation: str,
        raw_value: object,
        precision_bits: int,
        inputs: Mapping[str, Any],
        parents: tuple[BackendBall | BackendCharacter, ...] = (),
        whole_box: bool = False,
        zero_relation: str = "not_evaluated",
        branch_relation: str = "not_evaluated",
        details: Mapping[str, Any] | None = None,
    ) -> BackendBall:
        finite = self._is_finite_value(raw_value)
        if not finite:
            raise RealBackendFailure("nonfinite_ball", f"{operation} produced a nonfinite ball")
        evidence = self._evidence(
            operation=operation,
            precision_bits=precision_bits,
            inputs=inputs,
            output={"value": raw_value},
            parents=parents,
            whole_box=whole_box,
            finite=True,
            zero_relation=zero_relation,
            branch_relation=branch_relation,
            details=details,
        )
        return BackendBall(raw_value, evidence)

    def _require_backend_ball(self, value: object, *, whole_box: bool | None = None) -> BackendBall:
        if not isinstance(value, BackendBall):
            raise RealBackendFailure("native_L_semantics_unavailable", "input is not adapter-wrapped")
        if whole_box is True and value.evidence.whole_box is not True:
            raise RealBackendFailure("whole_box_semantics_missing")
        self._validate_parent(value)
        return value

    def construct_exact_real(self, endpoint: object, *, precision_bits: int) -> BackendBall:
        if isinstance(endpoint, float):
            raise RealBackendFailure("float_input_forbidden")
        if not isinstance(endpoint, str):
            raise RealBackendFailure("noncanonical_exact_input")
        try:
            exact = parse_canonical_exact_endpoint(endpoint)
        except ValueError as exc:
            raise RealBackendFailure("noncanonical_exact_input", str(exc)) from exc
        runtime = self._require_runtime()
        with self.precision_context(precision_bits):
            if "/" in endpoint:
                raw = runtime.arb(runtime.fmpq(exact.numerator, exact.denominator))
                kind = "reduced_noninteger_rational"
            elif "." in endpoint:
                raw = runtime.arb(endpoint)
                kind = "canonical_decimal"
            else:
                raw = runtime.arb(int(endpoint))
                kind = "integer"
        return self._wrap_ball(
            operation="construct_exact_real",
            raw_value=raw,
            precision_bits=precision_bits,
            inputs={"endpoint": endpoint, "kind": kind},
            details={"canonical_fraction": f"{exact.numerator}/{exact.denominator}", "kind": kind},
        )

    def construct_real_interval(self, lower: object, upper: object, *, precision_bits: int) -> BackendBall:
        if not isinstance(lower, str) or not isinstance(upper, str):
            raise RealBackendFailure("noncanonical_exact_input")
        try:
            low = parse_canonical_exact_endpoint(lower)
            high = parse_canonical_exact_endpoint(upper)
        except ValueError as exc:
            raise RealBackendFailure("noncanonical_exact_input", str(exc)) from exc
        if low > high:
            raise RealBackendFailure("noncanonical_exact_input", "interval lower exceeds upper")
        lower_ball = self.construct_exact_real(lower, precision_bits=precision_bits)
        upper_ball = self.construct_exact_real(upper, precision_bits=precision_bits)
        runtime = self._require_runtime()
        with self.precision_context(precision_bits):
            raw = runtime.real_interval(lower_ball.value, upper_ball.value)
        return self._wrap_ball(
            operation="construct_real_interval",
            raw_value=raw,
            precision_bits=precision_bits,
            inputs={"lower": lower, "upper": upper},
            parents=(lower_ball, upper_ball),
            details={
                "lower_fraction": f"{low.numerator}/{low.denominator}",
                "upper_fraction": f"{high.numerator}/{high.denominator}",
            },
        )

    def construct_complex_box(
        self,
        real_lower: object,
        real_upper: object,
        imag_lower: object,
        imag_upper: object,
        *,
        precision_bits: int,
    ) -> BackendBall:
        real = self.construct_real_interval(real_lower, real_upper, precision_bits=precision_bits)
        imag = self.construct_real_interval(imag_lower, imag_upper, precision_bits=precision_bits)
        runtime = self._require_runtime()
        with self.precision_context(precision_bits):
            raw = runtime.complex_box(real.value, imag.value)
        return self._wrap_ball(
            operation="construct_complex_box",
            raw_value=raw,
            precision_bits=precision_bits,
            inputs={
                "imag_lower": imag_lower,
                "imag_upper": imag_upper,
                "real_lower": real_lower,
                "real_upper": real_upper,
            },
            parents=(real, imag),
            whole_box=True,
            details={
                "entire_segment_covered": True,
                "imag_lower": imag_lower,
                "imag_upper": imag_upper,
                "real_lower": real_lower,
                "real_upper": real_upper,
                "whole_box_evaluation": True,
            },
        )

    def pi_ball(self, *, precision_bits: int) -> BackendBall:
        runtime = self._require_runtime()
        with self.precision_context(precision_bits):
            raw = runtime.pi()
        return self._wrap_ball(
            operation="pi_ball",
            raw_value=raw,
            precision_bits=precision_bits,
            inputs={"constant": "pi"},
            details={"precondition": "positive_real_constant"},
        )

    def real_log(self, value: BackendBall, *, precision_bits: int) -> BackendBall:
        value = self._require_backend_ball(value)
        runtime = self._require_runtime()
        with self.precision_context(precision_bits):
            raw = runtime.real_log(value.value)
        return self._wrap_ball(
            operation="real_log",
            raw_value=raw,
            precision_bits=precision_bits,
            inputs={"value": value.evidence.digest},
            parents=(value,),
            branch_relation="positive_real_log",
        )

    def complex_exp(self, value: BackendBall, *, precision_bits: int) -> BackendBall:
        value = self._require_backend_ball(value)
        runtime = self._require_runtime()
        with self.precision_context(precision_bits):
            raw = runtime.complex_exp(value.value)
        return self._wrap_ball(
            operation="complex_exp",
            raw_value=raw,
            precision_bits=precision_bits,
            inputs={"value": value.evidence.digest},
            parents=(value,),
        )

    def complex_gamma(self, value: BackendBall, *, precision_bits: int) -> BackendBall:
        value = self._require_backend_ball(value)
        runtime = self._require_runtime()
        with self.precision_context(precision_bits):
            raw = runtime.complex_gamma(value.value)
        return self._wrap_ball(
            operation="complex_gamma",
            raw_value=raw,
            precision_bits=precision_bits,
            inputs={"value": value.evidence.digest},
            parents=(value,),
        )

    def complex_multiply(self, *values: BackendBall, precision_bits: int) -> BackendBall:
        if not values:
            raise RealBackendFailure("scope_or_semantic_leak", "multiply requires inputs")
        wrapped = tuple(self._require_backend_ball(value) for value in values)
        runtime = self._require_runtime()
        with self.precision_context(precision_bits):
            raw = runtime.complex_multiply(*(value.value for value in wrapped))
        return self._wrap_ball(
            operation="complex_multiply",
            raw_value=raw,
            precision_bits=precision_bits,
            inputs={"values": [value.evidence.digest for value in wrapped]},
            parents=wrapped,
        )

    def complex_subtract(self, left: BackendBall, right: BackendBall, *, precision_bits: int) -> BackendBall:
        left = self._require_backend_ball(left)
        right = self._require_backend_ball(right)
        runtime = self._require_runtime()
        with self.precision_context(precision_bits):
            raw = runtime.complex_subtract(left.value, right.value)
        return self._wrap_ball(
            operation="complex_subtract",
            raw_value=raw,
            precision_bits=precision_bits,
            inputs={"left": left.evidence.digest, "right": right.evidence.digest},
            parents=(left, right),
        )

    def complex_divide(
        self, numerator: BackendBall, denominator: BackendBall, *, precision_bits: int
    ) -> BackendBall:
        numerator = self._require_backend_ball(numerator)
        denominator = self._require_backend_ball(denominator)
        runtime = self._require_runtime()
        with self.precision_context(precision_bits):
            raw = runtime.complex_divide(numerator.value, denominator.value)
        return self._wrap_ball(
            operation="complex_divide",
            raw_value=raw,
            precision_bits=precision_bits,
            inputs={"denominator": denominator.evidence.digest, "numerator": numerator.evidence.digest},
            parents=(numerator, denominator),
        )

    def real_ball_sum(self, values: tuple[BackendBall, ...], *, precision_bits: int) -> BackendBall:
        wrapped = tuple(self._require_backend_ball(value) for value in values)
        runtime = self._require_runtime()
        with self.precision_context(precision_bits):
            raw = runtime.real_ball_sum([value.value for value in wrapped])
        return self._wrap_ball(
            operation="real_ball_sum",
            raw_value=raw,
            precision_bits=precision_bits,
            inputs={"values": [value.evidence.digest for value in wrapped]},
            parents=wrapped,
        )

    def abs_lower(self, value: BackendBall, *, precision_bits: int) -> BackendBall:
        value = self._require_backend_ball(value)
        runtime = self._require_runtime()
        with self.precision_context(precision_bits):
            raw = runtime.abs_lower(value.value)
        return self._wrap_ball(
            operation="abs_lower",
            raw_value=raw,
            precision_bits=precision_bits,
            inputs={"value": value.evidence.digest},
            parents=(value,),
            zero_relation="absolute_value_lower_bound",
        )

    def contains_zero(self, value: BackendBall, *, precision_bits: int) -> Mapping[str, Any]:
        value = self._require_backend_ball(value)
        runtime = self._require_runtime()
        with self.precision_context(precision_bits):
            checker = getattr(runtime, "contains_zero", None)
            result = checker(value.value) if callable(checker) else None
        if result is not True and result is not False:
            raise RealBackendFailure("origin_not_excluded", "zero containment witness is missing")
        evidence = self._evidence(
            operation="contains_zero",
            precision_bits=precision_bits,
            inputs={"value": value.evidence.digest},
            output={"contains_zero": result},
            parents=(value,),
            zero_relation="contains_zero" if result else "excludes_zero_by_containment",
            details={"contains_zero": result},
        )
        return MappingProxyType({"contains_zero": result, "evidence": evidence})

    def is_finite(self, value: BackendBall) -> bool:
        value = self._require_backend_ball(value)
        return self._is_finite_value(value.value)

    def certify_origin_excluded(self, value: BackendBall, *, precision_bits: int) -> Mapping[str, Any]:
        containment = self.contains_zero(value, precision_bits=precision_bits)
        lower = self.abs_lower(value, precision_bits=precision_bits)
        raw_lower = getattr(lower.value, "abs_lower", None)
        if containment["contains_zero"] is not False or not _positive_decimal(raw_lower):
            raise RealBackendFailure("origin_not_excluded")
        return MappingProxyType(
            {
                "status": "origin_excluded",
                "contains_zero_evidence": containment["evidence"].digest,
                "abs_lower_evidence": lower.evidence.digest,
                "zero_relation": "not contains_zero and abs_lower strictly positive",
            }
        )

    def character_chi3(self, *, precision_bits: int) -> BackendCharacter:
        runtime = self._require_runtime()
        with self.precision_context(precision_bits):
            constructor = getattr(runtime, "dirichlet_char", None)
            if not callable(constructor):
                raise RealBackendFailure("character_metadata_mismatch", "dirichlet_char unavailable")
            raw = constructor(3, 2)
        metadata = dict(getattr(raw, "metadata", {}))
        try:
            validate_chi3_metadata(metadata)
        except (TypeError, ValueError) as exc:
            raise RealBackendFailure("character_metadata_mismatch", str(exc)) from exc
        evidence = self._evidence(
            operation="character_chi3",
            precision_bits=precision_bits,
            inputs={"modulus": 3, "number": 2},
            output={"metadata": metadata},
            details={"constructor": "flint.dirichlet_char(3, 2)"},
        )
        return BackendCharacter(raw, metadata, evidence)

    def chi3_metadata(self) -> Mapping[str, str]:
        return self.character_chi3(precision_bits=1).metadata

    def native_dirichlet_l(
        self,
        input_box: BackendBall,
        *,
        precision_bits: int,
        character: BackendCharacter | None = None,
    ) -> BackendBall:
        input_box = self._require_backend_ball(input_box, whole_box=True)
        if input_box.evidence.precision_bits != precision_bits:
            raise RealBackendFailure("effective_precision_below_request", "input precision mismatch")
        character = character or self.character_chi3(precision_bits=precision_bits)
        try:
            validate_chi3_metadata(character.metadata)
        except ValueError as exc:
            raise RealBackendFailure("character_metadata_mismatch", str(exc)) from exc
        runtime = self._require_runtime()
        acb = getattr(runtime, "acb", None)
        dirichlet_l = getattr(acb, "dirichlet_l", None)
        if not callable(dirichlet_l):
            raise RealBackendFailure("native_L_semantics_unavailable")
        with self.precision_context(precision_bits):
            raw = dirichlet_l(input_box.value, character.raw)
        return self._wrap_ball(
            operation="native_dirichlet_l",
            raw_value=raw,
            precision_bits=precision_bits,
            inputs={"character": dict(character.metadata), "input_box": input_box.evidence.digest},
            parents=(input_box, character),
            whole_box=True,
            details={
                "character_metadata": dict(character.metadata),
                "operation": "native_dirichlet_l",
                "whole_box_requested": True,
            },
        )

    def hurwitz_zeta_candidate(
        self,
        input_box: BackendBall,
        a_endpoint: str,
        *,
        precision_bits: int,
    ) -> BackendBall:
        input_box = self._require_backend_ball(input_box, whole_box=True)
        parameter = self.construct_exact_real(a_endpoint, precision_bits=precision_bits)
        runtime = self._require_runtime()
        acb = getattr(runtime, "acb", None)
        zeta = getattr(acb, "zeta", None)
        if not callable(zeta):
            raise RealBackendFailure("hurwitz_control_unavailable")
        with self.precision_context(precision_bits):
            raw = zeta(input_box.value, parameter.value)
        return self._wrap_ball(
            operation="hurwitz_zeta_candidate",
            raw_value=raw,
            precision_bits=precision_bits,
            inputs={"a": a_endpoint, "input_box": input_box.evidence.digest},
            parents=(input_box, parameter),
            whole_box=True,
            details={"api": "flint.acb.zeta(s, a)"},
        )

    def _hurwitz_power_factor(self, input_box: BackendBall, *, precision_bits: int) -> BackendBall:
        input_box = self._require_backend_ball(input_box, whole_box=True)
        runtime = self._require_runtime()
        builder = getattr(runtime, "hurwitz_power_factor", None)
        if callable(builder):
            with self.precision_context(precision_bits):
                raw = builder(input_box.value)
        else:
            raw = input_box.value
        return self._wrap_ball(
            operation="hurwitz_power_factor",
            raw_value=raw,
            precision_bits=precision_bits,
            inputs={"input_box": input_box.evidence.digest, "factor": "3^(-s)"},
            parents=(input_box,),
            whole_box=True,
            details={"factor": "3^(-s)"},
        )

    def hurwitz_control(self, input_box: BackendBall, *, precision_bits: int) -> BackendBall:
        zeta_one_third = self.hurwitz_zeta_candidate(input_box, "1/3", precision_bits=precision_bits)
        zeta_two_thirds = self.hurwitz_zeta_candidate(input_box, "2/3", precision_bits=precision_bits)
        difference = self.complex_subtract(zeta_one_third, zeta_two_thirds, precision_bits=precision_bits)
        factor = self._hurwitz_power_factor(input_box, precision_bits=precision_bits)
        product = self.complex_multiply(factor, difference, precision_bits=precision_bits)
        return self._wrap_ball(
            operation="hurwitz_control",
            raw_value=product.value,
            precision_bits=precision_bits,
            inputs={"input_box": input_box.evidence.digest},
            parents=(factor, difference),
            whole_box=True,
            details={
                "control_only": True,
                "formula": "3^(-s) * (zeta(s,1/3) - zeta(s,2/3))",
                "native_and_hurwitz_independent": False,
            },
        )

    def gamma_argument(self, input_box: BackendBall, *, precision_bits: int) -> BackendBall:
        input_box = self._require_backend_ball(input_box)
        runtime = self._require_runtime()
        with self.precision_context(precision_bits):
            raw = runtime.affine_half_plus_half(input_box.value)
        return self._wrap_ball(
            operation="gamma_argument",
            raw_value=raw,
            precision_bits=precision_bits,
            inputs={"formula": "(s + 1) / 2", "input_box": input_box.evidence.digest},
            parents=(input_box,),
        )

    def _positive_log_base(self, *, precision_bits: int) -> BackendBall:
        pi_value = self.pi_ball(precision_bits=precision_bits)
        runtime = self._require_runtime()
        builder = getattr(runtime, "power_base_3_over_pi", None)
        if not callable(builder):
            raise RealBackendFailure("scope_or_semantic_leak", "positive 3/pi builder unavailable")
        with self.precision_context(precision_bits):
            raw = builder(pi_value.value)
        base = self._wrap_ball(
            operation="positive_real_3_over_pi",
            raw_value=raw,
            precision_bits=precision_bits,
            inputs={"numerator": 3, "pi": pi_value.evidence.digest},
            parents=(pi_value,),
            branch_relation="positive_real",
            details={"complex_log_forbidden": True},
        )
        return self.real_log(base, precision_bits=precision_bits)

    def completed_lambda3(self, input_box: BackendBall, *, precision_bits: int) -> BackendBall:
        input_box = self._require_backend_ball(input_box, whole_box=True)
        if input_box.evidence.precision_bits != precision_bits:
            raise RealBackendFailure("effective_precision_below_request", "input precision mismatch")
        character = self.character_chi3(precision_bits=precision_bits)
        gamma_arg = self.gamma_argument(input_box, precision_bits=precision_bits)
        log_base = self._positive_log_base(precision_bits=precision_bits)
        power_arg = self.complex_multiply(gamma_arg, log_base, precision_bits=precision_bits)
        power = self.complex_exp(power_arg, precision_bits=precision_bits)
        gamma_factor = self.complex_gamma(gamma_arg, precision_bits=precision_bits)
        l_factor = self.native_dirichlet_l(
            input_box,
            precision_bits=precision_bits,
            character=character,
        )
        product = self.complex_multiply(power, gamma_factor, l_factor, precision_bits=precision_bits)
        return self._wrap_ball(
            operation="completed_lambda3",
            raw_value=product.value,
            precision_bits=precision_bits,
            inputs={"input_box": input_box.evidence.digest},
            parents=(power, gamma_factor, l_factor),
            whole_box=True,
            details={
                "formula": "(3/pi)^((s+1)/2) * Gamma((s+1)/2) * L(s,chi_3)",
                "parent_product_evidence": product.evidence.digest,
            },
        )

    def complex_log_analytic(
        self,
        value: BackendBall,
        *,
        precision_bits: int,
        branch_certificate: Mapping[str, object] | None = None,
    ) -> BackendBall:
        value = self._require_backend_ball(value)
        certificate = dict(branch_certificate or {})
        if (
            certificate.get("origin_excluded") is not True
            or certificate.get("branch_domain_certified") is not True
            or not certificate.get("branch_relation")
        ):
            raise RealBackendFailure("principal_log_branch_not_certified")
        runtime = self._require_runtime()
        acb = getattr(runtime, "acb", None)
        log = getattr(acb, "log", None)
        if not callable(log):
            raise RealBackendFailure("principal_log_branch_not_certified")
        with self.precision_context(precision_bits):
            raw = log(value.value, analytic=True)
        return self._wrap_ball(
            operation="complex_log_analytic",
            raw_value=raw,
            precision_bits=precision_bits,
            inputs={"value": value.evidence.digest},
            parents=(value,),
            branch_relation=str(certificate["branch_relation"]),
            details={"analytic": True},
        )

    def _blocked_until_006f(self):
        if self._flint is None:
            raise ExecutionNotAuthorized("real FLINT mathematics requires 006F")
        raise NotImplementedError("full real FLINT execution is reserved for 006F")

    def zeta_zero(self, index: int, precision_bits: int):
        return self._blocked_until_006f()

    def zeta_count_certificate(self, requested_height: int, precision_bits: int):
        return self._blocked_until_006f()

    def completed_l3_point(self, point, precision_bits: int):
        return self._blocked_until_006f()

    def completed_l3_segment(self, segment, precision_bits: int):
        return self._blocked_until_006f()

    def validate_half_plane(self, segment_certificate, precision_bits: int):
        return self._blocked_until_006f()

    def argument_increment(self, half_plane_certificate, precision_bits: int):
        return self._blocked_until_006f()

    def unique_integer(self, interval_lower, interval_upper):
        return self._blocked_until_006f()

    def l3_box_winding_count(self, box, precision_bits: int):
        return self._blocked_until_006f()

    def l3_critical_line_certified(self, box, precision_bits: int):
        return self._blocked_until_006f()

    def l3_count_certificate(self, requested_height: int, precision_bits: int):
        return self._blocked_until_006f()

    def real_completed_l3_point(self, point, precision_bits: int):
        return self._blocked_until_006f()

    def real_completed_l3_segment(self, segment, precision_bits: int):
        return self._blocked_until_006f()
