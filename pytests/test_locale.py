# Copyright 2004-2026 Tom Rothamel <pytom@bishoujo.us>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
Isolate native locale state and CPython initialization in fresh processes.
"""

import os
import subprocess
import sys
import textwrap

import pytest

pytestmark = pytest.mark.skipif(os.name != "posix", reason="Native POSIX locale tests")


def run_case(code: str, variables: dict[str, str] | None = None) -> None:
    """
    Runs a snippet in a fresh interpreter with Python UTF-8 mode but without automatic locale coercion.
    The snippet's assertions fail the test through a nonzero exit status, whose output is reported.

    The prelude provides a set_utf8_locale import and a check_utf8_child helper that asserts that a
    native child process also sees UTF-8. It also provides patch_object, a small replacement for
    mock.patch.object that restores the original attribute on exit.
    """

    env = {key: value for key, value in os.environ.items() if key != "LANG" and not key.startswith("LC_")}
    env.update(PYTHONCOERCECLOCALE="0", PYTHONUTF8="1")
    if variables:
        env.update(variables)

    prelude = """
import contextlib
import io
import locale
import os
import subprocess
import sys

import renpy
from renpy.bootstrap import set_utf8_locale

def check_utf8_child():
    assert locale.getencoding().lower().replace("-", "") == "utf8"
    output = subprocess.check_output(
        [sys.executable, "-c", "import locale; print(locale.nl_langinfo(locale.CODESET))"],
        text=True,
    )
    assert output.strip().lower().replace("-", "") == "utf8", output

@contextlib.contextmanager
def patch_object(target, attribute, value):
    original = getattr(target, attribute)
    setattr(target, attribute, value)
    try:
        yield
    finally:
        setattr(target, attribute, original)
"""
    result = subprocess.run(
        [sys.executable, "-X", "utf8", "-c", textwrap.dedent(prelude) + textwrap.dedent(code)],
        env=env,
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.parametrize(
    "variables",
    [
        {},
        {"LANG": "C"},
        {"LC_CTYPE": "C"},
        {"LANG": "C", "LC_ALL": "", "LC_CTYPE": ""},
        {"LC_ALL": "C", "LC_CTYPE": "C.UTF-8"},
    ],
    ids=["no-overrides", "lang-c", "lc-ctype-c", "empty-lc-all-and-ctype", "lc-all-c-with-utf8-ctype"],
)
def test_non_utf8_environments_reach_native_children(variables: dict[str, str]) -> None:
    """Python UTF-8 mode must not hide ASCII inherited by native children."""

    run_case(
        """
assert sys.flags.utf8_mode
assert locale.getpreferredencoding(False) == "utf-8"
assert locale.getencoding().lower().replace("-", "") != "utf8"
set_utf8_locale()
check_utf8_child()
""",
        variables,
    )


def test_utf8_environment_and_repeated_calls_are_unchanged() -> None:
    """A working environment, including LC_ALL, needs no rewriting."""

    run_case(
        """
set_utf8_locale()
os.environ["LC_ALL"] = os.environ["LC_CTYPE"]
before = dict(os.environ)
original = locale.setlocale(locale.LC_CTYPE)
set_utf8_locale()
set_utf8_locale()
assert dict(os.environ) == before
assert locale.setlocale(locale.LC_CTYPE) == original
check_utf8_child()
""",
        {"LANG": "C"},
    )


def test_native_utf8_does_not_hide_ascii_environment() -> None:
    """A UTF-8 native locale alone does not fix LC_ALL inherited by children."""

    run_case(
        """
set_utf8_locale()
os.environ["LC_ALL"] = "C"
set_utf8_locale()
check_utf8_child()
assert "LC_ALL" not in os.environ
""",
        {"LANG": "C"},
    )


def test_only_character_category_changes() -> None:
    """Numeric formatting and language selection are not replaced with the fallback locale."""

    run_case(
        """
categories = (locale.LC_COLLATE, locale.LC_MESSAGES, locale.LC_MONETARY, locale.LC_NUMERIC, locale.LC_TIME)
before = [locale.setlocale(category) for category in categories]
environment = dict(os.environ)
set_utf8_locale()
assert [locale.setlocale(category) for category in categories] == before
assert {key: value for key, value in os.environ.items() if key != "LC_CTYPE"} == environment
assert locale.localeconv()["decimal_point"] == "."
check_utf8_child()
""",
        {"LANG": "C", "LC_NUMERIC": "C", "LANGUAGE": "pt_BR:en"},
    )


@pytest.mark.parametrize("platform", ["linux", "darwin", "freebsd14"])
def test_lc_all_preserves_overridden_categories(platform: str) -> None:
    """Removing LC_ALL must not expose category values that it previously overrode."""

    run_case(
        f"""
with patch_object(sys, "platform", {platform!r}):
    set_utf8_locale()
assert "LC_ALL" not in os.environ
categories = ["LC_COLLATE", "LC_MESSAGES", "LC_MONETARY", "LC_NUMERIC", "LC_TIME"]
extensions = ["LC_PAPER", "LC_NAME", "LC_ADDRESS", "LC_TELEPHONE", "LC_MEASUREMENT", "LC_IDENTIFICATION"]
for category in categories:
    assert os.environ[category] == "C", (category, os.environ[category])
for category in extensions:
    if {platform!r} == "linux":
        assert os.environ[category] == "C"
    else:
        assert category not in os.environ
assert os.environ["LANG"] == "C"
assert os.environ["LANGUAGE"] == "pt_BR"
check_utf8_child()
""",
        {"LC_ALL": "C", "LC_NUMERIC": "invalid-hidden-locale", "LANG": "C", "LANGUAGE": "pt_BR"},
    )


@pytest.mark.parametrize("accepted", ["C.utf8", "UTF-8"])
def test_portable_candidate_fallbacks(accepted: str) -> None:
    """Support hosts with only C.utf8 or the macOS/BSD partial UTF-8 locale."""

    run_case(
        f"""
native_setlocale = locale.setlocale
def setlocale(category, value=None):
    if value in ("C.UTF-8", "C.utf8", "UTF-8"):
        if value != {accepted!r}:
            raise locale.Error("candidate unavailable")
        return value
    return native_setlocale(category, value)

# Selection is simulated; this does not validate a Darwin locale on Linux.
encodings = iter(["ASCII", "UTF-8"])
with patch_object(locale, "setlocale", setlocale), patch_object(locale, "getencoding", lambda: next(encodings)):
    set_utf8_locale()
assert os.environ["LC_CTYPE"] == {accepted!r}
""",
        {"LANG": "C"},
    )


def test_unavailable_utf8_warns_and_restores_state() -> None:
    """An unusable candidate must not leave partial native or environment changes."""

    run_case(
        """
original = locale.setlocale(locale.LC_CTYPE)
environment = dict(os.environ)
native_setlocale = locale.setlocale
def setlocale(category, value=None):
    if value in ("C.UTF-8", "C.utf8", "UTF-8"):
        # Even an accepted candidate must be rejected if its actual encoding is not UTF-8.
        return native_setlocale(category, "C")
    return native_setlocale(category, value)

warning = io.StringIO()
with patch_object(locale, "setlocale", setlocale), contextlib.redirect_stderr(warning):
    set_utf8_locale()
assert "Warning:" in warning.getvalue()
assert "UTF-8" in warning.getvalue()
assert dict(os.environ) == environment
assert locale.setlocale(locale.LC_CTYPE) == original
""",
        {"LC_ALL": "C", "LC_NUMERIC": "hidden"},
    )


def test_invalid_environment_warns_and_restores_state() -> None:
    """Report an invalid environment without changing the original native locale."""

    run_case(
        """
environment = dict(os.environ)
original = locale.setlocale(locale.LC_CTYPE)
warning = io.StringIO()
with contextlib.redirect_stderr(warning):
    set_utf8_locale()
assert "Warning:" in warning.getvalue()
assert dict(os.environ) == environment
assert locale.setlocale(locale.LC_CTYPE) == original
""",
        {"LC_ALL": "renpy-invalid-locale"},
    )


def test_non_posix_and_mobile_platforms_are_untouched() -> None:
    """Do not configure native locales on Windows, mobile, or web."""

    run_case(
        """
for target, attribute, value in (
    (os, "name", "nt"),
    (renpy, "android", True),
    (renpy, "ios", True),
    (renpy, "emscripten", True),
):
    environment = dict(os.environ)
    calls = []
    with patch_object(target, attribute, value), patch_object(locale, "setlocale", lambda *args: calls.append(args)):
        set_utf8_locale()
    assert not calls
    assert dict(os.environ) == environment
""",
        {"LANG": "C"},
    )


@pytest.mark.skipif(not sys.platform.startswith("linux"), reason="Controlled Linux tinyfiledialogs backend")
def test_native_dialog_preserves_utf8_text_and_cancellation() -> None:
    """Exercise C popen inheritance with a controlled kdialog, without a display server."""

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
    run_case(
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
