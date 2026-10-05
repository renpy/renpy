# By Sebulsik <sebulsik.dev@gmail.com>

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *

import renpy
import os
import sys
from renpy.gl2.gl2shadercache import register_shader

try:
    import renpy.gl2.spinemodel as spinemodel
except ImportError:
    spinemodel = None

import renpy.gl2.spinemotion as spinemotion


SPINE_DEBUG = os.environ.get("SPINE_DEBUG", "0") == "1"


def spine_log(message, *args, debug=True):
    if debug and not SPINE_DEBUG:
        return

    message = " ".join(str(part) for part in (message,) + args)
    renpy.log.open("spine", flush=True).write("%s", message)


class SpineRuntime(object):
    """
    Process-wide Spine state
    """

    def __init__(self):
        self.library = None
        self.initialized = False

        self.supported = None
        self.init_error = None

        # Shared resources keyed by (atlas_path, skeleton_path).
        self.common_cache = {}

    def load_library(self):
        """Load and link the spine-c shared library once per process."""
        if self.library is not None:
            return

        if renpy.windows:
            dll = "spine-c.dll"
        elif renpy.macintosh:
            dll = "libspine-c.dylib"
        elif renpy.ios:
            dll = sys.executable
        else:
            dll = "libspine-c.so"

        fn = os.path.join(os.path.dirname(sys.executable), dll)
        if os.path.exists(fn):
            dll = fn

        dll = dll.encode("utf-8")
        library = spinemodel.load(dll)
        if library is None:
            raise Exception("Could not load Spine. {} was not found.".format(dll))

        self.library = library

    def init(self):
        if self.initialized:
            return

        if spinemodel is None:
            raise Exception("Spine has not been built.")

        if renpy.emscripten:
            raise Exception("Spine is not supported on the web platform.")

        self.load_library()

        # Two-color tint on premultiplied texels, after renpy.texture sampling.
        # Zero dark RGB reduces to ordinary light tint.
        register_shader(
            "spine.colors",
            glsl=300,
            variables="""
            in vec4 a_color;
            in vec3 a_dark_color;
            out vec4 v_spine_light;
            out vec3 v_spine_dark;
        """,
            vertex_250="""
            v_spine_light = a_color;
            v_spine_dark = a_dark_color;
        """,
            fragment_250="""
            fragment_color.rgb = ((fragment_color.a - fragment_color.rgb) * v_spine_dark + fragment_color.rgb * v_spine_light.rgb) * v_spine_light.a;
            fragment_color.a = fragment_color.a * v_spine_light.a;
        """,
        )

        # Loaded scenes rebuild live sessions from saved targets.
        callbacks = renpy.config.after_load_callbacks
        if spinemotion.reset_states not in callbacks:
            callbacks.append(spinemotion.reset_states)

        self.initialized = True

    def has_spine(self):
        if self.supported is None:
            try:
                self.init()
                self.supported = True
                self.init_error = None
            except Exception as e:
                self.supported = False
                self.init_error = "{}: {}".format(type(e).__name__, e)
                spine_log("Spine: not available -", self.init_error, debug=False)

        return self.supported

    def reset(self):
        self.initialized = False
        self.supported = None
        self.init_error = None
        self.common_cache.clear()
        spinemotion.reset()

    def common_for(self, atlas_path, skeleton_path):
        """The shared SpineCommon for these files, created on first use."""
        key = (atlas_path, skeleton_path)
        common = self.common_cache.get(key)
        if common is None:
            common = SpineCommon(self.library, atlas_path, skeleton_path)
            self.common_cache[key] = common
            spine_log("Spine: Created shared common resources for", skeleton_path)
        return common

    def common_if_cached(self, atlas_path, skeleton_path):
        """The shared SpineCommon if one exists, without creating it."""
        return self.common_cache.get((atlas_path, skeleton_path))


runtime = SpineRuntime()


def init():
    runtime.init()

def has_spine():
    return runtime.has_spine()

def reset():
    runtime.reset()

class SpineCommon(object):
    """
    Stores information common to all SpineDisplayable instances using the same
    skeleton/atlas files:

    - Skeleton data (immutable bone structure, animations, skins)
    - Atlas data (texture page definitions)
    - Texture manager (atlas page displayables, resolved through Ren'Py's loader)
    """

    def __init__(self, library, atlas_path, skeleton_path):
        self.atlas_path = atlas_path
        self.skeleton_path = skeleton_path

        atlas_dir = os.path.dirname(atlas_path) if atlas_path else None
        self.texture_manager = spinemodel.SpineTextureManager(atlas_dir=atlas_dir)

        # Shared data outlives individual session drawables.
        self.spine_data = spinemodel.SpineData(library)

        # Expose atlas pages to Ren'Py prediction.
        self.textures = []

        self.load_error = None

        self.load_data()

    def load_data(self):
        if self.spine_data.is_loaded():
            return True

        if renpy.display.predict.predicting:
            return False

        status = self.spine_data.load(self.atlas_path, self.skeleton_path)
        if status != 0:
            message = self.spine_data.last_error
            if message != self.load_error:
                spine_log(message, debug=False)
                self.load_error = message
            return False

        self.load_error = None

        self.textures = [
            self.texture_manager.load_atlas_page(name)
            for name in self.spine_data.get_page_names()
            if name
        ]

        return True

def resolve_zoom(zoom, zoomX, zoomY):
    zoom = 1.0 if zoom is None else float(zoom)
    zoomX = zoom if zoomX is None else float(zoomX)
    zoomY = zoom if zoomY is None else float(zoomY)

    if zoom == 0.0 or zoomX == 0.0 or zoomY == 0.0:
        raise ValueError(
            "Spine: zoom, zoomX and zoomY must be non-zero (got zoom={!r}, zoomX={!r}, zoomY={!r}).".format(
                zoom, zoomX, zoomY))

    return (zoom, zoomX, zoomY)


class SpineDisplayable(renpy.display.displayable.Displayable):
    """
    Ren'Py displayable for a Spine character.

    An instance is a thin, picklable description of intent: which files, which
    zoom, and which animations/skins it asks to be shown. Live state - the
    native model, the render clock - is not saved. It is re-bound by the motion
    sweep (spinemotion.update_states) after a load, rollback, or reload.
    """

    nosave = ["common_cache", "_session", "_last_st"]

    common_cache = None
    _session = None
    _last_st = None

    _rollback_serial = None

    # One-shot _reset/_mix request, consumed by the sweep.
    _oneshot_mode = None

    # Default supports saves predating constructor-property preservation.
    properties = {}

    # Identify displayables without a circular import from spinemotion.
    _is_spine_displayable = True

    _duplicatable = True

    # Bound animation catch-up and physics substeps after stalls.
    MAX_DELTA = 0.064 # Lowkirkenuinely, this problem set can only be decided by the community

    def __init__(self, atlas_path, skeleton_path, zoom=1.0, zoomX=None, zoomY=None, animation=None, loop=True, skin=None, aliases=None, metadata=None, **properties):
        super(SpineDisplayable, self).__init__(**properties)

        self.properties = properties

        self.atlas_path = atlas_path
        self.skeleton_path = skeleton_path

        self.aliases = dict(aliases) if aliases else {}

        self.zoom, self.zoomX, self.zoomY = resolve_zoom(zoom, zoomX, zoomY)

        self.common_cache = None
        self.loaded = False

        self._session = None

        # None makes the first frame advance by zero.
        self._last_st = None

        self._target_animation = None
        self._target_animations = ()
        self._target_skins = ()
        self._target_loop = loop

        self._metadata = metadata

        self._oneshot_mode = None
        self._rollback_serial = None

        self.name = None

        self.width = 512 * abs(self.zoomX)
        self.height = 512 * abs(self.zoomY)

        self._initial_animation = animation
        self._initial_animation_loop = loop
        self._initial_skin = skin

        runtime.init()
        spine_log("Spine: Initializing with atlas {!r}, skeleton {!r}, zoom {}".format(atlas_path, skeleton_path, zoom))

        self._ensure_common()

        self._target_animations = tuple(self._resolve_alias(animation)) if animation else ()
        self._target_animation = self._target_animations[-1] if self._target_animations else None
        self._target_skins = tuple(self._resolve_alias(skin)) if skin else ()

    def create_common(self):
        self.common_cache = runtime.common_for(self.atlas_path, self.skeleton_path)
        return self.common_cache

    @property
    def common(self):
        if self.common_cache is not None:
            return self.common_cache
        return self.create_common()

    def _common_or_none(self):
        common = self.common_cache
        if common is None:
            common = runtime.common_if_cached(self.atlas_path, self.skeleton_path)
        if common is None:
            if renpy.display.predict.predicting:
                return None
            common = self.create_common()

        if not common.load_data():
            return None

        return common

    def _ensure_common(self):
        if not spinemodel:
            spine_log("Spine: spinemodel not available", debug=False)
            return

        common = self._common_or_none()
        if common is None:
            self.loaded = False
            return

        self.common_cache = common

        self._apply_aliases()

        size = self._size_from_data(common)
        if size:
            self.width, self.height = size

        self.loaded = True

    def _size_from_data(self, common):
        dx, dy, dw, dh = common.spine_data.get_setup_bounds()
        if dw <= 0.0 or dh <= 0.0:
            return None

        sx = self.zoomX
        sy = -self.zoomY  # yDown: skeleton Y maps to -Y in render space

        x0 = dx * sx
        x1 = (dx + dw) * sx
        y0 = dy * sy
        y1 = (dy + dh) * sy

        return (abs(x1 - x0), abs(y1 - y0))

    def _shared_names(self):
        """(animations, skins) name lists from the shared data, or ([], [])
        when it is not (and cannot now be) loaded."""
        common = self._common_or_none()
        if common is None:
            return ([], [])
        return (common.spine_data.get_animation_names(), common.spine_data.get_skin_names())

    def _resolve_alias(self, name):
        v = self.aliases.get(name, name)
        if isinstance(v, (list, tuple)):
            return list(v)
        return [v]

    def _apply_aliases(self):
        if not self.aliases:
            return

        anim_list, skin_list = self._shared_names()
        animations = set(anim_list)
        skins = set(skin_list)

        for k, v in self.aliases.items():
            values = list(v) if isinstance(v, (list, tuple)) else [v]
            for vv in values:
                if vv not in animations and vv not in skins:
                    raise Exception("Spine alias {!r}: {!r} is not a known animation or skin of {}.".format(k, vv, self.skeleton_path))
            if k in animations or k in skins:
                raise Exception("Spine alias {!r} is already an animation or skin of {}.".format(k, self.skeleton_path))

    def set_animation(self, animation_name, loop=True, track=0):
        self._target_animations = tuple(self._resolve_alias(animation_name)) if animation_name else ()
        self._target_animation = self._target_animations[-1] if self._target_animations else None
        self._target_loop = loop
        spinemotion.registry.mark_showing()  # ensure the sweep runs and applies it
        return True

    def get_animation_names(self):
        return self._shared_names()[0]

    def set_skin(self, skin_name):
        if skin_name is None:
            self._target_skins = ()
        elif isinstance(skin_name, (list, tuple)):
            resolved = []
            for s in skin_name:
                resolved.extend(self._resolve_alias(s))
            self._target_skins = tuple(resolved)
        else:
            self._target_skins = tuple(self._resolve_alias(skin_name))
        spinemotion.registry.mark_showing()
        return True

    def get_skin_names(self):
        return self._shared_names()[1]

    def get_current_skin_name(self):
        session = self._session
        if session is not None and session.model is not None:
            return session.model.get_current_skin_name()
        return None

    def _page_texture(self, page_key, width, height, st, at):
        common = self._common_or_none()
        if common is None:
            return None

        displayable = common.texture_manager.load_atlas_page(page_key)
        if displayable is None:
            return None

        # UnoptimizedTexture returns a texture; other displayables may return a Render.
        return renpy.display.im.render_for_texture(displayable, width, height, st, at)

    def render(self, width, height, st, at):
        session = self._session
        model = session.model if session is not None else None

        if model is None or not model.is_loaded():
            return renpy.exports.Render(self.width, self.height)

        # Retained transition copies render without advancing the shared model.
        is_driver = session.is_driver(self)

        wake = session.take_invalidation() if is_driver else None

        # Start and wake with zero delta to avoid catching up on idle time.
        if self._last_st is None or wake is not None:
            delta_time = 0.0
            step = True
        else:
            delta_time = min(max(st - self._last_st, 0.0), self.MAX_DELTA)
            step = delta_time > 0.0
        self._last_st = st

        if is_driver and step:
            model.update_animation(delta_time)

        render = renpy.exports.Render(self.width, self.height)

        try:
            # Preserve native draw order across consecutive mesh batches.
            for run in model.render_runs():
                texture = self._page_texture(run.page_key, width, height, st, at)
                if texture is None:
                    spine_log("Spine: texture not found for page {!r}, skipping run".format(run.page_key), debug=False)
                    continue

                run_render = model.run_render(run, texture, width, height)
                if run_render is not None:
                    render.subpixel_blit(run_render, (0, 0))

        except Exception as e:
            spine_log("Spine: error during render: {}".format(e), debug=False)

        if is_driver and model.needs_next_frame():
            renpy.display.render.redraw(self, 0)

        return render

    def _available_names(self):
        available_animations, available_skins = self._shared_names()
        anim_set = set(available_animations)
        skin_set = set(available_skins)

        alias_animations = []
        alias_skins = []
        for k, v in self.aliases.items():
            values = list(v) if isinstance(v, (list, tuple)) else [v]
            if values and all(x in anim_set for x in values):
                alias_animations.append(k)
            elif values and all(x in skin_set for x in values):
                alias_skins.append(k)

        return (available_animations + alias_animations, available_skins + alias_skins)

    def _expand(self, attributes):
        """Alias-expand an ordered list of attribute names into an ordered
        tuple of real names."""
        resolved = []
        for attr in attributes:
            resolved.extend(self._resolve_alias(attr))
        return tuple(resolved)

    def _duplicate(self, args):
        if not self._duplicatable:
            return self

        if not args:
            return self

        available_animations, available_skins = self._available_names()

        oneshot, attrs = self._extract_pseudo_attributes(args.args)

        animation_attributes = [attr for attr in attrs if attr in available_animations]
        skin_attributes = [attr for attr in attrs if attr in available_skins]

        # Prediction may lack data; carry initial values until names can be resolved.
        if self.loaded:
            for attr in attrs:
                if attr not in available_animations and attr not in available_skins:
                    raise Exception("When showing {}, {!r} is not a known Spine animation or skin.".format(
                        " ".join(args.name), attr))

        primary_animation = animation_attributes[0] if animation_attributes else self._initial_animation
        primary_skin = skin_attributes[0] if skin_attributes else self._initial_skin

        rv = SpineDisplayable(
            self.atlas_path,
            self.skeleton_path,
            zoom=self.zoom,
            zoomX=self.zoomX,
            zoomY=self.zoomY,
            animation=primary_animation,
            loop=self._initial_animation_loop,
            skin=primary_skin,
            aliases=self.aliases,
            metadata=self._metadata,
            **self.properties
        )
        rv.name = args.name
        rv._duplicatable = False

        if animation_attributes:
            rv._target_animations = self._expand(animation_attributes)
            rv._target_animation = rv._target_animations[-1]

        if skin_attributes:
            rv._target_skins = self._expand(skin_attributes)

        rv._oneshot_mode = oneshot

        spinemotion.registry.mark_showing()

        return rv

    @staticmethod
    def _extract_pseudo_attributes(attributes):
        oneshot = None
        remaining = []
        for a in attributes:
            if a == "_reset":
                if oneshot is None:
                    oneshot = "reset"
            elif a == "_mix":
                oneshot = "mix"
            else:
                remaining.append(a)
        return (oneshot, remaining)

    def _list_attributes(self, tag, attributes):

        if not self.loaded:
            return []

        available_animations, available_skins = self._available_names()
        return list(available_animations) + list(available_skins)

    def _choose_attributes(self, tag, attributes, optional):
        if not self.loaded:
            return tuple()

        pseudo = [a for a in attributes if a in ("_reset", "_mix")]
        attrs = [a for a in attributes if a not in ("_reset", "_mix")]
        opt = [a for a in (optional or ()) if a not in ("_reset", "_mix")]

        available_animations, available_skins = self._available_names()

        req_animations = [a for a in attrs if a in available_animations]
        req_skins = [a for a in attrs if a in available_skins]
        opt_animations = [a for a in opt if a in available_animations]
        opt_skins = [a for a in opt if a in available_skins]

        animation_attributes = req_animations if req_animations else opt_animations
        skin_attributes = req_skins if req_skins else opt_skins

        spinemotion.registry.mark_showing()

        return tuple(pseudo + animation_attributes + skin_attributes)

    def visit(self):
        """Return the atlas page displayables, so Ren'Py's predictor decodes
        and uploads them ahead of the first render (Live2D pattern)."""

        common = self.common_cache

        if common is None:
            # Prediction instances borrow the base displayable's loaded textures.
            common = runtime.common_if_cached(self.atlas_path, self.skeleton_path)

        if common is not None:
            return list(common.textures)

        return []

    def per_interact(self):
        spinemotion.registry.mark_showing()

    def after_setstate(self):
        for stale in ("_rendered_texture_cache", "texture_manager", "spine_model"):
            self.__dict__.pop(stale, None)

        self.common_cache = None
        self._session = None
        self._last_st = None


def Spine(
    atlas_path,
    skeleton_path,
    zoom=1.0,
    zoomX=None,
    zoomY=None,
    animation=None,
    skin=None,
    loop=True,
    aliases=None,
    metadata=None,
    **kwargs
):
    """
    Create a Spine model displayable.
    This is the main function used to create Spine animations in Ren'Py scripts.
    Args:
        atlas_path: Path to the .atlas file
        skeleton_path: Path to the .json or .skel file
        zoom, zoomX, zoomY: Skeleton scale. zoomX/zoomY default to zoom; a
            negative value mirrors that axis; zero is rejected.
        animation: Initial animation to play (optional)
        loop: Whether the initial animation should loop (default True)
        skin: Initial skin to apply (optional)
        aliases: A dict mapping user-facing alias names to real animation or skin
            names, e.g. {"happy": "smile_big", "casual": "outfit_01"} (optional)
        metadata: Per-character transition policy (optional). A static dict
            controlling how attribute changes transition, e.g.
            {"default_transition": "mix", "mix_time": 0.2,
             "transitions": {("idle", "talk"): {"mode": "mix", "time": 0.12}},
             "skin_transition": "setup",
             "tracks": {"wave": {"track": 1, "alpha": 0.8}}}.
            Omit for hard-cut behaviour (default_transition = "reset"). A
            callable hook returning such a dict is resolved at each transition.
        **kwargs: Displayable properties (position, style, ...), carried across
            attribute-based shows
    Returns:
        SpineDisplayable instance
    Example:
        image ryu = Spine("ryu.atlas", "ryu.json", zoom=1.0,
                          animation="idle", skin="default", loop=True)
    """
    return SpineDisplayable(atlas_path, skeleton_path, zoom, zoomX, zoomY,
                            animation=animation, loop=loop, skin=skin,
                            aliases=aliases, metadata=metadata, **kwargs)
