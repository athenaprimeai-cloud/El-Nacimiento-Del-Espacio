import json
import math
import tempfile
import unittest
from pathlib import Path

import numpy as np

from athena_azr.c03_laplace_chi3 import (
    build_c03_experiment,
    c03_cross_normalized,
    c03_linear_coefficient,
    c03_linear_normalized,
    c03_pole_normalized,
    chi3_log_derivative_at_zero,
    chi3_values,
    chi3_zeros_up_to,
    dirichlet_l_chi3,
    mixed_cesaro_c2_direct,
    mixed_cesaro_c2_from_prefix,
    mixed_convolution_direct,
    mixed_convolution_fft,
    write_c03_artifacts,
)
from athena_azr.cesaro_calibration import (
    cesaro_prefix_moments,
    riemann_zeros_up_to,
    von_mangoldt_values,
)


class C03LaplaceChi3Tests(unittest.TestCase):
    def test_chi3_values_follow_modulo_three_definition(self):
        self.assertEqual(chi3_values(8).tolist(), [0, 1, -1, 0, 1, -1, 0, 1, -1])

    def test_log_derivative_at_zero_matches_closed_form(self):
        self.assertAlmostEqual(chi3_log_derivative_at_zero(), 0.9481988266726209, places=14)

    def test_first_chi3_zero_and_rejects_foreign_frequencies(self):
        first_zero = 8.039737155681468

        self.assertLess(abs(dirichlet_l_chi3(0.5 + (1j * first_zero))), 1e-10)
        self.assertGreater(abs(dirichlet_l_chi3(0.5 + (1j * 4.5324))), 1e-3)
        self.assertGreater(abs(dirichlet_l_chi3(0.5 + (1j * 7.8096))), 1e-3)

    def test_chi3_zero_table_filters_by_height(self):
        zeros = chi3_zeros_up_to(16.0)

        self.assertEqual(len(zeros), 3)
        self.assertAlmostEqual(zeros[0], 8.039737155681468, places=12)
        self.assertAlmostEqual(zeros[2], 15.704619176721625, places=12)

    def test_twisted_fft_matches_direct_convolution(self):
        mangoldt = von_mangoldt_values(80)
        twisted = mangoldt * chi3_values(80)

        direct = mixed_convolution_direct(mangoldt, twisted, max_n=80)
        fast = mixed_convolution_fft(mangoldt, twisted, max_n=80)

        np.testing.assert_allclose(fast, direct, rtol=1e-11, atol=1e-10)

    def test_mixed_prefix_cesaro_matches_direct_definition(self):
        mangoldt = von_mangoldt_values(40)
        twisted = mangoldt * chi3_values(40)
        values = mixed_convolution_direct(mangoldt, twisted, max_n=40)
        moments = cesaro_prefix_moments(values)

        for x in (8, 20, 40):
            self.assertAlmostEqual(
                mixed_cesaro_c2_from_prefix(moments, x),
                mixed_cesaro_c2_direct(values, x),
                places=10,
            )

    def test_pole_model_has_negative_fixed_coefficient(self):
        xs = np.asarray([100.0, 10_000.0])
        expected = -(chi3_log_derivative_at_zero() / 6.0) / np.sqrt(xs)

        np.testing.assert_allclose(c03_pole_normalized(xs), expected, rtol=0.0, atol=1e-15)

    def test_linear_coefficient_uses_single_mixed_factor(self):
        rho = 0.5 + 8.039737155681468j
        expected = -1.0 / (rho * (rho + 1.0) * (rho + 2.0) * (rho + 3.0))

        self.assertAlmostEqual(c03_linear_coefficient(rho).real, expected.real, places=14)
        self.assertAlmostEqual(c03_linear_coefficient(rho).imag, expected.imag, places=14)

    def test_linear_and_cross_models_are_real_and_finite(self):
        xs = np.asarray([1_000.0, 5_000.0, 20_000.0])
        l_zeros = chi3_zeros_up_to(31.0)
        zeta_zeros = riemann_zeros_up_to(31.0)

        linear = c03_linear_normalized(xs, l_zeros)
        cross = c03_cross_normalized(xs, zeta_zeros, l_zeros)

        self.assertTrue(np.isrealobj(linear))
        self.assertTrue(np.isrealobj(cross))
        self.assertTrue(np.all(np.isfinite(linear)))
        self.assertTrue(np.all(np.isfinite(cross)))

    def test_build_experiment_scores_only_authorized_models(self):
        result = build_c03_experiment(
            max_x=500,
            min_x=50,
            log_samples=40,
            chi3_zero_heights=(30.0,),
            zeta_zero_height=30.0,
        )

        self.assertEqual(
            {(metric.split, metric.model) for metric in result.metrics},
            {
                ("discovery", "M0_pole"),
                ("discovery", "M1_pole_lzeros"),
                ("discovery", "M2_pole_lzeros_cross"),
                ("validation", "M0_pole"),
                ("validation", "M1_pole_lzeros"),
                ("validation", "M2_pole_lzeros_cross"),
            },
        )
        self.assertEqual(result.frozen_channels, ("C05", "C35", "C15"))
        self.assertFalse(result.explicit_formula_complete)
        self.assertTrue(result.samples)

    def test_artifacts_declare_controlled_truncation_and_isolation(self):
        result = build_c03_experiment(
            max_x=500,
            min_x=50,
            log_samples=30,
            chi3_zero_heights=(30.0,),
            zeta_zero_height=30.0,
        )

        with tempfile.TemporaryDirectory() as directory:
            paths = write_c03_artifacts(Path(directory), result)
            summary = json.loads(paths["summary_json"].read_text(encoding="utf-8"))
            names = {path.name for path in Path(directory).iterdir()}

            self.assertEqual(paths["series_csv"].name, "c03_series_X500.csv")
            self.assertEqual(paths["summary_json"].name, "c03_summary_X500.json")
            self.assertFalse(summary["explicit_formula_complete"])
            self.assertEqual(summary["expansion_status"], "controlled_truncation")
            self.assertEqual(summary["frozen_channels"], ["C05", "C35", "C15"])
            self.assertFalse(any("c05" in name.lower() for name in names))
            self.assertFalse(any("c35" in name.lower() for name in names))
            self.assertFalse(any("c15" in name.lower() for name in names))


if __name__ == "__main__":
    unittest.main()
