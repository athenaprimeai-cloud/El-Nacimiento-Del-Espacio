import unittest
from dataclasses import fields, replace

import athena_azr.h2_zero_certifier.real_evidence as real_evidence
from athena_azr.h2_zero_certifier.pipeline import require_probative_evidence
from athena_azr.h2_zero_certifier.real_evidence import (
    ComplexBallRecord,
    InvalidRealEvidence,
    RealEvidenceFactory,
)
from tests.h2_test_support import validated_test_authorization


def clone_without_constructor(source, **changes):
    clone = object.__new__(type(source))
    for descriptor in fields(source):
        value = changes.get(descriptor.name, getattr(source, descriptor.name))
        object.__setattr__(clone, descriptor.name, value)
    return clone


class H2RootIssuanceTests(unittest.TestCase):
    def setUp(self):
        self.trusted = RealEvidenceFactory.from_authorization(
            validated_test_authorization(),
            backend_id="sealed-backend",
        )
        self.trusted_root = self.trusted.segment_image(
            value=ComplexBallRecord("1", "2", "3", "4"),
            segment_id="trusted-root",
            precision_bits=192,
        )
        self.synthetic = RealEvidenceFactory(
            self.trusted_root.backend_id,
            self.trusted_root.authorization_digest,
            self.trusted_root.runtime_code_digest,
        )
        self.synthetic_root = self.synthetic.segment_image(
            value=ComplexBallRecord("9", "10", "11", "12"),
            segment_id="synthetic-root",
            precision_bits=192,
        )

    def forged_root(self):
        forged = clone_without_constructor(
            self.synthetic_root,
            probative=True,
            review_chain_digest=self.trusted_root.review_chain_digest,
        )
        object.__setattr__(
            forged,
            "digest",
            real_evidence._expected_digest(forged),
        )
        return forged

    def test_dataclasses_replace_cannot_promote_synthetic_root(self):
        with self.assertRaises(InvalidRealEvidence):
            replace(
                self.synthetic_root,
                probative=True,
                review_chain_digest=self.trusted_root.review_chain_digest,
            )

    def test_copied_provenance_and_recomputed_digest_do_not_authenticate_root(self):
        forged = self.forged_root()
        with self.assertRaises(InvalidRealEvidence):
            require_probative_evidence(forged)

    def test_validated_factory_rejects_unregistered_forged_root(self):
        forged = self.forged_root()
        with self.assertRaises(InvalidRealEvidence):
            self.trusted.half_plane(
                segment=forged,
                rotation_real="1",
                rotation_imag="0",
                rotated_real_lower="1",
            )

    def test_pipeline_rejects_forged_root_directly(self):
        with self.assertRaises(InvalidRealEvidence):
            require_probative_evidence(self.forged_root())

    def test_pipeline_rejects_child_descending_from_forged_root(self):
        valid_child = self.trusted.half_plane(
            segment=self.trusted_root,
            rotation_real="1",
            rotation_imag="0",
            rotated_real_lower="1",
        )
        forged_root = self.forged_root()
        forged_child = clone_without_constructor(
            valid_child,
            segment=forged_root,
            parent_evidence_hashes=(forged_root.digest,),
        )
        object.__setattr__(
            forged_child,
            "digest",
            real_evidence._expected_digest(forged_child),
        )

        with self.assertRaises(InvalidRealEvidence):
            require_probative_evidence(forged_child)

    def test_synthetic_and_probative_factories_do_not_share_capability(self):
        self.assertIsNot(
            self.synthetic_root._capability,
            self.trusted_root._capability,
        )

    def test_public_digest_recomputation_cannot_create_registered_issuance(self):
        unregistered_clone = clone_without_constructor(self.trusted_root)
        object.__setattr__(
            unregistered_clone,
            "digest",
            real_evidence._expected_digest(unregistered_clone),
        )

        with self.assertRaises(InvalidRealEvidence):
            require_probative_evidence(unregistered_clone)


if __name__ == "__main__":
    unittest.main()
