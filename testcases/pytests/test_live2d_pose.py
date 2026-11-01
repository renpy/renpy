"""
Tests for the Live2D pose logic. The expected fade values come from
CubismPose::DoFade in the Cubism SDK for Native.
"""

import collections
from types import SimpleNamespace

import pytest
from pytest_mock import MockerFixture

from renpy.gl2 import live2d
from renpy.gl2.live2dpose import DEFAULT_FADE_TIME, Pose, fade_group, select_part

KNOWN_PARTS = {"A", "B", "C", "LinkA"}

# The displayable, shared model data, render clock, and observed part opacities.
PoseDisplayable = tuple[live2d.Live2D, SimpleNamespace, SimpleNamespace, dict[str, float]]


def make_pose(groups=None, **properties) -> Pose:
    """
    Creates a pose from a list of groups of part ids.
    """

    if groups is None:
        groups = [["A", "B"]]

    return Pose({"Groups": [[{"Id": i, "Link": []} for i in group] for group in groups], **properties}, KNOWN_PARTS)


@pytest.mark.parametrize(
    ("properties", "expected"),
    [
        ({}, DEFAULT_FADE_TIME),
        ({"FadeInTime": 1.5}, 1.5),
        ({"FadeInTime": 0.0}, 0.0),
        ({"FadeInTime": -1.0}, DEFAULT_FADE_TIME),
    ],
)
def test_fade_time(properties, expected):
    assert make_pose(**properties).fade_time == expected


def test_unknown_parts_and_empty_groups_are_dropped():
    pose = make_pose([["Missing"], ["Missing", "B", "C"]])

    assert [[part.part_id for part in group] for group in pose.groups] == [["B", "C"]]
    assert pose.part_groups == {"B": 0, "C": 0}


def test_unknown_links_are_dropped():
    pose = Pose({"Groups": [[{"Id": "A", "Link": ["LinkA", "Missing"]}, {"Id": "B"}]]}, KNOWN_PARTS)

    assert pose.groups[0][0].links == ["LinkA"]
    assert pose.groups[0][1].links == []


@pytest.mark.parametrize(
    ("requested", "sustained", "expected"),
    [
        ({}, None, "A"),
        ({}, "B", "B"),
        ({"A": 0.0, "B": 1.0}, None, "B"),
        ({"A": 1.0, "B": 1.0}, "B", "A"),
        ({"B": 0.0}, "B", "A"),
        ({"A": 0.0}, None, "A"),
        ({"A": 0.0, "B": 0.0}, "B", "A"),
        ({"B": 1.0}, "A", "A"),
        ({"A": 0.0001, "B": 0.5}, "A", "B"),
    ],
)
def test_select_part(requested, sustained, expected):
    assert select_part(make_pose().groups[0], requested, sustained) == expected


@pytest.mark.parametrize(
    ("before", "dt", "expected_a", "expected_b"),
    [
        (0.0, 0.1, 0.2, 0.8125),  # Background limit applies.
        (0.25, 0.125, 0.5, 0.7),  # Background limit applies.
        (0.5, 0.125, 0.75, 0.4),  # Background limit applies.
        (0.8, 0.05, 0.9, 0.1),  # Background limit doesn't apply.
        (0.5, 0.25, 1.0, 0.0),
        (0.5, 10.0, 1.0, 0.0),
    ],
)
def test_fade_group_crossfade(before, dt, expected_a, expected_b):
    opacities = {"A": before, "B": 1.0}

    fade_group(make_pose().groups[0], "A", opacities, dt, 0.5)

    assert opacities["A"] == pytest.approx(expected_a)
    assert opacities["B"] == pytest.approx(expected_b)


def test_fade_group_reports_when_finished():
    group = make_pose().groups[0]
    opacities = {"A": 0.0, "B": 1.0}

    assert fade_group(group, "A", opacities, 0.25, 0.5)
    assert not fade_group(group, "A", opacities, 0.25, 0.5)


def test_fade_group_without_time_passing_keeps_opacity():
    opacities = {"A": 0.5, "B": 0.5}

    fade_group(make_pose().groups[0], "A", opacities, 0.0, 0.5)

    assert opacities == {"A": 0.5, "B": 0.5}


def test_fade_group_ignores_negative_time():
    opacities = {"A": 0.5, "B": 0.5}

    fade_group(make_pose().groups[0], "A", opacities, -1.0, 0.5)

    assert opacities == {"A": 0.5, "B": 0.5}


def test_fade_group_with_no_fade_time_is_immediate():
    opacities = {"A": 0.0, "B": 1.0}

    assert not fade_group(make_pose().groups[0], "A", opacities, 0.0, 0.0)
    assert opacities == {"A": 1.0, "B": 0.0}


def test_fade_group_never_raises_hidden_parts():
    opacities = {"A": 0.0, "B": 0.0}

    fade_group(make_pose().groups[0], "A", opacities, 0.1, 0.5)

    assert opacities["B"] == 0.0


def test_fade_group_copies_opacity_to_links():
    pose = Pose({"Groups": [[{"Id": "A", "Link": ["LinkA"]}, {"Id": "B"}]]}, KNOWN_PARTS)
    opacities = {"A": 0.25, "B": 1.0}

    fade_group(pose.groups[0], "A", opacities, 0.125, 0.5)

    assert opacities["LinkA"] == opacities["A"] == pytest.approx(0.5)


def test_blend_request_ignores_other_parameters():
    requests = {}

    make_pose().blend_request(requests, {}, {"Id": "ParamAngleX", "Blend": "Overwrite", "Value": 1.0}, 1.0)

    assert requests == {}


@pytest.mark.parametrize(
    ("blend", "value", "weight", "part_id", "expected"),
    [
        ("Overwrite", 0.0, 1.0, "B", 0.0),
        ("Overwrite", 0.0, 0.5, "B", 0.5),
        ("Overwrite", 1.0, 0.5, "A", 0.5),
        ("Add", 1.0, 1.0, "A", 1.0),
        ("Multiply", 0.5, 1.0, "B", 0.5),
    ],
)
def test_blend_request_starts_from_the_sustained_part(blend, value, weight, part_id, expected):
    requests = {}

    make_pose().blend_request(requests, {0: "B"}, {"Id": part_id, "Blend": blend, "Value": value}, weight)

    assert requests[part_id] == pytest.approx(expected)


def test_blend_request_starts_from_earlier_requests():
    requests = {"A": 1.0}

    make_pose().blend_request(requests, {}, {"Id": "A", "Blend": "Overwrite", "Value": 0.0}, 0.5)

    assert requests["A"] == pytest.approx(0.5)


@pytest.fixture
def pose_displayable(mocker: MockerFixture) -> PoseDisplayable:
    """Isolate the render clock and shared model so pose updates need neither a GPU nor the Cubism library."""

    pose = make_pose()
    opacities = {}
    model = mocker.Mock()
    model.blend_opacity.side_effect = lambda part_id, blend, value: opacities.update({part_id: value})
    common = SimpleNamespace(
        model=model,
        pose_requests={},
        pose_parameters={},
        get_pose=lambda: pose,
        motions={},
        is_seamless=lambda name: False,
        all_expressions={},
    )
    clock = SimpleNamespace(frame_time=0.0)
    mocker.patch.object(live2d, "states", collections.defaultdict(live2d.Live2DState))
    mocker.patch.object(live2d.renpy.display, "interface", clock)
    mocker.patch.object(live2d.Live2D, "common", new_callable=mocker.PropertyMock, return_value=common)

    displayable = live2d.Live2D.__new__(live2d.Live2D)
    displayable.name = ("master", "pose", "model", 0)
    displayable.pose = True
    displayable.motions = ["switch"]
    displayable.loop = False
    displayable.used_nonexclusive = None
    displayable.expression = None

    return displayable, common, clock, opacities


def test_pose_change_after_idle_starts_a_full_crossfade(pose_displayable: PoseDisplayable) -> None:
    """Time spent cached before a selection change must not count toward the newly requested fade."""

    displayable, common, clock, opacities = pose_displayable
    assert displayable.update_pose() is None
    assert opacities == {"A": 1.0, "B": 0.0}

    clock.frame_time = 10.0
    common.pose_requests.update(A=0.0, B=1.0)
    assert displayable.update_pose() == 0
    assert opacities == {"A": 1.0, "B": 0.0}

    clock.frame_time = 10.25
    assert displayable.update_pose() == 0
    assert opacities["B"] == pytest.approx(0.5)

    clock.frame_time = 10.5
    assert displayable.update_pose() is None
    assert opacities == {"A": 0.0, "B": 1.0}


@pytest.mark.parametrize("target", ["Parameter", "PartOpacity"])
def test_motion_curves_select_pose_parts(pose_displayable: PoseDisplayable, target: str) -> None:
    """Part ids can be virtual parameters absent from the core model, as well as part-opacity curves."""

    displayable, common, _clock, opacities = pose_displayable
    common.motions["switch"] = SimpleNamespace(
        duration=1.0,
        get=lambda *args: {(target, "A"): (1.0, 0.0), (target, "B"): (1.0, 1.0)},
        wait=lambda *args: None,
    )

    displayable.update(common, 0.1, None)
    displayable.update_expressions(0.1)
    displayable.update_pose()

    assert opacities == {"A": 0.0, "B": 1.0}


@pytest.mark.parametrize("weight", [0.0, 0.5, 1.0])
def test_parameter_pose_curves_respect_motion_weights(pose_displayable: PoseDisplayable, weight: float) -> None:
    """A fading parameter curve blends from the sustained selector rather than overriding it at zero weight."""

    displayable, common, _clock, _opacities = pose_displayable
    displayable.update_pose()
    common.motions["switch"] = SimpleNamespace(
        duration=1.0,
        get=lambda *args: {("Parameter", "A"): (weight, 0.0), ("Parameter", "B"): (weight, 1.0)},
        wait=lambda *args: None,
    )

    displayable.update(common, 0.1, None)
    displayable.update_expressions(0.1)

    assert common.pose_requests == {"A": pytest.approx(1.0 - weight), "B": pytest.approx(weight)}


def test_parameter_pose_curves_blend_old_and_new_motions(pose_displayable: PoseDisplayable) -> None:
    """The outgoing motion only fills the weight left by the incoming motion, as for ordinary parameters."""

    displayable, common, _clock, _opacities = pose_displayable
    common.motions["switch"] = SimpleNamespace(
        duration=1.0,
        get=lambda *args: {("Parameter", "A"): (0.5, 0.0), ("Parameter", "B"): (0.5, 1.0)},
        wait=lambda *args: None,
    )

    displayable.update(common, 0.1, None)
    common.motions["switch"].get = lambda *args: {("Parameter", "A"): (1.0, 1.0), ("Parameter", "B"): (1.0, 0.0)}
    displayable.update(common, 0.1, 0.1)
    displayable.update_expressions(0.1)

    assert common.pose_requests == {"A": pytest.approx(0.5), "B": pytest.approx(0.5)}


def test_part_opacity_curves_override_pose_parameter_curves(pose_displayable: PoseDisplayable) -> None:
    """Cubism applies direct part-opacity selector curves after parameter curves, independent of their fade weight."""

    displayable, common, _clock, opacities = pose_displayable
    common.motions["switch"] = SimpleNamespace(
        duration=1.0,
        get=lambda *args: {
            ("Parameter", "A"): (1.0, 1.0),
            ("Parameter", "B"): (1.0, 0.0),
            ("PartOpacity", "A"): (0.0, 0.0),
            ("PartOpacity", "B"): (0.0, 1.0),
        },
        wait=lambda *args: None,
    )

    displayable.update(common, 0.1, None)
    displayable.update_expressions(0.1)
    displayable.update_pose()

    assert opacities == {"A": 0.0, "B": 1.0}


def test_reset_pose_states_preserves_motion_and_expression_state(pose_displayable: PoseDisplayable) -> None:
    """Loading clears only unsaved pose state; still images then begin at the first part again."""

    displayable, common, _clock, opacities = pose_displayable
    common.pose_requests.update(A=0.0, B=1.0)
    displayable.update_pose()
    state = live2d.states[displayable.name]
    state.new = displayable
    state.expressions = [("smile", 0.0)]

    live2d.reset_pose_states()
    common.pose_requests.clear()
    displayable.update_pose()

    assert opacities == {"A": 1.0, "B": 0.0}
    assert state.new is displayable
    assert state.expressions == [("smile", 0.0)]
