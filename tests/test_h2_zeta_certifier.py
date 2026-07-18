import unittest
from decimal import Decimal

from athena_azr.h2_zero_certifier.config import CertificationConfig
from athena_azr.h2_zero_certifier.models import ComplexBox, CountCertificate, RealInterval
from athena_azr.h2_zero_certifier.zeta_certifier import (
    InconclusiveCertification,
    certify_zeta,
)


class FakeZetaBackend:
    def __init__(
        self,
        heights,
        *,
        irreducible_index=None,
        count_offset=0,
        isolated_count_offset=0,
        boundary_zero_free=True,
    ):
        self.heights = tuple(Decimal(str(value)) for value in heights)
        self.irreducible_index = irreducible_index
        self.count_offset = count_offset
        self.isolated_count_offset = isolated_count_offset
        self.boundary_zero_free = boundary_zero_free
        self.calls = []

    def zeta_zero(self, index, precision_bits):
        self.calls.append((index, precision_bits))
        center = self.heights[index - 1]
        if index == self.irreducible_index:
            radius = Decimal("0.1")
        elif precision_bits < 256:
            radius = Decimal("1e-9")
        else:
            radius = Decimal("1e-22")
        return ComplexBox(
            RealInterval("0.4999999999999999999999", "0.5000000000000000000001"),
            RealInterval(str(center - radius), str(center + radius)),
        )

    def zeta_count_certificate(self, requested_height, precision_bits):
        total = sum(height < Decimal(requested_height) for height in self.heights)
        return CountCertificate(
            function_id="zeta",
            requested_height=requested_height,
            counting_boundary=str(requested_height),
            boundary_zero_free=self.boundary_zero_free,
            certified_total_count=total + self.count_offset,
            isolated_count_with_multiplicity=(
                total + self.count_offset + self.isolated_count_offset
            ),
            counting_method="synthetic_independent_turing_count",
            working_precision_bits=precision_bits,
            parameters={"source": "fake-independent-count"},
        )


class H2ZetaCertifierTests(unittest.TestCase):
    def test_certifies_consecutive_intervals_and_counts_at_frozen_heights(self):
        backend = FakeZetaBackend([10, 100, 142, 150, 199, 201, 299, 301, 499, 501])

        result = certify_zeta(backend, CertificationConfig.frozen_default())

        self.assertEqual(len(result.zeros), 9)
        self.assertEqual([count.certified_total_count for count in result.counts], [3, 5, 7, 9])
        self.assertTrue(all(count.counts_match for count in result.counts))
        self.assertEqual(result.zeros[-1].box.imag.upper, "499.0000000000000000000001")
        self.assertIn((1, 192), backend.calls)
        self.assertIn((1, 256), backend.calls)
        self.assertIn((10, 256), backend.calls)

    def test_fails_when_a_zero_cannot_be_separated_from_counting_boundary(self):
        backend = FakeZetaBackend([10, 100, 143, 501], irreducible_index=3)

        with self.assertRaises(InconclusiveCertification):
            certify_zeta(backend, CertificationConfig.frozen_default())

    def test_rejects_an_empty_zero_sequence(self):
        with self.assertRaises(InconclusiveCertification):
            certify_zeta(FakeZetaBackend([501]), CertificationConfig.frozen_default())

    def test_rejects_independent_count_mismatch_or_nonzero_boundary(self):
        config = CertificationConfig.frozen_default()
        with self.assertRaises(InconclusiveCertification):
            certify_zeta(FakeZetaBackend([10, 501], count_offset=1), config)
        with self.assertRaises(InconclusiveCertification):
            certify_zeta(FakeZetaBackend([10, 501], boundary_zero_free=False), config)
        with self.assertRaises(InconclusiveCertification):
            certify_zeta(FakeZetaBackend([10, 501], isolated_count_offset=1), config)


if __name__ == "__main__":
    unittest.main()
