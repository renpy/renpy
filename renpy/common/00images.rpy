# Copyright 2004-2022 Tom Rothamel <pytom@bishoujo.us>
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
    config.late_images_scan = False

    def _scan_images_directory():

        import os

        if not config.images_directory:
            return

        prefix = config.images_directory.rstrip('/') + '/'

        for fn in renpy.list_files():
            if not fn.startswith(prefix):
                continue

            basename = os.path.basename(fn)
            base, ext = os.path.splitext(basename)

            if not ext.lower() in [ ".jpg", ".jpeg", ".png", ".webp", ".jxl", ".avif" ]:
                continue

            base = base.lower()

            if renpy.has_image(base, exact=True):
                continue

            renpy.image(base, fn)

init python:

    if not config.late_images_scan:
        _scan_images_directory()

init 1900 python:

    if config.late_images_scan:
        _scan_images_directory()

init 3000 python:
    def _heuristic_image_format_check():
        formats = {
            # PNG
            ".png": pygame_sdl2.image.INIT_PNG,
            # JPEG
            ".jpg": pygame_sdl2.image.INIT_JPG,
            ".jpeg": pygame_sdl2.image.INIT_JPG,
            # TIFF
            ".tif": pygame_sdl2.image.INIT_TIF,
            ".tiff": pygame_sdl2.image.INIT_TIF,
            # WebP
            ".webp": pygame_sdl2.image.INIT_WEBP,
            # JPEG-XL
            ".jxl": pygame_sdl2.image.INIT_JXL,
            # AVIF
            ".avif": pygame_sdl2.image.INIT_AVIF,
            ## There is no real way of checking the below,
            ## but they are built into SDL2_image by default
            # QOI
            ".qoi": 0,
            # BPM
            ".bmp": 0, ".ico": 0, ".cur": 0,
            # GIF
            ".gif": 0,
            # TGA
            ".tga": 0,
            # XCF
            ".xcf": 0,
        }

        from collections import defaultdict
        counter = defaultdict(lambda: 0)

        for _, d in renpy.display.image.images.items():
            if isinstance(d, renpy.display.im.Image):
                _, ext = os.path.splitext(d.filename)
                if ext:
                    counter[ext.lower()] += 1

        for ext, count in counter.items():
            if count > 0:
                itag = formats.get(ext, None)
                if itag is None:
                    renpy.log("Possibly unknown image format: %s (found %d images)" % (ext, count))
                elif not pygame_sdl2.image.has_init(itag):
                    renpy.log("Possibly missing image support in Ren'Py/SDL2_image build: %s (found %d images)"
                        % (ext, count))

        return counter
    
    if not renpy.official:
        _heuristic_image_format_check()
