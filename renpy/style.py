# Copyright 2004-2006 PyTom <pytom@bishoujo.us>
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
prefixes = [ 'hover_', 'idle_', 'insensitive_' ]

# A list of prefix, length, priority, (tuple of prefixes).
prefix_subs = [ ]

def register_prefix(prefix, prio):

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

    alts = [ a1 + a2 for a1 in alts1 for a2 in alts2 ]

    prefix_subs.append((prefix, len(prefix), prio, alts))


register_prefix('selected_hover_', 4)
register_prefix('selected_idle_', 4)
register_prefix('selected_insensitive_', 4)
register_prefix('selected_', 3)
register_prefix('hover_', 2)
register_prefix('idle_', 2)
register_prefix('insensitive_', 2)
register_prefix('', 1)
    
# A map of properties that we know about. The properties may take a
# function that is called on the argument.
style_properties = dict(
    activate_sound = None,
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
    xpos = None,
    yanchor = None,
    yfill = None,
    ymaximum = None,
    yminimum = None,
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
            except:
                raise Exception('Style %s is not known.' % style.parent)

        if not parent.cache:
            build_style(parent)

        if not style.properties:
            style.__dict__["cache"] = parent.cache
        else:
            style.__dict__["cache"] = parent.cache.copy()
            style.cache.update(style.properties)

    else:
        style.__dict__["cache"] = style.properties

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
        
    
class Style(object):

    def __getstate__(self):

        rv = self.__dict__.copy()
        rv["cache"] = { }
        return rv

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

        if properties:
            for prio, prop, val in expand_properties(properties):
                self.properties[prop] = val

        if styles_built:
            build_style(self)
        else:
            styles_pending.append(self)

    def set_prefix(self, prefix):
        vars(self)["prefix"] = prefix
            
    def __getattr__(self, name):
        return self.cache[self.prefix + name]

    def __setattr__(self, name, value):

        for prio, prop, val in expand_properties({ name : value }):
            self.properties[prop] = val

        if styles_built:
            build_style(self)

    def __delattr__(self, name):

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


def write_text(filename):

    f = file(filename, "w")

    styles = style_map.items()
    styles.sort()

    for name, sty in styles:

        print >>f, name, "inherits from", sty.parent

        props = sty.cache.items()
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
        
    
