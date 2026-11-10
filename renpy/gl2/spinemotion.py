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

# Persistent motion sessions and pure target planning.
# Records and policy types live in spinetypes.
# Import direction: spine -> spinemotion -> spinetypes; spinemotion -> spinemodel.


from __future__ import division, absolute_import, with_statement, print_function, unicode_literals, annotations

import os
import inspect
from typing import (Any, Callable, Dict, Iterable, List, Literal, Mapping, NamedTuple, Optional, Protocol,
                    Sequence, Tuple, TypeAlias, Union)

import renpy
from renpy.gl2.spinetypes import (DEFAULT_MIX_TIME, DEFAULT_POLICY, EMPTY_APPLIED, FadeOp, MetadataInputValidator,
                                  SpinePartialApplyError, MixOp, OverlayOp, ResetOp, SkinOp, SpineApplied, SpineAssetSpec,
                                  SpineDisplayableLike, SpineHookContext, SpineMetadata, SpineMetadataArgument,
                                  SpineModelLike, SpineModelSpec, SpineOneshot, SpineOp, SpinePolicy, SpinePolicyError,
                                  SpineRequest, SpineSlotPolicy, SpineTarget, SpineTrack, SpineTrackSpec,
                                  SpineTransition, SpineTransitionPlan, UpdateOp, playback_key, track_animation)

try:
    import renpy.gl2.spinemodel as spinemodel
except ImportError:
    spinemodel = None


# Shared by the Python and Cython Spine modules.
SPINE_DEBUG = os.environ.get("SPINE_DEBUG", "0") == "1"


def spine_log(message: object, *args: object, debug: bool = True) -> None:
    """Write a Spine diagnostic. Use debug=False for warnings and errors."""
    if debug and not SPINE_DEBUG:
        return

    message = " ".join(str(part) for part in (message,) + args)
    renpy.log.open("spine", flush=True).write("%s", message)


# Largest value the sweep epoch may reach before it is rebased to 0.
_EPOCH_MAX = 0x7FFFFFFF


# Validate policies before they can change a live character.


_read = MetadataInputValidator


def _parse_transition(rule: object, mix_time: float, where: str) -> SpineTransition:
    """Validate a transition rule and fill in its default blend duration."""
    if isinstance(rule, str):
        return SpineTransition(_read.mode(rule, where), mix_time)
    fields = _read.mapping(rule, where, ("mode", "time", "mix_time"))
    time = fields.get("time", fields.get("mix_time"))
    return SpineTransition(
        _read.mode(fields.get("mode", "reset"), where + ".mode"),
        mix_time if time is None else _read.number(time, where + ".time"),
    )


def _parse_track(config: object, mix_time: float, where: str) -> SpineTrack:
    fields = _read.mapping(config, where, ("track", "alpha", "additive", "loop", "mix_time"))
    loop = fields.get("loop")
    return SpineTrack(
        track=_read.track_index(fields.get("track", 0), where + ".track"),
        alpha=_read.number(fields.get("alpha", 1.0), where + ".alpha", high=1.0),
        additive=_read.boolean(fields.get("additive", False), where + ".additive"),
        loop=None if loop is None else _read.boolean(loop, where + ".loop"),
        mix_time=_read.number(fields.get("mix_time", mix_time), where + ".mix_time"),
    )


_POLICY_KEYS = ("default_transition", "mix_time", "transitions", "skin_transition", "skin_transitions", "tracks")


def parse_policy(raw: Mapping[object, object]) -> SpinePolicy:
    """Validate metadata and turn it into animation and skin rules.
    Raise SpinePolicyError for invalid fields."""
    fields = _read.mapping(raw, "metadata", _POLICY_KEYS)
    mix_time = _read.number(fields.get("mix_time", DEFAULT_MIX_TIME), "mix_time")

    pairs: Dict[Tuple[str, str], SpineTransition] = {}
    targets: Dict[str, SpineTransition] = {}
    for key, rule in _read.mapping(fields.get("transitions"), "transitions").items():
        where = "transitions[{!r}]".format(key)
        if isinstance(key, str):
            targets[key] = _parse_transition(rule, mix_time, where)
            continue
        names = _read.names(key, where)
        if len(names) != 2:
            raise SpinePolicyError("Spine: {} must be a name or a (from, to) pair".format(where))
        pairs[(names[0], names[1])] = _parse_transition(rule, mix_time, where)

    skin_sets: Dict[Tuple[str, ...], SpineSlotPolicy] = {}
    skin_names: Dict[str, SpineSlotPolicy] = {}
    for key, rule in _read.mapping(fields.get("skin_transitions"), "skin_transitions").items():
        where = "skin_transitions[{!r}]".format(key)
        if isinstance(key, str):
            skin_names[key] = _read.slot_policy(rule, where)
        else:
            skin_sets[_read.names(key, where)] = _read.slot_policy(rule, where)

    tracks: Dict[str, SpineTrack] = {}
    for key, config in _read.mapping(fields.get("tracks"), "tracks").items():
        where = "tracks[{!r}]".format(key)
        if not isinstance(key, str):
            raise SpinePolicyError("Spine: {} must be keyed by an animation name".format(where))
        tracks[key] = _parse_track(config, mix_time, where)

    return SpinePolicy(
        default=_parse_transition(fields.get("default_transition", "reset"), mix_time, "default_transition"),
        mix_time=mix_time,
        pairs=pairs,
        targets=targets,
        skin_default=_read.slot_policy(fields.get("skin_transition", "setup"), "skin_transition"),
        skin_sets=skin_sets,
        skin_names=skin_names,
        tracks=tracks,
    )


def coerce_policy(value: object, where: str) -> SpinePolicy:
    """Validate a policy or metadata dictionary, using defaults for None."""
    if value is None:
        return DEFAULT_POLICY
    if isinstance(value, SpinePolicy):
        # Route typed policies through the same validation as dictionary inputs.
        def transition_fields(rule: SpineTransition) -> Mapping[str, object]:
            return {"mode": rule.mode, "mix_time": rule.mix_time}
        transitions: Dict[object, object] = {k: transition_fields(v) for k, v in value.pairs.items()}
        transitions.update({k: transition_fields(v) for k, v in value.targets.items()})
        skins: Dict[object, object] = {k: v for k, v in value.skin_sets.items()}
        skins.update(value.skin_names)
        return parse_policy({
            "default_transition": transition_fields(value.default),
            "mix_time": value.mix_time,
            "transitions": transitions,
            "skin_transition": value.skin_default,
            "skin_transitions": skins,
            "tracks": {k: v._asdict() for k, v in value.tracks.items()},
        })
    if isinstance(value, Mapping):
        return parse_policy(value)
    raise SpinePolicyError("Spine: {} must be a dict, a SpinePolicy, or None, got {!r}".format(where, value))


def parse_metadata(metadata: SpineMetadataArgument) -> SpineMetadata:
    """Validate a fixed policy or keep a callback for later evaluation."""
    if callable(metadata):
        return metadata
    return coerce_policy(metadata, "metadata")



def _invoke_hook(hook: Callable[..., object], ctx: SpineHookContext) -> object:
    """Call a policy callback, passing transition details if it accepts them."""
    try:
        params = inspect.signature(hook).parameters
        positional = [
            p for p in params.values()
            if p.kind in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)
            and p.default is inspect.Parameter.empty
        ]
        takes_arg = len(positional) >= 1
    except (ValueError, TypeError):
        takes_arg = True

    return hook(ctx) if takes_arg else hook()


def resolve_policy(metadata: SpineMetadataArgument, ctx: SpineHookContext) -> SpinePolicy:
    """Choose the policy for this transition. Callbacks see the current game
    state; a callback that raises falls back to the default policy."""
    if not callable(metadata):
        return coerce_policy(metadata, "metadata")

    try:
        result = _invoke_hook(metadata, ctx)
    except Exception as e:
        spine_log("Spine: metadata hook for {!r} raised {}: {}; using reset".format(ctx.tag, type(e).__name__, e), debug=False)
        return DEFAULT_POLICY

    return coerce_policy(result, "metadata hook for {!r}".format(ctx.tag))


def validate_names(anim_names: Iterable[str], skins: Iterable[str],
                   known_animations: Iterable[str], known_skins: Iterable[str]) -> List[str]:
    """Return a list of error strings for names that the skeleton does not
    define. Empty when everything is known."""
    animation_set = set(known_animations)
    skin_set = set(known_skins)
    return (["unknown animation {!r}".format(n) for n in anim_names if n not in animation_set]
            + ["unknown skin {!r}".format(n) for n in skins if n not in skin_set])


def normalize_target(policy: SpinePolicy, request: SpineRequest) -> SpineTarget:
    """Assign requested animations to tracks using the policy.
    When several animations share a track, the last request wins."""
    configs = [(name, policy.track(name)) for name in request.animations]
    by_track = {
        cfg.track: SpineTrackSpec(name, request.loop if cfg.loop is None else cfg.loop, cfg.alpha, cfg.additive, cfg.mix_time)
        for name, cfg in configs
    }
    return SpineTarget(request.skins, tuple(sorted(by_track.items(), key=lambda t: t[0])))


def _track_op(index: int, spec: SpineTrackSpec, current: Optional[SpineTrackSpec], policy: SpinePolicy,
              oneshot: Optional[SpineOneshot], force_reset: bool) -> Optional[SpineOp]:
    """Choose how to change a track, or return None if it already matches."""
    restart = force_reset or oneshot == "reset"

    if current is not None and not restart:
        if playback_key(current) == playback_key(spec):
            return None
        if current.animation == spec.animation:
            return UpdateOp(index, spec)

    if index != 0:
        return OverlayOp(index, spec, 0.0 if force_reset else spec.mix_time)

    # Nothing to blend from on a first show or an empty track.
    if current is None or restart:
        return ResetOp(0, spec)

    rule = policy.transition(current.animation, spec.animation)
    if oneshot == "mix" or rule.mode == "mix":
        return MixOp(0, spec, rule.mix_time)
    return ResetOp(0, spec)


def plan_transition(applied: SpineApplied, target: SpineTarget, policy: SpinePolicy,
                    oneshot: Optional[SpineOneshot] = None, force_reset: bool = False) -> Optional[SpineTransitionPlan]:
    """Plan the changes needed to reach the requested appearance.
    Return None when nothing needs to change."""
    applied_tracks = dict(applied.tracks)
    target_tracks = dict(target.tracks)

    skin_ops: List[SpineOp] = (
        [SkinOp(target.skins, policy.slot_policy(target.skins) == "setup")]
        if target.skins != applied.skins else [])

    fade_time = 0.0 if force_reset else policy.mix_time
    fade_ops: List[SpineOp] = [FadeOp(index, fade_time) for index in sorted(applied_tracks) if index not in target_tracks]

    track_ops = [_track_op(index, spec, applied_tracks.get(index), policy, oneshot, force_reset)
                 for index, spec in target.tracks]

    ops = tuple(skin_ops + fade_ops + [op for op in track_ops if op is not None])
    if not ops:
        return None

    if force_reset:
        reason = "rollback"
    elif oneshot == "reset":
        reason = "reset"
    else:
        reason = "target"

    return SpineTransitionPlan(ops, reason)


def execute_plan(model: SpineModelLike, applied: SpineApplied,
                 plan: SpineTransitionPlan) -> Tuple[SpineApplied, Tuple[SpineOp, ...]]:
    """Apply a transition and return the updated state and failed operations.
    An incomplete reset or mix raises SpinePartialApplyError and stops the plan."""
    failed: List[SpineOp] = []
    for op in plan.ops:
        result = op.apply(model, applied)
        if result is None:
            failed.append(op)
        else:
            applied = result
    return (applied, tuple(failed))


# (layer, tag, ordinal) - see SpineRegistry.
SpineSessionKey: TypeAlias = Tuple[str, str, int]


class SpineSession(object):
    """Keep a character’s animation running when its displayable is replaced."""

    def __init__(self, key: SpineSessionKey) -> None:
        self.key = key

        self.model: Optional[SpineModelLike] = None

        self.spec: Optional[SpineModelSpec] = None

        # Record successes only, so failed operations remain retryable.
        self.applied: SpineApplied = EMPTY_APPLIED

        # Last fully applied request; avoid reevaluating hooks on unchanged sweeps.
        self._last_request: Optional[SpineRequest] = None

        self._last_report: Optional[str] = None

        self.last_seen_epoch = -1

        # Live serial does not rewind; compare it with the saved displayable serial.
        self.last_serial = -1

        self._force_reset = False

        self.driver: Optional[SpineDisplayableLike] = None

        self.pending_invalidation: Optional[str] = None

    def dispose(self) -> None:
        """Release the character’s live model."""
        if self.model is not None:
            try:
                self.model.dispose()
            except Exception as e:
                spine_log("Spine: error disposing session model:", e)
            self.model = None
        self.driver = None
        self.pending_invalidation = None

    def is_driver(self, d: object) -> bool:
        return self.driver is d

    def invalidate(self, reason: str) -> None:
        """Request a fresh frame after the character changes."""
        self.pending_invalidation = reason
        d = self.driver
        if d is not None:
            renpy.display.render.redraw(d, 0)

    def take_invalidation(self) -> Optional[str]:
        """Consume and return the pending invalidation reason, or None."""
        reason = self.pending_invalidation
        self.pending_invalidation = None
        return reason

    def report_once(self, message: str) -> None:
        if message != self._last_report:
            spine_log(message, debug=False)
            self._last_report = message

    def ensure_model(self, d: SpineDisplayableLike) -> bool:
        """Create the character’s model if needed. Return whether it is ready."""
        if self.model is not None and self.model.is_loaded():
            return True

        if spinemodel is None:
            return False

        common = d.common
        if common is None:
            return False

        if not common.load_data():
            return False

        spec = model_spec_of(d)
        model: SpineModelLike = spinemodel.SpineModel(scale=d.zoom, scaleX=spec.zoom_x, scaleY=spec.zoom_y)
        status = model.load_from_data(common.spine_data, common.texture_manager)
        if status != 0:
            self.report_once("Spine: could not build a model for {}: {}".format(
                d.skeleton_path, model.last_error))
            return False

        self.model = model
        self.spec = spec
        self.applied = EMPTY_APPLIED
        self._last_request = None

        # Keep the data-level default mix at zero so resets remain hard cuts.

        self.invalidate("model")
        return True

    def apply_target(self, d: SpineDisplayableLike) -> None:
        """Apply the requested animations and skins. Invalid requests leave the
        model unchanged. An incomplete reset or mix discards the model and raises;
        other failed operations remain pending for a later attempt."""
        model = self.model
        if model is None:
            return

        force_reset, self._force_reset = self._force_reset, False
        oneshot, d._oneshot_mode = d._oneshot_mode, None

        request = SpineRequest(d._target_animations, d._target_loop, d._target_skins)

        # Unchanged requests still honor reset; mix alone has nothing to blend to.
        if request == self._last_request and not force_reset and oneshot != "reset":
            return

        current_base = track_animation(self.applied, 0)
        ctx = SpineHookContext(
            tag=self.key[1],
            layer=self.key[0],
            current_animation=current_base,
            current_skin=self.applied.skins,
            target_animation=(request.animations[-1] if request.animations else None),
            target_skin=request.skins,
            first_show=(current_base is None),
        )

        # Validate before native mutation to avoid partially applying invalid requests.
        errors = validate_names(request.animations, request.skins, model.get_animation_names(), model.get_skin_names())
        try:
            policy = resolve_policy(d._metadata, ctx)
        except SpinePolicyError as e:
            errors.append(str(e))

        if errors:
            self.report_once("Spine: cannot show {!r}: {}".format(self.key[1], "; ".join(errors)))
            self._last_request = request  # nothing will change until a new request
            return

        plan = plan_transition(self.applied, normalize_target(policy, request), policy, oneshot, force_reset)
        if plan is None:
            self._last_request = request
            return

        try:
            self.applied, failed = execute_plan(model, self.applied, plan)
        except SpinePartialApplyError:
            self.dispose()
            self.applied = EMPTY_APPLIED
            self._last_request = None
            raise
        if failed:
            self.report_once("Spine: transition for {!r} partially applied; failed: {}".format(
                self.key[1], ", ".join(op.describe() for op in failed)))
            self._last_request = None
        else:
            self._last_report = None
            self._last_request = request

        self.invalidate(plan.reason)


def _rollback_serial() -> int:
    """Return the live rollback counter, used to detect a restored scene."""
    try:
        serial: int = renpy.rollback.serial
        return serial
    except Exception:
        return 0


def model_spec_of(d: SpineDisplayableLike) -> SpineModelSpec:
    """Return the settings that determine whether a model must be rebuilt."""
    return SpineModelSpec(
        SpineAssetSpec(d.atlas_path, d.skeleton_path),
        d.zoomX,
        d.zoomY,
    )


class SpineRegistry(object):
    """Keep live animation sessions for the Spine characters in the scene."""

    def __init__(self) -> None:
        self.sessions: Dict[SpineSessionKey, SpineSession] = {}

        # Retired sessions survive one more interaction for retained displayables.
        self.retired: List[SpineSession] = []

        self.epoch = 0

        self.showing = False

    def mark_showing(self) -> None:
        """Request a scene update when a Spine image is shown."""
        self.showing = True

    def retire(self, session: SpineSession) -> None:
        """Remove a session from the scene, keeping it alive for outgoing transitions."""
        self.sessions.pop(session.key, None)
        self.retired.append(session)

    def dispose_retired(self) -> None:
        """Release sessions retained for the previous interaction’s transitions."""
        for s in self.retired:
            s.dispose()
        del self.retired[:]

    def rebase_epochs(self) -> None:
        """Restart the scene counter before it grows too large."""
        for s in self.sessions.values():
            s.last_seen_epoch = 0
        self.epoch = 0

    def reset(self) -> None:
        """Release all live models when the game or scene is reset."""
        for s in list(self.sessions.values()):
            s.dispose()
        self.sessions.clear()
        self.dispose_retired()
        self.showing = False

    def sweep(self) -> None:
        """Update visible characters and retire those that left the scene.
        Skip prediction, which does not represent the live scene."""
        if spinemodel is None:
            return

        if renpy.display.predict.predicting:
            return

        if not self.showing and not self.sessions and not self.retired:
            return
        self.showing = False

        self.dispose_retired()

        if self.epoch >= _EPOCH_MAX:
            self.rebase_epochs()
        self.epoch += 1
        epoch = self.epoch

        serial = _rollback_serial()

        # Separate multiple Spine children under one tag by traversal ordinal.
        ordinals: Dict[Tuple[str, str], int] = {}

        sls = renpy.display.scenelists.scene_lists()

        for layer, tag, d in sls.get_all_layer_tag_displayable():
            if tag is None:
                continue
            # Retained transition copies keep their previous session and never drive it.
            if "$" in tag:
                continue
            if d is None:
                continue

            def visit(child: Any, layer: str = layer, tag: str = tag) -> None:
                if getattr(child, "_is_spine_displayable", False):
                    self._bind(child, layer, tag, epoch, serial, ordinals)

            d.visit_all(visit)

        for key in list(self.sessions.keys()):
            s = self.sessions[key]
            if s.last_seen_epoch != epoch:
                self.retire(s)

    def _bind(self, d: SpineDisplayableLike, layer: str, tag: str, epoch: int, serial: int,
              ordinals: Dict[Tuple[str, str], int]) -> None:
        """Connect a visible character to its session and apply its requested state."""
        base = (layer, tag)
        ordinal = ordinals.get(base, 0)
        ordinals[base] = ordinal + 1
        key = (layer, tag, ordinal)

        session = self.sessions.get(key)
        spec = model_spec_of(d)

        if session is None:
            session = SpineSession(key)
            self.sessions[key] = session
        elif session.spec is not None and session.spec != spec:
            # Retain the old session for transitions while rebuilding with the new spec.
            self.retire(session)
            session = SpineSession(key)
            self.sessions[key] = session
        else:
            # An older displayable serial indicates rollback relative to the live session.
            d_serial = d._rollback_serial
            if d_serial is not None and d_serial < session.last_serial:
                session._force_reset = True

        # Bind before applying so invalidation has a driver and failed loads remain retryable.
        session.driver = d
        session.last_seen_epoch = epoch
        d._session = session

        d._rollback_serial = serial
        session.last_serial = serial

        if not session.ensure_model(d):
            return

        session.apply_target(d)

        model = session.model
        size = model.get_size() if model is not None else None
        if size:
            d.width, d.height = size


registry = SpineRegistry()


def update_states() -> None:
    registry.sweep()


def reset() -> None:
    """Clear live animation state after a script reload."""
    registry.reset()


def reset_states() -> None:
    """Clear live animation state after a restart or load so the new scene can rebuild it."""
    registry.reset()
