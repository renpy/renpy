#!/usr/bin/env python2
from __future__ import print_function

import argparse
import os
import subprocess
import sys

from renpy import version_tuple  # @UnresolvedImport

SOURCE = [
    "/home/tom/ab/renpy",
    "/home/tom/ab/android/",
    "/home/tom/ab/ripe/renios",
    "/home/tom/ab/renpy-deps",
    "/home/tom/ab/pygame_sdl2",
    "/home/tom/ab/renpyweb",
    ]

version = ".".join(str(i) for i in version_tuple)
short_version = ".".join(str(i) for i in version_tuple[:-1])
print("Version", version)

ap = argparse.ArgumentParser()

ap.add_argument("--release", action="store_true")
ap.add_argument("--prerelease", action="store_true")
ap.add_argument("--experimental", action="store_true")
ap.add_argument("--no-tag", "-n", action="store_true")
ap.add_argument("--push-tags", action="store_true")
ap.add_argument("--delete-tag")

args = ap.parse_args()

if args.release:
    subprocess.check_call([ "/home/tom/ab/renpy/scripts/checksums.py", "/home/tom/ab/renpy/dl/" + short_version ])

if args.delete_tag:
    for i in SOURCE:

        os.chdir(i)

        if i == SOURCE[0]:
            tag = args.delete_tag
        else:
            tag = "renpy-" + args.delete_tag

        subprocess.call([ "git", "tag", "-d", tag, ])

    sys.exit(0)

if args.push_tags:
    for i in SOURCE:
        os.chdir(i)

        if subprocess.call([ "git", "push", "--tags" ]):
            print("Tags not pushed: {}".format(os.getcwd()))
            sys.exit(1)

    print("Pushed tags.")
    sys.exit(0)

if args.release:
    links = [ "release", "prerelease", "experimental" ]
    tag = True
elif args.prerelease:
    links = [ "prerelease", "experimental" ]
    tag = True
elif args.experimental:
    links = [ "experimental" ]
    tag = False
else:
    links = [ ]
    tag = False

if args.no_tag:
    tag = False

if tag:
    for i in SOURCE:
        os.chdir(i)

        if subprocess.call([ "git", "diff", "--quiet", "HEAD" ]):
            print("Directory not checked in: {}".format(os.getcwd()))
            sys.exit(1)

    for i in SOURCE:

        os.chdir(i)

        if i == SOURCE[0]:
            tag = version
        else:
            tag = "renpy-" + version

        subprocess.check_call([ "git", "tag", "-a", tag, "-m", "Tagging Ren'Py + " + version + " release." ])


os.chdir("/home/tom/ab/renpy/dl")

for i in links:
    if os.path.exists(i):
        os.unlink(i)
    os.symlink(short_version, i)


os.chdir("/home/tom/ab/website")
subprocess.check_call("./upload.sh")


os.chdir("/home/tom/ab/renpy/sphinx")
if args.release:
    subprocess.check_call("./upload.sh")
elif args.prerelease:
    subprocess.check_call("./upload_dev.sh")

print("Version", version)
