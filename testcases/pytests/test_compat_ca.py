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
import platform
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


@pytest.mark.parametrize("ssl_cert_file", ["unset", "invalid"])
@pytest.mark.parametrize("error", ["ImportError", "ValueError"])
def test_failed_truststore_import_falls_back_to_certifi(tmp_path, error: str, ssl_cert_file: str) -> None:
    """
    When truststore can't be imported, default SSL contexts verify against certifi's bundle and the error is kept for
    the log, rather than startup failing. ValueError is what truststore's macOS backend raises at import when
    platform.mac_ver() returns no version, as could happen on iOS, so the fallback must catch more than ImportError.
    An SSL_CERT_FILE that exists but holds no certificates is passed over, as loading it would make every default
    context fail. Runs in a fresh process because ssl.SSLContext is patched.
    """

    invalid = tmp_path / "invalid.pem"
    invalid.write_text("not a certificate\n")

    environment = {"SSL_CERT_FILE": str(invalid)} if ssl_cert_file == "invalid" else {}

    run_in_new_process(
        f"""
import os
import ssl
import sys

import certifi

import renpy
import renpy.compat.ca

class FailingFinder:
    def find_spec(self, fullname, path, target=None):
        if fullname == "truststore":
            raise {error}("truststore unavailable")
        return None

sys.modules.pop("truststore", None)
sys.meta_path.insert(0, FailingFinder())
os.environ.pop("SSL_CERT_FILE", None)
os.environ.update({environment!r})

renpy.compat.ca.use_system_certificates()

assert "truststore unavailable" in renpy.compat.ca.truststore_error
assert renpy.compat.ca.fallback_bundle == certifi.where()
assert ssl.SSLContext.__module__ == "ssl"

expected = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
expected.load_verify_locations(cafile=certifi.where())
context = ssl.create_default_context()
# On Windows, load_default_certs also adds the system stores, so certifi need only be a subset.
assert set(expected.get_ca_certs(binary_form=True)) <= set(context.get_ca_certs(binary_form=True))
"""
    )


@pytest.mark.parametrize("source", ["SSL_CERT_FILE", "SSL_CERT_DIR"])
def test_failed_truststore_import_uses_fallback_bundle_for_requests(tmp_path, source: str) -> None:
    """
    When truststore can't be imported, requests verifies against the same certificates as ssl: a bundle named by
    SSL_CERT_FILE rather than certifi's, or certifi's bundle plus a CA directory named by SSL_CERT_DIR, as OpenSSL would
    load. A self-signed certificate (made with the openssl command, so the test skips without it) is trusted only
    through `source`, so the request to a local TLS server succeeds only if requests uses it. The session ignores the
    environment so a proxy can't intercept the request. Runs in a fresh process because ssl.SSLContext and requests are
    patched.
    """

    import shutil

    pytest.importorskip("requests")
    certifi = pytest.importorskip("certifi")

    openssl = shutil.which("openssl")

    if openssl is None:
        pytest.skip("The openssl command is needed to make a self-signed certificate.")

    cert = tmp_path / "cert.pem"
    key = tmp_path / "key.pem"

    subprocess.run(
        [
            openssl, "req", "-x509", "-newkey", "rsa:2048", "-nodes", "-days", "1",
            "-subj", "/CN=127.0.0.1", "-addext", "subjectAltName=IP:127.0.0.1",
            "-keyout", str(key), "-out", str(cert),
        ],
        check=True,
        capture_output=True,
    )  # fmt: skip

    if source == "SSL_CERT_FILE":
        environment = {"SSL_CERT_FILE": str(cert)}
        expected_bundle = str(cert)
    else:
        # OpenSSL finds certificates in a CA directory by the hash of their subject.
        subject_hash = subprocess.run(
            [openssl, "x509", "-hash", "-noout", "-in", str(cert)], check=True, capture_output=True, text=True
        ).stdout.strip()

        directory = tmp_path / "certs"
        directory.mkdir()
        (directory / f"{subject_hash}.0").write_bytes(cert.read_bytes())

        environment = {"SSL_CERT_DIR": str(directory)}
        expected_bundle = certifi.where()

    run_in_new_process(
        f"""
import os
import socket
import ssl
import sys
import threading

import renpy
import renpy.compat.ca

class FailingFinder:
    def find_spec(self, fullname, path, target=None):
        if fullname == "truststore":
            raise ValueError("truststore unavailable")
        return None

sys.modules.pop("truststore", None)
sys.meta_path.insert(0, FailingFinder())
os.environ.pop("SSL_CERT_FILE", None)
os.environ.pop("SSL_CERT_DIR", None)
os.environ.update({environment!r})

renpy.compat.ca.use_system_certificates()
assert renpy.compat.ca.fallback_bundle == {expected_bundle!r}

server_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
server_context.load_cert_chain({str(cert)!r}, {str(key)!r})
listener = socket.create_server(("127.0.0.1", 0))
port = listener.getsockname()[1]

def serve():
    connection, _ = listener.accept()
    with server_context.wrap_socket(connection, server_side=True) as tls:
        tls.recv(65536)
        tls.sendall(b"HTTP/1.1 200 OK\\r\\nContent-Length: 2\\r\\nConnection: close\\r\\n\\r\\nok")

threading.Thread(target=serve, daemon=True).start()

import requests

session = requests.Session()
session.trust_env = False
assert session.get(f"https://127.0.0.1:{{port}}/", timeout=10).text == "ok"
"""
    )


@pytest.mark.parametrize("backend", ["truststore._macos", "truststore._windows"])
@pytest.mark.parametrize(
    "verify, uses_truststore",
    [
        ("raise ssl.SSLCertVerificationError('untrusted')", True),
        ("raise OSError('Security.framework failed')", False),
        ("return None", False),
    ],
    ids=["rejects", "fails", "accepts"],
)
def test_truststore_backend_is_checked_before_use(backend: str, verify: str, uses_truststore: bool) -> None:
    """
    On Windows, macOS, and iOS, truststore is used only if its backend rejects a self-signed certificate. A backend
    that raises something else, or accepts the certificate, is broken, so Ren'Py falls back to certifi and records why.
    Those backends need their operating system, so a fake verification function stands in for them, marked as coming
    from the backend's module, which is how the check tells backends apart. Runs in a fresh process because
    ssl.SSLContext is patched.
    """

    pytest.importorskip("certifi")

    run_in_new_process(
        f"""
import os
import ssl

import importlib

import certifi
import truststore

import renpy
import renpy.compat.ca

def verify(ssl_context, cert_chain, server_hostname=None):
    assert cert_chain == [ssl.PEM_cert_to_DER_cert(renpy.compat.ca.TRUSTSTORE_PROBE_CERTIFICATE)]
    {verify}

verify.__module__ = {backend!r}
importlib.import_module("truststore._api")._verify_peercerts_impl = verify
os.environ.pop("SSL_CERT_FILE", None)

renpy.compat.ca.use_system_certificates()

if {uses_truststore}:
    assert renpy.compat.ca.truststore_error is None
    assert ssl.SSLContext is truststore.SSLContext
else:
    assert renpy.compat.ca.truststore_error is not None
    assert renpy.compat.ca.fallback_bundle == certifi.where()
    assert ssl.SSLContext.__module__ == "ssl"
"""
    )


@pytest.mark.skipif(
    platform.system() in ("Windows", "Darwin"), reason="truststore uses its OpenSSL backend only on other platforms."
)
@pytest.mark.parametrize("store", ["file", "directory", "invalid_directory", "none"])
def test_truststore_openssl_backend_needs_ca_certificates(tmp_path, store: str) -> None:
    """
    With its OpenSSL backend (Linux and Android), truststore is used only if it finds CA certificates, as a CA file or
    a CA directory holding one. With neither, every certificate would be rejected, so Ren'Py falls back to certifi and
    records why. A directory with a hashed name that holds no certificate counts as neither. SSL_CERT_FILE and
    SSL_CERT_DIR choose what OpenSSL's default locations hold, and truststore's list of other common locations is
    emptied so the system's own store isn't found. Runs in a fresh process because ssl.SSLContext is patched.
    """

    pytest.importorskip("certifi")

    write_android_cacerts(tmp_path / "certs", 1)

    (tmp_path / "invalid").mkdir()
    (tmp_path / "invalid" / "00000000.0").write_text("not a certificate\n")

    directories = {"directory": tmp_path / "certs", "invalid_directory": tmp_path / "invalid"}

    environment = {
        "SSL_CERT_FILE": str(tmp_path / "certs" / "00000000.0") if store == "file" else str(tmp_path / "missing.pem"),
        "SSL_CERT_DIR": str(directories.get(store, tmp_path / "missing")),
    }

    run_in_new_process(
        f"""
import importlib
import os
import ssl

import certifi
import truststore

import renpy
import renpy.compat.ca

os.environ.update({environment!r})
importlib.import_module("truststore._openssl")._CA_FILE_CANDIDATES[:] = []

renpy.compat.ca.use_system_certificates()

if {store in ("file", "directory")}:
    assert renpy.compat.ca.truststore_error is None, renpy.compat.ca.truststore_error
    assert ssl.SSLContext is truststore.SSLContext
else:
    assert "truststore found no CA certificates" in renpy.compat.ca.truststore_error
    assert renpy.compat.ca.fallback_bundle == certifi.where()
    assert ssl.SSLContext.__module__ == "ssl"
"""
    )
