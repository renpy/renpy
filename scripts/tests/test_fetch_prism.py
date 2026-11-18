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

"""Tests for fetching standalone Prism libraries without initializing the Ren'Py engine."""

import io
import zipfile

import pytest

from scripts import fetch_prism


def _build_mock_sdk_zip(tag="v0.18.3"):
    """Build an in-memory SDK archive with fake binaries for each target platform plus one ignored shim."""
    buf = io.BytesIO()
    payloads = {
        f"prism-sdk-{tag}/windows/x64/dynamic/release/bin/prism.dll": b"MZ_FAKE_WINDOWS_DLL" * 50,
        f"prism-sdk-{tag}/macos/universal/dynamic/release/lib/libprism.dylib": b"\xcf\xfa\xed\xfe_FAKE_MAC_DYLIB" * 50,
        f"prism-sdk-{tag}/linux/x64/dynamic/release/lib/libprism.so": b"\x7fELF_FAKE_LINUX_X64_SO" * 50,
        f"prism-sdk-{tag}/linux/arm64/dynamic/release/lib/libprism.so": b"\x7fELF_FAKE_LINUX_ARM64_SO" * 50,
        f"prism-sdk-{tag}/windows/x64/dynamic/release/bin/tolk.dll": b"SHIM_SHOULD_BE_IGNORED",
    }
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_STORED) as zf:
        for name, content in payloads.items():
            zf.writestr(name, content)
    return buf.getvalue(), payloads


def _make_range_opener(zip_bytes, resolved_tag="v0.18.3"):
    """Return a urlopen replacement that serves the archive, honoring HEAD and HTTP Range requests.

    The "latest" release URL redirects to resolved_tag, mimicking GitHub's release redirect.
    """

    class FakeResponse:
        """Minimal response object supporting read() and the context-manager protocol."""

        def __init__(self, data, url, headers):
            self._data = data
            self.url = url
            self.headers = headers

        def read(self):
            return self._data

        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

    def opener(req):
        url = req.full_url
        method = getattr(req, "method", None) or "GET"
        if url.endswith("/releases/latest"):
            return FakeResponse(
                b"",
                f"https://github.com/ethindp/prism/releases/tag/{resolved_tag}",
                {},
            )
        if method == "HEAD":
            return FakeResponse(
                b"",
                url,
                {"Content-Length": str(len(zip_bytes))},
            )
        range_hdr = req.headers.get("Range") or req.headers.get("range")
        if range_hdr and range_hdr.startswith("bytes="):
            start_s, end_s = range_hdr[len("bytes=") :].split("-")
            start = int(start_s)
            end = int(end_s)
            return FakeResponse(zip_bytes[start : end + 1], url, {})
        return FakeResponse(zip_bytes, url, {})

    return opener


def test_resolve_release_tag():
    """resolve_release_tag normalizes explicit tags and follows the redirect for "latest".

    A bare version gains the "v" prefix, an explicit tag is returned unchanged, and "latest" is resolved through the
    release redirect served by the fake opener.
    """
    zip_bytes, _ = _build_mock_sdk_zip("v0.18.3")
    opener = _make_range_opener(zip_bytes, resolved_tag="v0.18.3")

    assert fetch_prism.resolve_release_tag("0.18.3", opener=opener) == "v0.18.3"
    assert fetch_prism.resolve_release_tag("v0.18.3", opener=opener) == "v0.18.3"
    assert fetch_prism.resolve_release_tag("latest", opener=opener) == "v0.18.3"


def test_fetch_prism_libraries_extracts_only_target_binaries(tmp_path):
    """fetch_prism_libraries extracts exact platform binaries via HTTP Range requests and ignores other entries.

    Four platform binaries are written, and the macOS dylib is also copied into the app bundle. The tolk.dll shim in
    the archive must not be extracted.
    """
    zip_bytes, payloads = _build_mock_sdk_zip("v0.18.3")
    opener = _make_range_opener(zip_bytes, resolved_tag="v0.18.3")

    root_dir = tmp_path
    lib_dir = root_dir / "lib"
    mac_app_dir = root_dir / "renpy.app" / "Contents" / "MacOS"
    mac_app_dir.mkdir(parents=True)

    tag, written = fetch_prism.fetch_prism_libraries(
        version="latest",
        dest_dir=lib_dir,
        platforms="all",
        opener=opener,
    )

    assert tag == "v0.18.3"
    assert len(written) == 4

    win_dll = lib_dir / "py3-windows-x86_64" / "prism.dll"
    mac_dylib = lib_dir / "py3-mac-universal" / "libprism.dylib"
    linux_x64_so = lib_dir / "py3-linux-x86_64" / "libprism.so"
    linux_arm_so = lib_dir / "py3-linux-aarch64" / "libprism.so"
    mac_app_dylib = mac_app_dir / "libprism.dylib"

    assert win_dll.read_bytes() == payloads["prism-sdk-v0.18.3/windows/x64/dynamic/release/bin/prism.dll"]
    assert mac_dylib.read_bytes() == payloads["prism-sdk-v0.18.3/macos/universal/dynamic/release/lib/libprism.dylib"]
    assert linux_x64_so.read_bytes() == payloads["prism-sdk-v0.18.3/linux/x64/dynamic/release/lib/libprism.so"]
    assert linux_arm_so.read_bytes() == payloads["prism-sdk-v0.18.3/linux/arm64/dynamic/release/lib/libprism.so"]
    assert (
        mac_app_dylib.read_bytes() == payloads["prism-sdk-v0.18.3/macos/universal/dynamic/release/lib/libprism.dylib"]
    )
    assert not (lib_dir / "py3-windows-x86_64" / "tolk.dll").exists()


def test_fetch_zip_entry_detects_crc_mismatch():
    """fetch_zip_entry raises RuntimeError when the downloaded entry's CRC32 does not match the directory.

    The expected CRC is flipped, which simulates a corrupted download. Only the RuntimeError type is asserted here.
    """
    zip_bytes, _ = _build_mock_sdk_zip("v0.18.3")
    opener = _make_range_opener(zip_bytes, resolved_tag="v0.18.3")

    final_url, entries = fetch_prism.read_remote_zip_directory(
        "https://example.com/prism-sdk-v0.18.3.zip",
        opener=opener,
    )
    entry = dict(entries["prism-sdk-v0.18.3/windows/x64/dynamic/release/bin/prism.dll"])
    entry["crc"] ^= 0xFFFFFFFF

    with pytest.raises(RuntimeError):
        fetch_prism.fetch_zip_entry(final_url, entry, opener=opener)
