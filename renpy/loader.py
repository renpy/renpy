import renpy.game as game


def load(name, flags="rb"):
    """
    Returns an open python file object of the given type.
    """

    return file(game.basepath + "/" + name, flags)


def transfn(name):
    return game.basepath + "/" + name
