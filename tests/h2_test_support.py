import hashlib
import json
import tempfile
from pathlib import Path

from athena_azr.h2_zero_certifier.authorization import (
    require_execution_authorization,
)


REVIEW_HASHES = {
    "plan_006e7_sha256": "7" * 64,
    "report_006e8_sha256": "8" * 64,
    "review_006e9_sha256": "9" * 64,
    "corrections_006e10_sha256": "a" * 64,
}


def validated_test_authorization():
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        output = root / "output"
        module = root / "module.py"
        module.write_bytes(b"code")
        payload = {
            "experiment_id": "G5B-006F",
            "execution_authorized": True,
            "max_height": 500,
            "requested_heights": [143, 200, 300, 500],
            "protocol_006b_sha256": "4f110d0926067e9e1eb44cbbfe78ee1acc93f85f526176c81d98446eafd492cb",
            "plan_006c_sha256": "c" * 64,
            "spec_006e2_sha256": "4b14ba44d08d80941a4ab69776c41479453f0f08661ffec9fcb304204f1212c5",
            "plan_006e3_sha256": "4b7a277e939fab39ac6a9ce95cfe771944964a90a37dab12d005908ab849e931",
            "approved_code_hashes": {
                "module.py": hashlib.sha256(module.read_bytes()).hexdigest()
            },
            "output_directory": str(output),
            **REVIEW_HASHES,
        }
        path = root / "authorization.json"
        path.write_text(json.dumps(payload, sort_keys=True), encoding="utf-8")
        return require_execution_authorization(
            path,
            expected_protocol_hash=payload["protocol_006b_sha256"],
            expected_plan_hash=payload["plan_006c_sha256"],
            expected_spec_hash=payload["spec_006e2_sha256"],
            expected_inert_plan_hash=payload["plan_006e3_sha256"],
            expected_review_hashes=REVIEW_HASHES,
            expected_output_dir=output,
            code_root=root,
            required_code_files=("module.py",),
        )
