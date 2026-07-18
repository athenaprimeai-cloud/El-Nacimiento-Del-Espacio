import json
import tempfile
import unittest
from pathlib import Path

from athena_azr.h2_zero_certifier.models import (
    ComplexBox,
    FunctionCertification,
    RealInterval,
    ZeroCertificate,
)
from athena_azr.h2_zero_certifier.serialization import (
    canonical_json_bytes,
    function_zero_csv_bytes,
    write_bytes_atomic,
)


class H2SerializationTests(unittest.TestCase):
    def test_json_is_compact_sorted_utf8_and_rejects_nan(self):
        data = canonical_json_bytes({"z": 1, "a": "á"})
        self.assertEqual(data, '{"a":"á","z":1}\n'.encode("utf-8"))

        with self.assertRaises(ValueError):
            canonical_json_bytes({"bad": float("nan")})

    def test_csv_has_fixed_header_lf_and_interval_strings(self):
        zero = ZeroCertificate(
            index=1,
            function_id="L3",
            conductor=3,
            character_id="3.2",
            parity=1,
            box=ComplexBox(
                RealInterval("0.4999999999999999999999", "0.5000000000000000000001"),
                RealInterval("8.0", "8.1"),
            ),
            multiplicity=1,
            isolation_method="synthetic",
            working_precision_bits=192,
            certificate_reference="fixture",
            critical_line_certified=True,
        )
        data = function_zero_csv_bytes(FunctionCertification("L3", (zero,), ()))

        self.assertTrue(data.startswith(b"index,function_id,conductor"))
        self.assertIn(b"8.0,8.1", data)
        self.assertNotIn(b"\r\n", data)

    def test_atomic_write_stays_inside_explicit_temporary_root(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "nested" / "synthetic.json"
            write_bytes_atomic(target, b"{}\n", allowed_root=root)
            self.assertEqual(target.read_bytes(), b"{}\n")

            with self.assertRaises(ValueError):
                write_bytes_atomic(root.parent / "escape.json", b"bad", allowed_root=root)


if __name__ == "__main__":
    unittest.main()
