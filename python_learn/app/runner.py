"""
Safe code execution: runs user code in a restricted environment,
captures stdout, and compares with expected output.
"""

import io
import sys
import traceback
import contextlib
from typing import Tuple


_FORBIDDEN = [
    "import os", "import sys", "import subprocess",
    "__import__", "eval(", "exec(", "open(",
    "os.system", "os.popen", "shutil",
]


def _is_safe(code: str) -> Tuple[bool, str]:
    lower = code.lower()
    for pat in _FORBIDDEN:
        if pat in lower:
            return False, f"Commande interdite détectée : {pat}"
    return True, ""


def run_code(code: str, timeout: int = 5) -> Tuple[bool, str, str]:
    """
    Execute code and return (success, stdout, error_message).
    """
    ok, reason = _is_safe(code)
    if not ok:
        return False, "", reason

    stdout_capture = io.StringIO()
    try:
        with contextlib.redirect_stdout(stdout_capture):
            exec(compile(code, "<exercise>", "exec"), {"__builtins__": __builtins__})
        output = stdout_capture.getvalue().rstrip("\n")
        return True, output, ""
    except Exception:
        err = traceback.format_exc().split("\n")
        clean = "\n".join(line for line in err if line.strip())
        return False, "", clean


def check_exercise(code: str, expected_output: str) -> Tuple[bool, str, str]:
    """
    Run code and check if output matches expected_output.
    Returns (passed, actual_output, error_message).
    """
    success, output, error = run_code(code)
    if not success:
        return False, "", error
    expected = expected_output.strip()
    actual = output.strip()
    return actual == expected, actual, ""
