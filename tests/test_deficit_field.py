import unittest

from athena_azr.deficit_field import (
    deficit,
    deficit_spectrum,
    deficit_histogram,
    deficit_layers,
    parity_deficit_analysis,
    goldbach_deficit_landscape,
    partition_deficit,
    deficit_spectrum_for_even,
)

class DeficitFieldTests(unittest.TestCase):
    def test_deficit_values_for_known_cases(self):
        # Primes should have deficit 0
        for p in [2, 3, 5, 7, 11, 13, 17, 19]:
            self.assertEqual(deficit(p), 0)
            
        # 4 should have deficit 0
        self.assertEqual(deficit(4), 0)
        
        # Composite cases
        self.assertEqual(deficit(6), 1)  # 6 - (2+3) = 1
        self.assertEqual(deficit(8), 2)  # 8 - (2+2+2) = 2
        self.assertEqual(deficit(9), 3)  # 9 - (3+3) = 3
        self.assertEqual(deficit(10), 3) # 10 - (2+5) = 3
        self.assertEqual(deficit(15), 7) # 15 - (3+5) = 7
        self.assertEqual(deficit(25), 15) # 25 - (5+5) = 15

    def test_deficit_raises_value_error_for_invalid_input(self):
        with self.assertRaises(ValueError):
            deficit(0)
        with self.assertRaises(ValueError):
            deficit(-5)

    def test_deficit_spectrum_generates_correct_sequence(self):
        # d(1) = 1 - 0 = 1
        # d(2) = 0
        # d(3) = 0
        # d(4) = 0
        # d(5) = 0
        # d(6) = 1
        # d(7) = 0
        # d(8) = 2
        # d(9) = 3
        # d(10) = 3
        expected = (1, 0, 0, 0, 0, 1, 0, 2, 3, 3)
        self.assertEqual(deficit_spectrum(10), expected)

    def test_deficit_histogram_counts_occurrences(self):
        hist = deficit_histogram(10)
        # Expected counts in 1..10:
        # d=0: 2, 3, 4, 5, 7 (5 numbers)
        # d=1: 1, 6 (2 numbers)
        # d=2: 8 (1 number)
        # d=3: 9, 10 (2 numbers)
        self.assertEqual(hist[0], 5)
        self.assertEqual(hist[1], 2)
        self.assertEqual(hist[2], 1)
        self.assertEqual(hist[3], 2)

    def test_deficit_layers_groups_correctly(self):
        layers = deficit_layers(10)
        self.assertEqual(set(layers[0]), {2, 3, 4, 5, 7})
        self.assertEqual(set(layers[1]), {1, 6})
        self.assertEqual(set(layers[2]), {8})
        self.assertEqual(set(layers[3]), {9, 10})

    def test_parity_deficit_analysis(self):
        analysis = parity_deficit_analysis(100)
        self.assertIn("mean_even", analysis)
        self.assertIn("mean_odd", analysis)
        self.assertIn("diff", analysis)

    def test_goldbach_deficit_landscape(self):
        # For N=10, candidates (min_term=2) are:
        # (2, 8) -> (0, 2)
        # (3, 7) -> (0, 0)
        # (4, 6) -> (0, 1)
        # (5, 5) -> (0, 0)
        landscape = goldbach_deficit_landscape(10, min_term=2)
        expected = (
            (0, 2),
            (0, 0),
            (0, 1),
            (0, 0)
        )
        self.assertEqual(landscape, expected)

    def test_partition_deficit(self):
        self.assertEqual(partition_deficit(3, 5), 0)
        self.assertEqual(partition_deficit(4, 6), 1)
        self.assertEqual(partition_deficit(9, 10), 6)

    def test_deficit_spectrum_for_even(self):
        # For N=10, candidates (min_term=2):
        # (2, 8) -> 2
        # (3, 7) -> 0
        # (4, 6) -> 1
        # (5, 5) -> 0
        # Spectrum should contain: {0: 2, 1: 1, 2: 1}
        spec = deficit_spectrum_for_even(10, min_term=2)
        self.assertEqual(spec, {0: 2, 1: 1, 2: 1})


if __name__ == "__main__":
    unittest.main()
