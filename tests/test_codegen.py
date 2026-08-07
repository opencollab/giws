# Copyright or Copr. INRIA/Scilab - Sylvestre LEDRU
#
# This software is a computer program whose purpose is to generate C++ wrapper
# for Java objects/methods.
#
# This software is governed by the CeCILL license under French law. See the
# file COPYING for details.

"""Tests for the code generator.

Each case runs giws on an example XML declaration (with the same flags
as the example's Makefile) and checks the generated C++. No JDK needed.
"""

import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
EXAMPLES = ROOT / "examples"
GIWS = ROOT / "giws"

# (example directory, giws flags) - mirrors GFLAGS in examples/*/Makefile
CASES = [
    ("basic_example", ["-p"]),
    ("bug_disable_return", ["-r"]),
    ("bug_no_param_int_array", []),
    ("bug_nonstatic_exception", ["-p", "--throws-exception-on-error", "-g"]),
    ("bug_string_array_len", ["-p"]),
    ("bytebuffer", ["-p", "--throws-exception-on-error", "-g"]),
    ("example1", ["-p"]),
    ("example2", ["-p", "--disable-return-size-array"]),
    ("example3", ["-p", "--throws-exception-on-error", "-g"]),
    ("example4", ["-p"]),
    ("example5", ["-p"]),
    ("inherit", ["-p"]),
]


def run_giws(args, cwd):
    return subprocess.run(
        [sys.executable, str(GIWS), *args],
        cwd=cwd,
        capture_output=True,
        text=True,
    )


def generate(example, flags, destination):
    """Run giws on an example and return the generated files by name."""
    xml = next((EXAMPLES / example).glob("*.giws.xml"))
    shutil.copy(xml, destination / xml.name)
    result = run_giws(["-f", xml.name, *flags], cwd=destination)
    assert result.returncode == 0, result.stderr
    generated = {
        p.name: p.read_text()
        for p in destination.iterdir()
        if p.suffix in (".cpp", ".hxx")
    }
    assert generated, f"giws produced no output for {example}"
    return generated


@pytest.mark.parametrize("example,flags", CASES, ids=[c[0] for c in CASES])
def test_examples_generate(example, flags, tmp_path):
    generated = generate(example, flags, tmp_path)
    for name, content in generated.items():
        assert content.strip(), f"{example}/{name} is empty"


def test_nonstatic_method_checks_exceptions(tmp_path):
    """A Java exception thrown by a non-static method must be detected.

    The check used to be generated for static methods only.
    """
    generated = generate(
        "bug_nonstatic_exception",
        ["-p", "--throws-exception-on-error", "-g"],
        tmp_path,
    )
    body = generated["bug_nonstatic_exception.cpp"]
    method = body.split("void MyThrowingObject::alwaysThrows")[1]
    assert "ExceptionCheck()" in method
    assert "JniCallMethodException" in method


def test_exception_class_checks_after_each_call(tmp_path):
    """GiwsException helpers must not call JNI functions while an
    exception raised by CallObjectMethod is pending (-Xcheck:jni)."""
    generated = generate(
        "example3", ["-p", "--throws-exception-on-error", "-g"], tmp_path
    )
    body = generated["GiwsException.cpp"]
    calls = list(re.finditer(r"CallObjectMethod\(", body))
    assert calls, "no CallObjectMethod in GiwsException.cpp"
    for call in calls:
        following = body[call.end() : call.end() + 400]
        assert "ExceptionCheck()" in following, (
            "CallObjectMethod without a following ExceptionCheck near "
            f"offset {call.start()}"
        )


def test_version_option():
    result = run_giws(["--version"], cwd=ROOT)
    assert result.returncode == 0
    assert "GIWS " in result.stdout


def test_no_arguments_is_an_error():
    result = run_giws([], cwd=ROOT)
    assert result.returncode == 2
    assert "description file" in result.stderr


def test_missing_description_file_is_an_error(tmp_path):
    result = run_giws(["-f", "doesnotexist.xml"], cwd=tmp_path)
    assert result.returncode == 2
    assert "doesnotexist.xml" in result.stderr
