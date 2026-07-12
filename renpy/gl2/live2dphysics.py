def from_physics3(physics_json):
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
            "inputs": [
                (i["Source"]["Id"], i["Weight"], i["Type"].lower(), i["Reflect"])
                for i in setting["Input"]
            ],
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