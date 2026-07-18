import json
import math
import tempfile
import unittest
from pathlib import Path

import numpy as np

from athena_azr.cesaro_calibration import (
    additive_convolution_direct,
    additive_convolution_fft,
    build_cesaro_calibration,
    cesaro_c2_direct,
    cesaro_c2_from_prefix,
    cesaro_prefix_moments,
    complex_log_gamma,
    explicit_double_normalized,
    explicit_linear_normalized,
    explicit_pole_correction_normalized,
    linear_zero_coefficient,
    logarithmic_integer_grid,
    riemann_zeros_up_to,
    von_mangoldt_values,
    write_calibration_artifacts,
)


class CesaroCalibrationTests(unittest.TestCase):
    def test_von_mangoldt_marks_prime_powers_only(self):
        values = von_mangoldt_values(10)

        self.assertAlmostEqual(values[2], math.log(2))
        self.assertAlmostEqual(values[3], math.log(3))
        self.assertAlmostEqual(values[4], math.log(2))
        self.assertAlmostEqual(values[5], math.log(5))
        self.assertEqual(values[6], 0.0)
        self.assertAlmostEqual(values[8], math.log(2))
        self.assertAlmostEqual(values[9], math.log(3))
        self.assertEqual(values[10], 0.0)

    def test_direct_additive_convolution_matches_small_goldbach_weights(self):
        mangoldt = von_mangoldt_values(6)
        values = additive_convolution_direct(mangoldt, max_n=6)

        self.assertAlmostEqual(values[4], math.log(2) ** 2)
        self.assertAlmostEqual(values[5], 2.0 * math.log(2) * math.log(3))
        self.assertAlmostEqual(values[6], 2.0 * math.log(2) ** 2 + math.log(3) ** 2)

    def test_fft_convolution_matches_direct_convolution(self):
        mangoldt = von_mangoldt_values(80)
        direct = additive_convolution_direct(mangoldt, max_n=80)
        fast = additive_convolution_fft(mangoldt, max_n=80)

        np.testing.assert_allclose(fast, direct, rtol=1e-11, atol=1e-10)

    def test_prefix_cesaro_matches_direct_definition(self):
        mangoldt = von_mangoldt_values(30)
        goldbach = additive_convolution_direct(mangoldt, max_n=30)
        moments = cesaro_prefix_moments(goldbach)

        for x in (6, 12, 30):
            self.assertAlmostEqual(
                cesaro_c2_from_prefix(moments, x),
                cesaro_c2_direct(goldbach, x),
                places=10,
            )

    def test_logarithmic_grid_is_sorted_unique_and_keeps_endpoints(self):
        grid = logarithmic_integer_grid(100, 1000, 30)

        self.assertEqual(grid[0], 100)
        self.assertEqual(grid[-1], 1000)
        self.assertEqual(grid, sorted(set(grid)))

    def test_certified_zero_table_filters_by_height(self):
        zeros = riemann_zeros_up_to(22.0)

        self.assertEqual(len(zeros), 2)
        self.assertAlmostEqual(zeros[0], 14.134725141734693, places=12)
        self.assertAlmostEqual(zeros[1], 21.022039638771556, places=12)

    def test_complex_log_gamma_matches_positive_real_values(self):
        self.assertAlmostEqual(complex_log_gamma(1.0 + 0.0j).real, 0.0, places=12)
        self.assertAlmostEqual(complex_log_gamma(0.5 + 0.0j).real, 0.5 * math.log(math.pi), places=12)
        self.assertAlmostEqual(complex_log_gamma(1.0 + 0.0j).imag, 0.0, places=12)

    def test_linear_zero_coefficient_uses_gamma_ratio_identity(self):
        rho = 0.5 + 14.134725141734693j
        expected = -2.0 / (rho * (rho + 1.0) * (rho + 2.0) * (rho + 3.0))

        self.assertAlmostEqual(linear_zero_coefficient(rho).real, expected.real, places=14)
        self.assertAlmostEqual(linear_zero_coefficient(rho).imag, expected.imag, places=14)

    def test_pole_correction_includes_the_known_order_x_term(self):
        xs = np.asarray([100.0, 10_000.0])

        correction = explicit_pole_correction_normalized(xs)
        expected = -(math.log(2.0 * math.pi) / 3.0) / np.sqrt(xs)

        np.testing.assert_allclose(correction, expected, rtol=0.0, atol=1e-15)

    def test_explicit_models_are_real_for_conjugate_zero_sets(self):
        xs = np.asarray([1000.0, 2000.0, 5000.0])
        zeros = riemann_zeros_up_to(31.0)

        linear = explicit_linear_normalized(xs, zeros)
        double = explicit_double_normalized(xs, zeros)

        self.assertTrue(np.all(np.isfinite(linear)))
        self.assertTrue(np.all(np.isfinite(double)))
        self.assertTrue(np.isrealobj(linear))
        self.assertTrue(np.isrealobj(double))

    def test_build_calibration_separates_splits_and_scores_three_models(self):
        result = build_cesaro_calibration(
            max_x=500,
            min_x=50,
            log_samples=40,
            zero_heights=(50.0,),
        )

        self.assertEqual(result.max_x, 500)
        self.assertEqual(result.zero_source, "Andrew Odlyzko, Tables of zeros of the Riemann zeta function")
        self.assertTrue(result.samples)
        self.assertTrue(any(sample.split == "discovery" for sample in result.samples))
        self.assertTrue(any(sample.split == "validation" for sample in result.samples))
        self.assertEqual(
            {(metric.split, metric.model) for metric in result.metrics},
            {
                ("discovery", "M0_pole_correction"),
                ("discovery", "M1_pole_linear"),
                ("discovery", "M2_pole_linear_double"),
                ("validation", "M0_pole_correction"),
                ("validation", "M1_pole_linear"),
                ("validation", "M2_pole_linear_double"),
            },
        )
        self.assertTrue(all(math.isfinite(metric.rmse) for metric in result.metrics))
        self.assertEqual(len(result.coefficient_audits), result.metrics[0].zero_count)
        self.assertTrue(all(math.isfinite(audit.amplitude_ratio) for audit in result.coefficient_audits))
        self.assertTrue(all(-math.pi <= audit.phase_error <= math.pi for audit in result.coefficient_audits))
        self.assertLess(max(check.absolute_error for check in result.convolution_checks), 1e-9)

    def test_artifact_writer_creates_machine_readable_outputs(self):
        result = build_cesaro_calibration(
            max_x=200,
            min_x=20,
            log_samples=20,
            zero_heights=(50.0,),
        )

        with tempfile.TemporaryDirectory() as directory:
            paths = write_calibration_artifacts(Path(directory), result)
            summary = json.loads(paths["summary_json"].read_text(encoding="utf-8"))

            self.assertTrue(paths["samples_csv"].exists())
            self.assertTrue(paths["metrics_csv"].exists())
            self.assertTrue(paths["checks_csv"].exists())
            self.assertTrue(paths["coefficient_audits_csv"].exists())
            self.assertEqual(summary["experiment_id"], "G5A-005")
            self.assertEqual(summary["window"], {"min": 20, "max": 200})
            self.assertEqual(summary["zero_heights"], [50.0])
            self.assertIn("calibration_passed", summary)
            self.assertIn("calibration_criteria", summary)


if __name__ == "__main__":
    unittest.main()
