import requests
import re

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
    f.write(content[:end - start + 1])
    f.truncate(total)


def write_multipart(f, headers, content):
    m = re.search(r"boundary=(.*)", headers["Content-Type"])
    separator = m.group(1).encode("utf-8")

    boundary = b"\r\n--" + separator + b"\r\n"
    end_boundary = b"\r\n--" + separator + b"--\r\n"

    content = content.split(end_boundary, 1)[0]

    for part in content.split(boundary):

        if not part:
            continue

        part_header_text, part_content = part.split(b"\r\n\r\n", 1)
        part_header_text = part_header_text.decode("utf-8")

        part_headers = { }

        for i in part_header_text.split("\r\n"):
            k, v = i.split(": ", 1)
            part_headers[k] = v

        write_range(f, part_headers, part_content)


def download_ranges(url, ranges, destination):
    """
    `url`
        The URL to download from.

    `ranges`
        A list of (offset, size) pairs, where together the offset and size
        represent a range that needs to be downloaded.

    `destination`
        The file to write to.
    """

    ranges = byte_ranges(ranges)

    with open(destination, "ab") as destination_file:

        while ranges:
            current = ranges[:10]
            ranges = ranges[10:]

            headers = { 'Range' : 'bytes=' + ', '.join('%d-%d' % (start, end) for start, end in current) }

            r = requests.get(url, headers=headers)
            r.raise_for_status()

            if r.status_code == 206:
                if r.headers.get("Content-Type", "").startswith("multipart/byteranges"):
                    write_multipart(destination_file, r.headers, r.content)
                else:
                    write_range(destination_file, r.headers, r.content)
            else:
                destination_file.seek(0)
                destination_file.truncate()
                destination_file.write(r.content)
                break

if __name__ == "__main__":
    download_ranges("http://share.renpy.org/who_nose.jpg", [ (0, 100), (200, 100), (400, 100) ], "/tmp/who_nose.jpg")
    download_ranges("http://share.renpy.org/who_nose.jpg", [ (100, 100) ], "/tmp/who_nose.jpg")
