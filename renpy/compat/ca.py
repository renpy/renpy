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
Sets up TLS certificate verification, so that ssl and requests verify certificates against the
operating system's trust store (through truststore) rather than certifi's bundle. On Android,
where neither OpenSSL nor truststore can find the system store, this bundles it for them.
"""

import importlib.abc
import importlib.util
import os
import sys

import renpy


def disable_requests_ca_bundle(adapters) -> None:
    """
    Stops requests from loading its default (certifi) CA bundle when `verify` is True, so that
    urllib3 loads the default certificates, which truststore provides from the system store. An
    explicit CA bundle path passed as `verify` (or via REQUESTS_CA_BUNDLE) is still honored.

    `adapters` is the requests.adapters module.
    """

    original_cert_verify = adapters.HTTPAdapter.cert_verify

    def cert_verify(self, conn, url, verify, cert):
        if verify is True and url.lower().startswith("https"):
            # Clears ca_certs and ca_cert_dir, then requires verification against the defaults.
            original_cert_verify(self, conn, url, False, cert)
            conn.cert_reqs = "CERT_REQUIRED"
        else:
            original_cert_verify(self, conn, url, verify, cert)

    adapters.HTTPAdapter.cert_verify = cert_verify


class RequestsAdaptersLoader(importlib.abc.Loader):
    """
    Wraps the loader of requests.adapters, calling disable_requests_ca_bundle once the module
    has been executed. Other attributes are delegated to the wrapped loader.
    """

    def __init__(self, loader):
        self.loader = loader

    def __getattr__(self, name):
        return getattr(self.loader, name)

    def create_module(self, spec):
        return self.loader.create_module(spec)

    def exec_module(self, module):
        self.loader.exec_module(module)
        disable_requests_ca_bundle(module)


class RequestsAdaptersFinder(importlib.abc.MetaPathFinder):
    """
    A one-shot meta path finder that arranges for requests.adapters to be patched when it is
    first imported, so requests need not be imported at startup.
    """

    def find_spec(self, fullname, path, target=None):
        if fullname != "requests.adapters":
            return None

        if self in sys.meta_path:
            sys.meta_path.remove(self)

        spec = importlib.util.find_spec(fullname)

        if spec is None or spec.loader is None:
            return spec

        spec.loader = RequestsAdaptersLoader(spec.loader)
        return spec


ANDROID_CA_DIRECTORIES: list[str] = [
    "/apex/com.android.conscrypt/cacerts",
    "/system/etc/security/cacerts",
]
"""
Directories holding Android's system CA certificates, one PEM file per certificate, in order of
preference. The conscrypt APEX directory exists on Android 14 and later, and is updated with the
APEX; the system directory is used on earlier versions.
"""


def android_certificate_der(data: bytes) -> bytes:
    """
    Returns the DER encoding of the certificate in `data`, which may be PEM (optionally followed
    by text, as in Android's system store) or DER (as in Android's records of disabled
    certificates). This identifies a certificate regardless of the file it was stored in.
    """

    begin = data.find(b"-----BEGIN CERTIFICATE-----")

    if begin == -1:
        return data

    end = data.find(b"-----END CERTIFICATE-----", begin)

    if end == -1:
        return data

    import base64

    body = data[begin + len(b"-----BEGIN CERTIFICATE-----") : end]

    try:
        return base64.b64decode(b"".join(body.split()), validate=True)
    except ValueError:
        return data


def bundle_android_certificates(directories: list[str], bundle: str, removed: str | None = None) -> str | None:
    """
    Concatenates the certificates in the first of `directories` that contains files into the
    PEM file at `bundle`, so OpenSSL can load them as a CA file. (Android names its certificate
    files with OpenSSL's old subject hash, so they can't be used as a CA directory.) The text
    Android places after each certificate is skipped by OpenSSL's PEM reader.

    `removed`, if given, is the directory where Android records the system certificates the
    user or an administrator disabled, as copies of those certificates. A system certificate is
    left out if a record has the same certificate (as Conscrypt's certificate store matches) or
    the same file name (as Android's app trust source matches), so nothing Android rejects is
    trusted. The two can differ because the numeric suffix of a name is assigned separately in
    each directory.

    The bundle is only rewritten when its contents change, through a temporary file unique to
    this process, so other processes never see a partial bundle. Returns `bundle`, or None if
    no certificates were found or the bundle could not be written.
    """

    disabled: set[bytes] = set()
    disabled_names: set[str] = set()

    if removed is not None:
        try:
            removed_names = os.listdir(removed)
        except OSError:
            removed_names = []

        for name in removed_names:
            disabled_names.add(name)

            try:
                with open(os.path.join(removed, name), "rb") as f:
                    disabled.add(android_certificate_der(f.read()))
            except OSError:
                continue

    certificates: list[bytes] = []

    for directory in directories:
        try:
            names = sorted(os.listdir(directory))
        except OSError:
            continue

        found = False

        for name in names:
            path = os.path.join(directory, name)

            if not os.path.isfile(path):
                continue

            found = True

            try:
                with open(path, "rb") as f:
                    certificate = f.read()
            except OSError:
                continue

            if name in disabled_names or android_certificate_der(certificate) in disabled:
                continue

            certificates.append(certificate)

        if found:
            break

    if not certificates:
        return None

    data = b"\n".join(certificates)

    try:
        with open(bundle, "rb") as f:
            if f.read() == data:
                return bundle
    except OSError:
        pass

    new_bundle = f"{bundle}.{os.getpid()}.new"

    try:
        with open(new_bundle, "wb") as f:
            f.write(data)

        os.replace(new_bundle, bundle)
    except OSError:
        try:
            os.unlink(new_bundle)
        except OSError:
            pass

        return None

    return bundle


def set_android_certificates() -> None:
    """
    On Android, makes a bundle of the system's CA certificates (or failing that, certifi's
    bundle) the default certificates of every ssl.SSLContext. truststore treats Android as
    generic Linux, and none of the locations OpenSSL or truststore search exist there, so
    without this no certificate could be verified.

    OpenSSL on Android ignores SSL_CERT_FILE, so SSLContext.set_default_verify_paths (which
    load_default_certs and truststore call) is replaced with one that loads the bundle
    explicitly. SSL_CERT_FILE is still set, as truststore only loads the default certificates
    when Python reports a default CA file. This must run before truststore is imported, so
    the contexts truststore creates use the replacement. An existing SSL_CERT_FILE naming a
    file is used as the bundle.
    """

    if not renpy.android:
        return

    import ssl

    bundle = os.environ.get("SSL_CERT_FILE")

    if bundle is not None and not os.path.isfile(bundle):
        bundle = None

    if bundle is None:
        bundle = bundle_android_certificates(
            ANDROID_CA_DIRECTORIES,
            os.path.join(os.environ["ANDROID_PRIVATE"], "cacerts.pem"),
            f"/data/misc/user/{os.getuid() // 100000}/cacerts-removed",
        )

    if bundle is None:
        try:
            import certifi

            bundle = certifi.where()
        except ImportError:
            return

    os.environ["SSL_CERT_FILE"] = bundle

    def set_default_verify_paths(self: ssl.SSLContext) -> None:
        self.load_verify_locations(cafile=bundle)

    ssl.SSLContext.set_default_verify_paths = set_default_verify_paths


def use_system_certificates() -> None:
    """
    Make ssl and requests verify TLS certificates against the operating system's trust store,
    rather than certifi's CA bundle.
    """

    set_android_certificates()

    import truststore

    if "urllib3" in sys.modules or "requests" in sys.modules:
        truststore.inject_into_ssl()
    else:
        # inject_into_ssl() imports urllib3 and requests to patch them. They have not been
        # imported yet, so replacing ssl.SSLContext is enough for them to use truststore.
        import ssl

        ssl.SSLContext = truststore.SSLContext  # type: ignore

    if "requests.adapters" in sys.modules:
        disable_requests_ca_bundle(sys.modules["requests.adapters"])
    else:
        sys.meta_path.insert(0, RequestsAdaptersFinder())
