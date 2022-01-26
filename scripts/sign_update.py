#!/usr/bin/env python
# Signs the update.json file.

import argparse
import rsa
import base64

ap = argparse.ArgumentParser()
ap.add_argument("private")
ap.add_argument("json")
args = ap.parse_args()

with open(args.private, "rb") as f:
    private = rsa.PrivateKey.load_pkcs1(f.read())

with open(args.json, "rb") as f:
    message = f.read()

signature = rsa.sign(message, private, "SHA-256")

with open(args.json + ".sig", "wb") as f:
    f.write(base64.b64encode(signature))
