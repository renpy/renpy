# Copyright 2025-2046 Sebulsik <sebulsik.dev@gmail.com>
#
# All rights reserved.
#
# This source code and its associated files are the property of
# Sebulsik. Unauthorized copying, modification, distribution,
# sublicensing, or use of this software, in whole or in part, is
# prohibited without prior written permission from the copyright holder.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER BE LIABLE FOR ANY CLAIM,
# DAMAGES, OR OTHER LIABILITY ARISING FROM, OUT OF, OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OF THIS SOFTWARE.

# Spine displayables, shared resources, shaders, and rendering.


from __future__ import division, absolute_import, with_statement, print_function, unicode_literals, annotations
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *

import renpy
import os
import sys
from typing import TYPE_CHECKING, Any, Dict, Iterable, List, Literal, Mapping, NamedTuple, Optional, Sequence, Tuple, TypeAlias, Union
from renpy.gl2.gl2shadercache import register_shader

try:
    import renpy.gl2.spinemodel as spinemodel
except ImportError:
    spinemodel = None

import renpy.gl2.spinemotion as spinemotion

if TYPE_CHECKING:
    from renpy.gl2.spinemotion import SpineSession
    from renpy.gl2.spinetypes import SpineDataLike, SpineMetadataArgument, SpineOneshot, SpineTextureManagerLike


# Shared by the Python and Cython Spine modules.
SPINE_DEBUG = os.environ.get("SPINE_DEBUG", "0") == "1"


def spine_log(message: object, *args: object, debug: bool = True) -> None:
    """Write a Spine diagnostic. Use debug=False for warnings and errors."""
    if debug and not SPINE_DEBUG:
        return

    message = " ".join(str(part) for part in (message,) + args)
    renpy.log.open("spine", flush=True).write("%s", message)


class SpineRuntime(object):
    """Manage Spine support, initialization, and shared character resources."""

    def __init__(self) -> None:
        self.library_loaded = False
        self.initialized = False

        self.supported: Optional[bool] = None
        self.init_error: Optional[str] = None

        # Shared resources keyed by (atlas_path, skeleton_path).
        self.common_cache: Dict[Tuple[str, str], SpineCommon] = {}

    def load_library(self) -> None:
        """Load and link the spine-c shared library once per process."""
        if self.library_loaded:
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

        dll_path = dll.encode("utf-8")
        if spinemodel.load(dll_path) is None:
            raise Exception("Could not load Spine. {!r} was not found.".format(dll_path))

        self.library_loaded = True

    def init(self) -> None:
        """Prepare Spine rendering and load callbacks. Failed initialization can be retried."""
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

    def has_spine(self) -> bool:
        """True if Spine is supported here. The reason for False is kept in
        ``init_error``."""
        if self.supported is None:
            self.supported = self._probe()
        return self.supported

    def _probe(self) -> bool:
        try:
            self.init()
        except Exception as e:
            self.init_error = "{}: {}".format(type(e).__name__, e)
            spine_log("Spine: not available -", self.init_error, debug=False)
            return False
        self.init_error = None
        return True

    def reset(self) -> None:
        """Clear cached resources and live sessions after a script reload."""
        self.initialized = False
        self.supported = None
        self.init_error = None
        self.common_cache.clear()
        spinemotion.reset()

    def common_for(self, atlas_path: str, skeleton_path: str) -> SpineCommon:
        """The shared SpineCommon for these files, created on first use."""
        key = (atlas_path, skeleton_path)
        common = self.common_cache.get(key)
        if common is None:
            common = SpineCommon(atlas_path, skeleton_path)
            self.common_cache[key] = common
            spine_log("Spine: Created shared common resources for", skeleton_path)
        return common

    def common_if_cached(self, atlas_path: str, skeleton_path: str) -> Optional[SpineCommon]:
        """The shared SpineCommon if one exists, without creating it."""
        return self.common_cache.get((atlas_path, skeleton_path))


runtime = SpineRuntime()


def init() -> None:
    runtime.init()

def has_spine() -> bool:
    return runtime.has_spine()

def reset() -> None:
    runtime.reset()


class SpineCommon(object):
    """Share loaded skeleton data and textures between instances of a character."""

    def __init__(self, atlas_path: str, skeleton_path: str) -> None:
        self.atlas_path = atlas_path
        self.skeleton_path = skeleton_path

        atlas_dir = os.path.dirname(atlas_path) if atlas_path else None
        self.texture_manager: SpineTextureManagerLike = spinemodel.SpineTextureManager(atlas_dir=atlas_dir)

        # Shared data outlives individual session drawables.
        self.spine_data: SpineDataLike = spinemodel.SpineData()

        # Expose atlas pages to Ren'Py prediction.
        self.textures: List[Any] = []

        self.load_error: Optional[str] = None

        self.load_data()

    def load_data(self) -> bool:
        """Load shared character data if needed. Return whether it is ready."""
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


SpineModelAliasKind: TypeAlias = Literal["animation", "skin"]

# A bare animation, skin or alias name, or a
# ("animation" | "skin", name) tuple that says which one a shared name means.
SpineModelAliasArgument: TypeAlias = Union[str, Tuple[SpineModelAliasKind, str]]

# An alias value: one argument, or a list of them composed in show order.
SpineModelAliasValue: TypeAlias = Union[SpineModelAliasArgument, List[SpineModelAliasArgument]]


def alias_argument(value: object, where: str) -> SpineModelAliasArgument:
    """Validate a name or an explicitly typed name. Existence is checked after loading."""
    if isinstance(value, str):
        return value
    if isinstance(value, tuple) and len(value) == 2 and isinstance(value[1], str):
        kind, name = value
        if kind == "animation":
            return ("animation", name)
        if kind == "skin":
            return ("skin", name)
    raise TypeError("Spine: {} must be a name or an (\"animation\" | \"skin\", name) tuple, got {!r}; "
                    "use a list for several names.".format(where, value))


def alias_arguments(value: object, where: str) -> List[SpineModelAliasArgument]:
    """Validate an alias’s names and return them in show order."""
    if isinstance(value, list):
        return [alias_argument(v, where) for v in value]
    return [alias_argument(value, where)]


class SpineExpansion(NamedTuple):
    """The animation and skin names represented by an alias or attribute."""
    animations: Tuple[str, ...] = ()
    skins: Tuple[str, ...] = ()

    def of(self, kind: SpineModelAliasKind) -> Tuple[str, ...]:
        return self.animations if kind == "animation" else self.skins


def typed_expansion(kind: SpineModelAliasKind, name: str) -> SpineExpansion:
    return SpineExpansion((name,), ()) if kind == "animation" else SpineExpansion((), (name,))


def join_expansions(expansions: Iterable[SpineExpansion]) -> SpineExpansion:
    """Combine resolved names while preserving their order."""
    parts = list(expansions)
    return SpineExpansion(tuple(n for e in parts for n in e.animations), tuple(n for e in parts for n in e.skins))


def resolve_zoom(zoom: Optional[float], zoomX: Optional[float], zoomY: Optional[float]) -> Tuple[float, float, float]:
    """Resolve the character’s scale. Negative values mirror an axis; zero is invalid."""
    z = 1.0 if zoom is None else float(zoom)
    zx = z if zoomX is None else float(zoomX)
    zy = z if zoomY is None else float(zoomY)

    if z == 0.0 or zx == 0.0 or zy == 0.0:
        raise ValueError(
            "Spine: zoom, zoomX and zoomY must be non-zero (got zoom={!r}, zoomX={!r}, zoomY={!r}).".format(
                z, zx, zy))

    return (z, zx, zy)


class SpineDisplayable(renpy.display.displayable.Displayable):  # type: ignore[misc]  # renpy is untyped
    """A Spine character that can be shown in a Ren’Py scene.
    Saves retain its requested appearance; live animation state is rebuilt on load."""

    # Class defaults restore excluded live state when unpickling bypasses __init__.
    nosave = ["common_cache", "_session", "_last_st", "_resolved_aliases"]

    common_cache: Optional[SpineCommon] = None
    _resolved_aliases: Optional[Dict[str, SpineExpansion]] = None
    _session: Optional[SpineSession] = None
    _last_st: Optional[float] = None

    # Saved serial for detecting backward jumps; default supports older saves.
    _rollback_serial: Optional[int] = None

    # One-shot _reset/_mix request, consumed by the sweep.
    _oneshot_mode: Optional[SpineOneshot] = None

    # Default supports saves predating constructor-property preservation.
    properties: Dict[str, Any] = {}

    # Identify displayables without a circular import from spinemotion.
    _is_spine_displayable = True

    _duplicatable = True

    # Bound animation catch-up and physics substeps after stalls.
    MAX_DELTA = 0.064 # Lowkirkenuinely, this problem set can only be decided by the community

    def __init__(self, atlas_path: str, skeleton_path: str, zoom: float = 1.0, zoomX: Optional[float] = None,
                 zoomY: Optional[float] = None, animation: Optional[SpineModelAliasArgument] = None, loop: bool = True,
                 skin: Optional[SpineModelAliasArgument] = None, aliases: Optional[Mapping[str, SpineModelAliasValue]] = None,
                 metadata: SpineMetadataArgument = None, **properties: Any) -> None:
        super(SpineDisplayable, self).__init__(**properties)

        self.properties = properties

        self.atlas_path = atlas_path
        self.skeleton_path = skeleton_path

        self.aliases: Dict[str, SpineModelAliasValue] = dict(aliases) if aliases else {}
        self._resolved_aliases = None

        self.zoom, self.zoomX, self.zoomY = resolve_zoom(zoom, zoomX, zoomY)

        self.common_cache = None
        self.loaded = False

        self._session = None

        # None makes the first frame advance by zero.
        self._last_st = None

        # Preserve show order when layering animations and skins.
        self._target_animation: Optional[str] = None
        self._target_animations: Tuple[str, ...] = ()
        self._target_skins: Tuple[str, ...] = ()
        self._target_loop = loop

        # Parsed now, so a bad policy is a script error. Metadata hooks must be
        # module-level functions to survive saves. A save may hold a raw dict.
        self._metadata: SpineMetadataArgument = spinemotion.parse_metadata(metadata)

        self._oneshot_mode = None
        self._rollback_serial = None

        self.name: Optional[Tuple[str, ...]] = None

        self.width: float = 512 * abs(self.zoomX)
        self.height: float = 512 * abs(self.zoomY)

        # Carry initial values through shows that omit animation or skin.
        self._initial_animation = animation
        self._initial_animation_loop = loop
        self._initial_skin = skin

        runtime.init()
        spine_log("Spine: Initializing with atlas {!r}, skeleton {!r}, zoom {}".format(atlas_path, skeleton_path, zoom))

        self._ensure_common()

        # Before the data loads this checks the alias shapes only.
        self._alias_table()

        self._target_animations = self._argument_names(animation, "animation") if animation else ()
        self._target_animation = self._target_animations[-1] if self._target_animations else None
        self._target_skins = self._argument_names(skin, "skin") if skin else ()

    def create_common(self) -> SpineCommon:
        """Get shared resources for this character’s files."""
        self.common_cache = runtime.common_for(self.atlas_path, self.skeleton_path)
        return self.common_cache

    @property
    def common(self) -> SpineCommon:
        """Return this character’s shared resources, creating them if needed."""
        if self.common_cache is not None:
            return self.common_cache
        return self.create_common()

    def _common_or_none(self) -> Optional[SpineCommon]:
        """Return loaded shared data when available. Avoid creating it during prediction."""
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

    def _ensure_common(self) -> None:
        """Load character data, check aliases, and determine its display size."""
        if not spinemodel:
            spine_log("Spine: spinemodel not available", debug=False)
            return

        common = self._common_or_none()
        if common is None:
            self.loaded = False
            return

        self.common_cache = common

        # The sweep supplies measured bounds for exports without editor bounds.
        size = self._size_from_data(common)
        if size:
            self.width, self.height = size

        self.loaded = True
        self._resolved_aliases = self._build_alias_table()

    def _size_from_data(self, common: SpineCommon) -> Optional[Tuple[float, float]]:
        """Calculate the scaled display size from exported bounds, or None if absent."""
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

    def _shared_names(self) -> Tuple[List[str], List[str]]:
        """Return available animation and skin names, or empty lists if data is unavailable."""
        common = self._common_or_none()
        if common is None:
            return ([], [])
        return (common.spine_data.get_animation_names(), common.spine_data.get_skin_names())

    def _classify(self, name: str) -> SpineExpansion:
        """Identify whether a name refers to an animation, a skin, or both."""
        if not self.loaded:
            return SpineExpansion((name,), (name,))
        animations, skins = self._shared_names()
        return SpineExpansion((name,) if name in animations else (), (name,) if name in skins else ())

    def _ambiguous(self, name: str) -> str:
        """The message for a bare name that is both an animation and a skin."""
        return (
            "{0!r} is both an animation and a skin of {1}; write (\"animation\", {0!r}) or "
            "(\"skin\", {0!r}) in an alias, e.g. aliases={{\"{0}_skin\": (\"skin\", {0!r})}}.".format(
                name, self.skeleton_path))

    def _bare_expansion(self, name: str, context: str) -> SpineExpansion:
        """Resolve a name, rejecting ambiguity between animations and skins."""
        expansion = self._classify(name)
        if self.loaded and expansion.animations and expansion.skins:
            raise Exception("{}: {}".format(context, self._ambiguous(name)))
        return expansion

    def _alias_expansion(self, alias: str, value: object) -> SpineExpansion:
        """Resolve an alias and check its names against loaded character data."""
        context = "Spine alias {!r}".format(alias)
        parts = []
        for arg in alias_arguments(value, "alias {!r}".format(alias)):
            if isinstance(arg, tuple):
                kind, name = arg
                if self.loaded and not self._classify(name).of(kind):
                    raise Exception("{}: {!r} is not a known {} of {}.".format(context, name, kind, self.skeleton_path))
                parts.append(typed_expansion(kind, name))
                continue
            expansion = self._bare_expansion(arg, context)
            if self.loaded and not (expansion.animations or expansion.skins):
                raise Exception("{}: {!r} is not a known animation or skin of {}.".format(context, arg, self.skeleton_path))
            parts.append(expansion)
        return join_expansions(parts)

    def _build_alias_table(self) -> Dict[str, SpineExpansion]:
        """Resolve aliases, rejecting invalid names and conflicts with real names."""
        table: Dict[str, SpineExpansion] = {}
        for k, v in self.aliases.items():
            if not isinstance(k, str):
                raise TypeError("Spine: alias names must be strings, got {!r}".format(k))
            shadowed = self._classify(k)
            if self.loaded and (shadowed.animations or shadowed.skins):
                raise Exception("Spine alias {!r} is already an animation or skin of {}.".format(k, self.skeleton_path))
            table[k] = self._alias_expansion(k, v)
        return table

    def _alias_table(self) -> Dict[str, SpineExpansion]:
        """Return resolved aliases, rebuilding them if needed."""
        if self._resolved_aliases is None:
            self._resolved_aliases = self._build_alias_table()
        return self._resolved_aliases

    def _attribute_expansion(self, attr: str) -> SpineExpansion:
        """Resolve a show attribute to animation and skin names."""
        table = self._alias_table()
        return table[attr] if attr in table else self._bare_expansion(attr, "Spine")

    def _argument_expansion(self, arg: SpineModelAliasArgument, kind: SpineModelAliasKind) -> SpineExpansion:
        """Resolve an argument using the animation or skin context of its caller."""
        if isinstance(arg, tuple):
            return typed_expansion(*arg)
        table = self._alias_table()
        return table[arg] if arg in table else typed_expansion(kind, arg)

    def _argument_names(self, value: object, kind: SpineModelAliasKind) -> Tuple[str, ...]:
        """Expand names and aliases into the requested animation or skin names."""
        args = [alias_argument(v, kind) for v in (value if isinstance(value, list) else [value])]
        wrong = [a for a in args if isinstance(a, tuple) and a[0] != kind]
        if wrong:
            raise ValueError("Spine: {} expects {} names, got {!r}".format(kind, kind, wrong[0]))

        names = join_expansions(self._argument_expansion(a, kind) for a in args).of(kind)
        if not names and self.loaded:
            raise ValueError("Spine: {!r} names no {} of {}".format(value, kind, self.skeleton_path))
        return names

    def set_animation(self, animation_name: Optional[SpineModelAliasArgument], loop: bool = True, track: int = 0) -> bool:
        """Request an animation for the next scene update. Metadata determines
        its track; the track argument is ignored."""
        self._target_animations = self._argument_names(animation_name, "animation") if animation_name else ()
        self._target_animation = self._target_animations[-1] if self._target_animations else None
        self._target_loop = loop
        spinemotion.registry.mark_showing()  # ensure the sweep runs and applies it
        return True

    def get_animation_names(self) -> List[str]:
        """Get list of available animations (from shared data)."""
        return self._shared_names()[0]

    def set_skin(self, skin_name: Union[SpineModelAliasArgument, List[SpineModelAliasArgument], None]) -> bool:
        """Request skins for the next scene update. Accept names or aliases;
        None restores the default skin."""
        if skin_name is None:
            self._target_skins = ()
        else:
            self._target_skins = self._argument_names(skin_name, "skin")
        spinemotion.registry.mark_showing()
        return True

    def get_skin_names(self) -> List[str]:
        """Get list of available skins (from shared data)."""
        return self._shared_names()[1]

    def get_current_skin_name(self) -> Optional[str]:
        """Get the name of the currently applied skin from the bound session."""
        session = self._session
        if session is not None and session.model is not None:
            return session.model.get_current_skin_name()
        return None

    def _page_texture(self, page_key: str, width: float, height: float, st: float, at: float) -> Any:
        """Return an atlas page’s texture, or None if it is unavailable."""
        common = self._common_or_none()
        if common is None:
            return None

        displayable = common.texture_manager.load_atlas_page(page_key)
        if displayable is None:
            return None

        # UnoptimizedTexture returns a texture; other displayables may return a Render.
        return renpy.display.im.render_for_texture(displayable, width, height, st, at)

    def render(self, width: float, height: float, st: float, at: float) -> Any:
        """Draw the character and advance its animation when this instance controls playback."""
        session = self._session
        model = session.model if session is not None else None

        if session is None or model is None or not model.is_loaded():
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

        # Only the driver schedules frames; idle models wake through invalidation.
        if is_driver and model.needs_next_frame():
            renpy.display.render.redraw(self, 0)

        return render

    def _split_attributes(self, attrs: Sequence[str]) -> Tuple[List[str], List[str]]:
        """Separate show attributes into animations and skins while preserving order."""
        if not self.loaded:
            return ([], [])
        expansions = [(a, self._attribute_expansion(a)) for a in attrs]
        return ([a for a, e in expansions if e.animations], [a for a, e in expansions if e.skins])

    def _joined(self, attrs: Sequence[str]) -> SpineExpansion:
        return join_expansions(self._attribute_expansion(a) for a in attrs)

    def _duplicate(self, args: Any) -> SpineDisplayable:
        """Create the shown instance with its chosen attributes and constructor settings."""
        if not self._duplicatable:
            return self

        if not args:
            return self

        oneshot, attrs = self._extract_pseudo_attributes(args.args)

        # Prediction may lack data; carry initial values until names can be resolved.
        animation_attributes, skin_attributes = self._split_attributes(attrs)

        if self.loaded:
            for attr in attrs:
                if attr not in animation_attributes and attr not in skin_attributes:
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

        # Preserve initial values when the show supplies no replacement.
        if animation_attributes:
            rv._target_animations = self._joined(animation_attributes).animations
            rv._target_animation = rv._target_animations[-1]

        if skin_attributes:
            rv._target_skins = self._joined(skin_attributes).skins

        rv._oneshot_mode = oneshot

        spinemotion.registry.mark_showing()

        return rv

    @staticmethod
    def _extract_pseudo_attributes(attributes: Sequence[str]) -> Tuple[Optional[SpineOneshot], List[str]]:
        """Separate transition requests from appearance attributes. _mix takes precedence."""
        oneshot: Optional[SpineOneshot] = "mix" if "_mix" in attributes else "reset" if "_reset" in attributes else None
        return (oneshot, [a for a in attributes if a not in ("_reset", "_mix")])

    def _list_attributes(self, tag: str, attributes: Sequence[str]) -> List[str]:
        """List the animation, skin, and alias names accepted by this image."""
        if not self.loaded:
            return []

        animations, skins = self._shared_names()
        table = self._alias_table()
        return list(dict.fromkeys(
            animations + [k for k, e in table.items() if e.animations]
            + skins + [k for k, e in table.items() if e.skins]))

    def _choose_attributes(self, tag: str, attributes: Sequence[str], optional: Optional[Sequence[str]]) -> Tuple[str, ...]:
        """Choose attributes for a show, keeping the current animations or skins
        when that category has no replacement."""
        if not self.loaded:
            return tuple()

        pseudo = [a for a in attributes if a in ("_reset", "_mix")]
        attrs = [a for a in attributes if a not in ("_reset", "_mix")]
        opt = [a for a in (optional or ()) if a not in ("_reset", "_mix")]

        req_animations, req_skins = self._split_attributes(attrs)
        opt_animations, opt_skins = self._split_attributes(opt)

        animation_attributes = req_animations if req_animations else opt_animations
        skin_attributes = req_skins if req_skins else opt_skins

        spinemotion.registry.mark_showing()

        # A mixed alias is in both categories but is one attribute.
        return tuple(dict.fromkeys(pseudo + animation_attributes + skin_attributes))

    def visit(self) -> List[Any]:
        """Expose atlas textures so Ren’Py can load them before drawing."""

        common = self.common_cache

        if common is None:
            # Prediction instances borrow the base displayable's loaded textures.
            common = runtime.common_if_cached(self.atlas_path, self.skeleton_path)

        if common is not None:
            return list(common.textures)

        return []

    def per_interact(self) -> None:
        """Request a scene update, including after rollback restores this displayable."""
        spinemotion.registry.mark_showing()

    def after_setstate(self) -> None:
        """Clear live resources after a load or rollback so they can be rebuilt safely."""
        for stale in ("_rendered_texture_cache", "texture_manager", "spine_model"):
            self.__dict__.pop(stale, None)

        self.common_cache = None
        self._resolved_aliases = None
        self._session = None
        self._last_st = None


def Spine(
    atlas_path: str,
    skeleton_path: str,
    zoom: float = 1.0,
    zoomX: Optional[float] = None,
    zoomY: Optional[float] = None,
    animation: Optional[SpineModelAliasArgument] = None,
    skin: Optional[SpineModelAliasArgument] = None,
    loop: bool = True,
    aliases: Optional[Mapping[str, SpineModelAliasValue]] = None,
    metadata: SpineMetadataArgument = None,
    **kwargs: Any
) -> SpineDisplayable:
    """
    Create a Spine model displayable.
    This is the main function used to create Spine animations in Ren'Py scripts.
    Args:
        atlas_path: Path to the .atlas file
        skeleton_path: Path to the .json or .skel file
        zoom, zoomX, zoomY: Skeleton scale. zoomX/zoomY default to zoom; a
            negative value mirrors that axis; zero is rejected.
        animation: Initial animation to play (optional). A name, or
            ("animation", name) for a name a skin shares.
        loop: Whether the initial animation should loop (default True)
        skin: Initial skin to apply (optional). A name, or ("skin", name).
        aliases: A dict mapping user-facing alias names to real animation or skin
            names, e.g. {"happy": "smile_big", "casual": "outfit_01"} (optional).
            A value is a SpineModelAliasArgument - a bare name, or an
            ("animation" | "skin", name) tuple for a name that is both - or a
            list of them composed in show order, e.g.
            {"default_skin": ("skin", "default"), "angry": ["frown", "brow_angry"]}.
        metadata: Per-character transition policy (optional). A static dict
            controlling how attribute changes transition, e.g.
            {"default_transition": "mix", "mix_time": 0.2,
             "transitions": {("idle", "talk"): {"mode": "mix", "time": 0.12}},
             "skin_transition": "setup",
             "tracks": {"wave": {"track": 1, "alpha": 0.8}}}.
            The dict is parsed when the image is defined, so an unknown key or
            a bad value is a script error; a spinetypes.SpinePolicy may be
            given instead. Omit for hard-cut behaviour (default_transition =
            "reset"). A callable hook returning a dict, a SpinePolicy, or None
            is resolved at each transition.
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
