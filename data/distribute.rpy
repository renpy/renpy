# This file contains the code needed to build a Ren'Py distribution.

init:
    python:
        # Returns true if a file or directory should not be included in
        # the distribution
        def ignored(fn):
            if fn[0] == ".":
                return True

            for i in store.ignore_extensions:
                if fn.endswith(i):
                    return True

            if fn.lower() in ("thumbs.db",
                              "launcherinfo.py",
                              "traceback.txt",
                              "errors.txt",
                              "completion.lua",):
                return True
            
            if fn == "saves":
                return True

            if fn == "archived":
                return True

            return False
            
label distribute:

    python hide:
        import zipfile
        import tarfile
        import os
        import os.path
        import time
        import sys
        import zlib

        zlib.Z_DEFAULT_COMPRESSION = 9

        store.progress_time = 0

        def progress(tit, n, m, time=time):
            
            if time.time() < store.progress_time + .1:
                return

            title(tit)

            mid(message)
            ui.bar(m, n, xmaximum=200, xalign=0.5)
            ui.close()

            ui.pausebehavior(0)
            interact()
            
             
        lint()

        store.message = ""

        title("Building Distributions")

        mid()
        text("I've just performed a lint on your project. If it contains errors, you should say no and fix them.\n\nDo you want to continue?")
        ui.close()

        bottom()
        button("Yes", clicked=ui.returns(True))
        button("No", clicked=ui.returns(False))
        ui.close()

        if not interact():
            renpy.jump("tools")


        if os.path.exists(config.renpy_base + "/renpy.exe"):
            windows = True
        else:
            windows = False

        if os.path.exists(config.renpy_base + "/lib/linux-x86"):
            linux = True
        else:
            linux = False

        if os.path.exists(config.renpy_base + "/renpy.app"):
            mac = True
        else:
            mac = False


        if not windows or not mac or not linux:
            store.message = "The full version of Ren'Py can build for Windows, Mac, and Linux. Download it from www.renpy.org."
            
        title("Building Distributions")

        mid()
        text("Distributions will be built for the following platforms:")

        spacer()

        if windows:
            text("Windows 98+", style='launcher_input')

        if linux:
            text("Linux x86", style='launcher_input')

        if mac:
            text("Mac OS X 10.3+", style='launcher_input')

        spacer()


        # TODO: If missing platforms, prompt for a DL.

        text("Is this okay?")
        ui.close()

        bottom()
        button("Yes", clicked=ui.returns(True))
        button("No", clicked=ui.returns(False))
        ui.close()

        if not interact():
            renpy.jump("tools")

        default_name = project.name
        if persistent.build_project == project.name:
            default_name = persistent.build_name        

        name = prompt("Building Distributions",
                      "Please enter a base name for the directories making up this distribution.",
                      "tools",
                      default_name,
                      "This usually should include a name and version number, like 'moonlight_walks-1.0'.")

        name = name.strip()

        if not name:
            store.error("Error", "The distribution name should not be empty.", "tools_menu")

        try:
            name = name.encode("ascii")
        except:
            store.error("Error", "Distribution names must be ASCII. This is because archive file formats do not support non-ASCII characters in a uniform way.", "tools_menu")

        persistent.build_project = project.name
        persistent.build_name = name

        ignore_extensions = persistent.ignore_extensions or "~ .bak"
        ignore_extensions = prompt("Building Distributions", "Please enter a space separated list of the file extensions you do not want included in the distribution.", "tools", ignore_extensions)
        persistent.ignore_extensions = ignore_extensions    
        store.ignore_extensions = [ i.strip() for i in ignore_extensions.strip().split() ]

        
        # Figure out the files that will make up the distribution.

        multi_dirs = [ ]
        multi_files = [ ]

        # Ren'Py Source.
        for dirname, dirs, files in os.walk(config.renpy_base + "/renpy"):

            shortdir = dirname[len(config.renpy_base)+1:]

            dirs[:] = [ i for i in dirs if not i[0] == '.' ]

            for d in dirs:
                multi_dirs.append((dirname + "/" + d, shortdir + "/" + d))

            for f in files:
                if f[0] == "." or f[-1] == "~":
                    continue

                if f.endswith(".pyc") or f.endswith(".pyo"):
                    continue
                
                multi_files.append((dirname + "/" + f, shortdir + "/" + f))

        multi_files.append((config.renpy_base + "/LICENSE.txt", "renpy/LICENSE.txt"))

        # Project files.
        for dirname, dirs, files in os.walk(project.path):

            shortdir = dirname[len(project.path)+1:]

            dirs[:] = [ i for i in dirs if not project.info["ignored"](i) ]
                                                                       

            for d in dirs:
                if project.info["ignored"](d):
                    continue
                
                multi_dirs.append((dirname + "/" + d, shortdir + "/" + d))

            for f in files:
                if project.info["ignored"](f):
                    continue
                
                multi_files.append((dirname + "/" + f, shortdir + "/" + f))

        # Common directory... doesn't include subdirs.
        multi_dirs.append((config.commondir, "common"))
        for i in os.listdir(config.commondir):
            if i[0] == "." or i[-1] == "~" or i.endswith(".bak"):
                continue

            multi_files.append((config.commondir + "/" + i,
                                "common/" + i))


        shortgamedir = project.gamedir[len(project.path)+1:]

        # Script version.
        multi_files.append((config.gamedir + "/script_version.rpy",
                            shortgamedir + "/script_version.rpy"))

        multi_files.append((config.gamedir + "/script_version.rpyc",
                            shortgamedir + "/script_version.rpyc"))
       
        # renpy.py
        multi_files.append((config.renpy_base + "/renpy.py", project.name + ".py"))


        multi_dirs.sort()
        multi_files.sort()

        # Windows Zip
        if windows:
            win_files = [
                ( config.renpy_base + "/renpy.exe", project.name + ".exe"),
                ( config.renpy_base + "/renpy.code", "renpy.code" ),
                ( config.renpy_base + "/python23.dll", "python23.dll" ),
                ]

            zf = zipfile.ZipFile(name + ".zip", "w", zipfile.ZIP_DEFLATED)

            progress_len = len(multi_files) + len(win_files)
            store.message = "Be sure to announce your project at the Lemma Soft Forums."
                               
            for i, (fn, an) in enumerate(multi_files + win_files):
                progress("Building Windows", i, progress_len)

                zi = zipfile.ZipInfo(name + "/" + an)

                s = os.stat(fn)
                zi.date_time = time.gmtime(s.st_mtime)[:6]
                zi.compress_type = zipfile.ZIP_DEFLATED
                zi.create_system = 3

                zi.external_attr = long(0100666) << 16 
                data = file(fn, "rb").read()

                zf.writestr(zi, data)


            zf.close()


        # Linux Tar Bz2
        if linux:

            linux_dirs = [
                (config.renpy_base + "/lib", "lib"),
                ]

            linux_files = [
                (config.renpy_base + "/renpy.sh", project.name + ".sh"),
                (config.renpy_base + "/lib/python", "lib/python"),
                ]
                

            linux_base = config.renpy_base + "/lib/linux-x86"
            

            for dirname, dirs, files in os.walk(linux_base):
                
                dirs[:] = [ i for i in dirs if not i[0] == '.' ]

                shortname = dirname[len(config.renpy_base)+1:]

                for d in dirs:
                    linux_dirs.append((dirname + "/" + d,
                                       shortname + "/" + d))

                for f in files:
                    if f.endswith(".pyc") or f.endswith(".pyo"):
                        continue
                    
                    linux_files.append((dirname + "/" + f,
                                        shortname + "/" + f))

            linux_dirs.sort()
            linux_files.sort()

            tf = tarfile.open(name + "-linux-x86.tar.bz2", "w:bz2")
            tf.dereference = True

            progress_len = len(multi_dirs) + len(linux_dirs) + len(multi_files) + len(linux_files)
            store.message = "If appropriate, please submit your game to www.renai.us."

            for j, i in enumerate(multi_dirs + linux_dirs + multi_files + linux_files):

                progress("Building Linux", j, progress_len)

                fn, an = i

                info = tf.gettarinfo(fn, name + "-linux-x86/" + an)

                if info.isdir():
                    perms = 0777
                elif info.name.endswith(".sh"):
                    perms = 0777
                elif info.name.endswith(".so"):
                    perms = 0777
                elif info.name.endswith("python"):
                    perms = 0777
                elif info.name.endswith("python.real"):
                    perms = 0777
                else:
                    perms = 0666

                info.mode = perms
                info.uid = 1000
                info.gid = 1000
                info.uname = "renpy"
                info.gname = "renpy"

                if info.isreg():
                    tf.addfile(info, file(fn, "rb"))
                else:
                    tf.addfile(info)

            tf.close()

        if mac:

            mac_files = [ ]

            for dirname, dirs, files in os.walk(config.renpy_base + "/renpy.app"):
                shortname = project.name + ".app/" + dirname[len(config.renpy_base + "/renpy.app")+1:]

                dirs[:] = [ i for i in dirs if not i[0] == '.' ]

                for f in files:
                    mac_files.append((dirname + "/" + f, shortname + "/" + f))


            zf = zipfile.ZipFile(name + "-mac.zip", "w", zipfile.ZIP_DEFLATED)


            progress_len = len(multi_files) + len(mac_files)
            store.message = "Thank you for choosing Ren'Py."

            for i, (fn, an) in enumerate(multi_files + mac_files):

                progress("Building Mac OS X", i, progress_len)

                zi = zipfile.ZipInfo(name + "-mac/" + an)

                s = os.stat(fn)
                zi.date_time = time.gmtime(s.st_mtime)[:6]

                zi.compress_type = zipfile.ZIP_DEFLATED

                zi.create_system = 3


                if os.path.dirname(fn).endswith("MacOS") or fn.endswith(".so") or fn.endswith(".dylib"):
                    zi.external_attr = long(0100777) << 16 
                    data = file(fn, "rb").read()
                else:
                    zi.external_attr = long(0100666) << 16 
                    data = file(fn, "rb").read()

                zf.writestr(zi, data)

        # Announce Success

        store.message = ""

        title("Success")

        mid()
        text("The distribution(s) have been built. Be sure to test them before release.")

        spacer()

        if mac:
            text("Note that unpacking and repacking Mac zips and Linux tarballs on Windows isn't supported.")

        ui.close()

        bottom()
        button("Return", clicked=ui.returns(True))
        ui.close()
        
        interact()

        
    jump tools
               
        
