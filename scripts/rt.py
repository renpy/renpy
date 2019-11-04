#!/usr/bin/env python3

from __future__ import print_function
import time
import argparse
import os
import pathlib
import subprocess
import shutil

# The path to Ren'Py.
RENPY = pathlib.Path(__file__).resolve().parent.parent

# The path to Tests.
TESTS = RENPY.parent / os.environ.get("RENPY_TESTS", "tests")

# The currently-selected test.
CURRENT = TESTS / 'current'


def list_command(args):
    modtimes = [ ]

    for i in TESTS.iterdir():
        if not i.is_dir():
            continue

        if i.is_symlink():
            continue

        modtimes.append((i.stat().st_ctime, i))

    modtimes.sort()

    if not args.all:
        last = modtimes[-1][0]
        modtimes = [ i for i in modtimes if i[0] > last - 7 * 86400 ]

    for t, p in modtimes:
        print(time.strftime("%Y-%m-%d %H:%M", time.localtime(t)), p.name)


def select(dn):
    p = pathlib.Path(dn)

    if CURRENT.exists():
        CURRENT.unlink()

    CURRENT.symlink_to(p)


def select_command(args):
    select(args.path)


def selected_command(args):
    print(CURRENT.resolve().name)


def edit_command(args):
    subprocess.call([ "atom", CURRENT.resolve(), CURRENT.resolve() / "game/script.rpy" ])


def new_command(args):

    p = TESTS / pathlib.Path(args.name)

    if p.exists():
        if not args.force:
            print(f'{p} exists.')
            return

        shutil.rmtree(p)

    shutil.copytree(RENPY / 'gui', p)
    shutil.copy(RENPY / 'scripts/rt/script.rpy', p / 'game')
    shutil.copy(RENPY / 'scripts/rt/augustina.rpy', p / 'game')

    subprocess.call([
        RENPY / "run.sh",
        RENPY / "launcher",
        "generate_gui",
        "--start",
        "--width", "1280",
        "--template", RENPY / "gui",
        p])

    def copy(src, dst):
        for i in RENPY.glob(src):
            shutil.copy(i, p / dst)

    copy("tutorial/game/images/eileen *", "game/images")
    copy("tutorial/game/images/lucy *", "game/images")
    copy("tutorial/game/images/bg *", "game/images")
    copy("scripts/rt/*.png", "game/images")


    (p / "project.json").unlink()

    select(p)
    edit_command(None)

def run_command(args):

    dash_args = [ i for i in args.args if i.startswith("-") if (i != "--") ]
    nodash_args = [ i for i in args.args if not i.startswith("-") ]

    if args.lint:
        dash_args.insert(0, "--lint")
    if args.compile:
        dash_args.insert(0, "--compile")

    args = [ RENPY / "run.sh" ] + dash_args + [ CURRENT.resolve() ] + nodash_args

    os.execv(args[0], args)


def main():

    ap = argparse.ArgumentParser()
    asp = ap.add_subparsers()

    sp = asp.add_parser('list')
    sp.set_defaults(func=list_command)
    sp.add_argument("--all", action='store_true')

    sp = asp.add_parser('select')
    sp.set_defaults(func=select_command)
    sp.add_argument("path")

    sp = asp.add_parser('selected')
    sp.set_defaults(func=selected_command)

    sp = asp.add_parser('edit')
    sp.set_defaults(func=edit_command)

    sp = asp.add_parser('new', aliases=['project'])
    sp.set_defaults(func=new_command)
    sp.add_argument("name")
    sp.add_argument("--force", action='store_true')

    sp = asp.add_parser('run')
    sp.set_defaults(func=run_command)
    sp.add_argument("--lint", action="store_true")
    sp.add_argument("--compile", action="store_true")
    sp.add_argument("args", nargs=argparse.REMAINDER)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
