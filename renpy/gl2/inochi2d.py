

import renpy
from renpy.gl2.gl2shadercache import register_shader
from renpy.display.core import absolute

try:
    import renpy.gl2.inochi2dmodel as inochi2dmodel
except ImportError:
    inochi2dmodel = None

import sys
import os
import json
import collections
import re
import time

did_onetime_init = False
def onetime_init():
    global did_onetime_init
    if did_onetime_init:
        return

    if renpy.emscripten:
        raise Exception("Inochi2D is not WASM compatible at current time.")
    elif renpy.windows:
        dll = "inochi2d.dll"
    elif renpy.macintosh:
        dll = "libinochi2d.dylib"
    elif renpy.ios:
        dll = sys.executable
    else:
        dll = "libinochi2d.so"
    
    if dll != "builtin":
        fn = os.path.join(os.path.dirname(sys.executable), dll)
        if os.path.exists(fn):
            dll = fn
    
    dll = dll.encode("utf-8")
    if not renpy.gl2.inochi2dmodel.load(dll):  # type: ignore
        raise Exception("Could not load Inochi2D. {} was not found.".format(dll))
    
    did_onetime_init = True

did_init = False
def init():
    """
    Called to initialize Inochi2D, if needed.
    """

    global did_init
    if did_init:
        return

    if inochi2dmodel is None:
        raise Exception("Inochi2D has not been built.")
    
    onetime_init()

# Caches the result of has_inochi2d.
_has_inochi2d = None
def has_inochi2d():
    """
    :doc: inochi2d

    Returns True if Inochi2D is supported on the current platform, and
    False otherwise.
    """

    global _has_inochi2d

    if _has_inochi2d is None:
        try:
            init()
            _has_inochi2d = True
        except Exception:
            _has_inochi2d = False

    return _has_inochi2d

