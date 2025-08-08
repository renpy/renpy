﻿# Copyright 2004-2025 Tom Rothamel <pytom@bishoujo.us>
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

    config.image_directories = [ "images" ]

    # Compat for < 8.5
    config.images_directory = None

    config.late_images_scan = False

    config.image_extensions =  [ ".jpg", ".jpeg", ".png", ".webp", ".avif", ".svg" ]

    def _scan_images_directory():

        import os

        directories = config.image_directories

        if config.images_directory and config.images_directory not in directories:
            directories = directories + [ config.images_directory ]

        for prefix in directories:

            prefix = prefix.rstrip('/') + '/'

            non_oversampled_images = [ ]

            oversampled_images = [ ]

            for fn in renpy.list_files():
                if not fn.startswith(prefix):
                    continue

                basename = os.path.basename(fn)
                base, ext = os.path.splitext(basename)

                if not ext.lower() in config.image_extensions:
                    continue

                base = base.lower()
                base, _, oversampled = base.partition("@")

                if oversampled:
                    oversampled_images.append((base, fn))
                else:
                    non_oversampled_images.append((base, fn))

            for base, fn in non_oversampled_images:
                if renpy.has_image(base, exact=True):
                    continue

                renpy.image(base, fn)

            for base, fn in oversampled_images:
                if renpy.has_image(base, exact=True):
                    continue

                renpy.image(base, fn)

init python:

    if not config.late_images_scan:
        _scan_images_directory()

init 1900 python:

    if config.late_images_scan:
        _scan_images_directory()
