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

# Immutable records, policy types, native structural types, and metadata input validation.
# Import direction: spine -> spinemotion -> spinetypes. Nothing here imports renpy.


from __future__ import division, absolute_import, with_statement, print_function, unicode_literals, annotations

from typing import (TYPE_CHECKING, Any, Callable, List, Literal, Mapping, NamedTuple, Optional, Protocol, Sequence,
                    Tuple, TypeAlias, Union)

if TYPE_CHECKING:
    from renpy.gl2.spinemotion import SpineSession

from dataclasses import dataclass, field
from types import MappingProxyType


# Module-level records preserve stable pickle identities.

class SpineAssetSpec(NamedTuple):
    """The atlas and skeleton files used by a character."""
    atlas_path: str
    skeleton_path: str


class SpineModelSpec(NamedTuple):
    """The files and scale needed to create a character model."""
    assets: SpineAssetSpec
    zoom_x: float
    zoom_y: float


class SpineTrackSpec(NamedTuple):
    """Playback and transition settings for one animation track."""
    animation: str
    loop: bool
    alpha: float
    additive: bool
    mix_time: float


SpineTracks: TypeAlias = Tuple[Tuple[int, SpineTrackSpec], ...]


class SpineTarget(NamedTuple):
    """The requested skins and animations, with tracks in index order."""
    skins: Tuple[str, ...]
    tracks: SpineTracks


class SpineApplied(NamedTuple):
    """The skins and animations successfully applied to the model."""
    skins: Tuple[str, ...]
    tracks: SpineTracks

    def with_skins(self, skins: Tuple[str, ...]) -> SpineApplied:
        return self._replace(skins=skins)

    def with_track(self, track: int, spec: SpineTrackSpec) -> SpineApplied:
        return self._replace(tracks=tuple(sorted({**dict(self.tracks), track: spec}.items(), key=lambda t: t[0])))

    def without_track(self, track: int) -> SpineApplied:
        return self._replace(tracks=tuple(t for t in self.tracks if t[0] != track))


class SpineRequest(NamedTuple):
    """The animations and skins requested by a displayable."""
    animations: Tuple[str, ...]
    loop: bool
    skins: Tuple[str, ...]


# A per-show one-shot: ``_reset`` or ``_mix``.
SpineOneshot: TypeAlias = Literal["reset", "mix"]

EMPTY_APPLIED = SpineApplied((), ())


def playback_key(spec: SpineTrackSpec) -> Tuple[str, bool, float, bool]:
    """Return the settings that affect current playback. Changing the next
    blend duration alone should not restart an animation."""
    return (spec.animation, spec.loop, spec.alpha, spec.additive)


def track_animation(state: Union[SpineTarget, SpineApplied], track: int) -> Optional[str]:
    """Animation name on `track` in a SpineTarget/SpineApplied, or None."""
    return next((spec.animation for index, spec in state.tracks if index == track), None)


# Default pose-blend duration when a mix rule names none.
DEFAULT_MIX_TIME = 0.2

SpineTransitionMode: TypeAlias = Literal["reset", "mix"]
SpineSlotPolicy: TypeAlias = Literal["setup", "preserve"]


class SpinePolicyError(ValueError):
    """An invalid animation or skin policy."""


class SpineTransition(NamedTuple):
    """How to switch the main animation."""
    mode: SpineTransitionMode = "reset"
    mix_time: float = DEFAULT_MIX_TIME


class SpineTrack(NamedTuple):
    """Playback settings for an animation. An unspecified loop follows the show."""
    track: int = 0
    alpha: float = 1.0
    additive: bool = False
    loop: Optional[bool] = None
    mix_time: float = DEFAULT_MIX_TIME


class SpineHookContext(NamedTuple):
    """The current and requested appearance, provided to a policy callback."""
    tag: str
    layer: str
    current_animation: Optional[str]
    current_skin: Tuple[str, ...]
    target_animation: Optional[str]
    target_skin: Tuple[str, ...]
    first_show: bool


@dataclass(frozen=True)
class SpinePolicy:
    """Rules for changing a character's animations and skins."""
    default: SpineTransition = SpineTransition()
    # Fade-out time for dropped tracks, and track mix time when none is given.
    mix_time: float = DEFAULT_MIX_TIME
    # (from, to) rules; either side may be "*".
    pairs: Mapping[Tuple[str, str], SpineTransition] = field(default_factory=dict)
    targets: Mapping[str, SpineTransition] = field(default_factory=dict)
    skin_default: SpineSlotPolicy = "setup"
    skin_sets: Mapping[Tuple[str, ...], SpineSlotPolicy] = field(default_factory=dict)
    skin_names: Mapping[str, SpineSlotPolicy] = field(default_factory=dict)
    tracks: Mapping[str, SpineTrack] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("pairs", "targets", "skin_sets", "skin_names", "tracks"):
            object.__setattr__(self, name, MappingProxyType(dict(getattr(self, name))))

    def __reduce__(self) -> Tuple[Any, Tuple[Any, ...]]:
        return (type(self), (self.default, self.mix_time, dict(self.pairs), dict(self.targets),
                            self.skin_default, dict(self.skin_sets), dict(self.skin_names), dict(self.tracks)))

    def transition(self, from_anim: str, to_anim: str) -> SpineTransition:
        """Choose the transition rule, preferring specific matches over defaults."""
        keys = ((from_anim, to_anim), ("*", to_anim), (from_anim, "*"))
        rule = next((self.pairs[k] for k in keys if k in self.pairs), None)
        return rule if rule is not None else self.targets.get(to_anim, self.default)

    def slot_policy(self, skins: Tuple[str, ...]) -> SpineSlotPolicy:
        """Choose whether a skin change restores its default attachments."""
        if skins in self.skin_sets:
            return self.skin_sets[skins]
        return next((self.skin_names[n] for n in skins if n in self.skin_names), self.skin_default)

    def track(self, animation: str) -> SpineTrack:
        return self.tracks.get(animation, SpineTrack(mix_time=self.mix_time))


DEFAULT_POLICY = SpinePolicy()

# What a displayable keeps: a parsed policy, or a hook returning one per transition.
SpineMetadata: TypeAlias = Union[SpinePolicy, Callable[..., object]]

# What Spine(metadata=...) accepts; a save may also hold a raw dict or None.
SpineMetadataArgument: TypeAlias = Union[SpineMetadata, Mapping[Any, object], None]


class MetadataInputValidator(object):
    """Validate policy values and report which field is invalid."""

    @staticmethod
    def mapping(value: object, where: str, allowed: Tuple[str, ...] = ()) -> Mapping[object, object]:
        if value is None:
            return {}
        if not isinstance(value, Mapping):
            raise SpinePolicyError("Spine: {} must be a dict, got {!r}".format(where, value))
        unknown = [k for k in value if allowed and k not in allowed]
        if unknown:
            raise SpinePolicyError("Spine: {} has unknown keys {}; expected {}".format(where, unknown, list(allowed)))
        return value

    @staticmethod
    def number(value: object, where: str, low: float = 0.0, high: float = 3.4028234663852886e38) -> float:
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not (low <= value <= high):
            raise SpinePolicyError("Spine: {} must be a number within [{}, {}], got {!r}".format(where, low, high, value))
        return float(value)

    @staticmethod
    def track_index(value: object, where: str) -> int:
        if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= 2147483647:
            raise SpinePolicyError("Spine: {} must be a non-negative integer at most 2147483647, got {!r}".format(where, value))
        return value

    @staticmethod
    def boolean(value: object, where: str) -> bool:
        if not isinstance(value, bool):
            raise SpinePolicyError("Spine: {} must be True or False, got {!r}".format(where, value))
        return value

    @staticmethod
    def names(value: object, where: str) -> Tuple[str, ...]:
        names = tuple(n for n in value if isinstance(n, str)) if isinstance(value, tuple) else ()
        if not isinstance(value, tuple) or len(names) != len(value):
            raise SpinePolicyError("Spine: {} must be a name or a tuple of names, got {!r}".format(where, value))
        return names

    @staticmethod
    def mode(value: object, where: str) -> SpineTransitionMode:
        if value == "reset":
            return "reset"
        if value == "mix":
            return "mix"
        raise SpinePolicyError("Spine: {} must be \"reset\" or \"mix\", got {!r}".format(where, value))

    @staticmethod
    def slot_policy(value: object, where: str) -> SpineSlotPolicy:
        if value == "setup":
            return "setup"
        if value == "preserve":
            return "preserve"
        raise SpinePolicyError("Spine: {} must be \"setup\" or \"preserve\", got {!r}".format(where, value))


# Python interfaces to the native model, for static type checking.

class SpineRunLike(Protocol):
    page_key: str


class SpineTextureManagerLike(Protocol):
    def load_atlas_page(self, path: str) -> Optional[Any]: ...


class SpineDataLike(Protocol):
    @property
    def last_error(self) -> Optional[str]: ...
    def is_loaded(self) -> bool: ...
    def load(self, atlas_path: str, skeleton_path: str) -> int: ...
    def get_page_names(self) -> List[str]: ...
    def get_setup_bounds(self) -> Tuple[float, float, float, float]: ...
    def get_animation_names(self) -> List[str]: ...
    def get_skin_names(self) -> List[str]: ...


class SpineModelLike(Protocol):
    @property
    def last_error(self) -> Optional[str]: ...
    def dispose(self) -> None: ...
    def load_from_data(self, data: SpineDataLike, texture_manager: SpineTextureManagerLike) -> int: ...
    def is_loaded(self) -> bool: ...
    def get_size(self) -> Optional[Tuple[float, float]]: ...
    def get_animation_names(self) -> List[str]: ...
    def get_skin_names(self) -> List[str]: ...
    def get_current_skin_name(self) -> Optional[str]: ...
    def apply_skin_combined(self, names: Sequence[str], setup_slots: bool) -> bool: ...
    def apply_animation_reset(self, track_index: int, animation_name: str, loop: bool) -> bool: ...
    def apply_animation_mix(self, track_index: int, animation_name: str, loop: bool, mix_time: float) -> bool: ...
    def apply_overlay_animation(self, track_index: int, animation_name: str, loop: bool,
                                mix_time: float, alpha: float, additive: bool) -> bool: ...
    def update_track_settings(self, track_index: int, loop: bool, alpha: float, additive: bool) -> bool: ...
    def fade_track(self, track_index: int, mix_out: float) -> bool: ...
    def update_animation(self, delta_time: float) -> None: ...
    def needs_next_frame(self) -> bool: ...
    def render_runs(self) -> List[SpineRunLike]: ...
    def run_render(self, run: SpineRunLike, texture: Any, width: float, height: float) -> Optional[Any]: ...


class SpineCommonLike(Protocol):
    spine_data: SpineDataLike
    texture_manager: SpineTextureManagerLike

    def load_data(self) -> bool: ...


class SpineDisplayableLike(Protocol):
    """The displayable information needed to manage a character's animation."""
    atlas_path: str
    skeleton_path: str
    zoom: float
    zoomX: float
    zoomY: float
    width: float
    height: float
    _session: Optional[SpineSession]
    _rollback_serial: Optional[int]
    _target_animations: Tuple[str, ...]
    _target_loop: bool
    _target_skins: Tuple[str, ...]
    _oneshot_mode: Optional[SpineOneshot]
    _metadata: SpineMetadataArgument

    @property
    def common(self) -> Optional[SpineCommonLike]: ...


class SpinePartialApplyError(RuntimeError):
    """An incomplete animation change that requires discarding the model."""


# Record successful changes only; incomplete reset or mix operations raise.

class SpineOp(Protocol):
    def apply(self, model: SpineModelLike, applied: SpineApplied) -> Optional[SpineApplied]: ...

    def describe(self) -> str: ...


class SkinOp(NamedTuple):
    """Change the character's skins, optionally restoring default attachments."""
    skins: Tuple[str, ...]
    setup_slots: bool

    def apply(self, model: SpineModelLike, applied: SpineApplied) -> Optional[SpineApplied]:
        if not model.apply_skin_combined(self.skins, self.setup_slots):
            return None
        return applied.with_skins(self.skins)

    def describe(self) -> str:
        return "skin {}".format(list(self.skins))


class FadeOp(NamedTuple):
    """Fade out an animation track."""
    track: int
    mix_time: float

    def apply(self, model: SpineModelLike, applied: SpineApplied) -> Optional[SpineApplied]:
        if not model.fade_track(self.track, self.mix_time):
            return None
        return applied.without_track(self.track)

    def describe(self) -> str:
        return "fade track {}".format(self.track)


class ResetOp(NamedTuple):
    """Restart an animation from the setup pose and reset physics."""
    track: int
    spec: SpineTrackSpec

    def apply(self, model: SpineModelLike, applied: SpineApplied) -> Optional[SpineApplied]:
        spec = self.spec
        if not model.apply_animation_reset(self.track, spec.animation, spec.loop):
            return None
        if not model.update_track_settings(self.track, spec.loop, spec.alpha, spec.additive):
            raise SpinePartialApplyError("Spine: {} changed animation but could not apply settings".format(self.describe()))
        return applied.with_track(self.track, spec)

    def describe(self) -> str:
        return "reset track {}".format(self.track)


class MixOp(NamedTuple):
    """Blend into an animation from the current pose."""
    track: int
    spec: SpineTrackSpec
    mix_time: float

    def apply(self, model: SpineModelLike, applied: SpineApplied) -> Optional[SpineApplied]:
        spec = self.spec
        if not model.apply_animation_mix(self.track, spec.animation, spec.loop, self.mix_time):
            return None
        if not model.update_track_settings(self.track, spec.loop, spec.alpha, spec.additive):
            raise SpinePartialApplyError("Spine: {} changed animation but could not apply settings".format(self.describe()))
        return applied.with_track(self.track, spec)

    def describe(self) -> str:
        return "mix track {}".format(self.track)


class OverlayOp(NamedTuple):
    """Layer an animation over the character's other tracks."""
    track: int
    spec: SpineTrackSpec
    mix_time: float

    def apply(self, model: SpineModelLike, applied: SpineApplied) -> Optional[SpineApplied]:
        spec = self.spec
        if not model.apply_overlay_animation(self.track, spec.animation, spec.loop, self.mix_time, spec.alpha, spec.additive):
            return None
        return applied.with_track(self.track, spec)

    def describe(self) -> str:
        return "overlay track {}".format(self.track)


class UpdateOp(NamedTuple):
    """Change playback settings without restarting the animation."""
    track: int
    spec: SpineTrackSpec

    def apply(self, model: SpineModelLike, applied: SpineApplied) -> Optional[SpineApplied]:
        spec = self.spec
        if not model.update_track_settings(self.track, spec.loop, spec.alpha, spec.additive):
            return None
        return applied.with_track(self.track, spec)

    def describe(self) -> str:
        return "update track {}".format(self.track)


class SpineTransitionPlan(NamedTuple):
    """The changes needed to reach a requested appearance."""
    ops: Tuple[SpineOp, ...]
    reason: str
