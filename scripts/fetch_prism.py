#!/usr/bin/env python3
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
Fetches the standalone Prism runtime shared libraries for Windows, macOS,
and Linux directly from Prism's GitHub Releases using HTTP Range requests,
extracting only the required release binaries without downloading the full
SDK archive.
"""

import argparse
import os
import pathlib
import shutil
import struct
import urllib.request
import zlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
PRISM_REPO = "ethindp/prism"

# Mapping of Ren'Py target platforms to (SDK zip suffix, destination relative to lib/).
PLATFORM_TARGETS = {
    "windows-x86_64": (
        "windows/x64/dynamic/release/bin/prism.dll",
        "py3-windows-x86_64/prism.dll",
    ),
    "mac-universal": (
        "macos/universal/dynamic/release/lib/libprism.dylib",
        "py3-mac-universal/libprism.dylib",
    ),
    "linux-x86_64": (
        "linux/x64/dynamic/release/lib/libprism.so",
        "py3-linux-x86_64/libprism.so",
    ),
    "linux-aarch64": (
        "linux/arm64/dynamic/release/lib/libprism.so",
        "py3-linux-aarch64/libprism.so",
    ),
}

EOCD_SIGNATURE = b"PK\x05\x06"
CD_SIGNATURE = b"PK\x01\x02"
LFH_SIGNATURE = b"PK\x03\x04"
TAIL_READ_BYTES = 65536
EXTRA_HEADER_MARGIN = 256


def resolve_release_tag(version="latest", repo=PRISM_REPO, opener=urllib.request.urlopen):
    """
    Resolves a release version string ('latest' or a tag like 'v0.18.3')
    to the canonical GitHub release tag.
    """
    if version and version != "latest":
        return version if version.startswith("v") else f"v{version}"

    url = f"https://github.com/{repo}/releases/latest"
    req = urllib.request.Request(url, method="HEAD")
    with opener(req) as resp:
        final_url = resp.url.rstrip("/")

    tag = final_url.split("/")[-1]
    if not tag or tag == "latest":
        raise RuntimeError(f"Could not resolve latest release tag from {url}")
    return tag


def read_remote_zip_directory(url, opener=urllib.request.urlopen):
    """
    Reads the Central Directory of a remote ZIP archive using HTTP Range requests.
    Returns (final_url, entries_dict) where entries_dict maps archive paths to
    metadata dicts.
    """
    req_head = urllib.request.Request(url, method="HEAD")
    with opener(req_head) as resp_head:
        total_size = int(resp_head.headers["Content-Length"])
        final_url = resp_head.url

    tail_start = max(0, total_size - TAIL_READ_BYTES)
    req_tail = urllib.request.Request(
        final_url,
        headers={"Range": f"bytes={tail_start}-{total_size - 1}"},
    )
    with opener(req_tail) as resp_tail:
        tail = resp_tail.read()

    eocd_pos = tail.rfind(EOCD_SIGNATURE)
    if eocd_pos < 0:
        raise RuntimeError("End of Central Directory signature not found in remote archive")

    _, _, _, _, _, cd_size, cd_offset, _ = struct.unpack(
        "<4sHHHHIIH",
        tail[eocd_pos : eocd_pos + 22],
    )

    if cd_offset >= tail_start and (cd_offset - tail_start + cd_size) <= len(tail):
        cd_data = tail[cd_offset - tail_start : cd_offset - tail_start + cd_size]
    else:
        req_cd = urllib.request.Request(
            final_url,
            headers={"Range": f"bytes={cd_offset}-{cd_offset + cd_size - 1}"},
        )
        with opener(req_cd) as resp_cd:
            cd_data = resp_cd.read()

    entries = {}
    pos = 0
    while pos < len(cd_data):
        if cd_data[pos : pos + 4] != CD_SIGNATURE:
            raise RuntimeError(f"Invalid Central Directory entry signature at offset {pos}")

        (
            _,
            _,
            _,
            _,
            method,
            _,
            _,
            crc,
            comp_size,
            uncomp_size,
            fn_len,
            extra_len,
            comm_len,
            _,
            _,
            _,
            lfh_offset,
        ) = struct.unpack("<4sHHHHHHIIIHHHHHII", cd_data[pos : pos + 46])

        fn = cd_data[pos + 46 : pos + 46 + fn_len].decode("utf-8")
        entries[fn] = {
            "method": method,
            "crc": crc,
            "comp_size": comp_size,
            "uncomp_size": uncomp_size,
            "lfh_offset": lfh_offset,
            "fn_len": fn_len,
        }
        pos += 46 + fn_len + extra_len + comm_len

    return final_url, entries


def fetch_zip_entry(final_url, entry, opener=urllib.request.urlopen):
    """
    Downloads and decompresses a single file entry from a remote ZIP archive
    using an HTTP Range request, verifying its CRC32 and uncompressed length.
    """
    lfh_offset = entry["lfh_offset"]
    fn_len = entry["fn_len"]
    comp_size = entry["comp_size"]
    uncomp_size = entry["uncomp_size"]
    method = entry["method"]
    expected_crc = entry["crc"]

    range_end = lfh_offset + 30 + fn_len + EXTRA_HEADER_MARGIN + comp_size - 1
    req = urllib.request.Request(
        final_url,
        headers={"Range": f"bytes={lfh_offset}-{range_end}"},
    )
    with opener(req) as resp:
        chunk = resp.read()

    if chunk[:4] != LFH_SIGNATURE:
        raise RuntimeError("Invalid Local File Header signature in range response")

    _, _, _, _, _, _, _, _, _, lfh_fn_len, lfh_extra_len = struct.unpack(
        "<4sHHHHHIIIHH",
        chunk[:30],
    )
    data_start = 30 + lfh_fn_len + lfh_extra_len

    if data_start + comp_size > len(chunk):
        data_offset = lfh_offset + data_start
        req_exact = urllib.request.Request(
            final_url,
            headers={"Range": f"bytes={data_offset}-{data_offset + comp_size - 1}"},
        )
        with opener(req_exact) as resp_exact:
            comp_data = resp_exact.read()
    else:
        comp_data = chunk[data_start : data_start + comp_size]

    if method == 0:
        raw_data = comp_data
    elif method == 8:
        raw_data = zlib.decompress(comp_data, -15)
    else:
        raise RuntimeError(f"Unsupported ZIP compression method: {method}")

    if len(raw_data) != uncomp_size:
        raise RuntimeError(f"Size mismatch after decompression: expected {uncomp_size}, got {len(raw_data)}")

    actual_crc = zlib.crc32(raw_data) & 0xFFFFFFFF
    if actual_crc != expected_crc:
        raise RuntimeError(f"CRC32 mismatch: expected {expected_crc:#010x}, got {actual_crc:#010x}")

    return raw_data


def _match_entry(entries, suffix):
    if suffix in entries:
        return entries[suffix]
    target_tail = "/" + suffix.lstrip("/")
    for name, meta in entries.items():
        if name.endswith(target_tail):
            return meta
    raise KeyError(f"Archive entry matching '{suffix}' not found")


def fetch_prism_libraries(
    version="latest",
    dest_dir=None,
    platforms=None,
    repo=PRISM_REPO,
    opener=urllib.request.urlopen,
):
    """
    Fetches the Prism dynamic libraries for the requested platforms and writes
    them into `dest_dir` (defaults to `<repo_root>/lib`).
    """
    if dest_dir is None:
        dest_dir = ROOT / "lib"
    else:
        dest_dir = pathlib.Path(dest_dir)

    if not platforms or platforms == "all":
        selected = list(PLATFORM_TARGETS.keys())
    elif isinstance(platforms, str):
        selected = [p.strip() for p in platforms.split(",") if p.strip()]
    else:
        selected = list(platforms)

    for p in selected:
        if p not in PLATFORM_TARGETS:
            raise ValueError(f"Unknown platform '{p}'. Expected one of: {', '.join(PLATFORM_TARGETS)}")

    tag = resolve_release_tag(version=version, repo=repo, opener=opener)
    sdk_url = f"https://github.com/{repo}/releases/download/{tag}/prism-sdk-{tag}.zip"

    final_url, entries = read_remote_zip_directory(sdk_url, opener=opener)

    written = []
    for p in selected:
        archive_suffix, rel_dest = PLATFORM_TARGETS[p]
        entry = _match_entry(entries, archive_suffix)
        data = fetch_zip_entry(final_url, entry, opener=opener)

        out_path = dest_dir / rel_dest
        out_path.parent.mkdir(parents=True, exist_ok=True)

        tmp_path = out_path.with_suffix(out_path.suffix + ".tmp")
        with open(tmp_path, "wb") as f:
            f.write(data)
        os.replace(tmp_path, out_path)
        os.chmod(out_path, 0o755)
        written.append(out_path)

        # Mirror macOS universal library into renpy.app bundle if present.
        if p == "mac-universal":
            mac_app_dir = dest_dir.parent / "renpy.app" / "Contents" / "MacOS"
            if mac_app_dir.is_dir():
                app_lib = mac_app_dir / out_path.name
                shutil.copy2(out_path, app_lib)

    return tag, written


def main():
    ap = argparse.ArgumentParser(description="Fetch Prism runtime dynamic libraries via HTTP Range requests.")
    ap.add_argument(
        "--version",
        default="latest",
        help="Prism release tag to fetch (default: latest).",
    )
    ap.add_argument(
        "--platforms",
        default="all",
        help="Comma-separated list of target platforms or 'all' (default: all).",
    )
    ap.add_argument(
        "--dest",
        default=str(ROOT / "lib"),
        help="Destination lib directory (default: <repo_root>/lib).",
    )
    args = ap.parse_args()

    tag, written = fetch_prism_libraries(
        version=args.version,
        dest_dir=args.dest,
        platforms=args.platforms,
    )
    print(f"Fetched Prism {tag} runtime libraries:")
    for path in written:
        size_kb = path.stat().st_size / 1024.0
        print(f"  {path} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
