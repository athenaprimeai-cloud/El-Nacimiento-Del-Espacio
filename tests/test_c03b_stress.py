import unittest
import tempfile
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

from athena_azr.c03b_stress import (
    build_c03b_audit,
    fit_log_frequency,
    hash_files,
    max_t_permutation_test,
    permute_within_classes,
    protected_baseline_paths,
    spectral_power,
    write_c03b_artifacts,
)


class C03BStressTests(unittest.TestCase):
    def test_permutation_preserves_values_inside_each_modular_class(self):
        values = np.asarray([10.0, 11.0, 12.0, 13.0, 14.0, 15.0])
        classes = np.asarray([0, 1, 2, 0, 1, 2])
        rng = np.random.default_rng(20260610)

        permuted = permute_within_classes(values, classes, rng)

        for residue in (0, 1, 2):
            mask = classes == residue
            self.assertEqual(sorted(permuted[mask]), sorted(values[mask]))
        self.assertFalse(np.array_equal(permuted, values))

    def test_spectral_power_peaks_at_the_injected_log_frequency(self):
        log_x = np.linspace(0.0, 8.0, 400)
        residual = np.cos(6.25 * log_x) + (0.2 * np.sin(6.25 * log_x))
        frequencies = np.asarray([4.0, 6.25, 9.0])

        powers = spectral_power(log_x, residual, frequencies)

        self.assertEqual(int(np.argmax(powers)), 1)
        self.assertGreater(powers[1], 10.0 * max(powers[0], powers[2]))

    def test_max_t_uses_global_control_maxima_and_is_reproducible(self):
        log_x = np.linspace(0.0, 6.0, 120)
        residual = np.cos(5.0 * log_x)
        classes = np.arange(len(log_x)) % 3
        frequencies = np.linspace(1.0, 9.0, 81)

        first = max_t_permutation_test(
            log_x,
            residual,
            classes,
            frequencies,
            controls=39,
            seed=17,
        )
        second = max_t_permutation_test(
            log_x,
            residual,
            classes,
            frequencies,
            controls=39,
            seed=17,
        )

        self.assertEqual(first.p_fwer, second.p_fwer)
        np.testing.assert_allclose(first.control_maxima, second.control_maxima)
        self.assertEqual(len(first.control_maxima), 39)
        self.assertAlmostEqual(first.rayleigh_resolution, 2.0 * np.pi / 6.0, places=12)
        expected = (1 + np.count_nonzero(first.control_maxima >= first.real_maximum)) / 40
        self.assertEqual(first.p_fwer, expected)
        self.assertLessEqual(first.p_fwer, 0.1)

    def test_frequency_fit_recovers_coefficient_and_scores_holdout(self):
        frequency = 8.0
        coefficient = 0.3 - 0.2j
        log_x = np.linspace(0.0, 10.0, 300)
        target = 2.0 * np.real(coefficient * np.exp(1j * frequency * log_x))

        result = fit_log_frequency(
            log_x[:200],
            target[:200],
            log_x[200:],
            target[200:],
            frequency,
        )

        self.assertAlmostEqual(result.estimated_real, coefficient.real, places=12)
        self.assertAlmostEqual(result.estimated_imag, coefficient.imag, places=12)
        self.assertLess(result.validation_rmse, 1e-12)

    def test_file_hashes_change_only_when_content_changes(self):
        with tempfile.TemporaryDirectory() as directory:
            first = Path(directory) / "first.txt"
            second = Path(directory) / "second.txt"
            first.write_text("alpha", encoding="utf-8")
            second.write_text("beta", encoding="utf-8")

            before = hash_files((first, second))
            first.write_text("changed", encoding="utf-8")
            after = hash_files((first, second))

            self.assertNotEqual(before[str(first)], after[str(first)])
            self.assertEqual(before[str(second)], after[str(second)])

    def test_small_audit_builds_all_falsification_families(self):
        result = build_c03b_audit(
            max_x=1_000,
            min_x=50,
            log_samples=80,
            window_maxima=(300, 1_000),
            ablation_counts=(0, 1, 2),
            full_chi3_zero_height=30.0,
            zeta_zero_height=30.0,
            random_frequency_controls=3,
            max_t_controls=9,
            max_t_frequency_min=1.0,
            max_t_frequency_max=20.0,
            max_t_frequency_step=0.5,
            seed=20260610,
        )

        self.assertEqual(result.window_maxima, (300, 1_000))
        self.assertEqual(result.ablation_counts, (0, 1, 2))
        self.assertEqual(
            {(row.window_max, row.zero_count, row.model, row.split) for row in result.ablations},
            {
                (window, count, model, split)
                for window in (300, 1_000)
                for count in (0, 1, 2)
                for model in ("M1_pole_lzeros", "M2_pole_lzeros_cross")
                for split in ("discovery", "validation")
            },
        )
        self.assertEqual(len(result.windows), 2)
        self.assertEqual(len(result.wrong_frequencies), 1 + 2 + 3)
        self.assertEqual(len(result.max_t.control_maxima), 9)
        self.assertFalse(result.novelty_claim)
        self.assertEqual(result.experiment_status, "falsification_audit")

    def test_artifacts_are_isolated_and_record_immutability(self):
        result = build_c03b_audit(
            max_x=600,
            min_x=50,
            log_samples=50,
            window_maxima=(300, 600),
            ablation_counts=(0, 1, 2),
            full_chi3_zero_height=30.0,
            zeta_zero_height=30.0,
            random_frequency_controls=2,
            max_t_controls=5,
            max_t_frequency_min=1.0,
            max_t_frequency_max=15.0,
            max_t_frequency_step=0.5,
            seed=13,
        )

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            protected = root / "c03_summary_X1e6.json"
            protected.write_text('{"locked": true}\n', encoding="utf-8")
            before = hash_files((protected,))
            output = root / "c03b_stress_tests"

            paths = write_c03b_artifacts(output, result, before)
            summary = json.loads(paths["summary_json"].read_text(encoding="utf-8"))

            self.assertEqual(before, hash_files((protected,)))
            self.assertTrue(summary["immutability_passed"])
            self.assertFalse(summary["novelty_claim"])
            self.assertEqual(summary["novelty_status"], "not_established")
            self.assertIn("peak_classification", summary["max_t"])
            self.assertEqual(summary["expansion_status"], "controlled_truncation_audit")
            self.assertIn("no descubre una frecuencia nueva", summary["interpretation"].lower())
            names = {path.name.lower() for path in output.iterdir()}
            self.assertTrue(any("ablation" in name for name in names))
            self.assertTrue(any("max_t" in name for name in names))
            self.assertFalse(any("c05" in name or "c35" in name or "c15" in name for name in names))

    def test_protected_paths_include_baselines_but_exclude_c03b_outputs(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            artifacts = root / "artifacts"
            stress = artifacts / "goldbach_cesaro" / "c03b_stress_tests"
            stress.mkdir(parents=True)
            expected = (
                artifacts / "c03_summary_X1e6.json",
                artifacts / "goldbach_cesaro" / "goldbach_005a_summary_1000_1000000.json",
                artifacts / "future_c05_lock.json",
            )
            for path in expected:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("locked", encoding="utf-8")
            (stress / "c03b_summary_X1e6.json").write_text("new", encoding="utf-8")

            protected = protected_baseline_paths(root)

            self.assertEqual(set(protected), set(expected))

    def test_runner_smoke_writes_isolated_artifacts(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "stress"
            command = [
                sys.executable,
                "scripts/run_c03b_stress.py",
                "--max-x", "300",
                "--min-x", "50",
                "--log-samples", "40",
                "--windows", "200,300",
                "--ablation-counts", "0,1",
                "--chi3-zero-height", "16",
                "--zeta-zero-height", "20",
                "--random-frequency-controls", "1",
                "--max-t-controls", "3",
                "--max-t-frequency-min", "1",
                "--max-t-frequency-max", "12",
                "--max-t-frequency-step", "1",
                "--output-dir", str(output),
            ]

            completed = subprocess.run(
                command,
                cwd=Path(__file__).resolve().parents[1],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertTrue((output / "c03b_summary_X300.json").is_file())


if __name__ == "__main__":
    unittest.main()
