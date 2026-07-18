# 006H12 L3 Real Backend Code Plan and Semantic Map

```text
phase_id = 006H12_L3_REAL_BACKEND_CODE_PLAN_AND_SEMANTIC_MAP
phase_type = documentary_technical_backend_plan
result = 006H12_L3_REAL_BACKEND_CODE_PLAN_AND_SEMANTIC_MAP_COMPLETED
code_modified = false
tests_executed = false
backend_invoked = false
FLINT_imported = false
Arb_or_Acb_imported = false
chi_l_function_called = false
Lambda_3_evaluated = false
contours_executed = false
zeros_isolated_or_counted = false
H2_opened = false
006F_opened = false
network_used = false
dependencies_installed = false
novelty_claim = false
```

## 1. Scope

006H12 defines a documentary and technical code plan for the future real L3
backend. It maps the current structural package to the missing Arb/Acb/FLINT
semantics needed by 006H01 and 006H02.

006H12 does not implement code, does not import FLINT, Arb or Acb, does not call
`chi.l_function`, does not evaluate `Lambda_3`, does not execute contours, does
not isolate or count zeros, does not open H2, does not open 006F and does not
authorize any later phase.

The plan explicitly assumes neither RH nor GRH:

```text
RH_assumed = false
GRH_assumed = false
zeros_presumed_on_critical_line = false
zero_simplicity_assumed = false
```

## 2. Sources Reviewed

Local documentary sources:

```text
006H01 H2 execution contract and 006F authorization schema freeze
006H02 L3 contour mathematical obligations review
006H03 L3 backend completion code plan
006H04 L3 structural synthetic implementation
006H05 static audit and code review
006H06 structural audit findings patch
006H07 structural patch reaudit
006H08 second structural patch
006H09 second structural patch reaudit
006H10 rational endpoint canonicality patch
006H11 rational endpoint canonicality reaudit
```

Static package sources:

```text
athena_azr/h2_zero_certifier/authorization.py
athena_azr/h2_zero_certifier/backend.py
athena_azr/h2_zero_certifier/ball_argument.py
athena_azr/h2_zero_certifier/boundary_certifier.py
athena_azr/h2_zero_certifier/chi3_function.py
athena_azr/h2_zero_certifier/completed_l3.py
athena_azr/h2_zero_certifier/config.py
athena_azr/h2_zero_certifier/contour.py
athena_azr/h2_zero_certifier/l3_argument_count.py
athena_azr/h2_zero_certifier/l3_certifier.py
athena_azr/h2_zero_certifier/l3_isolator.py
athena_azr/h2_zero_certifier/models.py
athena_azr/h2_zero_certifier/pipeline.py
athena_azr/h2_zero_certifier/python_flint_backend.py
athena_azr/h2_zero_certifier/real_argument.py
athena_azr/h2_zero_certifier/real_completed_l3.py
athena_azr/h2_zero_certifier/real_evidence.py
athena_azr/h2_zero_certifier/real_segment_enclosure.py
athena_azr/h2_zero_certifier/rigorous_ball_runtime.py
athena_azr/h2_zero_certifier/serialization.py
athena_azr/h2_zero_certifier/winding_certifier.py
athena_azr/h2_zero_certifier/zeta_certifier.py
```

Current closed state from 006H11:

```text
H09_F001_VERIFIED_CLOSED = true
INTEGER_VALUED_RATIONALS_REJECTED = true
NONINTEGER_REDUCED_RATIONALS_ACCEPTED = true
UNIQUE_TEXTUAL_REPRESENTATION_VERIFIED = true
CONTRACTS_006H01_006H02_PRESERVED = true
REAL_PATH_REMAINS_BLOCKED = true
L3_READY_FOR_REAL_BACKEND_CODE_PLAN = true
L3_READY_FOR_REAL_BACKEND_IMPLEMENTATION = false
L3_READY_FOR_REAL_EXECUTION = false
NEXT_PHASE_AUTHORIZED = false
```

## 3. Exact Backend Objective

The future real backend objective is:

```text
Implement a rigorous inclusion backend for Lambda_3 and its argument-principle
certificates over the frozen L3 rectangles, using sealed Arb/Acb/FLINT semantics,
with no RH/GRH assumption and no critical-line-only shortcut.
```

The backend must implement or support:

```text
Lambda_3(s)
Lambda_3(segment_box)
boundary zero exclusion
local argument increments
total winding intervals
local rectangle zero counts
individual zero isolation
multiplicity handling
cluster handling
```

The frozen function is:

```text
Lambda_3(s) =
(3/pi)^((s + 1)/2) * Gamma((s + 1)/2) * L(s, chi_3)
```

The frozen contours are:

```text
T_set = [143, 200, 300, 500]
sigma_left = -1/2
sigma_right = 3/2
bottom_height = 0
boundary_mode = exact_T_boundary
orientation = positive_counterclockwise
```

The backend passes only if every certified count is derived from a rigorous
argument-principle certificate and matches the isolated zeros with multiplicity.

## 4. Current Code Readiness Map

| Area | Current implementation | Status for 006H12 |
| --- | --- | --- |
| Character metadata | `chi3_function.py` freezes conductor 3, Conrey 2, parity odd, root number 1 and symbolic `Lambda_3`. | partial; metadata is present, real theorem package still needed |
| Frozen contours | `contour.py` builds exact `C_143`, `C_200`, `C_300`, `C_500`; rejects `T_star`. | structural ready |
| Structural boundary coverage | `boundary_certifier.py` subdivides segments and requires zero exclusion. | structural ready, real backend missing |
| Structural increments | `argument_increment.py` sums interval increments with common provenance and precision. | structural ready |
| Winding integer rule | `winding_certifier.py` uses exact endpoint parsing and closed integer enumeration. | structural ready |
| Real runtime protocol | `rigorous_ball_runtime.py` lists required operations and semantic audit flags. | protocol shell ready |
| Real Lambda skeleton | `real_completed_l3.py` composes pi, log, exp, gamma, native L and product through an injected runtime. | skeleton ready, runtime missing |
| Segment enclosure skeleton | `real_segment_enclosure.py` evaluates the whole rectangular hull and requires whole-box certification. | skeleton ready, runtime missing |
| Real argument skeleton | `real_argument.py` uses half-plane rotation, certified log at endpoints, interval summation and division by `2*pi`. | skeleton ready, semantic audit required |
| Real evidence | `real_evidence.py` enforces factory-issued, hashed, parent-linked evidence. | structural ready |
| FLINT adapter | `python_flint_backend.py` lazy-imports `flint` only after validated authorization, then raises `NotImplementedError` for real math. | intentionally blocked |
| Pipeline | `pipeline.py` checks authorization, output path and empty directory, then stops at real-pipeline blocker. | intentionally blocked |
| Serialization | `serialization.py` emits canonical JSON/CSV helpers and synthetic L3 report shapes. | partial; final real H2 manifest still future |

Current expected real-path blockers:

```text
argument_principle.py     DEPRECATED_SYNTHETIC_STUB
completed_l3.py           EXPECTED_REAL_BLOCKER
python_flint_backend.py   EXPECTED_REAL_BLOCKER
pipeline.py               EXPECTED_REAL_BLOCKER
```

## 5. FLINT Arb Acb Operation Inventory

All APIs below are candidate APIs or adapter responsibilities. 006H12 does not
verify python-flint names by import and does not claim that any candidate API is
available. A future code phase must confirm exact names locally without network.

| operation_id | python_flint_API_or_candidate_API | input_types | output_types | precision_context | inclusion_guarantee | zero_exclusion_semantics | branch_semantics | failure_conditions | 006H02_obligation | H2_requirement_ids |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OP01 | `arb` construction from canonical integer/rational/decimal strings | exact text bounds | Arb real ball | scoped precision, outward rounded | constructed ball contains exact endpoint or interval | n/a | n/a | noncanonical text, nonfinite, precision mismatch | ball construction | H2-R11, H2-R13, H2-R21 |
| OP02 | `acb` construction from two Arb intervals | real Arb, imag Arb | Acb rectangle | scoped precision | complex rectangle contains target box | can later test origin containment | n/a | reversed bounds, zero width where forbidden | segment boxes | H2-R07, H2-R08 |
| OP03 | pi ball, e.g. candidate `arb.pi()` or equivalent | precision | Arb ball for pi | scoped precision | contains mathematical pi | denominator must exclude zero before division | n/a | nonpositive pi ball impossible, API mismatch | division by `2*pi` | H2-R06, H2-R08 |
| OP04 | exact division `3 / pi_ball` | integer, Arb pi | Arb ball | scoped precision | contains exact `3/pi` | denominator excludes zero by positive pi | n/a | pi ball contains zero, precision exhausted | conductor power | H2-R06, H2-R11 |
| OP05 | real log, candidate Arb `.log()` | positive Arb ball | Arb ball | scoped precision | contains `log(3/pi)` | input must be strictly positive | real principal log | input includes nonpositive values | conductor power | H2-R06, H2-R11 |
| OP06 | affine exponent `(s+1)/2 * log(3/pi)` | Acb box, Arb log base | Acb box | scoped precision | contains exact exponent over whole input box | n/a | no complex log branch here | overflow, nonfinite result | `Lambda_3` evaluation | H2-R06, H2-R08 |
| OP07 | complex exp, candidate Acb `.exp()` | Acb exponent | Acb box | scoped precision | contains `exp(exponent)` over whole box | exp is nonzero mathematically, but ball may contain zero | entire single-valued | nonfinite/wide ball | conductor power | H2-R06, H2-R08 |
| OP08 | affine gamma argument `(s+1)/2` | Acb input box | Acb box | scoped precision | contains gamma argument over whole box | n/a | n/a | box crosses gamma pole without cancellation proof route | gamma factor | H2-R06, H2-R11 |
| OP09 | complex gamma, candidate Acb `.gamma()` | Acb gamma argument | Acb box | scoped precision | contains `Gamma((s+1)/2)` | gamma has no zeros; poles must be controlled | meromorphic; pole exclusion required | input contains or approaches pole ambiguously | gamma factor | H2-R06, H2-R11 |
| OP10 | native Dirichlet L, candidate `chi.l_function(s)` after sealed character construction | Acb input box, modulus 3, Conrey 2 | Acb box | scoped precision | contains `L(s, chi_3)` for whole input box | zero may be contained or excluded only by resulting image | native analytic continuation semantics required | wrong character, not whole-box, nonfinite, API mismatch | native L channel | H2-R06, H2-R11, H2-R12 |
| OP11 | Hurwitz control, candidate `hurwitz_zeta(s, 1/3)` and `hurwitz_zeta(s, 2/3)` | Acb input box, exact rationals | Acb boxes | scoped precision | contains Hurwitz control expression | control may compare to native L by inclusion overlap | same branch for `3^-s` must be defined | unavailable API, shared-library nonindependence, mismatch | control channel | H2-R11, H2-R15 |
| OP12 | complex multiplication | Acb factors | Acb box | scoped precision | contains product of factors | if product ball excludes zero then value zero-free | n/a | nonfinite, excessive width | `Lambda_3` product | H2-R06, H2-R08 |
| OP13 | complex subtraction | Acb left/right | Acb box | scoped precision | contains exact difference | used for log differences | n/a | nonfinite, precision exhausted | argument increment | H2-R08 |
| OP14 | complex division | Acb numerator/denominator | Acb box | scoped precision | contains quotient | divisor must exclude zero | n/a | divisor contains zero | optional log-derivative/integral route | H2-R08, H2-R11 |
| OP15 | absolute value lower bound, candidate Acb abs or norm interval | Acb image | Arb lower-bound interval | scoped precision | positive lower bound certifies origin exclusion | `lower(abs(z)) > 0` implies zero excluded | n/a | lower bound not positive | boundary zero-free | H2-R07, H2-R08 |
| OP16 | zero containment/exclusion on Acb rectangle | Acb image | boolean plus witness | scoped precision | true exclusion means 0 not in represented set | must distinguish contains-zero from unable-to-exclude | n/a | ambiguous containment, no witness | boundary zero-free | H2-R07, H2-R08 |
| OP17 | complex log, candidate Acb `.log()` with branch precondition | Acb value excluding negative real cut after rotation | Acb box | scoped precision | contains selected local log values | input must exclude zero | principal/local branch must be certified | branch cut intersects ball, zero not excluded | argument increment | H2-R08, H2-R11 |
| OP18 | argument enclosure via imaginary part of log difference | Acb log difference | Arb/real ball | scoped precision | contains local `delta_arg` | depends on prior branch and zero exclusion | branch inherited from OP17 | mixed branch, nonfinite width | argument increment | H2-R08 |
| OP19 | real-ball summation | list of Arb intervals | Arb interval | scoped precision | contains sum of all increments | n/a | n/a | mixed precision/provenance, precision exhaustion | total winding | H2-R06, H2-R08 |
| OP20 | division by `2*pi` | Arb total argument, Arb pi | Arb interval | scoped precision | contains winding interval | divisor positive | n/a | pi invalid, interval too wide | winding interval | H2-R06, H2-R08 |
| OP21 | integer containment in closed real interval | canonical exact endpoints or Arb exported intervals | integer set | exact Fraction or directed Arb bounds | identifies all integers contained | n/a | n/a | multiple/no integer, noncanonical export | unique integer count | H2-R06, H2-R08 |
| OP22 | whole-box certification | input Acb box, output Acb box | boolean/evidence | scoped precision | output encloses the image of the whole input box | may support zero exclusion | n/a | endpoint-only evaluation, midpoint-only evaluation | segment image | H2-R07, H2-R08 |
| OP23 | finite-ball audit | any Arb/Acb output | boolean | scoped precision | rejects NaN/Inf/nonfinite | n/a | n/a | nonfinite output | all real operations | H2-R11, H2-R12 |
| OP24 | precision context restore | requested precision, previous ctx | context guard evidence | scoped precision manager | all operations happen at or above request and restore prior ctx | n/a | n/a | ctx leak, effective precision below request | runtime seal | H2-R11, H2-R13 |
| OP25 | character construction audit | modulus 3, Conrey 2, parity odd | character object plus metadata | scoped precision | native object matches frozen `chi_3` | n/a | native L semantics tied to character | wrong character, missing metadata | exact `chi_3` definition | H2-R05, H2-R10 |

## 6. Precision and Subdivision Policy

The current frozen configuration in `CertificationConfig.frozen_default()` is:

```text
requested_heights = (143, 200, 300, 500)
target_interval_width = 1e-20
precision_steps_bits = (192, 256, 384, 512, 768, 1024)
max_contour_depth = 40
max_root_isolation_depth = 60
```

006H12 keeps this as the base future policy.

Future code should distinguish two kinds of adaptation:

```text
precision_adaptation = allowed only within frozen precision_steps_bits
scope_adaptation = forbidden
```

Allowed precision escalation:

```text
192 -> 256 -> 384 -> 512 -> 768 -> 1024
```

Allowed subdivision escalation:

```text
segment depth <= 40
root isolation depth <= 60
```

Escalation conditions:

```text
result ball nonfinite
effective precision below request
segment image may contain zero
half-plane separation not strict
complex log branch not certified
argument interval too wide
winding interval has no unique integer
zero box wider than 1e-20
cluster or multiplicity unresolved
```

Forbidden adaptation:

```text
changing T to T_star
adding new heights
changing sigma_left or sigma_right
changing target function
switching to another character
dropping difficult boxes
assuming RH/GRH
assuming critical-line location
assuming simplicity
precision chasing beyond the frozen budget
```

If the frozen budget is exhausted, the future phase must close as one of:

```text
boundary_not_certified_zero_free
argument_increment_not_certified
winding_interval_contains_multiple_integers
multiplicity_unresolved
unresolved_cluster
H2_INCONCLUSIVE
H2_BLOCKED
```

## 7. Lambda_3 Semantics

The future backend must evaluate the whole input ball, not only endpoints or
midpoints.

For a complex ball `S`:

```text
gamma_arg = (S + 1) / 2
base = 3 / pi
power = exp(gamma_arg * log(base))
gamma_value = Gamma(gamma_arg)
l_value = L(S, chi_3)
Lambda_3(S) = power * gamma_value * l_value
```

Required semantics:

```text
base is a positive real ball
log(base) is the real log of a positive real ball
exp is entire and single-valued
Gamma is evaluated only with pole handling/accounting compatible with 006H02
L(S, chi_3) is the primitive real nonprincipal character modulo 3, Conrey 2
the product is an inclusion ball over all points of S
all output balls are finite
all output balls carry nonzero widths unless a future exact singleton is justified
```

The future implementation must emit operation evidence for each factor and for
the product. A numeric match to a sampled value is not a certificate.

## 8. Native L and Control Channel Semantics

Primary native L channel:

```text
native_dirichlet_l(S, modulus=3, conrey_number=2, precision_bits=p)
```

The future code must verify:

```text
character metadata matches CHI3_METADATA exactly
native function is entire/analytically continued in the required box
input is a whole Acb box, not a midpoint
output is a rigorous Acb inclusion
precision context is restored after the call
```

Control channel:

```text
L(s, chi_3) =
3^(-s) * (HurwitzZeta(s, 1/3) - HurwitzZeta(s, 2/3))
```

The Hurwitz channel is a local consistency control, not automatically an
independent proof if it uses the same underlying library. The future comparison
must be inclusion-based:

```text
native_L_ball intersects_or_is_contained_in Hurwitz_control_ball
decimal equality = forbidden
midpoint equality = forbidden
```

If the native channel and control channel disagree under rigorous inclusion, the
future backend must close as:

```text
native_L_semantics_mismatch
```

## 9. Segment-Box Evaluation

For every boundary or isolation segment, the future backend must evaluate:

```text
Lambda_3(rectangular_hull(segment))
```

not:

```text
Lambda_3(segment.start only)
Lambda_3(segment.end only)
Lambda_3(midpoint only)
sampled points along the segment
```

Required evidence:

```text
segment_id
input_complex_ball
output_lambda3_complex_ball
entire_segment_covered = true
whole_box_evaluation = true
precision_bits
backend_id
operation_trace_hash
parent_evidence_hashes
```

The existing `real_segment_enclosure.enclose_completed_l3_segment` already
expresses this shape through a rectangular hull and `certifies_whole_box`; the
future backend must make that promise real and auditable.

## 10. Origin Exclusion

A segment or box image is zero-free only when the backend proves:

```text
0 notin Lambda_3(segment_box)
```

Acceptable witnesses:

```text
Acb rectangle excludes the origin
positive lower bound for abs(Lambda_3) over the whole segment box
certified half-plane or sector enclosure excluding zero
```

Rejected witnesses:

```text
endpoint values nonzero
midpoint value nonzero
sampled values nonzero
plot or visual inspection
decimal distance without directed inclusion
```

If the image contains zero or cannot exclude zero, the only allowed future
actions are precision escalation, subdivision inside budget or inconclusive
closure.

## 11. Argument Increment Route

006H12 selects this future primary route:

```text
half-plane or sector certification -> local principal log -> endpoint log
difference -> imaginary interval -> sum -> divide by 2*pi
```

Justification:

1. It matches the existing `real_argument.py` shape.
2. It keeps the branch decision local and evidenced.
3. It avoids using the legacy float-based `argument_principle.py`.
4. It preserves 006H02's demand for a continuous local branch and zero-free
   image.

Structural mapping:

| Step | Existing file/function | Future real requirement |
| --- | --- | --- |
| Segment image | `real_segment_enclosure.enclose_completed_l3_segment` | whole-box Acb image inclusion |
| Half-plane | `real_argument.certify_real_half_plane` | strict rotated real lower bound |
| Local log | `runtime.certifies_principal_log`, `runtime.complex_log` | branch certificate plus Acb inclusion |
| Increment | `real_argument.real_argument_increment` | imaginary interval of log difference |
| Accumulation | `real_argument.accumulate_real_winding` | real-ball summation and division by `2*pi` |
| Integer count | `winding_certifier.certify_unique_integer_winding_bounds` | exact closed interval integer enumeration |

Fallback routes are allowed only in a separately authorized future plan:

```text
sector-only argument interval
certified integral of Lambda_3'/Lambda_3
certified homotopy/cocycle route
```

006H12 does not authorize those routes.

## 12. Total Winding for T Set

For each `T in [143, 200, 300, 500]`, future code must compute a separate
certificate:

```text
C_T = boundary of [-1/2, 3/2] x [0, T]
Delta_arg_T = sum_j delta_arg_j
W_T = Delta_arg_T / (2*pi)
N_L3(T) = unique integer contained in W_T
```

No count may be inferred solely from `T=500`.

Required per-height artifacts:

```text
contour_id
target_height
bottom_edge_certificates
right_edge_certificates
top_edge_certificates
left_edge_certificates
boundary_zero_free = true
argument_increment_intervals
winding_interval
unique_integer_count = true
certified_total_count
working_precision_bits
maximum_subdivision_depth_used
```

Any height failure blocks the L3 H2 result.

## 13. Zero Isolation Strategy

The future isolation strategy is recursive argument-principle subdivision:

1. Start with the frozen rectangle `[-1/2, 3/2] x [0, 500]`.
2. Count zeros in a candidate rectangle by the same boundary/winding method.
3. Discard rectangles with count `0`.
4. If count is `1`, keep subdividing until both real and imaginary widths are
   `<= 1e-20`, then emit one `ZeroCertificate`.
5. If count is greater than `1`, subdivide until individual zeros are separated
   or multiplicities are certified.
6. If multiplicity or cluster resolution cannot close within budget, emit an
   unresolved-cluster failure, not a certificate.

Critical-line status is only an extra field:

```text
critical_line_certified = true | false
```

It is not allowed to omit off-critical zeros and it is not allowed to assume
that all zeros lie on `Re(s)=1/2`.

Multiplicity policy:

```text
each zero is counted with multiplicity
unique boxes must carry multiplicity >= 1
clusters require certified total multiplicity and internal resolution
unresolved multiplicity blocks H2-L3
```

## 14. Exact Boundary Policy

006H12 preserves the 006H02 policy:

```text
boundary_mode = exact_T_boundary
T_star = not authorized
adaptive boundary shift = not authorized
```

Edges for each height:

```text
bottom: -1/2 + 0*i  ->  3/2 + 0*i
right:   3/2 + 0*i  ->  3/2 + T*i
top:     3/2 + T*i  -> -1/2 + T*i
left:   -1/2 + T*i  -> -1/2 + 0*i
```

Every edge must be certified zero-free. If the bottom edge, top edge, left edge
or right edge cannot be certified, future execution must close inconclusive or
blocked. It may not silently shift the boundary.

## 15. ARB Independent Version Seal Policy

006H12 defines the seal policy but does not create a seal.

The future preflight must record:

```text
python_version
python_runtime_path
platform
python_flint_distribution_version
flint_python_module_version
FLINT_native_version
Arb_version_or_FLINT_bundled_Arb_policy
Acb_version_or_FLINT_bundled_Acb_policy
binary_file_hashes
runtime_path_hash
environment_variable_hash
approved_code_hashes
approved_protocol_hashes
artifact_directory
```

Accepted outcomes:

```text
ARB_SEAL_POLICY_DEFINED
ARB_SEAL_POLICY_BLOCKED
```

Policy details:

1. If python-flint exposes separate Arb/Acb version data, those exact versions
   must be recorded.
2. If Arb/Acb are bundled inside FLINT without separately exposed version
   strings, the future preflight must explicitly record the accepted bundled
   policy and the exact FLINT native version and binary hashes.
3. If no version or binary provenance can be established locally, the future
   phase must close as `ARB_SEAL_POLICY_BLOCKED`.
4. 006E71/006E74 smoke reproducibility does not create this seal.

006H12 decision:

```text
ARB_SEAL_POLICY = DEFINED
ARB_INDEPENDENT_VERSION_SEAL = false
```

## 16. Local Proof Package Plan

The future real backend must be accompanied by a local proof package. Network
access during the proof package construction or real execution is not permitted
unless separately authorized.

Required local proof materials:

```text
definition of primitive Dirichlet L-functions
analytic continuation of L(s, chi_3)
functional equation for primitive Dirichlet L-functions
Gauss sum and root number epsilon(chi_3) = 1
entireness of Lambda_3
trivial-zero and gamma-pole cancellation
argument principle for entire functions
equivalence between zeros of Lambda_3 and nontrivial zeros of L(s, chi_3)
no RH/GRH dependency statement
```

Required proof artifact fields:

```text
proof_package_id
source_file_hashes
theorem_inventory
dependency_to_006H02_obligation
auditor_notes
created_without_network = true
```

Current status:

```text
local_proof_package_complete = false
proof_package_plan_defined = true
```

## 17. Code Architecture Mapping

| function_name | file | purpose | inputs | outputs | preconditions | postconditions | backend_operations | evidence_type | failure_states | tests | requires_real_execution |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `build_frozen_l3_contour` | `contour.py` | Build one exact frozen contour. | height, boundary mode | `RectangularContour` | height in `[143,200,300,500]`; no `T_star` | positive oriented rectangle | none | structural contour record | `contour_accounting_ambiguous` | unit/contract | false |
| `build_frozen_l3_contours` | `contour.py` | Build all four contours. | none | map height to contour | frozen config | four independent contours | none | structural contour inventory | missing height | unit/contract | false |
| `validate_chi3_metadata` | `chi3_function.py` | Verify frozen character identity. | metadata mapping | none or error | strings only | metadata matches 006H02 | OP25 | metadata audit | character mismatch | unit/contract | false |
| `evaluate_completed_l3` | `real_completed_l3.py` | Evaluate `Lambda_3` on a complex ball. | runtime, `ComplexBallRecord`, precision, evidence factory | `RealCompletedL3PointEvidence` | audited runtime, metadata exact | finite product ball | OP03-OP12, OP23-OP25 | completed L3 evidence | native L mismatch, nonfinite, precision leak | fake runtime, real-blocked smoke | true |
| `rectangular_hull` | `real_segment_enclosure.py` | Convert directed segment to rectangular input box. | `DirectedSegment` | `ComplexBallRecord` | valid endpoints | hull covers entire segment | OP01-OP02 | input-box record | reversed bounds | unit | false |
| `enclose_completed_l3_segment` | `real_segment_enclosure.py` | Certify whole segment image. | runtime, segment, precision, factory | `RealSegmentImageEvidence` | segment in frozen strip | entire segment covered | OP06-OP12, OP22 | segment image evidence | segment image may contain zero, whole-box missing | fake runtime, real-blocked smoke | true |
| `certify_real_half_plane` | `real_argument.py` | Certify local half-plane branch domain. | runtime, segment image, precision, factory | `RealHalfPlaneEvidence` | segment image belongs to same precision | strict rotated real lower bound | OP16, OP17 | half-plane evidence | zero not excluded, separation not strict | fake runtime, real-blocked smoke | true |
| `real_argument_increment` | `real_argument.py` | Compute local argument increment. | half-plane, start/end evidence, runtime | `RealArgumentIncrementEvidence` | branch certified at endpoints | real interval for delta arg | OP17-OP18 | argument increment evidence | branch not certified, mixed evidence | fake runtime, real-blocked smoke | true |
| `accumulate_real_winding` | `real_argument.py` | Sum increments and divide by `2*pi`. | increments, runtime, precision | `RealWindingEvidence` | common precision/provenance | unique nonnegative integer | OP19-OP21 | winding evidence | multiple/no integer, precision exhausted | fake runtime, real-blocked smoke | true |
| `certify_boundary_segment` | `boundary_certifier.py` | Certify one segment zero-free by subdivision. | backend, segment, precision, max depth | `BoundarySegmentCertificate` | whole segment covered | all pieces zero-free | OP15-OP16, OP22 | boundary certificate | boundary not certified zero-free | synthetic, real-blocked smoke | true |
| `certify_boundary_contour` | future extension of `boundary_certifier.py` | Certify all four edges for a contour. | contour, backend/runtime, precision | contour boundary report | positive contour | `boundary_zero_free=true` | repeated OP15-OP22 | contour boundary evidence | any edge fails | synthetic, real-blocked smoke | true |
| `count_contour_winding` | `l3_argument_count.py` or real facade | Count zeros inside one contour. | backend, contour, precision, max depth | winding/count certificate | boundary zero-free path available | unique integer winding | OP17-OP21 | count certificate | winding interval ambiguous | synthetic, real-blocked smoke | true |
| `certify_unique_integer_winding_bounds` | `winding_certifier.py` | Enforce exact integer containment. | lower/upper strings, precision | `StructuralWindingCertificate` | canonical endpoints | one nonnegative integer | OP21 | winding integer proof | no/multiple integer | unit | false |
| `_isolate_box` | `l3_certifier.py` | Recursive box isolation. | box, parent count, backend, config, precision, depth | zero certificates | parent count certified | individual boxes or failure | count contour route | zero isolation evidence | unresolved cluster, depth exhausted | synthetic, real-blocked smoke | true |
| `certify_l3` | `l3_certifier.py` | Coordinate L3 isolation and counts. | backend, config | `FunctionCertification` | metadata valid, backend complete | isolated zeros and matching counts | all L3 ops | H2 L3 certification | count mismatch, boundary fail | synthetic, full future real | true |
| `l3_zero_csv_bytes` | `serialization.py` | Serialize L3 zeros. | `FunctionCertification` | CSV bytes | L3 certification object | canonical UTF-8/LF | none | artifact bytes | serialization invalid | unit/contract | false |
| `l3_isolation_report_json_bytes` | `serialization.py` | Serialize isolation report. | `FunctionCertification` | JSON bytes | canonical data | sorted JSON, hashes | none | artifact bytes | missing field/hash mismatch | unit/contract | false |
| `l3_completeness_report_json_bytes` | `serialization.py` | Serialize completeness report. | `FunctionCertification` | JSON bytes | count records exist | sorted JSON, counts by height | none | artifact bytes | count mismatch | unit/contract | false |
| `require_execution_authorization` | `authorization.py` | Validate future real authorization. | auth path, expected hashes | `ExecutionAuthorization` | exact schema and hashes | validated token only | none | preflight evidence | auth/hash/runtime mismatch | contract | false |
| `PythonFlintBackend.initialize` | `python_flint_backend.py` | Lazy construct real FLINT module. | `ExecutionAuthorization` | initialized backend | 006F authorization true | FLINT imported only after gate | OP24-OP25 | backend identity | unauthorized import, version mismatch | guarded real smoke | true |

## 18. Phase Separation

006H12 authorizes none of these future phases. It defines their safe order only.

| Phase | Purpose | Execution allowed in that phase | 006H12 authorization |
| --- | --- | --- | --- |
| A | Real backend implementation with fake/synthetic fixtures only. | no FLINT real math; no `chi.l_function`; synthetic fixtures only | not authorized |
| B | Static review and semantic audit of implementation. | read-only, static scans, tests that avoid real backend | not authorized |
| C | Guarded real integration smoke with tiny authorized inputs. | only after separate authorization and sealed runtime | not authorized |
| D | Review of smoke artifacts. | documentary/artifact review | not authorized |
| E | 006F preauthorization. | schema/hash/runtime readiness only | not authorized |
| F | Full real H2 execution. | zeta and L3 certification under 006F | not authorized |

## 19. Future Test Levels

| Level | Name | Scope | Backend use | Purpose |
| --- | --- | --- | --- | --- |
| 1 | Pure unit tests | exact strings, contours, integer intervals, serialization | none | prove structural contracts |
| 2 | Synthetic runtime tests | fake Arb/Acb-like records | fake only | prove dataflow and failure states |
| 3 | Static semantic audit | scans, hash inventory, `NotImplementedError` inventory | none | prove no scope leak |
| 4 | Guarded backend construction tests | authorization gate only | import only after gate, no real math unless authorized | prove fail-closed behavior |
| 5 | Tiny real smoke | minimal fixed boxes | sealed FLINT/Arb/Acb, separately authorized | prove adapter can produce bounded evidence |
| 6 | Full 006F H2 execution | all heights and artifacts | sealed backend, separately authorized | produce H2 certification candidate |

Level 5 and Level 6 require separate explicit authorization.

## 20. Required Failure States

Future implementation must expose and preserve these states:

```text
authorization_missing
authorization_schema_invalid
approved_code_hash_mismatch
protocol_hash_mismatch
runtime_missing
runtime_mismatch
backend_version_mismatch
ARB_SEAL_POLICY_BLOCKED
native_L_semantics_mismatch
backend_semantics_insufficient
effective_precision_below_request
precision_budget_exhausted
subdivision_budget_exhausted
whole_box_semantics_missing
segment_image_contains_or_may_contain_zero
boundary_not_certified_zero_free
principal_log_branch_not_certified
argument_increment_not_certified
winding_interval_contains_no_integer
winding_interval_contains_multiple_integers
completed_function_equivalence_unproved
contour_accounting_ambiguous
pole_or_trivial_zero_accounting_unproved
multiplicity_unresolved
unresolved_cluster
count_mismatch
serialization_semantics_invalid
artifact_hash_mismatch
scope_or_semantic_leak
```

No failure state may be converted into success by widening scope, changing
heights, assuming RH/GRH or relying on approximate decimal agreement.

## 21. Master Matrix

| 006H02_obligation | real_backend_operation | python_function | evidence_artifact | synthetic_test | real_smoke_test | full_006F_use | current_status | blocking_gap |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `chi_3_definition_frozen` | OP25 | `validate_chi3_metadata` | metadata audit | yes | yes | yes | partial | native character construction unverified |
| `completed_function_definition` | OP03-OP12 | `evaluate_completed_l3` | completed L3 evidence | yes | required | required | partial | real FLINT runtime missing |
| `equivalence_to_target_nontrivial_zeros` | proof package | proof validator future | proof package hashes | contract only | no | yes | missing | local theorem package absent |
| `contour_definition` | contour construction | `build_frozen_l3_contours` | contour inventory | yes | no | yes | satisfied structurally | none for code plan |
| `exact_T_boundary` | contour construction | `build_frozen_l3_contour` | contour records | yes | no | yes | satisfied structurally | no real certificates |
| `boundary_zero_free_certificate` | OP15-OP16, OP22 | `certify_boundary_segment`, future `certify_boundary_contour` | boundary certificates | yes | required | required | partial | real zero exclusion missing |
| `segment_image_excludes_zero` | OP12, OP15-OP16, OP22 | `enclose_completed_l3_segment` | segment image evidence | yes | required | required | partial | whole-box Acb semantics unverified |
| `ball_validated_subdivision` | OP01-OP02, OP22 | `subdivide_segment_cover` | subdivision certificates | yes | required | required | partial | real operation trace missing |
| `argument_increment_enclosures` | OP17-OP18 | `real_argument_increment` | argument increment evidence | yes | required | required | partial | branch semantics unverified |
| `total_winding_unique_integer` | OP19-OP21 | `accumulate_real_winding`, `certify_unique_integer_winding_bounds` | winding evidence | yes | required | required | partial | real interval too-wide risk |
| `four_independent_contours` | repeated contour count | `certify_l3` | count records by height | yes | required | required | partial | real certificates absent |
| `multiplicity_accounting` | local rectangle winding | `_isolate_box`, future isolator facade | zero certificates | yes | required | required | partial | real multiplicity proof missing |
| `cluster_handling` | recursive subdivision/counting | `_isolate_box` | unresolved cluster report | yes | required | required | partial | real cluster resolution missing |
| `symmetry_accounting` | proof/report field | `certify_l3` | L3 completeness report | yes | no | yes | partial | proof package and report audit missing |
| `no_RH_or_GRH_dependency` | contract audit | `certify_l3`, serializers | forbidden assumptions field | yes | yes | yes | partial | final report fields must be audited |
| `native_L_ball_semantics` | OP10 | future `PythonFlintBackend.native_dirichlet_l` | backend semantic report | no | required | required | missing | candidate API unverified |
| `Hurwitz_control` | OP11 | future control function | control comparison report | fake possible | optional required by plan | optional/secondary | missing | candidate API unverified |
| `origin_exclusion` | OP15-OP16 | boundary/argument functions | separation witness | yes | required | required | partial | real witness missing |
| `local_log_branch` | OP17 | `certify_real_half_plane`, `real_argument_increment` | branch certificate | yes | required | required | partial | Acb branch semantics unverified |
| `division_by_2pi` | OP03, OP20 | `accumulate_real_winding` | winding interval | yes | required | required | partial | real pi ball route unverified |
| `integer_containment` | OP21 | `winding_certifier.py` | unique integer certificate | yes | yes | yes | satisfied structurally | exported real interval canonicalization future |
| `runtime_seal` | OP24 | `require_execution_authorization`, backend initialize | runtime/backend seal | contract | required | required | missing | actual version/hash seal absent |
| `artifact_traceability` | serialization/hash | serializers and pipeline | JSON/CSV/SHA256SUMS | yes | required | required | partial | final H2 manifest future |

## 22. Final Decisions

```text
REAL_BACKEND_CODE_PLAN = COMPLETE
ARB_SEAL_POLICY = DEFINED
NATIVE_L_SEMANTIC_PLAN = DEFINED
LAMBDA3_BALL_EVALUATION_PLAN = DEFINED
BOUNDARY_CERTIFICATION_PLAN = DEFINED
ARGUMENT_INCREMENT_PLAN = DEFINED
WINDING_PLAN = DEFINED
ZERO_ISOLATION_PLAN = DEFINED

L3_READY_FOR_SEPARATE_REAL_BACKEND_CODE_AUTHORIZATION = true
L3_READY_FOR_REAL_BACKEND_IMPLEMENTATION = false
L3_READY_FOR_REAL_EXECUTION = false
NEXT_PHASE_AUTHORIZED = false
```

Interpretation:

```text
L3_READY_FOR_SEPARATE_REAL_BACKEND_CODE_AUTHORIZATION = true
```

means that the plan is sufficiently specified for the user to authorize a
future implementation phase. It does not authorize that phase.

```text
L3_READY_FOR_REAL_BACKEND_IMPLEMENTATION = false
```

means no implementation is active inside 006H12.

```text
L3_READY_FOR_REAL_EXECUTION = false
```

means real backend math, contours, zero isolation, zero counts, H2 and 006F all
remain blocked.

## 23. Closing State

```text
006H12_RESULT =
006H12_L3_REAL_BACKEND_CODE_PLAN_AND_SEMANTIC_MAP_COMPLETED

CODE_MODIFIED = false
TESTS_EXECUTED = false
FLINT_EXECUTED = false
ARB_EXECUTED = false
ACB_EXECUTED = false
CHI_L_FUNCTION_CALLED = false
LAMBDA_3_EVALUATED = false
CONTOURS_EXECUTED = false
ZEROS_ISOLATED = false
ZEROS_COUNTED = false
H2_OPENED = false
006F_OPENED = false
DOWNSTREAM_AUTHORIZED = false
NOVELTY_CLAIMED = false
NEXT_PHASE_AUTHORIZED = false
```

Any future real backend implementation, smoke execution, preflight, 006F phase
or H2 run requires separate explicit authorization.
