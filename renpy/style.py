import renpy

class StyleManager(object):
    """
    This is the singleton object that is exported into the store as
    'style', and to everyone as renpy.game.style. It's responsible for
    mapping style names to styles.
    """

    def __init__(self):
        self._style_list = [ ]

    def create(self, name, parent='default', description=''):
        """
        Creates a new style with the given parent and description, and
        adds it to the StyleManager.
        """

        if parent and not hasattr(self, parent):
            raise Exception("Style '%s' has non-existent parent '%s'." % (name, parent))
        
        s = Style(parent)
        s.name = name
        s.parent = parent
        s.description = description

        setattr(self, name, s)

        self._style_list.append(s)

    def _write_docs(self, filename):

        f = file(filename, "w")

        import re

        for s in self._style_list:
            f.write('    <renpy_style name="%s">' % s.name)
            
            if s.parent:
                f.write('<renpy_style_inherits>%s</renpy_style_inherits>' % s.parent)

            f.write(re.sub(r'\s+', ' ', s.description))
            f.write("</renpy_style>\n\n")

        f.close()

class Style(object):
    """
    This is an individual style object, which can have properties
    looked up on it or its parent. Call the constructor of this
    to create an anonymous style.
    """

    def __getstate__(self):
        return vars(self)

    # Not sure why this is necessary, but it seems to be. :-(
    def __setstate__(self, state):
        self.__dict__.update(state)

    def __getattr__(self, key):
        return self.lookup(key, self.prefix)

    def lookup(self, key, prefix):

        if prefix + key in vars(self):
            return vars(self)[prefix + key]

        if key in vars(self):
            return vars(self)[key]

        if self.parent:

            # This must always work, since we check for this in
            # create_style.
            ps = getattr(renpy.game.style, self.parent)
            return ps.lookup(key, prefix)

        else:
            raise Exception("Style property '%s' not found." % key)

    def set_prefix(self, prefix):
        self.prefix = prefix

    def __init__(self, parent, properties=None):

        if parent and not hasattr(renpy.game.style, parent):
            raise Exception("Style '%s' is not known." % parent)
            
        self.parent = parent
        self.prefix = ''

        if properties:
            vars(self).update(properties)

