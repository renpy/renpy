import renpy

def load(name, flags="rb"):
    """
    Returns an open python file object of the given type.
    """

    return file(renpy.game.basepath + "/" + name, flags)


def transfn(name):
    return renpy.game.basepath + "/" + name
