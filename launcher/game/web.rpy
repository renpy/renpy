# Copyright 2004-2024 Tom Rothamel <pytom@bishoujo.us>
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
    import re
    import hashlib

    WEB_PATH = None

    class ProgressiveFilter(object):
        def __init__(self, project, destination):
            self.project = project
            self.destination = destination
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
            if (ext.lower() in ('.jpg', '.jpeg', '.png', '.webp', '.avif', '.svg')
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
                self.remote_files[file.name[len('game/'):]] = 'video -'
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

    def generate_web_icons(p, destination):
        """
        Checks if the web-icon.png file exists in the game folder and generates
        required icons for PWA in subdirectory icons/ in the destination folder.
        If no web-icon.png is found, the default Ren'Py icon is used instead in
        the web folder, if exists.
        """
        # Check if there's a custom icon in the game directory
        icon_path = os.path.join(p.path, 'web-icon.png')
        # Generate a default icon if there isn't
        if not os.path.exists(icon_path):
            icon_path = os.path.join(WEB_PATH, 'web-icon.png')

        # Check if path is a valid image
        if not os.path.exists(icon_path):
            # Skip pwa support if no icon is found
            return
        # Create icons directory
        icons_dir = os.path.join(destination, 'icons')
        if not os.path.isdir(icons_dir):
            os.makedirs(icons_dir, 0o777)
        # Check the height and width of the icon
        icon = pygame_sdl2.image.load(icon_path)
        icon_width = icon.get_width()
        icon_height = icon.get_height()
        if icon_width != icon_height:
            raise RuntimeError("The icon must be square")
        if icon_width < 512:
            raise RuntimeError("The icon must be at least 512x512 pixels")

        scale = renpy.display.scale.smoothscale

        best_compression = 9
        # Generate 512x512 icon, if needed
        if icon_width != 512:
            icon512 = scale(icon, (512, 512))
            pygame_sdl2.image.save(icon512, os.path.join(icons_dir, 'icon-512x512.png'), best_compression)
        else:
            pygame_sdl2.image.save(icon, os.path.join(icons_dir, 'icon-512x512.png'), best_compression)

        # Generate 384x384 icon
        icon384 = scale(icon, (384, 384))
        pygame_sdl2.image.save(icon384, os.path.join(icons_dir, 'icon-384x384.png'), best_compression)

        # Generate 192x192 icon
        icon192 = scale(icon, (192, 192))
        pygame_sdl2.image.save(icon192, os.path.join(icons_dir, 'icon-192x192.png'), best_compression)

        # Generate 152x152 icon
        icon152 = scale(icon, (152, 152))
        pygame_sdl2.image.save(icon152, os.path.join(icons_dir, 'icon-152x152.png'), best_compression)

        # Generate 144x144 icon
        icon144 = scale(icon, (144, 144))
        pygame_sdl2.image.save(icon144, os.path.join(icons_dir, 'icon-144x144.png'), best_compression)

        # Generate 128x128 icon
        icon128 = scale(icon, (128, 128))
        pygame_sdl2.image.save(icon128, os.path.join(icons_dir, 'icon-128x128.png'), best_compression)

        # Generate 96x96 icon
        icon96 = scale(icon, (96, 96))
        pygame_sdl2.image.save(icon96, os.path.join(icons_dir, 'icon-96x96.png'), best_compression)

        # Generate 72x72 icon
        icon72 = scale(icon, (72, 72))
        pygame_sdl2.image.save(icon72, os.path.join(icons_dir, 'icon-72x72.png'), best_compression)

        # Add 128 pixels to the 384x384 icon to generate 512x512 icon maskable
        icon512_maskable = pygame_sdl2.Surface((512, 512), pygame_sdl2.SRCALPHA)
        icon512_maskable.blit(icon384, (64, 64))
        pygame_sdl2.image.save(icon512_maskable, os.path.join(icons_dir, 'icon-512x512-maskable.png'), best_compression)

        # Resize icon512_maskable to 384x384 to generate 384x384 icon maskable
        icon384_maskable = scale(icon512_maskable, (384, 384))
        pygame_sdl2.image.save(icon384_maskable, os.path.join(icons_dir, 'icon-384x384-maskable.png'), best_compression)

        # Resize icon512_maskable to 192x192 to generate 192x192 icon maskable
        icon192_maskable = scale(icon512_maskable, (192, 192))
        pygame_sdl2.image.save(icon192_maskable, os.path.join(icons_dir, 'icon-192x192-maskable.png'), best_compression)

        # Resize icon512_maskable to 152x152 to generate 152x152 icon maskable
        icon152_maskable = scale(icon512_maskable, (152, 152))
        pygame_sdl2.image.save(icon152_maskable, os.path.join(icons_dir, 'icon-152x152-maskable.png'), best_compression)

        # Resize icon512_maskable to 144x144 to generate 144x144 icon maskable
        icon144_maskable = scale(icon512_maskable, (144, 144))
        pygame_sdl2.image.save(icon144_maskable, os.path.join(icons_dir, 'icon-144x144-maskable.png'), best_compression)

        # Resize icon512_maskable to 128x128 to generate 128x128 icon maskable
        icon128_maskable = scale(icon512_maskable, (128, 128))
        pygame_sdl2.image.save(icon128_maskable, os.path.join(icons_dir, 'icon-128x128-maskable.png'), best_compression)

        # Resize icon512_maskable to 96x96 to generate 96x96 icon maskable
        icon96_maskable = scale(icon512_maskable, (96, 96))
        pygame_sdl2.image.save(icon96_maskable, os.path.join(icons_dir, 'icon-96x96-maskable.png'), best_compression)

        # Resize icon512_maskable to 72x72 to generate 72x72 icon maskable
        icon72_maskable = scale(icon512_maskable, (72, 72))
        pygame_sdl2.image.save(icon72_maskable, os.path.join(icons_dir, 'icon-72x72-maskable.png'), best_compression)

    def generate_files_catalog(destination):
        """
        Generates a JSON file with information about the game files.
        This file is used by the service worker to cache the game files.

        :param destination: string, The destination path where the files will be copied to and where
        game folder is located.
        :param version: string, the version of the game. Should be the same as the version in the
        manifest.json file.

        :return: None
        """
        catalog = {
            "files": [ ],
            "version": int(time.time())
        }
        # Walk through the game folder
        for root, dirs, files in os.walk(destination):
            for file in files:
                # Get the absolute path of the file
                file_path = os.path.join(root, file)
                # Convert it to relative path of the file
                file_name = os.path.relpath(file_path, destination)
                # Replace backslashes with forward slashes
                file_name = file_name.replace("\\", "/")
                # Add the file to the catalog
                catalog["files"].append(file_name)

        with io.open(os.path.join(destination, "pwa_catalog.json"), 'w', encoding='utf-8') as f:
            f.write(json.dumps(catalog))

    def prepare_pwa_files(p, destination):
        """
        Replaces in service-worker.js the cache name with the game name and current timestamp.
        Replace in manifest.json the project name with the ones in the game.
        """

        # Open the service-worker.js file
        with io.open(os.path.join(destination, "service-worker.js"), encoding='utf-8') as f:
            service_worker = f.read()

        # Use re to slugify the game name, avoiding use of 3rd party libraries
        slugified_name = re.sub(r'\W+', '-', p.dump['build']['display_name']).lower()
        service_worker = service_worker.replace('renpy-web-game', slugified_name)

        # Write the file
        with io.open(os.path.join(destination, "service-worker.js"), 'w', encoding='utf-8') as f:
            f.write(service_worker)

        # Open the manifest.json file
        with io.open(os.path.join(destination, "manifest.json"), encoding='utf-8') as f:
            manifest = json.load(f)



        # Replace the project name with the ones in the game
        manifest["name"] = p.dump['build']['display_name']

        screen_size = p.dump.get("size")
        # If width are smaller than height, set the orientation to portrait. If not, leave it as is.
        if screen_size[0] < screen_size[1]:
            manifest["orientation"] = "portrait-primary"

        # Write the file
        with io.open(os.path.join(destination, "manifest.json"), 'w', encoding='utf-8') as f:
            f.write(json.dumps(manifest))

        generate_files_catalog(destination)


    def build_web(p, gui=True, destination=None, launch=True):

        # Figure out the reporter to use.
        if gui:
            reporter = distribute.GuiReporter()
        else:
            reporter = distribute.TextReporter()

        # Determine details.
        p.update_dump(True, gui=gui)

        if destination is None:
            destination = get_web_destination(p)

        display_name = p.dump['build']['display_name']

        # Clean the folder, then remake it.
        if os.path.exists(destination):
            shutil.rmtree(destination)

        os.makedirs(destination, 0o777)

        files_filter = ProgressiveFilter(p, destination)

        # Use the distributor to make game.zip.
        distribute.Distributor(p, packages=[ "web" ], packagedest=os.path.join(destination, "game"),
                reporter=reporter, noarchive=True, scan=False, files_filter=files_filter)

        reporter.info(_("Preparing progressive download"))
        files_filter.finalize()

        # Copy the files from WEB_PATH to destination.
        for fn in os.listdir(WEB_PATH):
            if fn in { "game.zip", "hash.txt", "index.html", "web-icon.png" }:
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

        if not PY2:
            generate_web_icons(p, destination)
            prepare_pwa_files(p, destination)

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

        if launch:
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


init python:

    def web_build_command():
        ap = renpy.arguments.ArgumentParser()
        ap.add_argument("web_project", help="The path to the project directory.")
        ap.add_argument("--launch", action="store_true", help="Launches the app after build and install complete. Implies --install.")
        ap.add_argument("--destination", "--dest", default=None, action="store", help="The directory where the packaged files should be placed.")

        args = ap.parse_args()

        p = project.Project(args.web_project)

        build_web(p=p, gui=False, launch=args.launch, destination=args.destination)

        return False

    renpy.arguments.register_command("web_build", web_build_command)
