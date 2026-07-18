# 006E21R-METADATA-ONLY-FLINT-ARB-VERSION-INTROSPECTION

## 1. Alcance ejecutado

```text
phase_id = 006E21R
status = metadata_only_version_introspection_completed
result = 006E21R_VERSION_SEAL_LIMITED
runtime_authorized = C:\Users\johnn\AppData\Local\Temp\athena-006e20r\Scripts\python.exe
scope = metadata_only
flint_import = allowed_and_performed
arb_execution = forbidden
acb_execution = forbidden
ctx_workprec_execution = forbidden
dirichlet_char_execution = forbidden
l_function_execution = forbidden
contour_execution = forbidden
Lambda_3_evaluation = forbidden
zero_isolation = forbidden
zero_counting = forbidden
zero_tables = not_generated
MATHEMATICAL_PROOF = false
H2_CERTIFIED = false
006F = blocked
DOWNSTREAM_USE = forbidden
NOVELTY_CLAIM = false
```

006E21R inspected only import/package/wheel/native-file metadata. It did not
execute new mathematical semantics.

## 2. Runtime usado

```text
runtime_exists = PASS
runtime = C:\Users\johnn\AppData\Local\Temp\athena-006e20r\Scripts\python.exe
import_flint = PASS
```

This is the tempdir environment prepared by 006E20R and used by 006E20B. The
broken project `.venv` and the workspace `.venv-006e20r` were not used.

## 3. Metadata de Python y plataforma

```text
python_implementation = CPython
python_version = 3.12.13 (main, Mar  3 2026, 15:01:35) [MSC v.1944 64 bit (AMD64)]
platform = Windows-11-10.0.26200-SP0
machine = AMD64
processor = Intel64 Family 6 Model 126 Stepping 5, GenuineIntel
```

## 4. Metadata de python-flint

```text
distribution_name = python-flint
distribution_version = 0.8.0
flint.__version__ = 0.8.0
summary = Bindings for FLINT
requires_python = >=3.11
metadata_version = 2.1
installer = pip
```

The installed distribution metadata was found at:

```text
C:\Users\johnn\AppData\Local\Temp\athena-006e20r\Lib\site-packages\python_flint-0.8.0.dist-info
```

Key metadata file hashes:

```text
METADATA_SHA256 = 94ff47728ed9496579365103e391d182cfed697ea0622f021f4f766216834ae6
WHEEL_SHA256 = e743de01ba6503a3e4234858398a1e69c07d512d51e8482ec9f3a7b1c707d165
DELVEWHEEL_SHA256 = d4f9e2f7d935ec5c5e5bb64d87b44199e00120aac6ccc635d53f2d132feee57f
RECORD_SHA256 = 4b8019611e4b879c846b7371ed4ee86dfee44b92b0cccc3d5c505a4ff12ebc70
```

Wheel metadata:

```text
Wheel-Version = 1.0
Generator = meson
Root-Is-Purelib = false
Tag = cp312-cp312-win_amd64
```

The installed `DELVEWHEEL` metadata records repair of:

```text
python_flint-0.8.0-cp312-cp312-win_amd64.whl
```

with native libraries added from `.local/bin`.

## 5. Metadata FLINT/Arb encontrada o no encontrada

### FLINT

`flint` exposes a version-like string attribute:

```text
flint.__FLINT_VERSION__ = 3.3.1
```

The installed wheel includes a bundled FLINT dynamic library:

```text
relative_path = python_flint.libs/libflint.21.0.0-67b518837b39088fce997dec2b675a6a.dll
size = 14026918
sha256 = d5410bef059868b7bfe0f2e9fde9db02f02177cbf871ab74b21893a2664c25f9
```

The installed `METADATA` file states that the binary distribution bundles
FLINT as:

```text
Files: python_flint.libs/libflint*.dll
Description: bundled as a dynamically linked library
```

### Arb

No separate Arb version accessor was found through metadata-only
introspection:

```text
flint.arb_version = not_found
separate_Arb_DLL = not_found
separate_Arb_dist_info = not_found
```

Arb-related Python extension modules are present in the installed package:

```text
flint/types/arb.cp312-win_amd64.pyd
flint/types/acb.cp312-win_amd64.pyd
flint/types/arb_mat.cp312-win_amd64.pyd
flint/types/acb_mat.cp312-win_amd64.pyd
```

This supports only a limited native-version seal: FLINT is identified as
`3.3.1`; Arb is not independently versioned by the installed metadata observed
in this phase.

Other bundled native libraries observed:

```text
libgmp-10-a8a2bf81a7885e882dc5b408a196b72f.dll
libmpfr-6-58075fd5a9688dfd00e645316ed6a020.dll
libgcc_s_seh-1-f2b6825d483bdf14050493af93b5997d.dll
libwinpthread-1-e01b8e85fd67c2b861f64d4ccc7df607.dll
```

## 6. Metodo de introspeccion usado

Methods used:

```text
1. Test-Path on authorized Python executable.
2. importlib.metadata.distribution("python-flint").
3. import flint.
4. Read flint.__version__.
5. Inspect version-like attributes via dir(flint).
6. Read flint.__FLINT_VERSION__ as a string attribute.
7. Read installed dist-info files: METADATA, WHEEL, DELVEWHEEL, RECORD.
8. Inventory installed .pyd/.dll/native files by path, size and SHA-256.
```

Methods explicitly not used:

```text
arb construction = not_executed
acb construction = not_executed
ctx.workprec = not_executed
dirichlet_char = not_executed
l_function = not_executed
contours = not_executed
Lambda_3 = not_evaluated
zero isolation = not_executed
zero counting = not_executed
```

No callable version function was invoked. The version identity was obtained
from package metadata and string attributes.

## 7. Limites de la evidencia

This is a metadata seal, not a semantic proof.

It establishes:

```text
python-flint package identity = 0.8.0
module identity = flint.__version__ 0.8.0
native FLINT string identity = flint.__FLINT_VERSION__ 3.3.1
bundled libflint DLL path and SHA-256 = recorded
wheel tag = cp312-cp312-win_amd64
```

It does not establish:

```text
general Arb/acb inclusion semantics = not_proved
general outward rounding = not_proved
native L-function inclusion semantics = not_proved
absence of midpoint extraction in all bindings = not_proved
canonical ball serialization = not_proved
contour safety = not_proved
zero isolation or counting = not_proved
H2 certification = false
```

The absence of a separate Arb version accessor means Arb identity is bounded by
the observed FLINT wheel/native-library identity, not independently sealed.

## 8. Clasificacion del resultado

```text
FLINT_native_identity = sealed_limited
FLINT_version = 3.3.1
python_flint_identity = sealed_limited
python_flint_version = 0.8.0
Arb_native_identity = bounded_but_not_separately_versioned
wheel_identity = sealed_limited
result = 006E21R_VERSION_SEAL_LIMITED
```

`VERSION_SEAL_LIMITED` means the identity is strong enough to remove the
006E20B/006E21 warning for narrow non-certifying smoke interpretation. It does
not authorize probative mathematics.

## 9. Bloqueos preservados

```text
MATHEMATICAL_PROOF = false
H2_CERTIFIED = false
006F = blocked
ZERO_CERTIFICATION = forbidden
ZERO_TABLES = not_generated
DOWNSTREAM_USE = forbidden
NOVELTY_CLAIM = false
REAL_CONTOUR_EXECUTION = forbidden
LAMBDA_3_EVALUATION = forbidden
```

006E21R does not change the status of H2, 006F, or any downstream experiment.

## 10. Recomendacion no vinculante para Yonnah

Recommended next step:

```text
NEXT_STEP = 006E22_NARROW_REAL_SEMANTIC_CONTRACT_PLAN
```

006E22 should remain a plan, not execution. It can now cite:

```text
python-flint = 0.8.0
FLINT = 3.3.1
Arb = not independently versioned in observed metadata
```

Before any probative phase, the project should still decide whether the
limited Arb identity is sufficient or whether a stronger native build/runtime
attestation is required.

Do not proceed to contours, `Lambda_3`, zero isolation, zero counting, tables,
H2 certification, 006F, or downstream use from this metadata seal alone.

## 11. Verdict

```text
006E21R_RESULT = 006E21R_VERSION_SEAL_LIMITED
VERSION_GAP_FOR_006E20B = closed_limited
VERSION_GAP_FOR_PROBATIVE_PHASES = remains_limited_Arb_identity
PATCH_REQUIRED = no
MATHEMATICAL_PROOF = false
H2_CERTIFIED = false
006F_OPENED = false
ZERO_CERTIFICATION_COMPLETED = false
DOWNSTREAM_USE_ALLOWED = false
NOVELTY_CLAIM = false
```

006E21R improves the 006E20B/006E21 version warning from unresolved to a
limited metadata seal: python-flint 0.8.0 with FLINT 3.3.1, bundled in the
observed Windows wheel, with no separate Arb version accessor found.
