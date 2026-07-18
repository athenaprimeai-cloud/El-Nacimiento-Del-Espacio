import unittest
from dataclasses import replace

from athena_azr.h2_zero_certifier.real_evidence import (
    ComplexBallRecord,
    InvalidRealEvidence,
    RealBallRecord,
    RealCompletedL3PointEvidence,
    RealEvidenceFactory,
)
from tests.h2_test_support import validated_test_authorization


class H2RealEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.factory = RealEvidenceFactory(
            backend_id="fake-ball-runtime",
            authorization_digest="a" * 64,
            runtime_code_digest="b" * 64,
        )

    def test_validated_authorization_factory_emits_probative_evidence(self):
        authorization = validated_test_authorization()
        factory = RealEvidenceFactory.from_authorization(
            authorization,
            backend_id="authorized-fake-runtime",
        )
        evidence = factory.completed_l3_point(
            ComplexBallRecord("1", "2", "3", "4"),
            precision_bits=192,
        )
        self.assertTrue(evidence.probative)
        self.assertEqual(
            evidence.authorization_digest,
            authorization.source_digest,
        )

    def test_validated_factory_uses_sealed_backend_identity(self):
        factory = RealEvidenceFactory.from_authorization(
            validated_test_authorization(),
            backend_id="sealed-backend",
        )
        factory.backend_id = "mutated-backend"
        evidence = factory.completed_l3_point(
            ComplexBallRecord("1", "2", "3", "4"),
            precision_bits=192,
        )
        self.assertEqual(evidence.backend_id, "sealed-backend")

    def test_real_evidence_cannot_be_constructed_without_factory_capability(self):
        with self.assertRaises(InvalidRealEvidence):
            RealCompletedL3PointEvidence(
                value=ComplexBallRecord("1", "2", "3", "4"),
                precision_bits=192,
                backend_id="fake",
                authorization_digest="a" * 64,
                runtime_code_digest="b" * 64,
                review_chain_digest="c" * 64,
                probative=False,
                parent_evidence_hashes=(),
                segment_id="",
                digest="c" * 64,
            )

    def test_factory_emits_immutable_traceable_point_evidence(self):
        evidence = self.factory.completed_l3_point(
            ComplexBallRecord("1", "2", "3", "4"),
            precision_bits=192,
            segment_id="segment-1",
        )
        self.assertEqual(evidence.segment_id, "segment-1")
        self.assertEqual(len(evidence.digest), 64)
        with self.assertRaises(Exception):
            evidence.precision_bits = 256

    def test_half_plane_requires_the_exact_segment_parent(self):
        first = self.factory.segment_image(
            value=ComplexBallRecord("1", "2", "3", "4"),
            segment_id="segment-1",
            precision_bits=192,
        )
        second = self.factory.segment_image(
            value=ComplexBallRecord("5", "6", "7", "8"),
            segment_id="segment-2",
            precision_bits=192,
        )
        with self.assertRaises(InvalidRealEvidence):
            self.factory.half_plane(
                segment=first,
                claimed_parent_hash=second.digest,
                rotation_real="1",
                rotation_imag="0",
                rotated_real_lower="1",
            )

    def test_factory_rejects_evidence_from_different_provenance(self):
        foreign_factory = RealEvidenceFactory(
            backend_id="other-runtime",
            authorization_digest="c" * 64,
            runtime_code_digest="d" * 64,
        )
        foreign_segment = foreign_factory.segment_image(
            value=ComplexBallRecord("1", "2", "3", "4"),
            segment_id="foreign-segment",
            precision_bits=192,
        )
        with self.assertRaises(InvalidRealEvidence):
            self.factory.half_plane(
                segment=foreign_segment,
                rotation_real="1",
                rotation_imag="0",
                rotated_real_lower="1",
            )

    def test_validated_factory_rejects_non_probative_segment_with_copied_identity(self):
        trusted = RealEvidenceFactory.from_authorization(
            validated_test_authorization(),
            backend_id="sealed-backend",
        )
        seed = trusted.segment_image(
            value=ComplexBallRecord("1", "2", "3", "4"),
            segment_id="trusted-seed",
            precision_bits=192,
        )
        forged = RealEvidenceFactory(
            seed.backend_id,
            seed.authorization_digest,
            seed.runtime_code_digest,
        )
        untrusted_segment = forged.segment_image(
            value=ComplexBallRecord("1", "2", "3", "4"),
            segment_id="untrusted-segment",
            precision_bits=192,
        )

        with self.assertRaises(InvalidRealEvidence):
            trusted.half_plane(
                segment=untrusted_segment,
                rotation_real="1",
                rotation_imag="0",
                rotated_real_lower="1",
            )

    def test_dataclasses_replace_cannot_change_review_chain_digest(self):
        trusted = RealEvidenceFactory.from_authorization(
            validated_test_authorization(),
            backend_id="sealed-backend",
        )
        segment = trusted.segment_image(
            value=ComplexBallRecord("1", "2", "3", "4"),
            segment_id="trusted-segment",
            precision_bits=192,
        )
        with self.assertRaises(InvalidRealEvidence):
            replace(segment, review_chain_digest="f" * 64)

    def test_validated_factory_rejects_non_probative_half_plane_with_matching_ids(self):
        trusted = RealEvidenceFactory.from_authorization(
            validated_test_authorization(),
            backend_id="sealed-backend",
        )
        seed = trusted.segment_image(
            value=ComplexBallRecord("1", "2", "3", "4"),
            segment_id="trusted-seed",
            precision_bits=192,
        )
        forged = RealEvidenceFactory(
            seed.backend_id,
            seed.authorization_digest,
            seed.runtime_code_digest,
        )
        forged_segment = forged.segment_image(
            value=ComplexBallRecord("1", "2", "3", "4"),
            segment_id="forged-segment",
            precision_bits=192,
        )
        forged_half_plane = forged.half_plane(
            segment=forged_segment,
            rotation_real="1",
            rotation_imag="0",
            rotated_real_lower="1",
        )

        with self.assertRaises(InvalidRealEvidence):
            trusted.argument_increment(forged_half_plane, "0.1", "0.2")

    def test_validated_winding_rejects_one_bad_increment_among_valid_increments(self):
        trusted = RealEvidenceFactory.from_authorization(
            validated_test_authorization(),
            backend_id="sealed-backend",
        )
        trusted_segment = trusted.segment_image(
            value=ComplexBallRecord("1", "2", "3", "4"),
            segment_id="trusted-segment",
            precision_bits=192,
        )
        trusted_half_plane = trusted.half_plane(
            segment=trusted_segment,
            rotation_real="1",
            rotation_imag="0",
            rotated_real_lower="1",
        )
        good_increment = trusted.argument_increment(
            trusted_half_plane, "0.1", "0.2"
        )

        forged = RealEvidenceFactory(
            good_increment.backend_id,
            good_increment.authorization_digest,
            good_increment.runtime_code_digest,
        )
        forged_segment = forged.segment_image(
            value=ComplexBallRecord("1", "2", "3", "4"),
            segment_id="forged-segment",
            precision_bits=192,
        )
        forged_half_plane = forged.half_plane(
            segment=forged_segment,
            rotation_real="1",
            rotation_imag="0",
            rotated_real_lower="1",
        )
        bad_increment = forged.argument_increment(
            forged_half_plane, "0.1", "0.2"
        )

        with self.assertRaises(InvalidRealEvidence):
            trusted.winding(
                (good_increment, bad_increment),
                RealBallRecord("0.9", "1.1"),
                1,
            )


if __name__ == "__main__":
    unittest.main()
