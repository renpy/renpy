# Copyright 2004-2007 PyTom <pytom@bishoujo.us>
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

import renpy

# A list of roles we know about.
roles = [ 'selected_', '' ]

# A list of style prefixes we care about, including no prefix.
prefixes = [ 'hover_', 'idle_', 'insensitive_', 'activate_', ]

# A list of prefix, length, priority, (tuple of prefixes).
prefix_subs = [ ]

def register_prefix(prefix, prio, addprefixes=[]):

    for r in roles:
        if r and prefix.startswith(r):
            alts1 = [ r ]
            break
    else:
        alts1 = roles

    for p in prefixes:
        if prefix.endswith(p):
            alts2 = [ p ]
            break
    else:
        alts2 = prefixes

    alts2 += addprefixes
        
    alts = [ a1 + a2 for a1 in alts1 for a2 in alts2 ]

    prefix_subs.append((prefix, len(prefix), prio, alts))


register_prefix('selected_activate_', 6)
register_prefix('selected_hover_', 5, [ 'activate_' ])
register_prefix('selected_idle_', 5)
register_prefix('selected_insensitive_', 5)
register_prefix('selected_', 4)
register_prefix('activate_', 3)
register_prefix('hover_', 2, [ 'activate_' ])
register_prefix('idle_', 2)
register_prefix('insensitive_', 2)
register_prefix('', 1)

# A map of properties that we know about. The properties may take a
# function that is called on the argument.
style_properties = dict(
    antialias = None,
    background = renpy.easy.displayable,
    bar_invert = None,
    bar_vertical = None,
    black_color = renpy.easy.color,
    bold = None,
    bottom_bar = renpy.easy.displayable,
    bottom_gutter = None,
    bottom_margin = None,
    bottom_padding = None,
    box_first_spacing = None,
    box_layout = None,
    box_spacing = None,
    clipping = None,
    color = renpy.easy.color,
    drop_shadow = None,
    drop_shadow_color = renpy.easy.color,
    enable_hover = None, # Doesn't do anything anymore.
    first_indent = None,
    focus_mask = None,
    focus_rect = None,
    font = None,
    sound = None,
    italic = None,
    initial_time_offset = None,
    layout = None,
    left_bar = renpy.easy.displayable,
    left_gutter = None,
    left_margin = None,
    left_padding = None,
    line_spacing = None,
    min_width = None,
    rest_indent = None,
    right_bar = renpy.easy.displayable,
    right_gutter = None,
    right_margin = None,
    right_padding = None,
    size = None,
    slow_abortable = None,
    slow_cps = None,
    slow_cps_multiplier = None,
    subtitle_width = None,
    text_y_fudge = None,
    text_align = None,
    thumb = renpy.easy.displayable,
    thumb_offset = None,
    thumb_shadow = renpy.easy.displayable,
    top_bar = renpy.easy.displayable,
    top_gutter = None,
    top_margin = None,
    top_padding = None,
    underline = None,
    xanchor = None,
    xfill = None,
    xmaximum = None,
    xminimum = None,
    xoffset = None,
    xpos = None,
    yanchor = None,
    yfill = None,
    ymaximum = None,
    yminimum = None,
    yoffset = None,
    ypos = None,
    )

substitutes = dict(
    xmargin = [ 'left_margin', 'right_margin' ],
    ymargin = [ 'top_margin', 'bottom_margin' ],
    xalign = [ 'xpos', 'xanchor' ],
    yalign = [ 'ypos', 'yanchor' ],
    xpadding = [ 'left_padding', 'right_padding' ],
    ypadding = [ 'top_padding', 'bottom_padding' ],
    minwidth = [ 'min_width' ],
    textalign = [ 'text_align' ],
    slow_speed = [ 'slow_cps' ],
    )

# Map from property to number.
property_number = { }

# Map from prefix to offset.
prefix_offset = { }

# Map from prefix_property to prefix offset + property number.
prefixed_property_number = { }

# The total number of property numbers out there.
property_numbers = 0

# This is a function, to prevent namespace pollution. It's called
# once at module load time.
def init():

    global property_numbers
    
    # Expand out substitutes:
    for k in substitutes.keys():
        for p in prefixes:
            substitutes[p + k] = [ p + i for i in substitutes[k] ]

    # Figure out a map from style property name to an (arbitrary,
    # session-specific) style property number.
    for i, p in enumerate(style_properties):
        property_number[p] = i

    # Figure out a map from style prefix to style property number offset.
    property_numbers = 0    
    for r in roles:
        for p in prefixes:
            prefix_offset[r + p] = property_numbers
            property_numbers += len(style_properties)

    # Figure out a map from prefixed property to number.
    for prefix, prefixn in prefix_offset.iteritems():
        for prop, propn in property_number.iteritems():
            prefixed_property_number[prefix + prop] = prefixn + propn

init()
            
# A map from a style name to the style associated with that name.
style_map = { }

# A map from a style name to the style proxy associated with that name.
style_proxy_map = { }

# True if we have expanded all of the style caches, False otherwise.
styles_built = False

# A list of styles that are pending expansion.
styles_pending = [ ]

def reset():
    """
    This resets all of the data structures associated with style
    management.
    """

    global style_map
    global style_proxy_map
    global styles_built
    global styles_pending
    global style_info 
    
    style_map = { }
    style_proxy_map = { }
    styles_built = False
    styles_pending = [ ]

class StyleManager(object):
    """
    This is the singleton object that is exported into the store
    as style
    """

    def __getattr__(self, name):
        try:
            return style_proxy_map[name]
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

        s = Style(parent, { })        
        style_map[name] = s
        style_proxy_map[name] = StyleProxy(s)

    def exists(self, name):
        """
        This determines if the named style exists.
        """
        
        return name in style_map

def expand_properties(properties):

    rv = [ ]

    for prop, val in properties.iteritems():


        for prefix, plen, prio, alts in prefix_subs:

            # This will always terminate.
            if prop.startswith(prefix):
                break

        # We use the values of plen, prio, and alts.

            
        prop = prop[plen:]

        for prop in substitutes.get( prop, ( prop, )):

            try:
                func = style_properties[prop]
            except KeyError:
                if prop.startswith("activate_"):
                    continue

                if renpy.config.check_properties:
                    raise Exception("Style property %s is unknown." % prop)

                func = None


            if func:
                newval = func(val)
            else:
                newval = val

            for a in alts:
                rv.append((prio, a + prop, newval))

    # Places things in priority order... so more important properties
    # come last.
    rv.sort()
    return rv



# This builds the style. If recurse is True, this also builds the
# parent style.
def build_style(style):

    if style.parent:

        try:
            parent = style_map[style.parent]
        except:
            try:
                parent = getattr(renpy.game.style, parent)

                if isinstance(parent, StyleProxy):
                    parent = parent.target
                    
            except:
                raise Exception('Style %s is not known.' % style.parent)

        if not parent.cache:
            build_style(parent)

        cache = parent.cache[:]
    else:
        cache = [ None ] * property_numbers

    style.cache = cache
        
    # For speed, make this local.
    ppn = prefixed_property_number
    
    for k, v in style.properties.iteritems():
        cache[ppn[k]] = v

# This builds all pending styles, recursing to ensure that they are built
# in the right order.
def build_styles():

    global styles_pending
    global styles_built

    for s in styles_pending:
        build_style(s)

    styles_pending = None
    styles_built = True
        
def rebuild():

    global style_pending
    global styles_built

    styles_pending = style_map.values()
    styles_built = False
    
    for i in styles_pending:
        i.__dict__["cache"] = { }

    build_styles()

def backup():
    rv = { }
    
    for k, v in style_map.iteritems():
        rv[k] = v.properties.copy()

    return rv
        
def restore(o):
    global styles_built
    global styles_pending
    
    styles_pending = [ ]
    styles_built = False

    for k, v in o.iteritems():
        style_map[k].properties.clear()
        style_map[k].properties.update(v)
        styles_pending.append(style_map[k])

def style_metaclass(name, bases, attrs):
    
    for k, number in property_number.iteritems():
        def getter(self, number=number):
            return self.cache[self.offset + number]

        attrs[k] = property(getter)

    return type(name, bases, attrs)
    
class Style(object):

    __metaclass__ = style_metaclass
    
    def __getstate__(self):

        rv = self.__dict__.copy()
        rv["cache"] = [ ]
        return rv

    def __setstate__(self, state):
        vars(self).update(state)

        self.cache = [ ]
        self.offset = prefix_offset[self.prefix]

        build_style(self)

    def __init__(self, parent, properties):

        self.prefix = 'insensitive_'
        self.offset = prefix_offset['insensitive_']

        self.parent = parent
        self.cache = [ ]
        self.properties = { }
        
        if properties:
            for prio, prop, val in expand_properties(properties):
                self.properties[prop] = val

        if styles_built:
            build_style(self)
        else:
            styles_pending.append(self)

    def set_prefix(self, prefix):
        self.prefix = prefix
        self.offset = prefix_offset[prefix]
            
    def setattr(self, name, value):

        for prio, prop, val in expand_properties({ name : value }):
            self.properties[prop] = val

        if styles_built:
            build_style(self)

    def delattr(self, name):

        for prio, prop, val in expand_properties({ name : None }):
            if prop in self.properties:
                del self.properties[prop]
        
    def clear(self):
        if styles_built:
            raise Exception("Cannot clear a style after styles have been built.")
        else:
            self.properties.clear()
            
    def take(self, other):

        self.properties.update(other.properties)
        
        if styles_built:
            build_style(self)

    def setdefault(self, **properties):
        """
        This sets the default value of the given properties, if no more
        explicit values have been set.
        """

        for d, prop, val in expand_properties(properties):
            self.properties.setdefault(prop, val)
            
class StyleProxy(object):

    def __init__(self, target):
        self.__dict__["target"] = target

    def __getattr__(self, k):
        return getattr(self.target, k)
        
    def __setattr__(self, k, v):
        self.target.setattr(k, v)
        
    def __delattr__(self, k):
        self.target.delattr(k)

    def clear(self):
        self.target.clear()

    def take(self, other):
        if isinstance(other, StyleProxy):
            other = other.target

        self.target.take(other)

    def setdefault(self, **properties):
        self.target.setdefault(**properties)
            
        

def write_text(filename):

    f = file(filename, "w")

    styles = style_map.items()
    styles.sort()

    for name, sty in styles:

        print >>f, name, "inherits from", sty.parent

        props = [ (propname, sty.cache[n]) for propname, n in prefixed_property_number.iteritems() ]
        props.sort()

        for prop, val in props:

            pname = name

            while pname:
                psty = style_map[pname]

                if prop in psty.properties:
                    break
                else:
                    pname = psty.parent
 
            if pname != name:
                inherit = "(%s)" % pname
            else:
                inherit = "(****)"

            print >>f, "   ", inherit, prop, "=", repr(val)

        print >>f

    f.close()
        
    
