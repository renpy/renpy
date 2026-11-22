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
Tests for renpy.compat.ca, which sets up TLS certificate verification, chiefly the Android system certificate bundle.
"""

import os
import subprocess
import sys

import pytest


def run_in_new_process(code: str) -> None:
    """
    Runs `code` in a fresh interpreter, for tests that patch process-wide state such as ssl.SSLContext. The code's
    assertions fail the test through a nonzero exit status, whose output is reported.
    """

    result = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, check=False, timeout=30)
    assert result.returncode == 0, result.stdout + result.stderr


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

    from renpy.compat.ca import bundle_android_certificates

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

    from renpy.compat.ca import bundle_android_certificates

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

    from renpy.compat.ca import bundle_android_certificates

    bundle = tmp_path / "cacerts.pem"

    assert bundle_android_certificates([str(tmp_path / "missing")], str(bundle)) is None
    assert not bundle.exists()


@pytest.mark.skipif(not hasattr(os, "getuid"), reason="Simulates Android, which needs os.getuid (POSIX only)")
def test_android_certificates_become_ssl_defaults(tmp_path) -> None:
    """
    On Android, default SSL contexts verify against the bundled system certificates, even though OpenSSL there ignores
    SSL_CERT_FILE. That is simulated by removing the variable from the C environment with os.unsetenv, which leaves
    os.environ (what Python and truststore consult) unchanged. Runs in a fresh process because ssl.SSLContext is patched.
    """

    count = write_android_cacerts(tmp_path / "cacerts", 4)

    run_in_new_process(
        f"""
import os
import ssl

import renpy
import renpy.compat.ca

os.environ.pop("SSL_CERT_FILE", None)
os.environ["ANDROID_PRIVATE"] = {str(tmp_path)!r}

renpy.android = True
renpy.compat.ca.ANDROID_CA_DIRECTORIES = [{str(tmp_path / "cacerts")!r}]
renpy.compat.ca.set_android_certificates()

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

    from renpy.compat.ca import bundle_android_certificates

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
