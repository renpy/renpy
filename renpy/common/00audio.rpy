# Copyright 2004-2026 Tom Rothamel <pytom@bishoujo.us>
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
    config.audio_directory = None

    config.audio_directories = [ "audio" ]

    def _scan_audio_directory():

        directories = config.audio_directories

        if config.audio_directory and config.audio_directory not in directories:
            directories = directories + [ config.audio_directory ]

        import os

        for directory in directories:

            prefix = directory.strip('/') + '/'

            for fn in renpy.list_files():
                if not fn.startswith(prefix):
                    continue

                basename = os.path.basename(fn)
                base, ext = os.path.splitext(basename)

                if not ext.lower() in [ ".wav", ".mp2", ".mp3", ".ogg", ".opus", ".flac" ]:
                    continue

                base = base.lower()
                audio.__dict__.setdefault(base, fn)

init python
    if not config.late_audio_scan:
        _scan_audio_directory()

init 1900 python:
    if config.late_audio_scan:
        _scan_audio_directory()
