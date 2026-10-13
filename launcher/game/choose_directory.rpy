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

init python:

    from pathlib import Path

    def directory_is_writable(path):
        if path is None:
            return False

        path = Path(path).resolve()
        if not path.is_dir():
            return False

        test = path / "renpy test do not use"

        try:
            if test.is_dir():
                test.rmdir()

            test.mkdir()
            test.rmdir()

            return True

        except Exception:
            return False

    def __sdl_show_file_dialog(title, default_path):
        sdl = renpy.get_sdl_dll(3)
        window = renpy.get_sdl_window_pointer()

        if sdl is None or window is None or not hasattr(sdl, "SDL_ShowFileDialogWithProperties"):
            return None

        import ctypes

        path = None
        error = None
        completed = False

        def callback(userdata, filelist, filter):
            nonlocal path, error, completed

            if filelist:
                path = filelist[0].decode("utf-8") if filelist[0] else None
            else:
                error = renpy.pygame.get_error() or _("Unknown SDL error.")

            completed = True

        callback_type = ctypes.CFUNCTYPE(
            None,
            ctypes.c_void_p,
            ctypes.POINTER(ctypes.c_char_p),
            ctypes.c_int,
        )

        callback = callback_type(callback)
        show_folder_dialog = sdl.SDL_ShowFileDialogWithProperties
        show_folder_dialog.argtypes = [
            ctypes.c_int,
            callback_type,
            ctypes.c_void_p,
            ctypes.c_uint32,
        ]
        show_folder_dialog.restype = None

        sdl.SDL_CreateProperties.argtypes = []
        sdl.SDL_CreateProperties.restype = ctypes.c_uint32
        sdl.SDL_SetPointerProperty.argtypes = [ctypes.c_uint32, ctypes.c_char_p, ctypes.c_void_p]
        sdl.SDL_SetPointerProperty.restype = ctypes.c_bool
        sdl.SDL_SetStringProperty.argtypes = [ctypes.c_uint32, ctypes.c_char_p, ctypes.c_char_p]
        sdl.SDL_SetStringProperty.restype = ctypes.c_bool
        sdl.SDL_DestroyProperties.argtypes = [ctypes.c_uint32]
        sdl.SDL_DestroyProperties.restype = None

        chooser_error_msg = _("Could not open the directory chooser.")
        props = sdl.SDL_CreateProperties()
        if not props:
            interface.error(chooser_error_msg, submessage=renpy.pygame.get_error())

        try:
            if not sdl.SDL_SetPointerProperty(props, b"SDL.filedialog.window", window):
                interface.error(chooser_error_msg, submessage=renpy.pygame.get_error())

            if not sdl.SDL_SetStringProperty(props, b"SDL.filedialog.title", title.encode("utf-8")):
                interface.error(chooser_error_msg, submessage=renpy.pygame.get_error())

            if default_path is not None:
                default_path_bytes = str(default_path).encode("utf-8")
                if not sdl.SDL_SetStringProperty(props, b"SDL.filedialog.location", default_path_bytes):
                    interface.error(chooser_error_msg, submessage=renpy.pygame.get_error())

            # SDL_FILEDIALOG_OPENFOLDER is 2; multiple selection defaults to false.
            show_folder_dialog(2, callback, None, props)

            while not completed:
                renpy.pause(0.1)

        finally:
            sdl.SDL_DestroyProperties(props)

        if error is not None:
            interface.error(_("Could not open the directory chooser."), submessage=error)

        return path

    def choose_directory(default_path):
        """
        Pops up a directory chooser.

        `default_path`
            The directory that is selected by default. If None, config.renpy_base
            is selected.

        Returns a (path, is_default) tuple, where path is the chosen directory,
        and is_default is true if and only if it was chosen by default mechanism
        rather than user choice.
        """

        path = __sdl_show_file_dialog(__("Select Projects Directory"), default_path)

        # Path being None or "" means selection was cancelled or unsuccessful.
        if not path:
            if default_path is None:
                try:
                    default_path = Path(config.renpy_base).resolve().parent
                except Exception:
                    pass
            else:
                default_path = Path(default_path).resolve()

            if not directory_is_writable(default_path):
                interface.error(_("No directory was selected, but one is required."))

            return default_path, True

        result = Path(path)
        if not result.is_dir():
            interface.error(_("The selected directory does not exist."))
        elif not directory_is_writable(result):
            interface.error(_("The selected directory is not writable."))

        return str(result.resolve()), False
