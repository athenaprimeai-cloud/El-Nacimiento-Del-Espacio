import math
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np

from athena_azr.c05_laplace_chi5 import (
    C05_ALLOWED_MODELS,
    C05_IMPLEMENTATION_STATUS,
    C05_OFFICIAL_STATUS,
    C05_RETROSPECTIVE_APPROVAL,
    CHI5_B0,
    CHI5_ZERO_ORDINATES,
    c05_cross_normalized,
    c05_linear_coefficient,
    c05_linear_normalized,
    c05_pole_normalized,
    build_c05_experiment,
    chi5_values,
    chi5_zeros_up_to,
    dirichlet_l_chi5,
    mixed_cesaro_c2_direct,
    mixed_cesaro_c2_from_prefix,
    mixed_convolution_direct,
    mixed_convolution_fft,
    protected_c05_baseline_paths,
    canonical_c05_protocol_hash,
    validate_c05_output_dir,
    validate_c05_execution_authorization,
    validate_c05_rerun_protocol,
    write_c05_artifacts,
)
from athena_azr.c03b_stress import hash_files
from athena_azr.cesaro_calibration import (
    cesaro_prefix_moments,
    riemann_zeros_up_to,
    von_mangoldt_values,
)


class C05LaplaceChi5Tests(unittest.TestCase):
    def test_c05_is_explicitly_quarantined_and_not_official(self):
        self.assertEqual(C05_IMPLEMENTATION_STATUS, "provisional_quarantined")
        self.assertEqual(C05_OFFICIAL_STATUS, "not_accepted")
        self.assertEqual(C05_RETROSPECTIVE_APPROVAL, "rejected_for_now")

    def test_chi5_values_follow_quadratic_character_modulo_five(self):
        self.assertEqual(
            chi5_values(10).tolist(),
            [0, 1, -1, -1, 1, 0, 1, -1, -1, 1, 0],
        )

    def test_local_origin_data_matches_audited_derivation(self):
        step = 1e-5
        derivative = (
            dirichlet_l_chi5(step) - dirichlet_l_chi5(-step)
        ) / (2.0 * step)

        self.assertLess(abs(dirichlet_l_chi5(0.0)), 1e-12)
        self.assertAlmostEqual(derivative.real, math.log((1.0 + math.sqrt(5.0)) / 2.0), places=9)
        self.assertAlmostEqual(derivative.imag, 0.0, places=12)
        self.assertAlmostEqual(CHI5_B0, -0.022024657838726918, places=15)

    def test_first_zero_is_correct_and_foreign_values_are_rejected(self):
        first = 6.648453344727717

        self.assertAlmostEqual(CHI5_ZERO_ORDINATES[0], first, places=12)
        self.assertLess(abs(dirichlet_l_chi5(0.5 + (1j * first))), 1e-10)
        self.assertGreater(abs(dirichlet_l_chi5(0.5 + (1j * 6.0206))), 1e-3)
        self.assertGreater(abs(dirichlet_l_chi5(0.5 + (1j * 9.810574))), 1e-3)

    def test_zero_table_filters_by_height(self):
        zeros = chi5_zeros_up_to(12.0)

        self.assertGreaterEqual(len(zeros), 3)
        self.assertTrue(all(value <= 12.0 for value in zeros))
        self.assertEqual(zeros, tuple(sorted(zeros)))
        self.assertEqual(len(CHI5_ZERO_ORDINATES), 86)
        self.assertGreater(CHI5_ZERO_ORDINATES[-1], 143.0)
        self.assertEqual(len(chi5_zeros_up_to(143.0)), 85)

    def test_pole_background_contains_x_log_x_with_derived_sign(self):
        xs = np.asarray([100.0, 10_000.0])
        expected = ((11.0 / 6.0) - CHI5_B0 - np.log(xs)) / (6.0 * np.sqrt(xs))

        np.testing.assert_allclose(c05_pole_normalized(xs), expected, rtol=0.0, atol=1e-15)
        self.assertTrue(np.all(c05_pole_normalized(xs) < 0.0))

    def test_twisted_fft_matches_direct_convolution(self):
        mangoldt = von_mangoldt_values(80)
        twisted = mangoldt * chi5_values(80)

        direct = mixed_convolution_direct(mangoldt, twisted, max_n=80)
        fast = mixed_convolution_fft(mangoldt, twisted, max_n=80)

        np.testing.assert_allclose(fast, direct, rtol=1e-11, atol=1e-10)

    def test_mixed_prefix_cesaro_matches_direct_definition(self):
        mangoldt = von_mangoldt_values(40)
        twisted = mangoldt * chi5_values(40)
        values = mixed_convolution_direct(mangoldt, twisted, max_n=40)
        moments = cesaro_prefix_moments(values)

        for x in (8, 20, 40):
            self.assertAlmostEqual(
                mixed_cesaro_c2_from_prefix(moments, x),
                mixed_cesaro_c2_direct(values, x),
                places=10,
            )

    def test_linear_and_cross_models_are_real_and_finite(self):
        xs = np.asarray([1_000.0, 5_000.0, 20_000.0])
        l_zeros = chi5_zeros_up_to(20.0)
        zeta_zeros = riemann_zeros_up_to(31.0)

        linear = c05_linear_normalized(xs, l_zeros)
        cross = c05_cross_normalized(xs, zeta_zeros, l_zeros)

        self.assertTrue(np.isrealobj(linear))
        self.assertTrue(np.isrealobj(cross))
        self.assertTrue(np.all(np.isfinite(linear)))
        self.assertTrue(np.all(np.isfinite(cross)))

    def test_linear_coefficient_and_allowed_models_match_mixed_generator(self):
        rho = 0.5 + (1j * CHI5_ZERO_ORDINATES[0])
        expected = -1.0 / (rho * (rho + 1.0) * (rho + 2.0) * (rho + 3.0))

        self.assertAlmostEqual(c05_linear_coefficient(rho).real, expected.real, places=14)
        self.assertAlmostEqual(c05_linear_coefficient(rho).imag, expected.imag, places=14)
        self.assertEqual(
            C05_ALLOWED_MODELS,
            ("M0_local", "M1_local_lzeros", "M2_local_lzeros_cross"),
        )
        self.assertFalse(any("l5_l5" in model.lower() for model in C05_ALLOWED_MODELS))

    def test_build_experiment_scores_only_authorized_models(self):
        result = build_c05_experiment(
            max_x=500,
            min_x=50,
            log_samples=40,
            chi5_zero_heights=(20.0,),
            zeta_zero_height=30.0,
        )

        self.assertEqual(
            {(metric.split, metric.model) for metric in result.metrics},
            {
                ("discovery", "M0_local"),
                ("discovery", "M1_local_lzeros"),
                ("discovery", "M2_local_lzeros_cross"),
                ("validation", "M0_local"),
                ("validation", "M1_local_lzeros"),
                ("validation", "M2_local_lzeros_cross"),
            },
        )
        self.assertEqual(result.frozen_channels, ("C00", "C03", "C03-B", "C35", "C15"))
        self.assertFalse(result.explicit_formula_complete)
        self.assertTrue(result.samples)

    def test_artifacts_declare_controlled_truncation_and_immutability(self):
        result = build_c05_experiment(
            max_x=500,
            min_x=50,
            log_samples=30,
            chi5_zero_heights=(20.0,),
            zeta_zero_height=30.0,
        )

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            protected = root / "c03_summary_X1e6.json"
            protected.write_text('{"locked": true}\n', encoding="utf-8")
            hashes = hash_files((protected,))
            output = root / "c05_controlled"
            paths = write_c05_artifacts(output, result, hashes)
            summary = json.loads(paths["summary_json"].read_text(encoding="utf-8"))

            self.assertEqual(hashes, hash_files((protected,)))
            self.assertTrue(summary["immutability_passed"])
            self.assertFalse(summary["explicit_formula_complete"])
            self.assertEqual(summary["expansion_status"], "controlled_truncation")
            self.assertEqual(summary["double_terms"], "zeta-L5 crosses only")
            self.assertFalse(summary["novelty_claim"])
            self.assertEqual(summary["local_background"], "X/6 * (H3 - b0 - log X)")
            self.assertIsInstance(summary["numerical_calibration_passed"], bool)
            self.assertFalse(summary["calibration_passed"])
            self.assertEqual(summary["calibration_status"], "provisional_quarantined")
            self.assertEqual(summary["official_status"], "not_accepted")
            self.assertFalse(summary["eligible_for_downstream_use"])

    def test_rerun_protocol_requires_prior_seal_and_approval(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            missing = root / "missing.json"
            with self.assertRaisesRegex(RuntimeError, "sealed protocol"):
                validate_c05_rerun_protocol(missing)

            unapproved = root / "unapproved.json"
            unapproved.write_text(
                json.dumps(
                    {
                        "experiment_id": "G5B-005E-R",
                        "status": "draft",
                        "approved": False,
                    }
                ),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(RuntimeError, "not approved"):
                validate_c05_rerun_protocol(unapproved)

    def test_sealed_protocol_hash_is_verified_without_authorizing_execution(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            payload = {
                "parameters": {"min_x": 1000, "max_x": 1_000_000},
                "falsifiers": ["wrong_frequency", "ablation"],
                "execution_authorized": False,
            }
            protocol = root / "C05_SEALED_PROTOCOL.json"
            protocol.write_text(
                json.dumps(
                    {
                        "experiment_id": "G5B-005E-R",
                        "status": "sealed_pending_execution_authorization",
                        "approved": True,
                        "approved_by": "project_owner",
                        "sealed_at": "2026-06-11T00:00:00-04:00",
                        "hash_definition": "sha256_canonical_json_of_sealed_payload",
                        "protocol_sha256": canonical_c05_protocol_hash(payload),
                        "sealed_payload": payload,
                    }
                ),
                encoding="utf-8",
            )

            validated = validate_c05_rerun_protocol(protocol)
            self.assertEqual(validated["sealed_payload"], payload)
            with self.assertRaisesRegex(RuntimeError, "execution authorization"):
                validate_c05_execution_authorization(None, validated["protocol_sha256"])

            tampered = json.loads(protocol.read_text(encoding="utf-8"))
            tampered["sealed_payload"]["parameters"]["max_x"] = 999
            protocol.write_text(json.dumps(tampered), encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "hash mismatch"):
                validate_c05_rerun_protocol(protocol)

    def test_clean_rerun_cannot_overwrite_quarantine_archive(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            archive = root / "artifacts" / "goldbach_cesaro" / "c05_controlled"
            clean = root / "artifacts" / "goldbach_cesaro" / "c05_rerun_clean"

            with self.assertRaisesRegex(RuntimeError, "quarantine archive"):
                validate_c05_output_dir(archive, root)
            clean.mkdir(parents=True)
            (clean / "C05_SEALED_PROTOCOL.json").write_text("{}\n", encoding="utf-8")
            self.assertEqual(validate_c05_output_dir(clean, root), clean.resolve())
            (clean / "unexpected.csv").write_text("data\n", encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "unexpected files"):
                validate_c05_output_dir(clean, root)

    def test_protected_paths_exclude_c05_output_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            artifacts = root / "artifacts"
            protected = artifacts / "c03_summary_X1e6.json"
            c05_output = artifacts / "goldbach_cesaro" / "c05_controlled" / "c05_summary_X1e6.json"
            protected.parent.mkdir(parents=True)
            c05_output.parent.mkdir(parents=True)
            protected.write_text("locked", encoding="utf-8")
            c05_output.write_text("replaceable", encoding="utf-8")

            paths = protected_c05_baseline_paths(root)

            self.assertIn(protected, paths)
            self.assertNotIn(c05_output, paths)

    def test_runner_refuses_to_write_without_sealed_protocol(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "c05"
            command = [
                sys.executable,
                "scripts/run_c05_laplace.py",
                "--max-x", "500",
                "--min-x", "50",
                "--log-samples", "40",
                "--chi5-zero-heights", "20",
                "--zeta-zero-height", "30",
                "--output-dir", str(output),
            ]

            completed = subprocess.run(
                command,
                cwd=Path(__file__).resolve().parents[1],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("quarantined", (completed.stdout + completed.stderr).lower())
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
