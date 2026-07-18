import unittest

from athena_azr.operators import (
    ced_confluence,
    ced_state,
    eps,
    factorize,
    goldbach_partitions,
    rap_signature,
)


class AthenaOperatorTests(unittest.TestCase):
    def test_ced_state_and_confluence_use_z2_algebra(self):
        self.assertEqual(ced_state(8), "I")
        self.assertEqual(ced_state(7), "D")
        self.assertEqual(ced_confluence("D", "D"), "I")
        self.assertEqual(ced_confluence("I", "D"), "D")

    def test_rap_signature_requires_integrity_for_primality(self):
        four = rap_signature(4)
        seven = rap_signature(7)

        self.assertEqual(factorize(4), [(2, 2)])
        self.assertEqual(four.potential, 4)
        self.assertEqual(four.integrity, 2)
        self.assertEqual(four.loss, 0)
        self.assertFalse(four.is_prime)

        self.assertEqual(seven.potential, 7)
        self.assertEqual(seven.integrity, 1)
        self.assertEqual(seven.loss, 0)
        self.assertTrue(seven.is_prime)

    def test_eps_measures_distance_between_prime_columns(self):
        self.assertEqual(eps(3, 17), 14)
        self.assertEqual(eps(11, 11), 0)

    def test_goldbach_partitions_keep_prime_resonances_only(self):
        partitions = goldbach_partitions(20)
        pairs = [(item.p, item.q) for item in partitions]

        self.assertEqual(pairs, [(3, 17), (7, 13)])
        self.assertTrue(all(item.ced_result == "I" for item in partitions))
        self.assertTrue(all(item.p_is_prime and item.q_is_prime for item in partitions))


if __name__ == "__main__":
    unittest.main()
