# Copyright 2004-2010 PyTom <pytom@bishoujo.us>
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

##############################################################################
# Data types.

class InvalidType(Exception):
    """
    An exception that is thrown when we can't parse an object of
    the expected type.
    """

# Sentinel type used for classes that do not have a default type.
NoDefault = object()

class Type(renpy.object.Object):
    """
    Base class for types.
    """

    default = NoDefault

    def __init__(self, l):

        try:
            self.state = self.parse(l)
        except renpy.parser.ParseError:
            if self.default:
                self.state = self.default
            else:
                raise
                
    def parse(self, l):
        """
        The parse method is responsible for parsing an expression of the given
        type. It returns some state, or raises InvalidType if it can't.
        """

        # Since most of the types are really wrappers around simple_expression,
        # we default to that.
        return l.require(l.simple_expression)
            

    def evaluate(self, state):
        """
        This is called at runtime with the result of parse, and is
        responsible for returning an actual value. It can also raise
        InvalidType if the expression does not return the appropriate
        type.
        """

        raise NotImplemented

    def get_value(self):
        return self.evaluate(self.state)
    
    
class IntegerLiteral(Type):
    def parse(self, l):
        return l.require(l.integer)

    def evaluate(self, state):
        return state

class OptionalIntegerLiteral(Type):
    def parse(self, l):
        return l.integer()

    def evaluate(self, state):
        return state
    
class Name(Type):
    def parse(self, l):
        return l.require(l.name)

    def evaluate(self, state):
        return state

class NameList(Type):
    def parse(self, l):
        rv = [ ]

        rv.append(l.require(l.name))

        while l.match(r','):
            rv.append(l.require(l.name))

        return rv

    def evaluate(self, state):
        return state

class Expression(Type):
    def evaluate(self, state):
        return eval(state)
    

##############################################################################
# Parsing.

class Positional(object):
    """
    This represents a positional parameter to a function.
    """

    def __init__(self, name, type=Expression, help=None):
        self.name = name
        self.type = type
        self.help = help

class Keyword(object):
    """
    This represents an optional keyword parameter to a function.
    """
    
    def __init__(self, name, type=Expression, help=None):
        self.name = name
        self.type = type
        self.help = help
        self.style = False
        
class Style(object):
    """
    This represents a style parameter to a function.
    """

    def __init__(self, name, type=Expression, help=None):
        self.name = name
        self.type = type
        self.help = help
        self.style = True
        
class Parser(object):
    """
    This represents a parser.
    """
        
class FunctionStatementParser(Parser):
    """
    This is responsible for parsing function statements.
    """

    def __init__(self, name, function, close_function=None, pass_children=False):

        # The name of this statement. Also, the keyword that introduces
        # this statement.
        self.name = name
        
        # Functions that are called when this statement runs.
        self.function = function
        self.close_function = close_function

        # True if the children should be passed into the function as an
        # argument. False if they should be run.
        self.pass_children = pass_children
        
        # The positional arguments, keyword arguments, and child
        # statements.
        self.positional = [ ]
        self.keyword = { }
        self.children = { }

        # A list of keyword arguments and styles. Used to generate
        # help.
        self.original_keyword = [ ]
        
        
    def add(self, i):
        """
        Adds a clause to this parser.
        """

        if isinstance(i, list):
            for j in i:
                self.add(j)

            return
        
        if isinstance(i, Positional):
            self.positional.append(i)

        elif isinstance(i, Keyword):
            self.original_keyword.append(i)
            self.keyword[i.name] = i                

        elif isinstance(i, Style):
            self.original_keyword.append(i)

            for j in renpy.style.prefix_subs:
                self.keyword[j + i.name] = i

        elif isinstance(i, Parser):
            self.children[i.name] = i

            
    def parse(self, l):
        """
        Parses this statement (and the associated block) into a
        FunctionStatement object.
        """

        # These are used to store the various arguments as they come in.        
        positional = [ ]
        keyword = { }
        children = [ ]


        # Parses a keyword argument from the lexer.
        def parse_keyword(l):
            name = l.word()

            if not Name:
                l.error('expected a keyword argument, colon, or end of line.')
            
            if name not in self.keyword:
                l.error('%r is not a keyword argument or valid child for the %s statement.' % (name, self.name))
            
            if name in keyword:
                l.error('keyword argument %r appears more than once in a %s statement.' % (name, self.name))

            keyword[name] = self.keyword[name].type(l)
        
        # We assume that the initial keyword has been parsed already,
        # so we start with the positional arguments.

        for i in self.positional:
            positional.append(i.type(l))

        # Next, we allow keyword arguments on the starting line.
        while True:
            if l.match(':'):
                l.expect_eol()
                l.expect_block(self.name)
                block = True
                break

            if l.eol():
                l.expect_noblock(self.name)
                block = False
                break

            parse_keyword(l)

        # If we have a block, then parse each line.
        if block:

            l = l.subblock_lexer()

            while l.advance():

                state = l.checkpoint()

                word = l.word()
                if word and word in self.children:
                    c = self.children[word].parse(l)
                    children.append(c)
                    continue

                l.revert(state)

                while not l.eol():
                    parse_keyword(l)

        return FunctionStatement(self.function, self.close_function, positional, keyword, children, self.pass_children)
                    

class FunctionStatement(object):
    def __init__(self, function, close_function, positional, keyword, children, pass_children):
        self.function = function
        self.close_function = close_function
        self.positional = positional
        self.keyword = keyword
        self.children = children
        self.pass_children = pass_children

                
    def evaluate(self):

        positional = [ i.get_value() for i in self.positional ]
        keyword = dict((k, v.get_value()) for k, v in self.keyword.iteritems())

        if self.pass_children:
            keyword['children'] = self.children

        rv = self.function(*positional, **keyword)

        if not self.pass_children:
            for i in self.children:
                i.evaluate()

        if self.close_function:
            self.close_function()
            
        return rv
        

##############################################################################
# Definitions of screen language statements.

# Used to allow statements to take styles.
styles = [ ]

position_styles = [ Style(i, Expression) for i in [
        "anchor",
        "xanchor",
        "yanchor",
        "pos",
        "xpos",
        "ypos",
        "align",
        "xalign",
        "yalign",
        "xoffset",
        "yoffset",
        "area",
        ] ]

text_styles = [ Style(i, Expression) for i in [
        "antialias",
        "black_color",
        "bold",
        "color",
        "drop_shadow",
        "drop_shadow_color",
        "first_indent",
        "font",
        "size",
        "italic",
        "justify",
        "language",
        "layout",
        "line_spacing",
        "minwidth",
        "min_width",
        "outlines",
        "rest_indent",
        "slow_cps",
        "slow_cps_multiplier",
        "slow_abortable",
        "text_align",
        "text_y_fudge",
        "underline",
        "xmaximum",
        "ymaximum",
        "xminimum",
        "yminimum",
        "xfill",
        "yfill",
        "clipping",
        ] ]

window_styles = [ Style(i, Expression) for i in [
        "background",
        "foreground",
        "left_margin",
        "right_margin",
        "bottom_margin",
        "top_margin",
        "xmargin",
        "ymargin",
        "left_padding",
        "right_padding",
        "top_padding",
        "bottom_padding",
        "xpadding",
        "ypadding",
        "side_group",
        ] ]

button_properties = [ Style(i, Expression) for i in [
        "sound",
        "focus_mask",
        "focus_rect",
        "time_policy",
        "child",
        "mouse",
        ] ]

bar_properties = [ Style(i, Expression) for i in [
        "bar_vertical",
        "bar_invert"
        "bar_resizing",
        "left_gutter",
        "right_gutter",
        "top_gutter",
        "bottom_gutter",
        "left_bar",
        "right_bar",
        "top_bar",
        "bottom_bar",
        "thumb",
        "thumb_shadow",
        "unscrollable",
        ] ]

box_properties = [ Style(i, Expression) for i in [
        "box_layout",
        "spacing",
        "first_spacing",
        ] ]


    

def pass_function():
    pass

pass_stmt = FunctionStatementParser("pass", pass_function)

statements = [
    pass_stmt,
    ]


##############################################################################
# Definition of the screen statement.

def screen_function(priority, name, children=[]):
    print "Creating new screen: priority", priority, "name", name

screen_stmt = FunctionStatementParser("screen", screen_function)
screen_stmt.add(Positional("priority", OptionalIntegerLiteral, "If this screen statement is not inside an init block, and a name is given, it is placed into an init block with this priority. Defaults to 0."))
screen_stmt.add(Positional("name", Name, "The name of the screen being defined."))

screen_stmt.add(statements)



def parse_screen(l):
    """
    Parses the screen statement.
    """

    return screen_stmt.parse(l).evaluate()
    
        
