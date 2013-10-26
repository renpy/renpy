#!/usr/bin/env python

import argparse
import os
import subprocess
import sys

from renpy import version_tuple #@UnresolvedImport

version = ".".join(str(i) for i in version_tuple)
short_version = ".".join(str(i) for i in version_tuple[:3])
print "Version", version

ap = argparse.ArgumentParser()

ap.add_argument("--release", action="store_true")
ap.add_argument("--prerelease", action="store_true")
ap.add_argument("--experimental", action="store_true")
ap.add_argument("--no-tag", "-n", action="store_true")

args = ap.parse_args()

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


def check_dirty():
    if args.no_tag:
        return

    if subprocess.check_call([ "git", "diff", "--quiet", "HEAD" ]):
        print "Directory not checked in: {}".format(os.getcwd())
        sys.exit(1)

os.chdir("/home/tom/ab/renpy")
check_dirty()

os.chdir("/home/tom/ab/renpy/android")
check_dirty()
subprocess.check_call([ "./add_renpy.sh", short_version ])

if not args.no_tag:
    subprocess.check_call([ "git", "tag", "-a" "rapt-" + version, "-m", "Tagging RAPT release." ])

os.chdir("/home/tom/ab/renpy/dl")

for i in links:
    if os.path.exists(i):
        os.unlink(i)
    os.symlink(short_version, i)

os.chdir("/home/tom/ab/renpy")

if tag and not args.no_tag:
    cmd = [ "git", "tag", "-a", version, "-m", "Ren'Py " + version ]
    subprocess.check_call(cmd)

os.chdir("/home/tom/ab/website")
subprocess.check_call("./upload.sh")
