import renpy

# A list of style prefixes we care about, including no prefix.
prefixes = [ 'hover_', 'idle_', '' ]

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
        
        s = Style(parent, defer=True)
        s.name = name
        s.parent = parent
        s.description = description

        setattr(self, name, s)

        self._style_list.append(s)

    def _build_style_caches(self):

        for i in self._style_list:
            i.build_cache()

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
        return dict(properties=self.properties,
                    prefix=self.prefix,
                    parent=self.parent)
                    

    def __setstate__(self, state):
        self.__dict__.update(state)

        # This should always work, as only one layer of these styles will
        # be serialized.

        self.build_cache()

    def __setattr__(self, key, value):

        for prefix in prefixes:
            prefkey = prefix + key

            self.properties[prefkey] = value
            self.cache[prefkey] = value

    def __getattr__(self, key):

        cache = self.cache
        
        try:
            return cache[self.prefix + key]
        except KeyError:
            raise AttributeError("Style property '%s' not found." % key)

    def __delattr__(self, key):
        del self.properties[key]
        del self.cache[key]

    def lookup(self, key, prefix):

        cache = self.cache

        try:
            return cache.get(prefix + key, cache[key])
        except KeyError:
            raise AttributeError("Style property '%s' not found." % key)


    def set_prefix(self, prefix):
        vars(self)["prefix"] = prefix
        self.prefix = prefix


    def build_cache(self):
        vars(self)["cache"] = { }

        self.cache = { }

        if self.parent:
            self.cache.update(getattr(renpy.game.style, self.parent).cache)

        self.cache.update(self.properties)

    def __init__(self, parent, properties=None, defer=False):

        if parent and not hasattr(renpy.game.style, parent):
            raise Exception("Style '%s' is not known." % parent)

        if not properties:
            properties = { }

        for k in properties.keys():
            for p in prefixes:
                if p + k not in properties:
                    properties[p + k] = properties[k]

        vars(self)["parent"] = parent
        vars(self)["prefix"] = ''
        vars(self)["properties"] = properties
        vars(self)["cache"] = { }
            
        if not defer:
            self.build_cache()
