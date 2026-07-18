import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


AUTHORIZATION_ENV = "ATHENA_H2_EXECUTION_AUTHORIZED"
AUTHORIZATION_PATH_ENV = "ATHENA_H2_AUTHORIZATION_PATH"


def real_execution_gate() -> bool:
    if os.environ.get(AUTHORIZATION_ENV) != "1":
        return False
    path_text = os.environ.get(AUTHORIZATION_PATH_ENV)
    if not path_text:
        return False
    try:
        payload = json.loads(Path(path_text).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    return payload.get("experiment_id") == "G5B-006F" and payload.get(
        "execution_authorized"
    ) is True


class H2RealExecutionGateTests(unittest.TestCase):
    def test_environment_flag_alone_does_not_open_gate(self):
        with patch.dict(
            os.environ,
            {AUTHORIZATION_ENV: "1"},
            clear=True,
        ):
            self.assertFalse(real_execution_gate())

    def test_authorization_file_alone_does_not_open_gate(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "authorization.json"
            path.write_text(
                json.dumps(
                    {"experiment_id": "G5B-006F", "execution_authorized": True}
                ),
                encoding="utf-8",
            )
            with patch.dict(
                os.environ,
                {AUTHORIZATION_PATH_ENV: str(path)},
                clear=True,
            ):
                self.assertFalse(real_execution_gate())

    def test_new_l3_backend_endpoints_raise_unauthorized_if_uninitialized(self):
        from athena_azr.h2_zero_certifier.python_flint_backend import PythonFlintBackend
        from athena_azr.h2_zero_certifier.authorization import ExecutionNotAuthorized
        backend = PythonFlintBackend()
        
        with self.assertRaises(ExecutionNotAuthorized):
            backend.completed_l3_point(None, 192)
            
        with self.assertRaises(ExecutionNotAuthorized):
            backend.completed_l3_segment(None, 192)
            
        with self.assertRaises(ExecutionNotAuthorized):
            backend.validate_half_plane(None, 192)

        with self.assertRaises(ExecutionNotAuthorized):
            backend.argument_increment(None, 192)
            
        with self.assertRaises(ExecutionNotAuthorized):
            backend.unique_integer(None, None)
            
        with self.assertRaises(ExecutionNotAuthorized):
            backend.l3_box_winding_count(None, 192)

        with self.assertRaises(ExecutionNotAuthorized):
            backend.l3_critical_line_certified(None, 192)

        with self.assertRaises(ExecutionNotAuthorized):
            backend.l3_count_certificate(143, 192)

        with self.assertRaises(ExecutionNotAuthorized):
            backend.real_completed_l3_point(None, 192)

        with self.assertRaises(ExecutionNotAuthorized):
            backend.real_completed_l3_segment(None, 192)



@unittest.skipUnless(
    real_execution_gate(),
    "requires both the 006F environment gate and a readable 006F authorization",
)
class H2RealFlintGuardedTests(unittest.TestCase):
    def test_real_flint_certification_requires_a_reviewed_implementation(self):
        self.fail("006F real FLINT certification is not implemented or authorized")


if __name__ == "__main__":
    unittest.main()
