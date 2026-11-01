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

"""
Support for Live2D pose files (.pose3.json), following CubismPose in the Cubism
SDK for Native.

A pose file divides parts into groups of alternatives, like two versions of an
arm, of which only one should be visible at a time. Each frame, the requests
made by motions and expressions select one part from each group. That part
fades in while the others fade out, and it stays selected until a later request
changes it.

The state that changes from frame to frame belongs to the caller, as a model is
shared between all of the images that display it.
"""

import json

import renpy

# Requests at or below this value do not make a part visible.
EPSILON = 0.001

# The time used when a pose file does not give a valid fade time, in seconds.
DEFAULT_FADE_TIME = 0.5

# The opacity at which the fading in and fading out parts cross.
PHI = 0.5

# The most background that's allowed to show through a crossfade.
BACK_OPACITY_THRESHOLD = 0.15


class PosePart:
    """
    A part that belongs to a pose group, and the parts that copy its opacity.
    """

    def __init__(self, part_id: str, links: list[str]):
        self.part_id: str = part_id
        self.links: list[str] = links


class Pose:
    """
    The contents of a pose file, limited to parts that exist in the model.
    """

    def __init__(self, pose_json: dict, known_parts) -> None:
        fade_time = pose_json.get("FadeInTime")

        if fade_time is None or fade_time < 0.0:
            fade_time = DEFAULT_FADE_TIME

        # The time it takes a newly selected part to fade in, in seconds.
        self.fade_time: float = fade_time

        # The groups of alternative parts. A part's position in a group is significant.
        self.groups: list[list[PosePart]] = []

        # Maps the id of each part in a group to the index of that group.
        self.part_groups: dict[str, int] = {}

        for group_json in pose_json.get("Groups", []):
            group = [
                PosePart(i["Id"], [link for link in i.get("Link") or [] if link in known_parts])
                for i in group_json
                if i["Id"] in known_parts
            ]

            if not group:
                continue

            for part in group:
                self.part_groups[part.part_id] = len(self.groups)

            self.groups.append(group)

    def blend_request(self, requests: dict[str, float], sustained: dict[int, str], parameter: dict, weight: float):
        """
        Applies an expression parameter to `requests` if it names a part in a
        group. An expression selects a part with a parameter that has the id
        of the part, as there is no separate way for it to change a part.

        `sustained`
            A map from group index to the id of the part selected by that group.
        """

        part_id = parameter["Id"]
        group_index = self.part_groups.get(part_id)

        if group_index is None:
            return

        old = requests.get(part_id, 1.0 if part_id == sustained.get(group_index) else 0.0)
        blend = parameter["Blend"]
        value = parameter["Value"]

        if blend == "Multiply":
            value = old * value
        elif blend == "Add":
            value = old + value

        requests[part_id] = old + weight * (value - old)


def load_pose(model, base: str, filename: str | None) -> Pose | None:
    """
    Loads a pose file for `model`. Returns None if `filename` is None or can't
    be loaded, as a model can be used without its pose file.
    """

    if not filename:
        return None

    if not renpy.loader.loadable(base + filename, directory="images"):
        return None

    with renpy.loader.load(base + filename, directory="images") as f:
        return Pose(json.load(f), model.parts)


def select_part(group: list[PosePart], requested: dict[str, float], sustained: str | None) -> str:
    """
    Returns the id of the part in `group` that should be visible.

    `requested`
        A map from part id to the value requested by motions and expressions.

    `sustained`
        The id of the part selected previously, which is requested unless
        something says otherwise. None if nothing has been selected.
    """

    if sustained is None:
        sustained = group[0].part_id

    for part in group:
        value = requested.get(part.part_id, 1.0 if part.part_id == sustained else 0.0)

        if value > EPSILON:
            return part.part_id

    return group[0].part_id


def fade_group(group: list[PosePart], visible: str, opacities: dict[str, float], dt: float, fade_time: float) -> bool:
    """
    Advances a crossfade by `dt` seconds, updating `opacities` with the opacity
    of each part in `group`, and of the parts linked to them. Parts missing from
    `opacities` are treated as hidden. Returns True if the fade isn't finished.

    The visible part fades in linearly. The others only ever lose opacity, by
    just enough to keep too much of the background from showing.
    """

    if fade_time == 0.0:
        new_opacity = 1.0
    else:
        new_opacity = min(opacities.get(visible, 0.0) + max(dt, 0.0) / fade_time, 1.0)

    if new_opacity < PHI:
        limit = new_opacity * (PHI - 1.0) / PHI + 1.0
    else:
        limit = (1.0 - new_opacity) * PHI / (1.0 - PHI)

    if (1.0 - limit) * (1.0 - new_opacity) > BACK_OPACITY_THRESHOLD:
        limit = 1.0 - BACK_OPACITY_THRESHOLD / (1.0 - new_opacity)

    for part in group:
        if part.part_id == visible:
            opacity = new_opacity
        else:
            opacity = min(opacities.get(part.part_id, 0.0), limit)

        opacities[part.part_id] = opacity

        for link in part.links:
            opacities[link] = opacity

    return new_opacity < 1.0
