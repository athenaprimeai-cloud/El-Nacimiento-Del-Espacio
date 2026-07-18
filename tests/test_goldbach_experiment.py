import unittest

from athena_azr.goldbach_transform import (
    build_extraction_experiment,
    build_goldbach_experiment,
    build_multispectrum_experiment,
    build_persistence_experiment,
    dominant_frequencies,
    local_goldbach_factor,
    modular_projection_residual,
    nearest_rational,
)


class GoldbachExperimentTests(unittest.TestCase):
    def test_build_goldbach_experiment_counts_small_even_window(self):
        result = build_goldbach_experiment(20)
        counts_by_n = {row.N: row.partition_count for row in result.rows}

        self.assertEqual(
            counts_by_n,
            {
                4: 1,
                6: 1,
                8: 1,
                10: 2,
                12: 1,
                14: 2,
                16: 2,
                18: 2,
                20: 2,
            },
        )
        self.assertEqual(result.counterexamples, [])
        self.assertEqual(result.evidence_level, "Observación")

    def test_dominant_frequencies_exclude_zero_frequency(self):
        powers = dominant_frequencies([1.0, -1.0, 1.0, -1.0], sample_spacing=2.0, limit=2)

        self.assertEqual(len(powers), 1)
        self.assertAlmostEqual(powers[0].frequency, 0.25)
        self.assertGreater(powers[0].power, 0)

    def test_local_goldbach_factor_uses_odd_prime_divisors(self):
        self.assertAlmostEqual(local_goldbach_factor(12), 2.0)
        self.assertAlmostEqual(local_goldbach_factor(30), 8.0 / 3.0)
        self.assertAlmostEqual(local_goldbach_factor(49), 6.0 / 5.0)

    def test_nearest_rational_identifies_one_sixth_peak(self):
        rational = nearest_rational(0.1666333267, max_denominator=30)

        self.assertEqual(rational.numerator, 1)
        self.assertEqual(rational.denominator, 6)
        self.assertAlmostEqual(rational.value, 1.0 / 6.0)
        self.assertEqual(rational.candidate_modulus, 6)

    def test_multispectrum_experiment_builds_four_reproducible_channels(self):
        first = build_multispectrum_experiment(60, random_seed=7, peak_limit=3)
        second = build_multispectrum_experiment(60, random_seed=7, peak_limit=3)

        self.assertEqual(
            [channel.name for channel in first.channels],
            ["raw_counts", "smooth_residual", "desingularized_ratio", "random_control"],
        )
        self.assertEqual(first.channels[-1].peaks, second.channels[-1].peaks)
        self.assertTrue(all(channel.peaks for channel in first.channels))
        self.assertTrue(all(0.0 <= peak.normalized_power <= 1.0 for channel in first.channels for peak in channel.peaks))

    def test_spectral_peaks_include_absolute_energy_fraction_and_rank(self):
        result = build_multispectrum_experiment(60, random_seed=7, peak_limit=3)
        peak = result.channels[0].peaks[0]

        self.assertGreater(peak.absolute_power, 0.0)
        self.assertGreater(peak.total_spectral_energy, 0.0)
        self.assertGreaterEqual(peak.fraction_of_total_energy, 0.0)
        self.assertLessEqual(peak.fraction_of_total_energy, 1.0)
        self.assertEqual(peak.rank_within_channel, 1)

    def test_persistence_experiment_scores_candidates_across_windows(self):
        result = build_persistence_experiment(
            windows=[(4, 40), (4, 60)],
            control_seeds=[7, 11],
            peak_limit=4,
        )

        self.assertEqual(result.evidence_level, "Observación multiescala")
        self.assertEqual(result.windows, ((4, 40), (4, 60)))
        self.assertTrue(result.candidates)
        self.assertTrue(all(0.0 <= candidate.coverage <= 1.0 for candidate in result.candidates))
        self.assertTrue(all(0.0 <= candidate.control_percentile <= 1.0 for candidate in result.candidates))

    def test_persistence_counts_each_rational_once_per_window(self):
        result = build_persistence_experiment(
            windows=[(4, 240), (4, 240)],
            control_seeds=[7],
            peak_limit=12,
        )

        self.assertTrue(all(candidate.windows_detected <= len(result.windows) for candidate in result.candidates))
        self.assertTrue(all(candidate.coverage <= 1.0 for candidate in result.candidates))

    def test_persistence_candidates_include_origin_novelty_and_global_p(self):
        result = build_persistence_experiment(
            windows=[(4, 240), (4, 500)],
            control_seeds=[7, 11],
            peak_limit=8,
        )

        self.assertTrue(all(candidate.structural_origin for candidate in result.candidates))
        self.assertTrue(all(candidate.novelty_status for candidate in result.candidates))
        self.assertTrue(all(0.0 < candidate.global_empirical_p <= 1.0 for candidate in result.candidates))

        trend = next(candidate for candidate in result.candidates if candidate.nearest_rational == "0/1")
        self.assertEqual(trend.structural_origin, "residual_trend")
        self.assertEqual(trend.novelty_status, "not_applicable")
        self.assertTrue(trend.exclude_from_candidate_ranking)

    def test_modular_projection_removes_known_modular_wave(self):
        ns = list(range(4, 80, 2))
        values = [2.0 * __import__("math").cos((2.0 * __import__("math").pi * n) / 3.0) for n in ns]

        residual = modular_projection_residual(ns, values, modular_primes=(3,))

        self.assertLess(max(abs(value) for value in residual), 1e-9)

    def test_extraction_experiment_builds_r0_to_r3_stages(self):
        result = build_extraction_experiment(240, control_seeds=[7], peak_limit=5)
        stage_names = [stage.name for stage in result.stages]
        stages = {stage.name: stage for stage in result.stages}

        self.assertEqual(
            stage_names,
            ["R0_desingularized", "R1_mean_centered", "R2_log_detrended", "R3_modular_orthogonal"],
        )
        self.assertAlmostEqual(sum(stages["R1_mean_centered"].values), 0.0, places=9)
        self.assertLessEqual(
            stages["R3_modular_orthogonal"].total_spectral_energy,
            stages["R2_log_detrended"].total_spectral_energy,
        )
        self.assertTrue(all(0.0 < peak.global_empirical_p <= 1.0 for stage in result.stages for peak in stage.peaks))


if __name__ == "__main__":
    unittest.main()
