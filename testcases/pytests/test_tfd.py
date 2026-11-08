"""
Tests for renpy.tfd, the tinyfiledialogs wrapper, run against a controlled native backend.
"""

import os
import subprocess
import sys
import textwrap

import pytest

PRELUDE = """
import os
import sys

from renpy.bootstrap import set_utf8_locale
"""


def run_in_fresh_interpreter(code: str, variables: dict[str, str]) -> None:
    """
    Runs a snippet in a fresh interpreter with Python UTF-8 mode but without automatic locale coercion, and with
    the given environment variables in place of any inherited locale variables. The snippet's assertions fail the
    test through a nonzero exit status, whose output is reported.

    A fresh process is needed because tinyfiledialogs starts its backend with the C library's popen, which
    inherits the native locale of the process, and not the encoding that Python's UTF-8 mode gives its own text.
    The snippet starts with set_utf8_locale, os, and sys already imported.
    """

    env = {key: value for key, value in os.environ.items() if key != "LANG" and not key.startswith("LC_")}
    env.update(PYTHONCOERCECLOCALE="0", PYTHONUTF8="1")
    env.update(variables)

    result = subprocess.run(
        [sys.executable, "-X", "utf8", "-c", textwrap.dedent(PRELUDE) + textwrap.dedent(code)],
        env=env,
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.skipif(not sys.platform.startswith("linux"), reason="Controlled Linux tinyfiledialogs backend")
def test_native_dialog_preserves_utf8_text_and_cancellation() -> None:
    """
    selectFolderDialog passes UTF-8 titles to the native backend and returns its UTF-8 answer, and returns None
    when the user cancels.

    This exercises C popen inheritance with a controlled kdialog, without a display server. A script named
    kdialog on the PATH logs the locale encoding it was started with and the arguments it was given, and
    answers with a directory whose name is not ASCII. LC_ALL=C is set in the environment, so the dialog only
    sees UTF-8 because set_utf8_locale fixed the native locale.
    """

    backend = """
import json
import locale
import os
import sys

if "--getexistingdirectory" not in sys.argv:
    print("Unknown")
    sys.exit(0)

with open(os.environ["RENPY_TEST_DIALOG_LOG"], "w", encoding="utf-8") as log:
    json.dump({"encoding": locale.nl_langinfo(locale.CODESET), "args": sys.argv[1:]}, log)
if os.environ.get("RENPY_TEST_CANCEL"):
    sys.exit(1)
print(os.environ["RENPY_TEST_DIRECTORY"])
"""
    run_in_fresh_interpreter(
        f"""
import json
import tempfile
from pathlib import Path
from renpy import tfd

set_utf8_locale()
with tempfile.TemporaryDirectory() as directory:
    backend = Path(directory, "kdialog")
    backend.write_text("#!" + sys.executable + "\\n" + {textwrap.dedent(backend)!r}, encoding="utf-8")
    backend.chmod(0o700)
    selected = Path(directory, "caf\\u00e9")
    selected.mkdir()
    log = Path(directory, "dialog.json")
    os.environ.update(
        PATH=directory,
        DISPLAY=":renpy-test",
        XDG_SESSION_DESKTOP="KDE",
        RENPY_TEST_DIALOG_LOG=str(log),
        RENPY_TEST_DIRECTORY=str(selected),
    )
    title = "Selecione o diret\\u00f3rio de projetos"
    assert tfd.selectFolderDialog(title, None) == str(selected)
    record = json.loads(log.read_text(encoding="utf-8"))
    assert record["encoding"].lower().replace("-", "") == "utf8", record
    assert record["args"][record["args"].index("--title") + 1] == title, record
    os.environ["RENPY_TEST_CANCEL"] = "1"
    assert tfd.selectFolderDialog(title, None) is None
""",
        {"LC_ALL": "C"},
    )
