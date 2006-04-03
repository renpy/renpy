import renpy

# A list of style prefixes we care about, including no prefix.
prefixes = [ 'hover_', 'idle_', 'activate_' , 'insensitive_' ]

def startswith_prefix(s):
    for i in prefixes:
        if s.startswith(i):
            return True
    else:
        return False

substitutes = dict(
    xmargin = [ 'left_margin', 'right_margin' ],
    ymargin = [ 'top_margin', 'bottom_margin' ],
    xpadding = [ 'left_padding', 'right_padding' ],
    ypadding = [ 'top_padding', 'bottom_padding' ],
    )

# Expand out substitutes:
for k in substitutes.keys():
    for p in prefixes:
        substitutes[p + k] = [ p + i for i in substitutes[k] ]

# A map from a style name to the style associated with that name.
style_map = { }

# True if we have expanded all of the style caches, False otherwise.
styles_built = False

# A list of styles that are pending expansion.
styles_pending = [ ]

# A list of created styles giving the style's name, parent, and description.
style_info = [ ]

def reset():
    """
    This resets all of the data structures associated with style
    management.
    """

    global style_map
    global styles_built
    global styles_pending
    global style_info 
    
    style_map = { }
    styles_built = False
    styles_pending = [ ]
    style_info = [ ]


class StyleManager(object):
    """
    This is the singleton object that is exported into the store
    as style
    """

    def __getattr__(self, name):
        try:
            return style_map[name]
        except:
            raise Exception('The style %s does not exist.' % name)

    def create(self, name, parent, description=None):
        """
        Creates a new style.

        @param name: The name of the new style, as a string.

        @param parent: The parent of the new style, as a string. This
        is either 'default' or something more specific.

        @param description: A description of the style, for
        documentation purposes.
        """

        style_map[name] = Style(parent, { })

        if description:
            style_info.append((name, parent, description))

    def exists(self, name):
        """
        This determines if the named style exists.
        """
        
        return name in style_map

def expand_properties(properties):
    props = { }

    # Expand substitutions.
    for k, v in properties.items():
        if k in substitutes:
            for j in substitutes[k]:
                props[j] = v
        else:
            props[k] = v

    # Expand prefixes, where necessary.
    for k, v in props.items():
        if startswith_prefix(k):
            continue

        del props[k]

        for p in prefixes:
            props[p + k] = v

    return props

# This expands out property names and adds them to style's property
# dictionary. 
def compute_properties(style, properties):

    props = expand_properties(properties)

    style.properties.update(props)
    style.cache.update(props)

# This expands out names, and removes them from the properties of
# the style. (But not the cache!)
def remove_properties(style, properties):

    props = expand_properties(properties)

    for k in props:
        if k in style.properties:
            del style.properties[k]



# This builds the style. If recurse is True, this also builds the
# parent style.
def build_style(style, recurse=False):

    style.cache.clear()

    if style.parent:

        try:
            parent = style_map[style.parent]
        except:
            raise Exception('Style %s is not known.' % style.parent)

        if recurse:
            build_style(parent)
        
        style.cache.update(parent.cache)

    style.cache.update(style.properties)

# This builds all pending styles, recursing to ensure that they are built
# in the right order.
def build_styles():

    global styles_pending
    global styles_built

    for s in styles_pending:
        build_style(s, True)

    styles_pending = None
    styles_built = True
        

class Style(object):

    def __getstate__(self):
        return dict(prefix = self.prefix,
                    parent = self.parent,
                    cache = { },
                    properties = self.properties)

    def __setstate__(self, state):
        vars(self).update(state)
        build_style(self)

    def __init__(self, parent, properties):

        fields = dict(
            prefix = 'insensitive_',
            parent = parent,
            cache = { },
            properties = { },
            )

        vars(self).update(fields)

        if styles_built:
            build_style(self)
        else:
            styles_pending.append(self)
    
        compute_properties(self, properties)

    def set_prefix(self, prefix):
        vars(self)["prefix"] = prefix
            
    def __getattr__(self, name):
        return self.cache[self.prefix + name]

    def __setattr__(self, name, value):
        compute_properties(self, { name : value } )

    def __delattr__(self, name):
        remove_properties(self, { name : None })

    
        
def write_docs(filename):

    f = file(filename, "w")

    import re
 
    for name, parent, description in style_info:
        f.write('    <renpy_style name="%s">' % name)

        if parent:
            f.write('<renpy_style_inherits>%s</renpy_style_inherits>' % parent)

        f.write(re.sub(r'\s+', ' ', description))
        f.write("</renpy_style>\n\n")

    f.close()            
        

def write_hierarchy(fn):

    f = file(fn, "w")

    kids = { }
    
    for name, parent, description in style_info:
        kids.setdefault(parent, []).append(name)

    def do(name):

        f.write('<li> <a href="#%s">%s</a>\n' % (name, name))

        if name in kids:
            f.write('<ul>\n')

            l = kids[name]
            l.sort()

            for n in l:
                do(n)

            f.write('</ul>\n')

        f.write('</li>')

    do('default')

    f.close()
