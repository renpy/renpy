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

# This file contains the launcher support for creating RenPyWeb projects,
# other than the logic in the standard distribute code.


init python:

    import shutil
    import webserver
    import io
    import tempfile
    import time
    import pygame_sdl2
    import zipfile

    WEB_PATH = None

    class ProgressiveFilter(object):
        def __init__(self, project):
            self.project = project
            self.destination = get_web_destination(project)
            self.remote_files = {}
            self.images = []
            self.path_filters = []
            load_filters(project, self.path_filters)

        def filter(self, file, variant, format):
            """
            Detect and copy the files to be downloaded progressively,
            and prevent them to be put in the ZIP archive.
            Returns True if the file must be included in the ZIP archive.
            """
            if variant != 'web' or format != 'zip':  # useless?
                return True

            base, ext = os.path.splitext(file.name)

            copy_file = False
            # Images
            if (ext.lower() in ('.jpg', '.jpeg', '.png', '.webp')
                    and filters_match(self.path_filters, file.name, 'image')):
                # Add image to list and generate placeholder later
                self.images.append((file.path, file.name))
                copy_file = True

            # Musics (but not SFX - no placeholders for short, non-looping sounds)
            elif (ext.lower() in ('.wav', '.mp2', '.mp3', '.ogg', '.opus')
                    and filters_match(self.path_filters, file.name, 'music')):
                self.remote_files[file.name[len('game/'):]] = 'music -'
                copy_file = True

            # Voices
            elif (ext.lower() in ('.wav', '.mp2', '.mp3', '.ogg', '.opus')
                    and filters_match(self.path_filters, file.name, 'voice')):
                self.remote_files[file.name[len('game/'):]] = 'voice -'
                copy_file = True

            # Videos are never included.
            elif (ext.lower() in ('.ogv', '.webm', '.mp4', '.mkv', '.avi')):
                copy_file = True

            if not copy_file:
                return True

            # Copy the file to the destination folder, keeping metadata
            dst_path = os.path.join(self.destination, file.name)
            dst_dir = os.path.dirname(dst_path)
            if not os.path.isdir(dst_dir):
                os.makedirs(dst_dir, 0o755)
            shutil.copy2(file.path, dst_path)

            return False

        def finalize(self):
            """
            Append some generated files to the ZIP archive.
            """
            zout = zipfile.ZipFile(os.path.join(self.destination, 'game.zip'), 'a')
            tmpdir = tempfile.mkdtemp()

            # Generate and append placeholder image files to archive
            for (src, dst) in self.images:
                surface = pygame_sdl2.image.load(src)
                (w, h) = (surface.get_width(), surface.get_height())
                self.remote_files[dst[len('game/'):]] = 'image {},{}'.format(w,h)
                tmpfile = generate_image_placeholder(surface, tmpdir)
                placeholder_relpath = os.path.join('_placeholders', dst[len('game/'):])
                zout.write(tmpfile, placeholder_relpath)

            # Prepare a list of remote files for renpy.loader
            remote_files_str = ''
            for f in sorted(self.remote_files):
                remote_files_str += f + "\n"
                remote_files_str += self.remote_files[f] + "\n"
            zout.writestr('game/renpyweb_remote_files.txt',
                          remote_files_str,
                          zipfile.ZIP_DEFLATED)

            # Clean-up
            shutil.rmtree(tmpdir)
            zout.close()

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
        Creates size-efficient 1/32 thumbnail for use as download preview.
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

    def load_filters(p, path_filters):
        """
        Type- and path-based filtering, following
        progressive_download.txt rules (created with default rules if
        not there already).  Assumes prior filtering based on
        hard-coded list of file extensions.
        """

        rules_path = os.path.join(p.path,'progressive_download.txt')
        if not os.path.exists(rules_path):
            open(rules_path, 'w').write(
                "# RenPyWeb progressive download rules - first match applies\n"
                + "# '+' = progressive download, '-' = keep in game.zip (default)\n"
                + "# See https://www.renpy.org/doc/html/build.html#classifying-and-ignoring-files for matching\n"
                + "#\n"
                + "# +/- type path\n"
                + '- image game/gui/**\n'
                + '+ image game/**\n'
                + '+ music game/audio/**\n'
                + '+ voice game/voice/**\n'
            )

        # Parse rules
        line_no = 0
        for line in open(rules_path, 'r').readlines():
            line_no += 1

            if line.startswith('#') or line.strip() == '':
                continue

            try:
                (f_rule, f_type, f_pattern) = line.rstrip("\r\n").split(' ', 3-1)
            except ValueError:
                raise RuntimeError("Missing element at progressive_download.txt:%d" % line_no)

            try:
                f_rule = {'+': True, '-': False}[f_rule]
            except KeyError:
                raise RuntimeError("Invalid rule '%s' at progressive_download.txt:%d" % (f_rule, line_no))

            if f_type not in ('image', 'music', 'voice'):
                raise RuntimeError("Invalid type '%s' at progressive_download.txt:%d" % (f_type, line_no))

            path_filters.append((f_rule, f_type, f_pattern))

    def filters_match(path_filters, path, path_type):
        """
        Returns whether path matches a progressive download rule
        """
        for (f_rule, f_type, f_pattern) in path_filters:
            if path_type == f_type and distribute.match(path, f_pattern):
                return f_rule
        return False

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

        # Clean the folder, then remake it.
        if os.path.exists(destination):
            shutil.rmtree(destination)

        os.makedirs(destination, 0o777)

        files_filter = ProgressiveFilter(p)

        # Use the distributor to make game.zip.
        distribute.Distributor(p, packages=[ "web" ], packagedest=os.path.join(destination, "game"),
                reporter=reporter, noarchive=True, scan=False, files_filter=files_filter)

        reporter.info(_("Preparing progressive download"))
        files_filter.finalize()

        # Copy the files from WEB_PATH to destination.
        for fn in os.listdir(WEB_PATH):
            if fn in { "game.zip", "hash.txt", "index.html" }:
                continue

            shutil.copy(os.path.join(WEB_PATH, fn), os.path.join(destination, fn))

        # Find the presplash and copy it over.
        presplash = None

        if not PY2:
            for fn in [ "web-presplash.png", "web-presplash.jpg", "web-presplash.webp" ]:
                fullfn = os.path.join(project.current.path, fn)

                if os.path.exists(fullfn):
                    presplash = fn
                    break

        if presplash:
            os.unlink(os.path.join(destination, "web-presplash.jpg"))
            shutil.copy(os.path.join(project.current.path, presplash), os.path.join(destination, presplash))

        # Copy over index.html.
        with io.open(os.path.join(WEB_PATH, "index.html"), encoding='utf-8') as f:
            html = f.read()

        if PY2:
            html = html.replace("%%TITLE%%", display_name)
        else:
            html = html.replace("Ren'Py Web Game", display_name)

            if presplash:
                html = html.replace("web-presplash.jpg", presplash)

        with io.open(os.path.join(destination, "index.html"), "w", encoding='utf-8') as f:
            f.write(html)

        # Zip up the game.

        zip_targets = [ ]

        for dn, dirs, files in os.walk(destination):
            for directory in dirs:
                zip_targets.append(os.path.join(dn, directory))
            for file in files:
                zip_targets.append(os.path.join(dn, file))

        with zipfile.ZipFile(destination + ".zip", 'w') as zf:
            for i, target in enumerate(zip_targets):
                zf.write(target, os.path.relpath(target, destination))
                reporter.progress(_("Creating package..."), i + 1, len(zip_targets))

        # Start the web server.

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

                            textbutton _("Force Recompile") action DataToggle("force_recompile") style "l_checkbox"


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

                        text _("Images and music can be downloaded while playing. A 'progressive_download.txt' file will be created so you can configure this behavior.")

                        add SPACER

                        text _("Current limitations in the web platform mean that loading large images may cause audio or framerate glitches, and lower performance in general. Movies aren't supported.")


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
    $ renpy.run(OpenDirectory(get_web_destination(project.current), absolute=True))
    jump web

label web_start:
    $ project.current.update_dump(True, gui=True)
    $ webserver.start(get_web_destination(project.current))
    $ launch_web()
    jump web
