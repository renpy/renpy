#!/usr/bin/env python
# Generate a pair of update keys.
#

import argparse
import rsa

ap = argparse.ArgumentParser()
ap.add_argument("private")
ap.add_argument("public")
args = ap.parse_args()

public, private = rsa.newkeys(2048)

with open(args.public, "wb") as f:
    f.write(public.save_pkcs1())

with open(args.private, "wb") as f:
    f.write(private.save_pkcs1())
