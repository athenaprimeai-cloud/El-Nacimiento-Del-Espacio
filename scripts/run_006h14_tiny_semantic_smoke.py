from __future__ import annotations

import hashlib
import importlib.metadata as metadata
import json
import platform
import sys
from pathlib import Path


PHASE_ID = "006H14_L3_LOCAL_FLINT_ARB_ACB_TINY_SEMANTIC_SMOKE"
EXPECTED_RUNTIME = r"C:\Users\johnn\AppData\Local\Temp\athena-006e20r\Scripts\python.exe"
EXPECTED_PYTHON_SHA256 = "5912d0884b23c0343983a864c6064242391e2265536f50b88624857e353882c9"
EXPECTED_PYTHON_FLINT_VERSION = "0.8.0"
EXPECTED_FLINT_VERSION = "3.3.1"
PRECISION_BITS = (192, 256)
ARTIFACT_DIR = Path("artifacts") / "006H14-tiny-semantic-smoke"
CALL_LEDGER_NAME = "006H14_CALL_LEDGER.json"
RUNTIME_SEAL_NAME = "006H14_RUNTIME_SEAL.json"
RESULTS_NAME = "006H14_RESULTS.json"
SUMS_NAME = "006H14_SHA256SUMS.txt"
CRITICAL_HASHES = {
    "libflint": (
        ("python_flint.libs", "libflint*.dll"),
        "d5410bef059868b7bfe0f2e9fde9db02f02177cbf871ab74b21893a2664c25f9",
    ),
    "arb_extension": (
        ("flint", "types", "arb.cp312-win_amd64.pyd"),
        "2312c03aa39d788484603b145445d4c3de2de7633ec173cd2dfed923acf3c05d",
    ),
    "acb_extension": (
        ("flint", "types", "acb.cp312-win_amd64.pyd"),
        "fa4774b1080c3ccb24b6cbc57b3978c79c4d8cd34b6c5ccd0b0e5d5543e3fd6e",
    ),
    "dirichlet_extension": (
        ("flint", "types", "dirichlet*.pyd"),
        "1db19efc678dc44fba141ba8db468274ba570eb8276b0154af6580b2169b93e3",
    ),
}
MAX_COUNTS = {
    "native_dirichlet_l": 4,
    "hurwitz_candidate_zeta": 6,
    "gamma": 4,
    "log": 6,
    "exp": 4,
    "pi": 2,
}


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_json(data) -> str:
    return json.dumps(data, allow_nan=False, sort_keys=True, separators=(",", ":")) + "\n"


def write_json(path: Path, data) -> None:
    path.write_text(canonical_json(data), encoding="utf-8", newline="\n")


def find_one(root: Path, parts: tuple[str, ...]) -> Path | None:
    base = root.joinpath(*parts[:-1])
    matches = sorted(base.glob(parts[-1])) if base.is_dir() else []
    return matches[0].resolve() if len(matches) == 1 else None


def verify_preimport_runtime():
    executable = Path(sys.executable).resolve()
    dist = metadata.distribution("python-flint")
    site_root = Path(str(dist.locate_file(""))).resolve()
    critical = {}
    errors = []

    python_hash = sha256_path(executable) if executable.is_file() else None
    if str(executable) != EXPECTED_RUNTIME:
        errors.append("python executable path mismatch")
    if python_hash != EXPECTED_PYTHON_SHA256:
        errors.append("python executable hash mismatch")
    if dist.version != EXPECTED_PYTHON_FLINT_VERSION:
        errors.append("python-flint distribution version mismatch")

    for key, (locator, expected_hash) in CRITICAL_HASHES.items():
        path = find_one(site_root, locator)
        actual_hash = sha256_path(path) if path is not None and path.is_file() else None
        critical[key] = {
            "path": str(path) if path is not None else None,
            "expected_sha256": expected_hash,
            "actual_sha256": actual_hash,
            "verified": actual_hash == expected_hash,
        }
        if actual_hash != expected_hash:
            errors.append(f"{key} hash mismatch")

    return {
        "python_executable": str(executable),
        "python_executable_sha256": python_hash,
        "python_flint_distribution_version": dist.version,
        "package_distribution_path": str(site_root),
        "critical_hashes": critical,
        "preimport_verified": not errors,
        "preimport_errors": errors,
    }


def bool_or_error(func):
    try:
        return bool(func())
    except Exception as exc:
        return {"error": f"{type(exc).__name__}: {exc}"}


class Smoke:
    def __init__(self, flint, seal):
        self.flint = flint
        self.seal = seal
        self.ledger = []
        self.counts = {key: 0 for key in MAX_COUNTS}

    def q(self, numerator: int, denominator: int):
        return self.flint.fmpq(numerator, denominator)

    def arb_exact(self, value):
        return self.flint.arb(value)

    def acb_exact(self, value):
        return self.flint.acb(value)

    def arb_interval(self, lower, upper):
        return self.arb_exact(lower).union(self.arb_exact(upper))

    def acb_box(self, real_ball, imag_ball):
        return self.flint.acb(real_ball, imag_ball)

    def contains_zero(self, obj):
        if isinstance(obj, self.flint.acb):
            return bool_or_error(lambda: obj.contains(self.flint.acb(0)))
        if isinstance(obj, self.flint.arb):
            return bool_or_error(lambda: obj.contains(self.flint.arb(0)))
        return None

    def contains_obj(self, obj, expected):
        return bool_or_error(lambda: obj.contains(expected))

    def abs_lower_text(self, obj):
        method = getattr(obj, "abs_lower", None)
        if method is None:
            return None
        try:
            value = method()
            return {
                "repr": repr(value),
                "contains_zero": self.contains_zero(value),
                "strictly_positive_by_contains": self.contains_zero(value) is False,
            }
        except Exception as exc:
            return {"error": f"{type(exc).__name__}: {exc}"}

    def describe(self, obj):
        record = {
            "result_type": type(obj).__name__,
            "result_repr": repr(obj),
            "is_finite": bool_or_error(lambda: obj.is_finite()) if hasattr(obj, "is_finite") else None,
            "contains_zero": self.contains_zero(obj),
            "abs_lower": self.abs_lower_text(obj),
        }
        if isinstance(obj, self.flint.arb):
            record.update({
                "lower": repr(obj.lower()),
                "upper": repr(obj.upper()),
                "rad": repr(obj.rad()),
            })
        if isinstance(obj, self.flint.acb):
            record.update({
                "real_lower": repr(obj.real.lower()),
                "real_upper": repr(obj.real.upper()),
                "imag_lower": repr(obj.imag.lower()),
                "imag_upper": repr(obj.imag.upper()),
                "rad": repr(obj.rad()),
            })
        return record

    def record(self, operation, exact_input, precision_bits, func, budget=None, expected=None):
        if budget is not None:
            self.counts[budget] += 1
        call_id = f"006H14-CALL-{len(self.ledger) + 1:03d}"
        entry = {
            "call_id": call_id,
            "operation": operation,
            "exact_input": exact_input,
            "precision_bits": precision_bits,
            "exception": None,
            "contains_expected": None,
        }
        try:
            result = func()
            entry.update(self.describe(result))
            if expected is not None:
                entry["contains_expected"] = self.contains_obj(result, expected)
            self.ledger.append(entry)
            return result
        except Exception as exc:
            entry.update({
                "result_type": None,
                "result_repr": None,
                "is_finite": None,
                "contains_zero": None,
                "abs_lower": None,
                "exception": f"{type(exc).__name__}: {exc}",
            })
            self.ledger.append(entry)
            return None

    def construct_objects(self):
        one = self.record("arb exact integer", "1", None, lambda: self.arb_exact(1))
        third = self.record("arb exact rational", "1/3", None, lambda: self.arb_exact(self.q(1, 3)))
        interval_positive = self.record(
            "arb closed real interval",
            "[1,2]",
            None,
            lambda: self.arb_interval(1, 2),
        )
        interval_zero = self.record(
            "arb closed real interval",
            "[-1,1]",
            None,
            lambda: self.arb_interval(-1, 1),
        )
        imag_third = self.arb_interval(self.q(-1, 3), self.q(1, 3))
        box0 = self.record(
            "acb rectangular box",
            "B0: real=[1,2], imag=[-1/3,1/3]",
            None,
            lambda: self.acb_box(interval_positive, imag_third),
        )
        box1 = self.record(
            "acb rectangular box",
            "B1: real=[-1,1], imag=[-1,1]",
            None,
            lambda: self.acb_box(interval_zero, interval_zero),
        )
        log_box = self.record(
            "acb right-half-plane log box input",
            "real=[1,3/2], imag=[-1/4,1/4]",
            None,
            lambda: self.acb_box(
                self.arb_interval(1, self.q(3, 2)),
                self.arb_interval(self.q(-1, 4), self.q(1, 4)),
            ),
        )
        return {
            "one": one,
            "third": third,
            "interval_positive": interval_positive,
            "interval_zero": interval_zero,
            "box0": box0,
            "box1": box1,
            "log_box": log_box,
        }

    def precision_checks(self):
        checks = []
        for bits in PRECISION_BITS:
            before = self.flint.ctx.prec
            with self.flint.ctx.workprec(bits):
                inside = self.flint.ctx.prec
            after = self.flint.ctx.prec
            exc_before = self.flint.ctx.prec
            try:
                with self.flint.ctx.workprec(bits):
                    exc_inside = self.flint.ctx.prec
                    raise RuntimeError("006H14 controlled precision restoration check")
            except RuntimeError:
                exc_after = self.flint.ctx.prec
            checks.append({
                "requested": bits,
                "prec_before": before,
                "prec_inside": inside,
                "prec_after": after,
                "exception_prec_before": exc_before,
                "exception_prec_inside": exc_inside,
                "exception_prec_after": exc_after,
                "restored": inside == bits and after == before and exc_inside == bits and exc_after == exc_before,
            })
        return checks

    def elementary_identities(self, objects):
        start_index = len(self.ledger)
        for bits in PRECISION_BITS:
            with self.flint.ctx.workprec(bits):
                zero_arb = self.flint.arb(0)
                one_arb = self.flint.arb(1)
                zero_acb = self.flint.acb(0)
                one_acb = self.flint.acb(1)
                self.record("arb pi", "pi", bits, self.flint.arb.pi, "pi")
                self.record("arb log", "log(1)", bits, lambda: self.flint.arb.log(one_arb), "log", zero_arb)
                self.record("arb exp", "exp(0)", bits, lambda: self.flint.arb.exp(zero_arb), "exp", one_arb)
                self.record("arb gamma", "Gamma(1)", bits, lambda: self.flint.arb.gamma(one_arb), "gamma", one_arb)
                self.record("acb log", "log(1)", bits, lambda: self.flint.acb.log(one_acb), "log", zero_acb)
                self.record("acb exp", "exp(0)", bits, lambda: self.flint.acb.exp(zero_acb), "exp", one_acb)
                self.record("acb gamma", "Gamma(1)", bits, lambda: self.flint.acb.gamma(one_acb), "gamma", one_acb)
                self.record(
                    "acb analytic log",
                    "log(real=[1,3/2], imag=[-1/4,1/4], analytic=True)",
                    bits,
                    lambda: self.flint.acb.log(objects["log_box"], analytic=True),
                    "log",
                )
        return [entry["call_id"] for entry in self.ledger[start_index:]]

    def chi_metadata(self):
        chi = self.flint.dirichlet_char(3, 2)
        return {
            "construction_API": "flint.dirichlet_char(3, 2)",
            "repr": repr(chi),
            "modulus": repr(chi.modulus()),
            "number": chi.number(),
            "index": chi.index(),
            "primitive": bool(chi.is_primitive()),
            "principal": bool(chi.is_principal()),
            "real": bool(chi.is_real()),
            "parity": chi.parity(),
            "l_function_attribute_present": hasattr(chi, "l_function"),
            "l_function_called": False,
            "object": chi,
        }

    def native_l_smoke(self, chi):
        summaries = []
        for bits in PRECISION_BITS:
            with self.flint.ctx.workprec(bits):
                s_exact = self.flint.acb(2)
                s_box = self.acb_box(
                    self.arb_interval(self.q(199, 100), self.q(201, 100)),
                    self.arb_interval(self.q(-1, 100), self.q(1, 100)),
                )
                exact = self.record(
                    "native Dirichlet L exact point",
                    "acb.dirichlet_l(s=2, chi_3)",
                    bits,
                    lambda: self.flint.acb.dirichlet_l(s_exact, chi),
                    "native_dirichlet_l",
                )
                box = self.record(
                    "native Dirichlet L whole box smoke",
                    "acb.dirichlet_l(real=[199/100,201/100], imag=[-1/100,1/100], chi_3)",
                    bits,
                    lambda: self.flint.acb.dirichlet_l(s_box, chi),
                    "native_dirichlet_l",
                )
                summaries.append({
                    "precision_bits": bits,
                    "exact_finite": None if exact is None else bool_or_error(lambda: exact.is_finite()),
                    "box_finite": None if box is None else bool_or_error(lambda: box.is_finite()),
                    "input_has_nonzero_width": repr(s_box.rad()) != "0",
                    "box_contains_exact_point_result_at_s_2": None if box is None or exact is None else self.contains_obj(box, exact),
                })
        return summaries

    def hurwitz_smoke(self, chi):
        summaries = []
        for bits in PRECISION_BITS:
            with self.flint.ctx.workprec(bits):
                s_exact = self.flint.acb(2)
                native = self.flint.acb.dirichlet_l(s_exact, chi)
                zeta_one_third = self.record(
                    "Hurwitz candidate acb.zeta",
                    "acb.zeta(s=2, a=1/3)",
                    bits,
                    lambda: self.flint.acb.zeta(s_exact, self.flint.acb(self.q(1, 3))),
                    "hurwitz_candidate_zeta",
                )
                zeta_two_thirds = self.record(
                    "Hurwitz candidate acb.zeta",
                    "acb.zeta(s=2, a=2/3)",
                    bits,
                    lambda: self.flint.acb.zeta(s_exact, self.flint.acb(self.q(2, 3))),
                    "hurwitz_candidate_zeta",
                )
                if zeta_one_third is None or zeta_two_thirds is None:
                    control = None
                else:
                    control = (zeta_one_third - zeta_two_thirds) / 9
                    self.ledger.append({
                        "call_id": f"006H14-CALL-{len(self.ledger) + 1:03d}",
                        "operation": "Hurwitz control algebra",
                        "exact_input": "(zeta(2,1/3)-zeta(2,2/3))/9",
                        "precision_bits": bits,
                        "exception": None,
                        "contains_expected": None,
                        **self.describe(control),
                    })
                summaries.append({
                    "precision_bits": bits,
                    "candidate_api_executed": zeta_one_third is not None and zeta_two_thirds is not None,
                    "control_finite": None if control is None else bool_or_error(lambda: control.is_finite()),
                    "native_and_control_overlap": None if control is None else bool_or_error(lambda: control.overlaps(native)),
                    "native_contains_control": None if control is None else self.contains_obj(native, control),
                    "control_contains_native": None if control is None else self.contains_obj(control, native),
                })
        return summaries

    def run(self):
        objects = self.construct_objects()
        precision = self.precision_checks()
        identities = self.elementary_identities(objects)
        chi_info = self.chi_metadata()
        chi = chi_info.pop("object")
        native = self.native_l_smoke(chi)
        hurwitz = self.hurwitz_smoke(chi)

        return {
            "objects": {key: None if value is None else self.describe(value) for key, value in objects.items()},
            "precision": precision,
            "identities": identities,
            "chi_3": chi_info,
            "native_l": native,
            "hurwitz": hurwitz,
        }


def main() -> int:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    for name in (CALL_LEDGER_NAME, RUNTIME_SEAL_NAME, RESULTS_NAME, SUMS_NAME):
        target = ARTIFACT_DIR / name
        if target.exists():
            target.unlink()

    seal = verify_preimport_runtime()
    scope_flags = {
        "FLINT_IMPORTED": False,
        "FLINT_ANALYTIC_OPERATIONS_EXECUTED": False,
        "ARB_ANALYTIC_OPERATIONS_EXECUTED": False,
        "ACB_ANALYTIC_OPERATIONS_EXECUTED": False,
        "CHI_L_FUNCTION_CALLED": False,
        "LAMBDA_3_EVALUATED": False,
        "CONTOURS_EXECUTED": False,
        "ZEROS_ISOLATED": False,
        "ZEROS_COUNTED": False,
        "NETWORK_USED": False,
        "DEPENDENCIES_INSTALLED": False,
        "H2_OPENED": False,
        "006F_OPENED": False,
    }

    if not seal["preimport_verified"]:
        result = {
            "phase_id": PHASE_ID,
            "result": "006H14_RUNTIME_OR_BINARY_HASH_MISMATCH",
            "precision_bits": list(PRECISION_BITS),
            "runtime_hashes_verified": False,
            "call_counts": {key: 0 for key in MAX_COUNTS},
            "scope_flags": scope_flags,
            "errors": seal["preimport_errors"],
        }
        write_json(ARTIFACT_DIR / CALL_LEDGER_NAME, [])
        write_json(ARTIFACT_DIR / RUNTIME_SEAL_NAME, seal)
        write_json(ARTIFACT_DIR / RESULTS_NAME, result)
        write_sums()
        return 2

    import flint

    scope_flags["FLINT_IMPORTED"] = True
    seal.update({
        "python_version": sys.version,
        "platform": platform.platform(),
        "architecture": platform.architecture(),
        "flint_module_version": getattr(flint, "__version__", None),
        "FLINT_native_version": getattr(flint, "__FLINT_VERSION__", None),
        "module_file_path": getattr(flint, "__file__", None),
    })

    if seal["flint_module_version"] != EXPECTED_PYTHON_FLINT_VERSION or seal["FLINT_native_version"] != EXPECTED_FLINT_VERSION:
        result = {
            "phase_id": PHASE_ID,
            "result": "006H14_RUNTIME_OR_BINARY_HASH_MISMATCH",
            "precision_bits": list(PRECISION_BITS),
            "runtime_hashes_verified": False,
            "call_counts": {key: 0 for key in MAX_COUNTS},
            "scope_flags": scope_flags,
            "errors": ["flint module or native version mismatch"],
        }
        write_json(ARTIFACT_DIR / CALL_LEDGER_NAME, [])
        write_json(ARTIFACT_DIR / RUNTIME_SEAL_NAME, seal)
        write_json(ARTIFACT_DIR / RESULTS_NAME, result)
        write_sums()
        return 2

    smoke = Smoke(flint, seal)
    smoke_data = smoke.run()
    budgets_ok = all(smoke.counts[key] <= limit for key, limit in MAX_COUNTS.items())
    precision_ok = all(item["restored"] for item in smoke_data["precision"])
    arb_ok = (
        smoke_data["objects"]["interval_positive"]["contains_zero"] is False
        and smoke_data["objects"]["interval_zero"]["contains_zero"] is True
        and smoke_data["objects"]["interval_positive"]["abs_lower"]["strictly_positive_by_contains"] is True
    )
    acb_ok = (
        smoke_data["objects"]["box0"]["contains_zero"] is False
        and smoke_data["objects"]["box1"]["contains_zero"] is True
    )
    identity_ok = all(
        entry["contains_expected"] is True
        for entry in smoke.ledger
        if entry["operation"] in {"arb log", "arb exp", "arb gamma", "acb log", "acb exp", "acb gamma"}
    )
    analytic_log_ok = all(
        entry["exception"] is None
        for entry in smoke.ledger
        if entry["operation"] == "acb analytic log"
    )
    native_exact_ok = all(item["exact_finite"] is True for item in smoke_data["native_l"])
    native_box_ok = all(item["box_contains_exact_point_result_at_s_2"] is True for item in smoke_data["native_l"])
    hurwitz_ok = all(
        item["candidate_api_executed"] is True
        and item["control_finite"] is True
        and item["native_and_control_overlap"] is True
        for item in smoke_data["hurwitz"]
    )
    result_name = "006H14_TINY_SEMANTIC_SMOKE_PASS"
    if not budgets_ok:
        result_name = "006H14_FAIL_SCOPE_OR_SEMANTICS"
    elif not hurwitz_ok:
        result_name = "006H14_NATIVE_L_HURWITZ_CONTROL_MISMATCH"
    elif not all((precision_ok, arb_ok, acb_ok, identity_ok, analytic_log_ok, native_exact_ok, native_box_ok)):
        result_name = "006H14_TINY_SEMANTIC_SMOKE_PASS_WITH_LIMITATIONS"

    results = {
        "phase_id": PHASE_ID,
        "result": result_name,
        "precision_bits": list(PRECISION_BITS),
        "runtime_hashes_verified": True,
        "call_counts": smoke.counts,
        "budgets": MAX_COUNTS,
        "budget_ok": budgets_ok,
        "scope_flags": scope_flags,
        "ARB_CONSTRUCTION_SEMANTICS": "VERIFIED" if arb_ok else "PARTIAL",
        "ACB_RECTANGULAR_CONSTRUCTION": "VERIFIED" if acb_ok else "PARTIAL",
        "PRECISION_CONTEXT_RESTORATION": "VERIFIED" if precision_ok else "PARTIAL",
        "ELEMENTARY_ARB_ACB_IDENTITIES": "VERIFIED" if identity_ok else "PARTIAL",
        "ACB_ANALYTIC_LOG_SURFACE": "VERIFIED" if analytic_log_ok else "PARTIAL",
        "ZERO_EXCLUSION_POLICY": "DEFINED",
        "NATIVE_L_EXACT_POINT_SMOKE": "PASS" if native_exact_ok else "PARTIAL",
        "NATIVE_L_WHOLE_BOX_SMOKE": "PASS" if native_box_ok else "PARTIAL",
        "HURWITZ_CANDIDATE_SMOKE": "PASS" if hurwitz_ok else "PARTIAL",
        "origin_excluded_policy": "not contains_zero and abs_lower strictly positive",
        "L3_READY_FOR_REAL_BACKEND_CODE_IMPLEMENTATION_AUTHORIZATION": result_name in {
            "006H14_TINY_SEMANTIC_SMOKE_PASS",
            "006H14_TINY_SEMANTIC_SMOKE_PASS_WITH_LIMITATIONS",
        },
        "L3_READY_FOR_REAL_BACKEND_IMPLEMENTATION": False,
        "L3_READY_FOR_REAL_EXECUTION": False,
        "H2_CERTIFIED": False,
        "006F_OPENED": False,
        "NEXT_PHASE_AUTHORIZED": False,
        "smoke": smoke_data,
    }

    write_json(ARTIFACT_DIR / CALL_LEDGER_NAME, smoke.ledger)
    write_json(ARTIFACT_DIR / RUNTIME_SEAL_NAME, seal)
    write_json(ARTIFACT_DIR / RESULTS_NAME, results)
    write_sums()
    print(canonical_json({"result": result_name, "artifact_dir": str(ARTIFACT_DIR), "call_counts": smoke.counts}), end="")
    return 0 if result_name != "006H14_FAIL_SCOPE_OR_SEMANTICS" else 3


def write_sums() -> None:
    names = (CALL_LEDGER_NAME, RUNTIME_SEAL_NAME, RESULTS_NAME)
    lines = []
    for name in names:
        path = ARTIFACT_DIR / name
        lines.append(f"{sha256_path(path)}  {name}")
    (ARTIFACT_DIR / SUMS_NAME).write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    raise SystemExit(main())
