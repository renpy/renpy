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
Tests for renpy.bootstrap.set_utf8_locale, set_android_umask, and bundle_android_certificates. The locale and umask
cases run in a fresh process, to isolate native locale state, CPython initialization, and the umask.
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


@pytest.mark.parametrize("android, expected", [(True, 0o2770), (False, 0o2700)], ids=["android", "other_platform"])
def test_android_umask_gives_new_directories_group_access(tmp_path, android: bool, expected: int) -> None:
    """
    A directory made in a setgid parent gets group access on Android, starting from Android's owner-only umask.

    Group access has to come from the umask because chmod on Android would clear the setgid bit the directory inherits.
    """

    run_case(
        f"""
import stat
from renpy.bootstrap import set_android_umask

os.umask(0o077)

with patch_object(renpy, "android", {android}):
    set_android_umask()

os.chmod({str(tmp_path)!r}, 0o2770)
child = os.path.join({str(tmp_path)!r}, "child")
os.mkdir(child)

assert stat.S_IMODE(os.stat(child).st_mode) == {expected}
"""
    )


# Android CA certificate bundling.


def write_android_cacerts(directory, count: int) -> int:
    """
    Writes `count` certificates from certifi's bundle into `directory`, one per file, each followed by a text dump the
    way Android stores them, and returns the number written. Skips the test if certifi is unavailable.
    """

    certifi = pytest.importorskip("certifi")

    with open(certifi.where()) as f:
        pems = [p + "-----END CERTIFICATE-----\n" for p in f.read().split("-----END CERTIFICATE-----")[:-1]]

    pems = [p[p.index("-----BEGIN CERTIFICATE-----") :] for p in pems[:count]]
    assert len(pems) == count

    directory.mkdir(parents=True, exist_ok=True)

    for i, pem in enumerate(pems):
        (directory / f"{i:08x}.0").write_text(pem + "Certificate:\n    Data:\n        Version: 3 (0x2)\n")

    return count


def test_android_certificate_bundle_loads_every_certificate(tmp_path) -> None:
    """
    The bundle built from an Android-style certificate directory loads into OpenSSL with every certificate, despite the
    text dump after each one. A rebuild with the same certificates leaves the bundle unchanged.
    """

    import ssl

    from renpy.bootstrap import bundle_android_certificates

    count = write_android_cacerts(tmp_path / "cacerts", 5)
    bundle = str(tmp_path / "cacerts.pem")

    assert bundle_android_certificates([str(tmp_path / "cacerts")], bundle) == bundle

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations(cafile=bundle)
    assert context.cert_store_stats()["x509_ca"] == count

    with open(bundle, "rb") as f:
        first = f.read()

    assert bundle_android_certificates([str(tmp_path / "cacerts")], bundle) == bundle

    with open(bundle, "rb") as f:
        assert f.read() == first


@pytest.mark.parametrize(
    "first, second, expected",
    [(3, 5, 3), (None, 5, 5), (0, 5, 5)],
    ids=["first_wins", "missing_first", "empty_first"],
)
def test_android_certificate_bundle_uses_first_nonempty_directory(
    tmp_path, first: int | None, second: int, expected: int
) -> None:
    """
    Certificates come from the first directory that exists and contains certificates, so the updatable APEX store is
    preferred over the older system store, and a missing or empty APEX directory falls through to the system store.
    """

    import ssl

    from renpy.bootstrap import bundle_android_certificates

    if first is not None:
        if first:
            write_android_cacerts(tmp_path / "first", first)
        else:
            (tmp_path / "first").mkdir()

    write_android_cacerts(tmp_path / "second", second)
    bundle = str(tmp_path / "cacerts.pem")

    assert bundle_android_certificates([str(tmp_path / "first"), str(tmp_path / "second")], bundle) == bundle

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations(cafile=bundle)
    assert context.cert_store_stats()["x509_ca"] == expected


def test_android_certificate_bundle_without_certificates(tmp_path) -> None:
    """
    With no certificate directory present, no bundle is written and None is returned, so the caller falls back to
    certifi rather than pointing OpenSSL at an empty file.
    """

    from renpy.bootstrap import bundle_android_certificates

    bundle = tmp_path / "cacerts.pem"

    assert bundle_android_certificates([str(tmp_path / "missing")], str(bundle)) is None
    assert not bundle.exists()


def test_android_certificates_become_ssl_defaults(tmp_path) -> None:
    """
    On Android, default SSL contexts verify against the bundled system certificates, even though OpenSSL there ignores
    SSL_CERT_FILE. That is simulated by removing the variable from the C environment with os.unsetenv, which leaves
    os.environ (what Python and truststore consult) unchanged. Runs in a fresh process because ssl.SSLContext is patched.
    """

    count = write_android_cacerts(tmp_path / "cacerts", 4)

    run_case(
        f"""
import ssl
import renpy.bootstrap

os.environ.pop("SSL_CERT_FILE", None)
os.environ["ANDROID_PRIVATE"] = {str(tmp_path)!r}

with patch_object(renpy, "android", True), patch_object(renpy.bootstrap, "ANDROID_CA_DIRECTORIES", [{str(tmp_path / "cacerts")!r}]):
    renpy.bootstrap.set_android_certificates()

bundle = os.path.join({str(tmp_path)!r}, "cacerts.pem")
assert os.environ["SSL_CERT_FILE"] == bundle
os.unsetenv("SSL_CERT_FILE")

assert ssl.get_default_verify_paths().cafile == bundle
assert ssl.create_default_context().cert_store_stats()["x509_ca"] == {count}
"""
    )


@pytest.mark.parametrize("encoding", ["der", "pem"])
def test_android_certificate_bundle_omits_disabled_certificates(tmp_path, encoding: str) -> None:
    """
    A system certificate the user or an administrator disabled is left out of the bundle, so Ren'Py doesn't trust a CA
    that Android rejects. Android records the disabled certificate itself, and the record's file name suffix is assigned
    independently of the system store's, so the record here is deliberately named after a different certificate. Parts
    of Android match by certificate and parts by name, so both the disabled certificate and the one whose name the
    record shares are left out, and the other two stay trusted.
    """

    import ssl

    from renpy.bootstrap import bundle_android_certificates

    write_android_cacerts(tmp_path / "cacerts", 4)

    def read_pem(name: str) -> str:
        text = (tmp_path / "cacerts" / name).read_text()
        end = "-----END CERTIFICATE-----"
        return text[: text.index(end) + len(end)] + "\n"

    disabled_pem = read_pem("00000001.0")
    same_name_pem = read_pem("00000000.0")
    kept_pem = read_pem("00000002.0")

    removed = tmp_path / "removed"
    removed.mkdir()

    if encoding == "der":
        (removed / "00000000.0").write_bytes(ssl.PEM_cert_to_DER_cert(disabled_pem))
    else:
        (removed / "00000000.0").write_text(disabled_pem)

    bundle = str(tmp_path / "cacerts.pem")
    assert bundle_android_certificates([str(tmp_path / "cacerts")], bundle, str(removed)) == bundle

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations(cafile=bundle)
    trusted = {ssl.DER_cert_to_PEM_cert(der) for der in context.get_ca_certs(binary_form=True)}

    def normalize(pem: str) -> str:
        return ssl.DER_cert_to_PEM_cert(ssl.PEM_cert_to_DER_cert(pem))

    assert len(trusted) == 2
    assert normalize(kept_pem) in trusted
    assert normalize(disabled_pem) not in trusted
    assert normalize(same_name_pem) not in trusted
