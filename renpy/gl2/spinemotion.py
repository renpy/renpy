# By Sebulsik <sebulsik.dev@gmail.com>

# Persistent motion sessions and pure target planning.

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals

import os
import inspect
import types
from collections import namedtuple

import renpy

try:
    import renpy.gl2.spinemodel as spinemodel
except ImportError:
    spinemodel = None

SPINE_DEBUG = os.environ.get("SPINE_DEBUG", "0") == "1"


def spine_log(message, *args, debug=True):
    if debug and not SPINE_DEBUG:
        return

    message = " ".join(str(part) for part in (message,) + args)
    renpy.log.open("spine", flush=True).write("%s", message)


_EPOCH_MAX = 0x7FFFFFFF

# Default pose-blend duration when a mix rule names none.
_DEFAULT_MIX_TIME = 0.2

SpineAssetSpec = namedtuple("SpineAssetSpec", "atlas_path skeleton_path")
SpineAssetSpec.__doc__ = "Shared asset identity: the atlas and skeleton resource names."

SpineModelSpec = namedtuple("SpineModelSpec", "assets zoom_x zoom_y")
SpineModelSpec.__doc__ = "Live model configuration: assets plus effective per-axis scale. A session is rebuilt when this changes."

SpineTrackSpec = namedtuple("SpineTrackSpec", "animation loop alpha additive mix_time")
SpineTrackSpec.__doc__ = "One track's desired entry. animation/loop/alpha/additive are playback properties; mix_time is transition-only."

SpineTarget = namedtuple("SpineTarget", "skins tracks")
SpineTarget.__doc__ = "Normalized desired state: ordered skin names, and ((track_index, SpineTrackSpec), ...) sorted by track."

SpineApplied = namedtuple("SpineApplied", "skins tracks")
SpineApplied.__doc__ = "What actually succeeded on the live model, in the same shape as SpineTarget."

SkinOp = namedtuple("SkinOp", "skins setup_slots")
TrackOp = namedtuple("TrackOp", "kind track spec mix_time")
SpineTransitionPlan = namedtuple("SpineTransitionPlan", "skin_op track_ops reason")
SpineTransitionPlan.__doc__ = "Ordered operations: the skin op (or None), then track ops in execution order, plus the reason for the resulting invalidation."

OP_RESET = "reset"      # track 0: setup pose, restart at time 0, zero physics
OP_MIX = "mix"          # track 0: set on the live state, pose-blend from current
OP_OVERLAY = "overlay"  # track >= 1: set with weight/additive, mix from current
OP_UPDATE = "update"    # any track: loop/alpha/additive of the playing entry
OP_FADE = "fade"        # any track: fade to empty and forget it

EMPTY_APPLIED = SpineApplied((), ())


def freeze_names(names):
    if names is None:
        return ()
    if isinstance(names, str):
        return (names,)
    rv = []
    for n in names:
        if not isinstance(n, str):
            raise TypeError("Spine: expected a name string, got {!r}".format(n))
        rv.append(n)
    return tuple(rv)


def playback_key(spec):
    return (spec.animation, spec.loop, spec.alpha, spec.additive)


def track_animation(state, track):
    for index, spec in state.tracks:
        if index == track:
            return spec.animation
    return None


# Only _resolve_policy runs user hooks; remaining helpers use resolved values.
# So the policy concept is due to Tom not having an ATL API for custom ATLs. 
# https://github.com/renpy/renpy/issues/7249
# If there's ever a custom ATL workflow, this should be deprecated in favor of it.

def _policy_to_dict(policy):
    """Coerce a resolved policy value into a plain dict."""
    if policy is None:
        return {}
    if isinstance(policy, dict):
        return policy
    return getattr(policy, "__dict__", None) or {}


def _invoke_hook(hook, ctx):
    """Call a metadata hook, tolerating both ``metadata(ctx)`` and a zero-arg
    ``metadata()`` by an arity check."""
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


def _resolve_policy(d, ctx):
    """Resolve the effective policy dict for a transition."""
    metadata = getattr(d, "_metadata", None)
    if metadata is None:
        return {}

    if callable(metadata):
        try:
            return _policy_to_dict(_invoke_hook(metadata, ctx))
        except Exception as e:
            spine_log("Spine: metadata hook for {!r} raised {}: {}; using reset".format(ctx.tag, type(e).__name__, e), debug=False)
            return {}

    return _policy_to_dict(metadata)


def _normalize_rule(rule, default_mix_time):
    if isinstance(rule, str):
        mode = rule
        mix_time = default_mix_time
    elif isinstance(rule, dict):
        mode = rule.get("mode", "reset")
        mix_time = rule.get("time", rule.get("mix_time", default_mix_time))
    else:
        mode = "reset"
        mix_time = default_mix_time

    if mode not in ("reset", "mix"):
        mode = "reset"
    return (mode, float(mix_time))


def _resolve_anim_mode(policy, from_anim, to_anim):
    """Most specific wins"""
    default_mix_time = policy.get("mix_time", _DEFAULT_MIX_TIME)
    transitions = policy.get("transitions", {}) or {}

    for key in ((from_anim, to_anim), ("*", to_anim), (from_anim, "*")):
        if key in transitions:
            return _normalize_rule(transitions[key], default_mix_time)

    if to_anim in transitions:
        return _normalize_rule(transitions[to_anim], default_mix_time)

    return _normalize_rule(policy.get("default_transition", "reset"), default_mix_time)


def _resolve_skin_policy(policy, from_skins, to_skins):
    skin_transitions = policy.get("skin_transitions", {}) or {}

    rule = None
    if to_skins in skin_transitions:
        rule = skin_transitions[to_skins]
    else:
        for name in (to_skins or ()):
            if name in skin_transitions:
                rule = skin_transitions[name]
                break
        if rule is None:
            rule = policy.get("skin_transition", "setup")

    if rule not in ("setup", "preserve"):
        rule = "setup"
    return rule


def validate_names(anim_names, skins, known_animations, known_skins):
    errors = []
    known_animations = set(known_animations)
    known_skins = set(known_skins)
    for name in anim_names:
        if name not in known_animations:
            errors.append("unknown animation {!r}".format(name))
    for name in skins:
        if name not in known_skins:
            errors.append("unknown skin {!r}".format(name))
    return errors


def normalize_target(policy, anim_names, loop, skins):
    tracks_cfg = policy.get("tracks", {}) or {}
    default_mix_time = _number(policy.get("mix_time", _DEFAULT_MIX_TIME), "mix_time")

    by_track = {}
    for name in freeze_names(anim_names):
        cfg = tracks_cfg.get(name, {}) or {}
        track = _number(cfg.get("track", 0), "tracks[{!r}].track".format(name))
        if track != int(track) or track < 0:
            raise ValueError("Spine: tracks[{!r}].track must be a non-negative integer, got {!r}".format(name, cfg.get("track")))
        track = int(track)

        alpha = _number(cfg.get("alpha", 1.0), "tracks[{!r}].alpha".format(name))
        if not (0.0 <= alpha <= 1.0):
            raise ValueError("Spine: tracks[{!r}].alpha must be within [0, 1], got {!r}".format(name, alpha))

        mix_time = _number(cfg.get("mix_time", default_mix_time), "tracks[{!r}].mix_time".format(name))
        if mix_time < 0.0:
            raise ValueError("Spine: tracks[{!r}].mix_time must be >= 0, got {!r}".format(name, mix_time))

        by_track[track] = SpineTrackSpec(
            name,
            bool(cfg.get("loop", loop)),
            alpha,
            bool(cfg.get("additive", False)),
            mix_time,
        )

    return SpineTarget(freeze_names(skins), tuple(sorted(by_track.items())))


def _number(value, field):
    try:
        rv = float(value)
    except (TypeError, ValueError):
        raise ValueError("Spine: {} must be a number, got {!r}".format(field, value))
    if rv != rv:
        raise ValueError("Spine: {} must be a number, got NaN".format(field))
    return rv


def plan_transition(applied, target, policy, oneshot=None, force_reset=False):
    default_mix_time = _number(policy.get("mix_time", _DEFAULT_MIX_TIME), "mix_time")
    restart_all = force_reset or oneshot == "reset"

    skin_op = None
    if target.skins != applied.skins:
        slot_policy = _resolve_skin_policy(policy, applied.skins, target.skins)
        skin_op = SkinOp(target.skins, slot_policy == "setup")

    applied_tracks = dict(applied.tracks)
    target_tracks = dict(target.tracks)
    ops = []

    for index in sorted(applied_tracks):
        if index not in target_tracks:
            ops.append(TrackOp(OP_FADE, index, None, 0.0 if force_reset else default_mix_time))

    for index in sorted(target_tracks):
        spec = target_tracks[index]
        current = applied_tracks.get(index)

        if current is not None and not restart_all:
            if playback_key(current) == playback_key(spec):
                continue
            if current.animation == spec.animation:
                ops.append(TrackOp(OP_UPDATE, index, spec, None))
                continue

        if index == 0:
            mode, mix_time = _resolve_anim_mode(policy, current.animation if current else None, spec.animation)
            if force_reset or oneshot == "reset":
                mode = "reset"
            elif oneshot == "mix":
                mode = "mix"

            if mode == "mix" and current is not None:
                ops.append(TrackOp(OP_MIX, 0, spec, mix_time))
            else:
                ops.append(TrackOp(OP_RESET, 0, spec, None))
        else:
            ops.append(TrackOp(OP_OVERLAY, index, spec, 0.0 if force_reset else spec.mix_time))

    if skin_op is None and not ops:
        return None

    if force_reset:
        reason = "rollback"
    elif oneshot == "reset":
        reason = "reset"
    else:
        reason = "target"

    return SpineTransitionPlan(skin_op, tuple(ops), reason)


class SpineSession(object):
    def __init__(self, key):
        self.key = key

        self.model = None

        self.spec = None

        # Record successes only, so failed operations remain retryable.
        self.applied = EMPTY_APPLIED

        # Last fully applied request; avoid reevaluating hooks on unchanged sweeps.
        self._last_request = None

        self._last_report = None

        self.last_seen_epoch = -1

        # Live serial does not rewind; compare it with the saved displayable serial.
        self.last_serial = -1

        self._force_reset = False

        self.driver = None

        self.pending_invalidation = None

    def dispose(self):
        if self.model is not None:
            try:
                self.model.dispose()
            except Exception as e:
                spine_log("Spine: error disposing session model:", e)
            self.model = None
        self.driver = None
        self.pending_invalidation = None

    def is_driver(self, d):
        return self.driver is d

    def invalidate(self, reason):
        self.pending_invalidation = reason
        d = self.driver
        if d is not None:
            renpy.display.render.redraw(d, 0)

    def take_invalidation(self):
        reason = self.pending_invalidation
        self.pending_invalidation = None
        return reason

    def report_once(self, message):
        if message != self._last_report:
            spine_log(message, debug=False)
            self._last_report = message

    def ensure_model(self, d):
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
        model = spinemodel.SpineModel(scale=d.zoom, scaleX=spec.zoom_x, scaleY=spec.zoom_y)
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

    def apply_target(self, d):
        if self.model is None:
            return

        force_reset = self._force_reset
        self._force_reset = False

        oneshot = getattr(d, "_oneshot_mode", None)

        try:
            request = (
                freeze_names(getattr(d, "_target_animations", ())),
                bool(getattr(d, "_target_loop", True)),
                freeze_names(getattr(d, "_target_skins", ())),
            )
        except TypeError as e:
            self.report_once("Spine: cannot show {!r}: {}".format(self.key[1], e))
            self._consume_oneshot(d)
            return

        if request == self._last_request and not force_reset and oneshot != "reset":
            self._consume_oneshot(d)
            return

        anim_names, loop, skins = request

        current_base = track_animation(self.applied, 0)
        ctx = types.SimpleNamespace(
            tag=self.key[1],
            layer=self.key[0],
            current_animation=current_base,
            current_skin=self.applied.skins,
            target_animation=(anim_names[-1] if anim_names else None),
            target_skin=skins,
            first_show=(current_base is None),
        )
        policy = _resolve_policy(d, ctx)

        # Validate before native mutation to avoid partially applying invalid requests.
        errors = validate_names(anim_names, skins,
                                self.model.get_animation_names(), self.model.get_skin_names())
        target = None
        if not errors:
            try:
                target = normalize_target(policy, anim_names, loop, skins)
            except (TypeError, ValueError) as e:
                errors.append(str(e))

        if errors:
            self.report_once("Spine: cannot show {!r}: {}".format(self.key[1], "; ".join(errors)))
            self._last_request = request  # nothing will change until a new request
            self._consume_oneshot(d)
            return

        plan = plan_transition(self.applied, target, policy, oneshot, force_reset)
        self._consume_oneshot(d)

        if plan is None:
            self._last_request = request
            return

        complete = self._execute_plan(plan)
        self._last_request = request if complete else None
        self.invalidate(plan.reason)

    def _consume_oneshot(self, d):
        if getattr(d, "_oneshot_mode", None) is not None:
            d._oneshot_mode = None

    def _execute_plan(self, plan):
        model = self.model
        skins = self.applied.skins
        tracks = dict(self.applied.tracks)
        failures = []

        op = plan.skin_op
        if op is not None:
            if model.apply_skin_combined(op.skins, op.setup_slots):
                skins = op.skins
            else:
                failures.append("skin {}".format(list(op.skins)))

        for op in plan.track_ops:
            spec = op.spec
            if op.kind == OP_FADE:
                ok = model.fade_track(op.track, op.mix_time)
                if ok:
                    tracks.pop(op.track, None)
            elif op.kind == OP_RESET:
                ok = model.apply_animation_reset(op.track, spec.animation, spec.loop)
                if ok:
                    model.update_track_settings(op.track, spec.loop, spec.alpha, spec.additive)
            elif op.kind == OP_MIX:
                ok = model.apply_animation_mix(op.track, spec.animation, spec.loop, op.mix_time)
                if ok:
                    model.update_track_settings(op.track, spec.loop, spec.alpha, spec.additive)
            elif op.kind == OP_OVERLAY:
                ok = model.apply_overlay_animation(
                    op.track, spec.animation, spec.loop, op.mix_time, spec.alpha, spec.additive)
            elif op.kind == OP_UPDATE:
                ok = model.update_track_settings(op.track, spec.loop, spec.alpha, spec.additive)
            else:
                ok = False

            if ok:
                if spec is not None:
                    tracks[op.track] = spec
            else:
                failures.append("{} track {}".format(op.kind, op.track))

        self.applied = SpineApplied(skins, tuple(sorted(tracks.items())))

        if failures:
            self.report_once("Spine: transition for {!r} partially applied; failed: {}".format(
                self.key[1], ", ".join(failures)))
            return False

        self._last_report = None
        return True


def _rollback_serial():
    try:
        return renpy.rollback.serial
    except Exception:
        return 0


def model_spec_of(d):
    return SpineModelSpec(
        SpineAssetSpec(d.atlas_path, d.skeleton_path),
        float(d.zoomX),
        float(d.zoomY),
    )


class SpineRegistry(object):
    def __init__(self):
        self.sessions = {}

        # Retired sessions survive one more interaction for retained displayables.
        self.retired = []

        self.epoch = 0

        self.showing = False

    def mark_showing(self):
        self.showing = True

    def retire(self, session):
        self.sessions.pop(session.key, None)
        self.retired.append(session)

    def dispose_retired(self):
        for s in self.retired:
            s.dispose()
        del self.retired[:]

    def rebase_epochs(self):
        for s in self.sessions.values():
            s.last_seen_epoch = 0
        self.epoch = 0

    def reset(self):
        for s in list(self.sessions.values()):
            s.dispose()
        self.sessions.clear()
        self.dispose_retired()
        self.showing = False

    def sweep(self):
        """
        Called once per interact
        """
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
        ordinals = {}

        sls = renpy.display.scenelists.scene_lists()

        for layer, tag, d in sls.get_all_layer_tag_displayable():
            if tag is None:
                continue
            # Retained transition copies keep their previous session and never drive it.
            if "$" in tag:
                continue
            if d is None:
                continue

            def visit(child, layer=layer, tag=tag):
                if getattr(child, "_is_spine_displayable", False):
                    self._bind(child, layer, tag, epoch, serial, ordinals)

            d.visit_all(visit)

        for key in list(self.sessions.keys()):
            s = self.sessions[key]
            if s.last_seen_epoch != epoch:
                self.retire(s)

    def _bind(self, d, layer, tag, epoch, serial, ordinals):
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
            # Inversely, an older displayable serial indicates rollback relative to the live session.
            d_serial = getattr(d, "_rollback_serial", None)
            if d_serial is not None and d_serial < session.last_serial:
                session._force_reset = True

        # Bind before applying so invalidation has a driver and failed loads remain retryable
        session.driver = d
        session.last_seen_epoch = epoch
        d._session = session

        d._rollback_serial = serial
        session.last_serial = serial

        if not session.ensure_model(d):
            return

        session.apply_target(d)

        size = session.model.get_size()
        if size:
            d.width, d.height = size


registry = SpineRegistry()


def update_states():
    registry.sweep()


def reset():
    registry.reset()


def reset_states():
    registry.reset()
