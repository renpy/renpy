import renpy

class StyleManager(object):
    """
    This is the singleton object that is exported into the store as
    'style', and to everyone as renpy.game.style. It's responsible for
    mapping style names to styles.
    """

    def create(self, name, parent='default', description=''):
        """
        Creates a new style with the given parent and description, and
        adds it to the StyleManager.
        """

        if parent and not hasattr(self, parent):
            raise Exception("Style '%s' has non-existent parent '%s'." % (name, parent))
        
        s = Style(parent)
        s.name = name
        s.description = description

        setattr(self, name, s)
        


class Style(object):
    """
    This is an individual style object, which can have properties
    looked up on it or its parent. Call the constructor of this
    to create an anonymous style.
    """

    def __getattr__(self, key):
        if key in vars(self):
            return vars(self)[key]

        if self.parent:

            # This must always work, since we check for this in
            # create_style.
            ps = getattr(renpy.game.style, self.parent)

            return getattr(ps, key)

        else:
            raise Exception("Style property '%s' not found." % key)


    def __init__(self, parent, properties=None):

        if parent and not hasattr(renpy.game.style, parent):
            raise Exception("Style '%s' is not known." % parent)
            
        self.parent = parent

        if properties:
            vars(self).update(properties)

