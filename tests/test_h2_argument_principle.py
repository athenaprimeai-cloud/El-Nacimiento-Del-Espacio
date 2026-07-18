import cmath
import math
import unittest

from athena_azr.h2_zero_certifier.argument_principle import (
    InconclusiveWinding,
    WindingSample,
    certified_winding_number,
    synthetic_winding_number,
)


def polynomial_samples(roots, *, contour_radius=2.0, sample_count=128):
    samples = []
    for index in range(sample_count + 1):
        z = contour_radius * cmath.exp(2j * math.pi * index / sample_count)
        value = 1 + 0j
        for root in roots:
            value *= z - root
        samples.append(WindingSample(center=value, radius=0.0))
    return samples


class H2ArgumentPrincipleTests(unittest.TestCase):
    def test_counts_known_synthetic_roots_with_multiplicity(self):
        self.assertEqual(synthetic_winding_number(polynomial_samples([3.0])), 0)
        self.assertEqual(synthetic_winding_number(polynomial_samples([0.25])), 1)
        self.assertEqual(synthetic_winding_number(polynomial_samples([-0.5, 0.5])), 2)
        self.assertEqual(synthetic_winding_number(polynomial_samples([0.0, 0.0])), 2)

    def test_rejects_a_contour_image_that_can_contain_zero(self):
        samples = polynomial_samples([0.0])
        samples[10] = WindingSample(center=0j, radius=0.1)

        with self.assertRaises(InconclusiveWinding):
            synthetic_winding_number(samples)

    def test_rejects_sampling_too_coarse_to_fix_argument_branch(self):
        with self.assertRaises(InconclusiveWinding):
            synthetic_winding_number(polynomial_samples([0.0, 0.0], sample_count=4))

    def test_rigorous_entrypoint_is_inert_until_flint_integration_is_reviewed(self):
        with self.assertRaises(NotImplementedError):
            certified_winding_number(object(), object())


if __name__ == "__main__":
    unittest.main()
