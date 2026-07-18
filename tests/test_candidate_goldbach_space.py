import unittest

from athena_azr.candidate_goldbach_space import (
    candidate_partitions,
    ced_operator,
    commutator_observation,
    feature_matrix,
    feature_separation_for_even,
    feature_separation_window,
    inverse_jaccard_distance,
    kappa_window,
    rap_ranking_observation,
    rap_selection_operator,
)


class CandidateGoldbachSpaceTests(unittest.TestCase):
    def test_candidate_partitions_include_unfiltered_pairs_by_default(self):
        candidates = candidate_partitions(20)
        pairs = [item.key for item in candidates]
        goldbach_pairs = [item.key for item in candidates if item.is_goldbach_pair]

        self.assertEqual(
            pairs,
            [
                (1, 19),
                (2, 18),
                (3, 17),
                (4, 16),
                (5, 15),
                (6, 14),
                (7, 13),
                (8, 12),
                (9, 11),
                (10, 10),
            ],
        )
        self.assertEqual(goldbach_pairs, [(3, 17), (7, 13)])

    def test_documented_n8_toy_model_is_available_with_min_term_two(self):
        candidates = candidate_partitions(8, min_term=2)
        ced_pairs = [item.key for item in ced_operator(candidates)]
        rap_pairs = [item.key for item in rap_selection_operator(candidates, 1.0 / 3.0)]
        observation = commutator_observation(8, 1.0 / 3.0, min_term=2)

        self.assertEqual([item.key for item in candidates], [(2, 6), (3, 5), (4, 4)])
        self.assertEqual(ced_pairs, [(3, 5)])
        self.assertEqual(rap_pairs, [(2, 6)])
        self.assertEqual(observation.ced_after_rap, ())
        self.assertEqual(observation.rap_after_ced, ((3, 5),))
        self.assertEqual(observation.distance, 1.0)

    def test_unit_boundary_changes_the_n8_commutator_signal(self):
        observation = commutator_observation(8, 1.0 / 3.0, min_term=1)

        self.assertEqual(observation.candidate_count, 4)
        self.assertEqual(observation.ced_after_rap, ((1, 7),))
        self.assertEqual(observation.rap_after_ced, ((1, 7),))
        self.assertEqual(observation.distance, 0.0)

    def test_inverse_jaccard_distance_handles_empty_agreement(self):
        candidates = candidate_partitions(8, min_term=2)
        left = [candidates[0]]
        right = [candidates[1]]

        self.assertEqual(inverse_jaccard_distance([], []), 0.0)
        self.assertEqual(inverse_jaccard_distance(left, right), 1.0)
        self.assertEqual(inverse_jaccard_distance(left, left), 0.0)

    def test_kappa_window_averages_local_commutator_distances(self):
        result = kappa_window(8, 12, 1.0 / 3.0, min_term=2)
        expected = sum(item.distance for item in result.observations) / len(result.observations)

        self.assertEqual([item.N for item in result.observations], [8, 10, 12])
        self.assertAlmostEqual(result.kappa, expected)

    def test_rap_ranking_observation_compares_selection_to_prime_pairs(self):
        result = rap_ranking_observation(20, 0.2)

        self.assertEqual(result.selected_pairs, ((2, 18), (4, 16)))
        self.assertEqual(result.goldbach_total, 2)
        self.assertEqual(result.goldbach_selected, 0)
        self.assertEqual(result.precision, 0.0)
        self.assertEqual(result.recall, 0.0)

    def test_feature_matrix_exposes_rap_ced_candidate_variables(self):
        rows = {row.key: row for row in feature_matrix(20)}
        goldbach = rows[(3, 17)]
        composite = rows[(4, 16)]

        self.assertTrue(goldbach.is_goldbach_pair)
        self.assertEqual(goldbach.a_loss, 0)
        self.assertEqual(goldbach.b_loss, 0)
        self.assertEqual(goldbach.loss_sum, 0)
        self.assertEqual(goldbach.integrity_sum, 2)
        self.assertEqual(goldbach.combined_rap_loss, 11)
        self.assertTrue(goldbach.ced_is_dd)

        self.assertFalse(composite.is_goldbach_pair)
        self.assertEqual(composite.b_loss, 8)
        self.assertEqual(composite.integrity_sum, 6)
        self.assertFalse(composite.ced_is_dd)

    def test_feature_separation_reports_direction_not_only_strength(self):
        separations = {item.feature: item for item in feature_separation_for_even(20)}

        self.assertEqual(separations["loss_sum"].separation_auc, 1.0)
        self.assertEqual(separations["loss_sum"].preferred_direction, "lower_for_goldbach")
        self.assertEqual(separations["combined_rap_loss"].separation_auc, 1.0)
        self.assertEqual(separations["combined_rap_loss"].preferred_direction, "higher_for_goldbach")

    def test_feature_separation_window_aggregates_candidate_rows(self):
        separations = feature_separation_window(4, 20, min_term=2)
        best = separations[0]

        self.assertEqual(best.feature, "integrity_sum")
        self.assertEqual(best.preferred_direction, "lower_for_goldbach")
        self.assertEqual(best.separation_auc, 1.0)
        self.assertGreater(best.positive_count, 0)
        self.assertGreater(best.negative_count, 0)


if __name__ == "__main__":
    unittest.main()
