import unittest
from decimal import Decimal

from athena_azr.h2_zero_certifier.chi3_function import CHI3_METADATA, validate_chi3_metadata
from athena_azr.h2_zero_certifier.config import CertificationConfig
from athena_azr.h2_zero_certifier.l3_certifier import (
    InconclusiveL3Certification,
    certify_l3,
)
from athena_azr.h2_zero_certifier.models import (
    ComplexBox,
    CountCertificate,
    IsolatedZeroBox,
    RealInterval,
)


def structural_config():
    base = CertificationConfig.frozen_default()
    return CertificationConfig(
        requested_heights=base.requested_heights,
        max_height=base.max_height,
        target_interval_width=Decimal("1e-3"),
        precision_steps_bits=(192,),
        l3_conductor=base.l3_conductor,
        l3_conrey_number=base.l3_conrey_number,
        l3_parity=base.l3_parity,
        contour_sigma_left=base.contour_sigma_left,
        contour_sigma_right=base.contour_sigma_right,
        max_contour_depth=base.max_contour_depth,
        max_root_isolation_depth=base.max_root_isolation_depth,
    )


class FakeL3Backend:
    def __init__(self, heights, counts=None, metadata=None):
        self.heights = tuple(Decimal(str(value)) for value in heights)
        self._counts = counts
        self._metadata = metadata or dict(CHI3_METADATA)

    def chi3_metadata(self):
        return self._metadata

    def l3_box_winding_count(self, box, precision_bits):
        real_lower = Decimal(box.real.lower)
        real_upper = Decimal(box.real.upper)
        imag_lower = Decimal(box.imag.lower)
        imag_upper = Decimal(box.imag.upper)
        critical_real = Decimal("0.5")
        if real_lower <= critical_real <= real_upper and any(
            height in (imag_lower, imag_upper) for height in self.heights
        ):
            raise InconclusiveL3Certification("synthetic zero lies on box boundary")
        return sum(
            real_lower < critical_real < real_upper and imag_lower < height < imag_upper
            for height in self.heights
        )

    def l3_critical_line_certified(self, box, precision_bits):
        return box.real.contains_decimal(Decimal("0.5"))

    def l3_zero_boxes(self, max_height, precision_bits):
        radius = Decimal("1e-9") if precision_bits < 256 else Decimal("1e-22")
        return tuple(
            IsolatedZeroBox(
                box=ComplexBox(
                    RealInterval("0.4999999999999999999999", "0.5000000000000000000001"),
                    RealInterval(str(height - radius), str(height + radius)),
                ),
                multiplicity=1,
                unique_zero=True,
                certificate_reference=f"synthetic-{index}",
            )
            for index, height in enumerate(self.heights, start=1)
            if height <= Decimal(max_height)
        )

    def l3_count_certificate(self, requested_height, precision_bits):
        if self._counts is not None:
            total = self._counts[requested_height]
        else:
            total = sum(height < Decimal(requested_height) for height in self.heights)
        return CountCertificate(
            function_id="L3",
            requested_height=requested_height,
            counting_boundary=str(requested_height),
            boundary_zero_free=True,
            certified_total_count=total,
            isolated_count_with_multiplicity=total,
            counting_method="synthetic_argument_principle",
            working_precision_bits=precision_bits,
            parameters={"fixture": "true"},
        )


class H2L3CertifierTests(unittest.TestCase):
    def test_validates_exact_chi3_identity(self):
        validate_chi3_metadata(FakeL3Backend([]).chi3_metadata())

        bad = FakeL3Backend([], metadata={"conductor": "5"})
        with self.assertRaises(ValueError):
            validate_chi3_metadata(bad.chi3_metadata())

    def test_certifies_boxes_only_when_independent_counts_match(self):
        backend = FakeL3Backend([8, 100, 142, 150, 199, 201, 299, 301, 499])

        result = certify_l3(backend, structural_config())

        self.assertEqual(len(result.zeros), 9)
        self.assertEqual([count.certified_total_count for count in result.counts], [3, 5, 7, 9])
        self.assertTrue(all(zero.critical_line_certified for zero in result.zeros))

    def test_rejects_count_mismatch(self):
        mismatch = FakeL3Backend(
            [8, 100, 142, 150, 199, 201, 299, 301, 499],
            counts={143: 2, 200: 5, 300: 7, 500: 9},
        )
        with self.assertRaises(InconclusiveL3Certification):
            certify_l3(mismatch, structural_config())

    def test_rejects_unresolved_recursive_cluster(self):
        class UnresolvedBackend(FakeL3Backend):
            def l3_box_winding_count(self, box, precision_bits):
                return 2

        with self.assertRaises(InconclusiveL3Certification):
            certify_l3(UnresolvedBackend([8]), structural_config())

    def test_rejects_an_empty_zero_sequence(self):
        with self.assertRaises(InconclusiveL3Certification):
            certify_l3(FakeL3Backend([]), structural_config())


if __name__ == "__main__":
    unittest.main()
