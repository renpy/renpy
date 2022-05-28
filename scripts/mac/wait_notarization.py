#!/usr/bin/env python

from __future__ import print_function

import subprocess
import plistlib
import time
import sys


def check_notarization():
    p = subprocess.Popen([
        "xcrun", "altool",
        "--notarization-history", "0",
        "--asc-provider", "XHTE5H7Z79",
        "-u", "tom@rothamel.us", "-p", "@keychain:altool",
        "--output-format", "xml" ], stdout=subprocess.PIPE)

    plist = p.communicate()[0]

    p = plistlib.readPlistFromString(plist)

    return p["notarization-history"]["items"][0]["Status"]


def main():

    start = time.time()
    next_check = start + 60
    failures = 0

    while True:

        now = time.time()

        while next_check < now:
            next_check += 10

        time.sleep(next_check - now)

        status = check_notarization()

        try:
            now = time.time()
        except Exception as e:
            failures += 1
            if failures >= 3:
                raise e

        print(round(time.time() - start), "notarization", status, file=sys.stderr)

        if status == "success":
            sys.exit(0)
        elif status == "in progress":
            pass
        else:
            sys.exit(0)


if __name__ == "__main__":
    main()
