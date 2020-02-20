# Copyright 2004-2019 Tom Rothamel <pytom@bishoujo.us>
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

# This file contains the launcher support for creating RenPyWeb projects,
# other than the logic in the standard distribute code.


init python:

    import shutil
    import webserver
    import io
    import tempfile
    import time
    import pygame_sdl2

    WEB_PATH = None

    def find_web():

        global WEB_PATH

        candidates = [ ]

        WEB_PATH = os.path.join(config.renpy_base, "web")

        if os.path.isdir(WEB_PATH) and check_hash_txt("web"):
            pass
        else:
            WEB_PATH = None

    find_web()

    def get_web_destination(p):
        """
        Returns the path to the desint
        """

        build = p.dump['build']

        base_name = build['directory_name']
        destination = build["destination"]

        parent = os.path.dirname(p.path)
        destination = os.path.join(parent, destination, base_name + "-web")

        return destination

    def generate_image_placeholder(surface, tmpdir):
        """
        Creates a 1/32 thumbnail for small download size.
        Pixellate first for better graphic results.
        Will be stretched back when playing.
        """

        if surface.get_width() > 32 and surface.get_height() > 32:
            renpy.display.module.pixellate(surface,surface,32,32,32,32)
            thumbnail = renpy.display.pgrender.transform_scale(surface,
                (surface.get_width()/32, surface.get_height()/32))
        else:
            # avoid unsupported 0-width or 0-height picture
            thumbnail = surface

        save_as_png = os.path.join(tmpdir, 'use_png_format.png')
        best_compression = 9
        pygame_sdl2.image.save(thumbnail, save_as_png, best_compression)

        return save_as_png

    def build_web(p, gui=True):

        # Figure out the reporter to use.
        if gui:
            reporter = distribute.GuiReporter()
        else:
            reporter = distribute.TextReporter()

        # Determine details.
        p.update_dump(True, gui=gui)

        destination = get_web_destination(p)
        display_name = p.dump['build']['display_name']

        # Clean the folder, then remale it.
        if os.path.exists(destination):
            shutil.rmtree(destination)

        os.makedirs(destination, 0o777)

        # Use the distributor to make game.zip.
        distribute.Distributor(p, packages=[ "web" ], packagedest=os.path.join(destination, "game"), reporter=reporter, noarchive=True, scan=False)

        # Filter out downloadable resources
        reporter.info(_("Preparing downloadable files"))
        MIN_REMOTE_SIZE=50*1024
        # TODO: configurable min_size? use archives to better describe web distribution?
        # TODO: predict/include title screen's resources for a smooth start (no black blink)
        shutil.move(
            os.path.join(destination, 'game.zip'),
            os.path.join(destination, 'game-old.zip'))
        import zipfile
        zin  = zipfile.ZipFile(os.path.join(destination, 'game-old.zip'))
        zout = zipfile.ZipFile(os.path.join(destination, 'game.zip'), 'w')
        remote_files = {}
        tmpdir = tempfile.mkdtemp()
        for m in zin.infolist():
            base, ext = os.path.splitext(m.filename)
            # Images
            if (ext.lower() in ('.jpg', '.jpeg', '.png', '.webp')
                and m.file_size > MIN_REMOTE_SIZE
                and m.filename.lower().startswith('game/')
                and not m.filename.lower().startswith('game/gui/')):

                zin.extract(m, path=destination)
                surface = pygame_sdl2.image.load(os.path.join(destination,m.filename))
                (w,h) = (surface.get_width(),surface.get_height())

                remote_files[m.filename[len('game/'):]] = 'image {},{}'.format(w,h)
                print("extract:", m.filename)

                tmpfile = generate_image_placeholder(surface, tmpdir)
                placeholder_relpath = os.path.join('_placeholders', m.filename[len('game/'):])
                zout.write(tmpfile, placeholder_relpath)
            # Musics (but not SFX - no placeholders for short, non-looping sounds)
            elif (ext.lower() in ('.wav', '.mp2', '.mp3', '.ogg', '.opus')
                and m.file_size > MIN_REMOTE_SIZE
                and m.filename.lower().startswith('game/music/')):
                zin.extract(m, path=destination)
                remote_files[m.filename[len('game/'):]] = 'music -'
                print("extract:", m.filename)
            # Videos are currently not supported, strip them if not already
            elif (ext.lower() in ('.ogv', '.webm', '.mp4', '.mkv', '.avi')):
                pass
                print("exclude:", m.filename)
            # Default: extract & recompress
            else:
                # Not using zout.writestr(m, zin.read(m)) to avoid MemoryError
                tmpfile = zin.extract(m, tmpdir)
                date_time = time.mktime(m.date_time+(0,0,0))
                os.utime(tmpfile, (date_time,date_time))
                zout.write(tmpfile, m.filename, m.compress_type)
                print("keep:", m.filename)
        shutil.rmtree(tmpdir)
        zin.close()
        remote_files_str = ''
        for f in sorted(remote_files):
            remote_files_str += f + "\n"
            remote_files_str += remote_files[f] + "\n"
        zout.writestr('game/renpyweb_remote_files.txt',
                      remote_files_str,
                      zipfile.ZIP_DEFLATED)
        zout.close()
        os.unlink(os.path.join(destination, 'game-old.zip'))

        # Copy the files from WEB_PATH to destination.
        for fn in os.listdir(WEB_PATH):
            if fn in { "game.zip", "hash.txt", "index.html" }:
                continue

            shutil.copy(os.path.join(WEB_PATH, fn), os.path.join(destination, fn))

        # Copy over index.html.
        with io.open(os.path.join(WEB_PATH, "index.html"), encoding='utf-8') as f:
            html = f.read()

        html = html.replace("%%TITLE%%", display_name)

        with io.open(os.path.join(destination, "index.html"), "w", encoding='utf-8') as f:
            f.write(html)

        webserver.start(destination)


    def launch_web():
        renpy.run(OpenURL("http://127.0.0.1:8042/index.html"))

screen web():

    frame:
        style_group "l"
        style "l_root"

        window:

            has vbox

            label _("Web: [project.current.display_name!q]")

            add HALF_SPACER


            hbox:

                # Left side.
                frame:
                    style "l_indent"
                    xmaximum ONEHALF
                    xfill True

                    has vbox

                    add SEPARATOR2
                    add HALF_SPACER

                    frame:
                        style "l_indent"
                        has vbox

                        text _("Build:")

                        add HALF_SPACER

                        frame style "l_indent":

                            has vbox

                            textbutton _("Build Web Application") action Jump("web_build")
                            textbutton _("Build and Open in Browser") action Jump("web_launch")
                            textbutton _("Open in Browser") action Jump("web_start")
                            textbutton _("Open build directory") action Jump("open_build_directory")

                        add SPACER

                        text _("Support:")

                        add HALF_SPACER

                        frame style "l_indent":

                            has vbox

                            textbutton _("RenPyWeb Home") action OpenURL("https://renpy.beuc.net/")
                            textbutton _("Beuc's Patreon") action OpenURL("https://www.beuc.net/donate/")


                # Right side.
                frame:
                    style "l_indent"
                    xmaximum ONEHALF
                    xfill True

                    has vbox

                    add SEPARATOR2
                    add HALF_SPACER

                    frame:
                        style "l_indent"
                        has vbox

                        text _("Ren'Py web applications require the entire game to be downloaded to the player's computer before it can start.")

                        add SPACER

                        text _("Current limitations in the web platform mean that loading large images, audio files, or movies may cause audio or framerate glitches, and lower performance in general.")

    textbutton _("Return") action Jump("front_page") style "l_left_button"



label web:

    if WEB_PATH is None:
        $ interface.yesno(_("Before packaging web apps, you'll need to download RenPyWeb, Ren'Py's web support. Would you like to download RenPyWeb now?"), no=Jump("front_page"))
        $ add_dlc("web", restart=True)

    call screen web

    jump front_page


label web_build:
    $ build_web(project.current, gui=True)
    jump web


label web_launch:
    $ build_web(project.current, gui=True)
    $ launch_web()
    jump web

label open_build_directory():
    $ project.current.update_dump(True, gui=True)
    $ OpenDirectory(get_web_destination(project.current))()
    jump web

label web_start:
    $ project.current.update_dump(True, gui=True)
    $ webserver.start(get_web_destination(project.current))
    $ launch_web()
    jump web
