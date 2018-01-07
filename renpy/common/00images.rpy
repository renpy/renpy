# Copyright 2004-2018 Tom Rothamel <pytom@bishoujo.us>
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

init -1900 python:
    config.images_directory = 'images'


init 1900 python hide:

    def scan_images_directory():

        import os

        if not config.images_directory:
            return

        prefix = config.images_directory.rstrip('/') + '/'

        for fn in renpy.list_files():
            if not fn.startswith(prefix):
                continue

            basename = os.path.basename(fn)
            base, ext = os.path.splitext(basename)

            if not ext.lower() in [ ".jpg", ".jpeg", ".png", ".webp" ]:
                continue

            base = base.lower()

            if renpy.has_image(base, exact=True):
                continue

            renpy.image(base, fn)

    scan_images_directory()
