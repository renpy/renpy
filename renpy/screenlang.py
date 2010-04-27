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
            

    def evaluate(self, state, context):
        """
        This is called at runtime with the result of parse, and is
        responsible for returning an actual value. It can also raise
        InvalidType if the expression does not return the appropriate
        type.
        """

        raise NotImplemented

    
class IntegerLiteral(Type):
    def parse(self, l):
        return l.require(l.integer)

    def evaluate(self, state, context):
        return state

class OptionalIntegerLiteral(Type):
    def parse(self, l):
        return l.integer()

    def evaluate(self, state, context):
        return state
    
class Name(Type):
    def parse(self, l):
        return l.require(l.name)

    def evaluate(self, state, context):
        return state

class NameList(Type):
    def parse(self, l):
        rv = [ ]

        rv.append(l.require(name))

        while l.match(r','):
            rv.append(l.require(name))

        return rv

    def evaluate(self, state, context):
        return state


class Function(Type):
    pass


##############################################################################
# Parsing.


class Positional(object):
    """
    This represents a positional parameter to a function.
    """

    def __init__(self, name, type, help):
        self.name = name
        self.type = type
        self.help = help

class Keyword(object):
    """
    This represents an optional keyword parameter to a function.
    """
    
    def __init__(self, name, type, help):
        self.name = name
        self.type = type
        self.help = help
        self.style = False
        
class Style(object):
    """
    This represents a style parapeter to a function.
    """

    def __init__(self, name, type, help):
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

    def __init__(self, name, function, takes_children):

        # The name of this statement. Also, the keyword that introduces
        # this statement.
        self.name = None
        
        # The function that is called when this statement is executed.
        self.function = function

        # True if the function takes children. False otherwise.
        self.takes_children = takes_children
        
        # The positional arguments, keyword arguments, and child
        # statements.
        self.positional = [ ]
        self.keyword = { }
        self.children = { }

        # A list of keyword arguments and styles. Used to generate
        # help.
        self.original_keyword = [ ]
        
        
    def add(self, l):
        """
        Adds a clause to this parser.
        """
        
        for i in l:        
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




class FunctionStatement(object):
    def __init__(self, function, keyword, children):
        self.function = function
        self.keyword = keyword
        self.children = children

    




def parse_screen(self):

    pass
