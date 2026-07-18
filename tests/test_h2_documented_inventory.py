import hashlib
import unittest
from pathlib import Path

from athena_azr.h2_zero_certifier.authorization import PROBATIVE_RUNTIME_CODE_FILES


class H2DocumentedInventoryTests(unittest.TestCase):
    def test_006e8_lists_every_probative_runtime_file_with_current_hash(self):
        root = Path(__file__).resolve().parents[1]
        report = (
            root
            / "docs"
            / "experimentos"
            / "experimento-006e8-c03b-l3-real-backend-inert-code-report.md"
        ).read_text(encoding="utf-8")

        for relative_name in PROBATIVE_RUNTIME_CODE_FILES:
            digest = hashlib.sha256((root / relative_name).read_bytes()).hexdigest()
            self.assertIn(
                f"{relative_name} {digest}",
                report,
                msg=f"006E8 inventory is missing or stale: {relative_name}",
            )


if __name__ == "__main__":
    unittest.main()
