import requests
import re
import os


def byte_ranges(ranges):
    """
    Given a list of (offset, size) pairs, returns a list of byte ranges
    that will cover those ranges.
    """

    ranges = list(ranges)
    ranges.sort()

    rv = [ ]


    for offset, size in ranges:
        start = offset
        end = offset + size - 1

        if rv and rv[-1][1] == start - 1:
            start = rv.pop()[0]

        rv.append((start, end))

    return rv


def write_range(f, headers, content):
    m = re.search(r"bytes (\d+)-(\d+)/(\d+)", headers["Content-Range"])
    start = int(m.group(1))
    end = int(m.group(2))
    total = int(m.group(3))

    f.seek(start)
    f.write(content)
    f.truncate(total)

    return [ (start, end) ]


def write_multipart(f, headers, content):
    m = re.search(r"boundary=(.*)", headers["Content-Type"])
    separator = m.group(1).encode("utf-8")

    boundary = b"\r\n--" + separator + b"\r\n"
    end_boundary = b"\r\n--" + separator + b"--\r\n"

    content = content.split(end_boundary, 1)[0]

    rv = [ ]

    for part in content.split(boundary):

        if not part:
            continue

        part_header_text, part_content = part.split(b"\r\n\r\n", 1)
        part_header_text = part_header_text.decode("utf-8")

        part_headers = { }

        for i in part_header_text.split("\r\n"):
            k, v = i.split(": ", 1)
            part_headers[k] = v

        rv.append(write_range(f, part_headers, part_content))

    return rv

def download_ranges(url, ranges, destination, progress_callback=None):
    """
    `url`
        The URL to download from.

    `ranges`
        A list of (offset, size) pairs, where together the offset and size
        represent a range that needs to be downloaded.

    `destination`
        The file to write to.

    `progress_callback`
        A function that will be called with the number of bytes downloaded
        and the total number of bytes to download. (This is not perfect, as
        the

    """

    ranges = byte_ranges(ranges)
    total_size = sum(end - start + 1 for start, end in ranges)
    downloaded = 0

    if os.path.exists(destination):
        mode = "r+b"
    else:
        mode = "wb"

    with open(destination, mode) as destination_file:

        while ranges:

            old_ranges = list(ranges)

            headers = { 'Range' : 'bytes=' + ', '.join('%d-%d' % (start, end) for start, end in ranges[:10]) }

            r = requests.get(url, headers=headers, stream=True)
            r.raise_for_status()

            blocks = [ ]

            while True:
                b = r.raw.read(128 * 1024)

                if not b:
                    break

                blocks.append(b)
                downloaded += len(b)
                if progress_callback is not None:
                    progress_callback(min(downloaded, total_size), total_size)

            content = b"".join(blocks)

            if r.status_code == 206:
                if r.headers.get("Content-Type", "").startswith("multipart/byteranges"):
                    got_ranges = write_multipart(destination_file, r.headers, content)
                else:
                    got_ranges = write_range(destination_file, r.headers, content)

                for i in got_ranges:
                    ranges.remove(i)

                if old_ranges == ranges:
                    raise Exception("No progress made.")

            else:
                destination_file.seek(0)
                destination_file.truncate()
                destination_file.write(content)
                break
