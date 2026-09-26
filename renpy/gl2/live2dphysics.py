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

import json
import math

import renpy
from renpy.gl2.gl2physics import PendulumPhysics

class Live2DPhysics:
    """
    Own the frame clock and redraw policy for one shared Live2D model.
    """

    def __init__(self, model, rig):
        self.physics = PendulumPhysics(model.get_physics_parameters(), rig)
        self._last_update = None

    def evaluate(self, now):
        if not math.isfinite(now):
            raise ValueError(f"Live2D physics time must be finite, not {now!r}.")

        if self._last_update is None:
            delta = 0.0
        elif now < self._last_update:
            self.physics.reset()
            delta = 0.0
        else:
            delta = now - self._last_update

        self._last_update = now
        self.physics.evaluate(delta)

        return 0.0 if self.physics.is_active() else None

def load_physics(model, base, filename):
    """
    Load a physics3 file and bind its simulation to the model's parameters.
    """

    if not filename:
        return None

    with renpy.loader.load(base + filename, directory="images") as f:
        rig = _from_physics3(json.load(f))

    return Live2DPhysics(model, rig)

def _from_physics3(physics_json):
    """
    Convert a parsed physics3.json dict into a rig.
    """

    strands = []

    for setting in physics_json["PhysicsSettings"]:
        normalization = setting["Normalization"]

        strands.append({
            "name": setting.get("Id"),
            "normalization_position": (
                normalization["Position"]["Minimum"],
                normalization["Position"]["Maximum"],
                normalization["Position"]["Default"],
            ),
            "normalization_angle": (
                normalization["Angle"]["Minimum"],
                normalization["Angle"]["Maximum"],
                normalization["Angle"]["Default"],
            ),
            "inputs": [(i["Source"]["Id"], i["Weight"], i["Type"].lower(), i["Reflect"]) for i in setting["Input"]],
            "outputs": [
                (o["Destination"]["Id"], o["VertexIndex"], o["Scale"], o["Weight"], o["Type"].lower(), o["Reflect"])
                for o in setting["Output"]
            ],
            "vertices": [
                (v["Mobility"], v["Delay"], v["Acceleration"], v["Radius"], v["Position"]["X"], v["Position"]["Y"])
                for v in setting["Vertices"]
            ],
        })

    return {
        "fps": physics_json["Meta"].get("Fps", 30.0),
        "strands": strands,
    }
