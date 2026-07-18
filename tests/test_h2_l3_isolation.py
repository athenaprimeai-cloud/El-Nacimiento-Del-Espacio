import unittest
from decimal import Decimal
from athena_azr.h2_zero_certifier.models import (
    ComplexBox,
    RealInterval,
    ZeroCertificate,
)
from athena_azr.h2_zero_certifier.config import CertificationConfig
from athena_azr.h2_zero_certifier.chi3_function import CHI3_METADATA

from athena_azr.h2_zero_certifier.l3_certifier import (
    _isolate_box,
    certify_l3,
    InconclusiveL3Certification,
)
from athena_azr.h2_zero_certifier.l3_argument_count import InconclusiveWindingCount


class FakeL3Backend:
    def __init__(self, roots):
        self.roots = tuple((Decimal(str(real)), Decimal(str(imag))) for real, imag in roots)
        self.calls = []

    def chi3_metadata(self) -> dict[str, str]:
        return dict(CHI3_METADATA)

    def l3_box_winding_count(self, box: ComplexBox, precision_bits: int) -> int:
        self.calls.append((box, precision_bits))
        rl = Decimal(box.real.lower)
        ru = Decimal(box.real.upper)
        il = Decimal(box.imag.lower)
        iu = Decimal(box.imag.upper)

        for real, imag in self.roots:
            if (real in (rl, ru) and il <= imag <= iu) or (
                imag in (il, iu) and rl <= real <= ru
            ):
                raise InconclusiveWindingCount(
                    f"synthetic root {(real, imag)} lies on the boundary"
                )

        # Count roots strictly inside
        count = 0
        for real, imag in self.roots:
            if rl < real < ru and il < imag < iu:
                count += 1
        return count

    def l3_critical_line_certified(self, box: ComplexBox, precision_bits: int) -> bool:
        contained = [
            (real, imag)
            for real, imag in self.roots
            if Decimal(box.real.lower) < real < Decimal(box.real.upper)
            and Decimal(box.imag.lower) < imag < Decimal(box.imag.upper)
        ]
        return len(contained) == 1 and contained[0][0] == Decimal("0.5")

    def l3_count_certificate(self, height: int, precision_bits: int):
        # Synthetic count certificate
        total = sum(1 for _, imag in self.roots if imag < Decimal(height))
        from athena_azr.h2_zero_certifier.models import CountCertificate
        return CountCertificate(
            function_id="L3",
            requested_height=height,
            counting_boundary=str(height),
            boundary_zero_free=True,
            certified_total_count=total,
            isolated_count_with_multiplicity=total,
            counting_method="synthetic_winding_count",
            working_precision_bits=precision_bits,
        )


class H2L3IsolationTests(unittest.TestCase):
    def test_rejects_negative_parent_count_from_backend(self):
        config = CertificationConfig.frozen_default()
        box = ComplexBox(
            RealInterval("-0.5", "1.5"),
            RealInterval("0", "1"),
        )

        with self.assertRaisesRegex(InconclusiveL3Certification, "nonnegative"):
            _isolate_box(
                box,
                -1,
                object(),
                config,
                192,
                config.max_root_isolation_depth,
            )

    def test_certify_l3_isolates_and_counts_zeros_on_critical_line(self):
        # Two zeros on the critical line (real=0.5)
        backend = FakeL3Backend([("0.5", "6.25"), ("0.5", "11.25")])
        
        # Configure target width to 1e-3 for faster synthetic bisection in tests
        config = CertificationConfig(
            max_height=15,
            requested_heights=(10, 14),
            target_interval_width=Decimal("1e-3"),
            precision_steps_bits=(192,),
            l3_conductor=3,
            l3_conrey_number=2,
            l3_parity=1,
            contour_sigma_left=Decimal("-0.5"),
            contour_sigma_right=Decimal("1.5"),
            max_contour_depth=40,
            max_root_isolation_depth=60,
        )

        cert = certify_l3(backend, config)
        self.assertEqual(cert.function_id, "L3")
        self.assertEqual(len(cert.zeros), 2)
        self.assertTrue(all(z.critical_line_certified for z in cert.zeros))
        
        # Zeros must be sorted by height
        self.assertLess(Decimal(cert.zeros[0].box.imag.lower), Decimal(cert.zeros[1].box.imag.lower))

    def test_certify_l3_handles_zero_off_critical_line(self):
        # One zero off the critical line (real=0.6)
        backend = FakeL3Backend([("0.6", "6.25")])
        
        config = CertificationConfig(
            max_height=10,
            requested_heights=(9,),
            target_interval_width=Decimal("1e-3"),
            precision_steps_bits=(192,),
            l3_conductor=3,
            l3_conrey_number=2,
            l3_parity=1,
            contour_sigma_left=Decimal("-0.5"),
            contour_sigma_right=Decimal("1.5"),
            max_contour_depth=40,
            max_root_isolation_depth=60,
        )

        cert = certify_l3(backend, config)
        self.assertEqual(len(cert.zeros), 1)
        self.assertFalse(cert.zeros[0].critical_line_certified)

    def test_certify_l3_boundary_shifting(self):
        # Zero exactly on the imaginary midpoint of [0, 16], which is 8.0
        # When bisecting, the split line is imag=8.0, so the root lies on the boundary.
        # This will trigger boundary shifting!
        backend = FakeL3Backend([("0.5", "8.0")])
        
        config = CertificationConfig(
            max_height=16,
            requested_heights=(12,),
            target_interval_width=Decimal("1e-3"),
            precision_steps_bits=(192,),
            l3_conductor=3,
            l3_conrey_number=2,
            l3_parity=1,
            contour_sigma_left=Decimal("-0.5"),
            contour_sigma_right=Decimal("1.5"),
            max_contour_depth=40,
            max_root_isolation_depth=60,
        )

        cert = certify_l3(backend, config)
        self.assertEqual(len(cert.zeros), 1)
        self.assertTrue(cert.zeros[0].critical_line_certified)

    def test_containing_one_half_does_not_certify_the_critical_line(self):
        backend = FakeL3Backend([("0.6", "6.25")])
        config = CertificationConfig(
            max_height=10,
            requested_heights=(9,),
            target_interval_width=Decimal("2"),
            precision_steps_bits=(192,),
            l3_conductor=3,
            l3_conrey_number=2,
            l3_parity=1,
            contour_sigma_left=Decimal("-0.5"),
            contour_sigma_right=Decimal("1.5"),
            max_contour_depth=40,
            max_root_isolation_depth=60,
        )

        cert = certify_l3(backend, config)

        self.assertTrue(cert.zeros[0].box.real.contains_decimal(Decimal("0.5")))
        self.assertFalse(cert.zeros[0].critical_line_certified)

    def test_uses_configured_root_isolation_depth(self):
        backend = FakeL3Backend([("0.5", "6.25")])
        config = CertificationConfig(
            max_height=10,
            requested_heights=(9,),
            target_interval_width=Decimal("1e-3"),
            precision_steps_bits=(192,),
            l3_conductor=3,
            l3_conrey_number=2,
            l3_parity=1,
            contour_sigma_left=Decimal("-0.5"),
            contour_sigma_right=Decimal("1.5"),
            max_contour_depth=40,
            max_root_isolation_depth=1,
        )

        with self.assertRaises(InconclusiveL3Certification):
            certify_l3(backend, config)

    def test_uses_configured_contour_bounds(self):
        backend = FakeL3Backend([("0.5", "6.25")])
        config = CertificationConfig(
            max_height=10,
            requested_heights=(9,),
            target_interval_width=Decimal("1e-3"),
            precision_steps_bits=(192,),
            l3_conductor=3,
            l3_conrey_number=2,
            l3_parity=1,
            contour_sigma_left=Decimal("-1"),
            contour_sigma_right=Decimal("2"),
            max_contour_depth=40,
            max_root_isolation_depth=60,
        )

        certify_l3(backend, config)

        first_box, _ = backend.calls[0]
        self.assertEqual(first_box.real.lower, "-1")
        self.assertEqual(first_box.real.upper, "2")


if __name__ == "__main__":
    unittest.main()
