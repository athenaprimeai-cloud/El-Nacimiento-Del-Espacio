import unittest
from decimal import Decimal

from athena_azr.h2_zero_certifier.config import CertificationConfig
from athena_azr.h2_zero_certifier.models import (
    CertificationBundle,
    ComplexBox,
    CountCertificate,
    CrossReferenceResult,
    FunctionCertification,
    RealInterval,
    ZeroCertificate,
)
from athena_azr.h2_zero_certifier.validation import validate_bundle


def zero(function_id, index, height, *, overlap=False):
    center = height if not overlap else 10
    center_decimal = Decimal(center)
    radius = Decimal("1e-22")
    real = RealInterval("0.4999999999999999999999", "0.5000000000000000000001")
    imag = RealInterval(str(center_decimal - radius), str(center_decimal + radius))
    return ZeroCertificate(
        index=index,
        function_id=function_id,
        conductor=1 if function_id == "zeta" else 3,
        character_id="principal" if function_id == "zeta" else "3.2",
        parity=0 if function_id == "zeta" else 1,
        box=ComplexBox(real, imag),
        multiplicity=1,
        isolation_method="synthetic",
        working_precision_bits=192,
        certificate_reference=f"{function_id}-{index}",
        critical_line_certified=True,
    )


def function_certification(function_id, *, mismatch=False, overlap=False):
    zeros = (zero(function_id, 1, 10), zero(function_id, 2, 20, overlap=overlap))
    counts = tuple(
        CountCertificate(
            function_id=function_id,
            requested_height=height,
            counting_boundary=str(height),
            boundary_zero_free=True,
            certified_total_count=2 + int(mismatch),
            isolated_count_with_multiplicity=2,
            counting_method="synthetic",
            working_precision_bits=192,
            parameters={},
        )
        for height in (143, 200, 300, 500)
    )
    return FunctionCertification(function_id, zeros, counts)


class H2ValidationTests(unittest.TestCase):
    def test_accepts_complete_synthetic_bundle(self):
        bundle = CertificationBundle(
            protocol_sha256="a" * 64,
            dependency_versions={"engine": "synthetic"},
            functions=(function_certification("zeta"), function_certification("L3")),
            protected_hashes={"006B": "b" * 64},
            cross_references=(
                CrossReferenceResult("odlyzko", "match", "c" * 64),
                CrossReferenceResult("lmfdb", "match", "d" * 64),
            ),
        )

        self.assertEqual(validate_bundle(bundle, CertificationConfig.frozen_default()), ())

    def test_accepts_uncertified_critical_line_for_l3(self):
        # Create a zero that is not certified on the critical line
        uncert_zero = ZeroCertificate(
            index=1,
            function_id="L3",
            conductor=3,
            character_id="3.2",
            parity=1,
            box=ComplexBox(
                RealInterval("0.5999999999999999999999", "0.6000000000000000000001"),
                RealInterval("9.9999999999999999999999", "10.0000000000000000000001"),
            ),
            multiplicity=1,
            isolation_method="synthetic",
            working_precision_bits=192,
            certificate_reference="L3-1",
            critical_line_certified=False,
        )
        
        counts = tuple(
            CountCertificate(
                function_id="L3",
                requested_height=height,
                counting_boundary=str(height),
                boundary_zero_free=True,
                certified_total_count=1,
                isolated_count_with_multiplicity=1,
                counting_method="synthetic",
                working_precision_bits=192,
                parameters={},
            )
            for height in (143, 200, 300, 500)
        )
        l3_func = FunctionCertification("L3", (uncert_zero,), counts)
        
        bundle = CertificationBundle(
            protocol_sha256="a" * 64,
            dependency_versions={"engine": "synthetic"},
            functions=(function_certification("zeta"), l3_func),
            protected_hashes={"006B": "b" * 64},
            cross_references=(
                CrossReferenceResult("odlyzko", "match", "c" * 64),
                CrossReferenceResult("lmfdb", "match", "d" * 64),
            ),
        )
        
        # This must not raise any error or return errors about critical-line symmetry
        errors = validate_bundle(bundle, CertificationConfig.frozen_default())
        self.assertEqual(errors, ())

    def test_reports_all_structural_failures_without_early_exit(self):

        bundle = CertificationBundle(
            protocol_sha256="bad",
            dependency_versions={},
            functions=(
                function_certification("zeta", mismatch=True, overlap=True),
                function_certification("L3"),
            ),
            protected_hashes={},
            cross_references=(CrossReferenceResult("external", "disagreement"),),
        )

        errors = validate_bundle(bundle, CertificationConfig.frozen_default())

        self.assertGreaterEqual(len(errors), 5)
        self.assertTrue(any("sha256" in error for error in errors))
        self.assertTrue(any("overlap" in error for error in errors))
        self.assertTrue(any("count mismatch" in error for error in errors))
        self.assertTrue(any("cross-reference" in error for error in errors))

    def test_requires_both_frozen_external_cross_references(self):
        bundle = CertificationBundle(
            protocol_sha256="a" * 64,
            dependency_versions={"engine": "synthetic"},
            functions=(function_certification("zeta"), function_certification("L3")),
            protected_hashes={"006B": "b" * 64},
            cross_references=(
                CrossReferenceResult("odlyzko", "match", "c" * 64),
                CrossReferenceResult("lmfdb", "not_checked"),
            ),
        )

        errors = validate_bundle(bundle, CertificationConfig.frozen_default())

        self.assertTrue(any("lmfdb" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
