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
import re
import sys
from collections.abc import Callable

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


TRUSTSTORE_PROBE_CERTIFICATE: str = """\
-----BEGIN CERTIFICATE-----
MIIBnjCCAUOgAwIBAgIUQv9Tde1zFs9z0+IJtS4iCqLTiy0wCgYIKoZIzj0EAwIw
IzEhMB8GA1UEAwwYdHJ1c3RzdG9yZS1wcm9iZS5pbnZhbGlkMCAXDTI2MTEyMjIx
NTIxN1oYDzIxMjYxMDI5MjE1MjE3WjAjMSEwHwYDVQQDDBh0cnVzdHN0b3JlLXBy
b2JlLmludmFsaWQwWTATBgcqhkjOPQIBBggqhkjOPQMBBwNCAAQzH5ymZSJmNGYk
WVZf3W/k2a6eMK/y5gpZAHZr0d+NrAjCYs3F7Ij5AodC2/ym9TY3Ay+YrzvWXZAq
S4B4+7UZo1MwUTAdBgNVHQ4EFgQUGtVRzMfPk//yVfJcaF4/i771tY4wHwYDVR0j
BBgwFoAUGtVRzMfPk//yVfJcaF4/i771tY4wDwYDVR0TAQH/BAUwAwEB/zAKBggq
hkjOPQQDAgNJADBGAiEAh2WTup4CaTVMMOi1eNOBoHAMIO1zM8t8R7zNG+MsYhAC
IQDU878j+UMsMCR0ReVbrigjmoVz7O7zTD8p6b7hzSy5Fg==
-----END CERTIFICATE-----
"""
"""
A self-signed certificate for truststore-probe.invalid, whose private key was discarded, so no
trust store contains it. check_truststore expects truststore to reject it.
"""


def ca_file_loads(path: str) -> bool:
    """
    Returns True if `path` is a file OpenSSL can load at least one CA certificate from, or False
    if it doesn't exist, can't be read, or holds no CA certificates.
    """

    import ssl

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)

    try:
        context.load_verify_locations(cafile=path)
    except (OSError, ssl.SSLError):
        return False

    return context.cert_store_stats()["x509_ca"] > 0


HASHED_CERTIFICATE_NAME = re.compile(r"^[0-9a-fA-F]{8}\.[0-9]+$")
"""
Matches the names OpenSSL looks certificates up by in a CA directory: the subject hash, a dot,
and a sequence number.
"""


def ca_directory_loads(directory: str) -> bool:
    """
    Returns True if `directory` is a CA directory holding at least one CA certificate OpenSSL
    can load under a hashed name, or False if it doesn't exist or holds none.
    """

    try:
        names = sorted(os.listdir(directory))
    except OSError:
        return False

    return any(HASHED_CERTIFICATE_NAME.match(i) and ca_file_loads(os.path.join(directory, i)) for i in names)


WINDOWS_OFFLINE_CHAIN_FLAGS: int = 0x00000004 | 0x00000100
"""
CERT_CHAIN_CACHE_ONLY_URL_RETRIEVAL | CERT_CHAIN_DISABLE_AUTH_ROOT_AUTO_UPDATE, which keep
Windows from contacting the network while building a certificate chain.
"""


def check_truststore() -> None:
    """
    Checks that truststore's backend for this platform works, so a backend that imports but
    fails when used is found at startup rather than failing every HTTPS request. The check is
    offline, and can't go stale as certificates expire.

    The Windows, macOS, and iOS backends verify certificates with the operating system, so they
    are asked to verify TRUSTSTORE_PROBE_CERTIFICATE, and must give the rejection a working
    backend gives. This runs the backend's whole verification path, but doesn't check that the
    trust store has useful roots. On Windows, building a chain to an unknown root may contact
    Windows Update for its list of roots, so WINDOWS_OFFLINE_CHAIN_FLAGS are added to the chain
    flags truststore uses during the check, to keep it from delaying startup.

    The OpenSSL backend (Linux and Android) only finds the system's CA certificates and leaves
    verification to OpenSSL, failing when there are none. So it is asked to configure a context,
    which must then have CA certificates, or OpenSSL's default CA directory must hold one (as
    OpenSSL loads those only when needed).

    Raises an exception if the check fails. Must be called before truststore is injected into
    ssl, so the contexts it uses are plain ssl.SSLContexts.
    """

    import ssl

    # truststore's __init__ deletes its _api attribute, so the module is found through importlib.
    api = importlib.import_module("truststore._api")
    verify = api._verify_peercerts_impl

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)

    if verify.__module__ == "truststore._openssl":
        with api._configure_context(context):
            pass

        if context.cert_store_stats()["x509_ca"]:
            return

        capath = ssl.get_default_verify_paths().capath

        if capath and ca_directory_loads(capath):
            return

        raise RuntimeError("truststore found no CA certificates.")

    certificate = ssl.PEM_cert_to_DER_cert(TRUSTSTORE_PROBE_CERTIFICATE)

    # On Windows, truststore's chain building is wrapped to add the offline flags.
    windows = sys.modules.get("truststore._windows")
    name = "_get_and_verify_cert_chain"
    original: Callable[..., None] | None = getattr(windows, name, None)

    if windows is not None and original is not None:
        chain: Callable[..., None] = original

        def offline_get_and_verify_cert_chain(*args: object, chain_flags: int = 0, **kwargs: object) -> None:
            chain(*args, chain_flags=chain_flags | WINDOWS_OFFLINE_CHAIN_FLAGS, **kwargs)

        setattr(windows, name, offline_get_and_verify_cert_chain)

    try:
        verify(context, [certificate], server_hostname="truststore-probe.invalid")
    except ssl.SSLCertVerificationError:
        return
    finally:
        if windows is not None and original is not None:
            setattr(windows, name, original)

    raise RuntimeError("truststore accepted a self-signed certificate that no trust store contains.")


truststore_error: str | None = None
"""
The traceback of the exception that prevented truststore from being imported or used, if
use_system_certificates had to fall back to a CA bundle, or None. log_certificate_fallback
writes it to the log, as the log directory isn't known when certificates are set up.
"""

fallback_bundle: str | None = None
"""
The CA bundle that default SSL contexts verify against when truststore couldn't be used, or
None if there is none. Only meaningful when truststore_error is set.
"""


def use_certifi_certificates() -> str | None:
    """
    Makes certifi's CA bundle the default certificates of every ssl.SSLContext, for when
    truststore can't be used, as OpenSSL's default locations may not exist on the platform.
    (use_system_certificates makes requests use these defaults too.) An SSL_CERT_FILE naming a
    file with CA certificates is used instead. On Android, set_android_certificates has already
    chosen the default certificates, so nothing is changed.

    Returns the bundle that default SSL contexts verify against, or None if there is none.
    """

    if renpy.android:
        return os.environ.get("SSL_CERT_FILE")

    import ssl

    bundle = os.environ.get("SSL_CERT_FILE")

    if bundle is None or not ca_file_loads(bundle):
        try:
            import certifi

            bundle = certifi.where()
        except ImportError:
            return None

    # CA directories named by SSL_CERT_DIR, which OpenSSL would load by default, are kept. Like
    # OpenSSL, capath takes a list separated by os.pathsep, and skips entries that don't exist.
    directory = os.environ.get("SSL_CERT_DIR")

    if directory is not None and not any(os.path.isdir(i) for i in directory.split(os.pathsep)):
        directory = None

    def set_default_verify_paths(self: ssl.SSLContext) -> None:
        self.load_verify_locations(cafile=bundle, capath=directory)

    ssl.SSLContext.set_default_verify_paths = set_default_verify_paths

    return bundle


def log_certificate_fallback() -> None:
    """
    Writes to the log why use_system_certificates couldn't use truststore, and the CA bundle it
    used instead, if that happened. Called once the log directory is known.
    """

    if truststore_error is None:
        return

    if fallback_bundle is not None:
        renpy.display.log.write("Could not use the system certificate store, using %s instead:", fallback_bundle)
    else:
        renpy.display.log.write("Could not use the system certificate store, and no CA bundle was found:")

    renpy.display.log.write("%s", truststore_error.rstrip())


def use_system_certificates() -> None:
    """
    Make ssl and requests verify TLS certificates against the operating system's trust store,
    rather than certifi's CA bundle. If truststore can't be imported on this platform, or fails
    check_truststore, falls back to a CA bundle, recording the error in truststore_error and the
    bundle in fallback_bundle.
    """

    global truststore_error, fallback_bundle

    set_android_certificates()

    try:
        import truststore

        check_truststore()
    except Exception:
        import traceback

        truststore_error = traceback.format_exc()
        fallback_bundle = use_certifi_certificates()

        # Make requests use the same bundle as ssl, which may not be certifi's (on Android, or
        # with SSL_CERT_FILE). Without a bundle, requests keeps using certifi's, if it can.
        if fallback_bundle is not None:
            use_default_certificates_for_requests()

        return

    if "urllib3" in sys.modules or "requests" in sys.modules:
        truststore.inject_into_ssl()
    else:
        # inject_into_ssl() imports urllib3 and requests to patch them. They have not been
        # imported yet, so replacing ssl.SSLContext is enough for them to use truststore.
        import ssl

        ssl.SSLContext = truststore.SSLContext  # type: ignore

    use_default_certificates_for_requests()


def use_default_certificates_for_requests() -> None:
    """
    Makes requests verify against the default certificates of ssl.SSLContext rather than its
    certifi bundle, now if requests.adapters is imported, or else when it is first imported.
    """

    if "requests.adapters" in sys.modules:
        disable_requests_ca_bundle(sys.modules["requests.adapters"])
    else:
        sys.meta_path.insert(0, RequestsAdaptersFinder())
