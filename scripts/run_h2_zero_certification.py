from __future__ import annotations

import argparse
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from athena_azr.h2_zero_certifier.authorization import ExecutionNotAuthorized  # noqa: E402
from athena_azr.h2_zero_certifier.config import CertificationConfig  # noqa: E402
from athena_azr.h2_zero_certifier.pipeline import run_certification_pipeline  # noqa: E402
from athena_azr.h2_zero_certifier.python_flint_backend import PythonFlintBackend  # noqa: E402


PLAN_006C_SHA256 = "cbf9e6ef8d39032cefdd467fab274d6cd7e1569978292ecfd1fb9da70768db3f"


def parse_args(argv=None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="H2 zero certification runner (006F-gated).")
    parser.add_argument("--authorization", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--dry-validate-config", action="store_true")
    return parser.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    config = CertificationConfig.frozen_default()
    if args.dry_validate_config:
        if config.max_height != 500 or config.requested_heights != (143, 200, 300, 500):
            return 3
        return 0
    if args.authorization is None:
        return 2

    try:
        run_certification_pipeline(
            authorization_path=args.authorization,
            output_dir=args.output_dir,
            backend_factory=PythonFlintBackend,
            expected_plan_hash=PLAN_006C_SHA256,
        )
    except ExecutionNotAuthorized:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
