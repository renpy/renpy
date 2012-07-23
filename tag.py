#!/usr/bin/env python

import argparse
import subprocess

from renpy import version_tuple #@UnresolvedImport

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", "-n", action="store_true")
    
    args = ap.parse_args()
    
    version = ".".join(str(i) for i in version_tuple)

    print "Tagging", version
    
    if args.dry_run:
        print "(but not really)"
        return
    
    cmd = [ "git", "tag", "-a", version, "-m", "Ren'Py " + version ]
    subprocess.check_call(cmd)
    
if __name__ == "__main__":
    main()
