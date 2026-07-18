import unittest
from fractions import Fraction


class H006H10RationalEndpointCanonicalityPatchTests(unittest.TestCase):
    def test_integer_valued_rational_endpoints_are_rejected(self):
        from athena_azr.h2_zero_certifier import winding_certifier as winding

        invalid_integer_valued_rationals = (
            "1/1",
            "2/2",
            "4/2",
            "10/5",
            "-6/3",
            "999999999999999999999/3",
        )

        for value in invalid_integer_valued_rationals:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    winding.parse_canonical_exact_endpoint(value)

    def test_noninteger_reduced_rational_endpoints_are_accepted(self):
        from athena_azr.h2_zero_certifier import winding_certifier as winding

        cases = (
            ("1/3", Fraction(1, 3)),
            ("2/3", Fraction(2, 3)),
            ("-3/2", Fraction(-3, 2)),
            ("-1/2", Fraction(-1, 2)),
            ("1000000000000000000001/3", Fraction(1000000000000000000001, 3)),
        )

        for value, expected in cases:
            with self.subTest(value=value):
                self.assertEqual(winding.parse_canonical_exact_endpoint(value), expected)

    def test_integer_endpoint_syntax_remains_the_only_integer_representation(self):
        from athena_azr.h2_zero_certifier import winding_certifier as winding

        valid_integer_cases = (
            ("0", Fraction(0, 1)),
            ("1", Fraction(1, 1)),
            ("-1", Fraction(-1, 1)),
            ("333333333333333333333", Fraction(333333333333333333333, 1)),
        )
        invalid_integer_text = ("00", "01", "-0", "+1", " 1", "1 ")

        for value, expected in valid_integer_cases:
            with self.subTest(value=value):
                self.assertEqual(winding.parse_canonical_exact_endpoint(value), expected)
        for value in invalid_integer_text:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    winding.parse_canonical_exact_endpoint(value)

    def test_other_invalid_rational_forms_are_rejected(self):
        from athena_azr.h2_zero_certifier import winding_certifier as winding

        invalid_values = (
            "2/4",
            "3/6",
            "0/5",
            "1/01",
            "1/-2",
            "1/0",
        )

        for value in invalid_values:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    winding.parse_canonical_exact_endpoint(value)

    def test_corrected_large_interval_uses_canonical_integer_endpoint(self):
        from athena_azr.h2_zero_certifier import winding_certifier as winding

        self.assertEqual(
            winding.integers_in_exact_closed_interval(
                "333333333333333333333",
                "1000000000000000000001/3",
            ),
            (333333333333333333333,),
        )
        self.assertEqual(
            winding.integers_in_closed_interval(
                "333333333333333333333",
                "1000000000000000000001/3",
            ),
            (333333333333333333333,),
        )


if __name__ == "__main__":
    unittest.main()
