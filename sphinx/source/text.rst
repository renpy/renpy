.. _text:

====
Text
====

Ren'Py contains several ways of displaying text. The :ref:`say <say-statement>`
and :ref:`menu <menu-statments>` are primarily concerned with the
display of text to the user. The user interface often contains text,
displayed using the :ref:`text <sl-text>`, :ref:`textbutton <sl-textbutton>`, 
and :ref:`label <sl-label>` screen language statements. These
functions, along with others, create :func:`Text` displayables, and
show them on the screen.

The Text displayable is responsible for managing the process of
showing the text to the user. The text displayable performs actions in
the following order:

1. Translating text.
2. Interpolating data into the text.
3. Styling the text using styles and text tags.
4. Laying out the styled text.
5. Drawing the text to the screen.

This chapter discusses the process of text display in Ren'Py.


Escape Characters
=================

There are three special characters that can control the way Ren'Py
displays text. A creator needs to be aware of these characters to
ensure that their writing is not accidentally misinterpreted by the engine. 

\ (backslash)
    The backslash character is used to introduce when writing a Ren'Py
    or Python string. Some common escape codes are:

    ``\"`` (backslash-doublequote)
        Includes a doublequote in a double-quoted string.

    ``\'`` (backslash-quote)
        Includes a single quote in a single-quoted string.
    
    ``\\ `` (backslash-space)
        Includes an additional space in a Ren'Py string. By default,
        Ren'Py script text collapses adjacent whitespace into a single
        space character.

    ``\n`` (backslash-n)
        Includes a newline character in the text.

    ``\\`` (backslash-backslash)
        Includes a backslash character in the text.

[ (left bracket)
    The left bracket is used to introduce interpolation of a value
    into the text. To include a single left bracket in your text,
    double it - write ``[[``.

{ (left brace)
    The left brace is used to introduce a text tag. To include a left
    brace in your text, double it - write ``{{``.

    
Interpolating Data
==================

Ren'Py supports interpolating data into the text string before it is
displayed. For example, if the player's name is stored in the
``playername`` variable, one could write a line of dialogue like::

    g "Welcome to the Nekomimi Institute, [playername]!"

Ren'Py will interpolate variables found in the global store. When
using a text widget in a screen, Ren'Py will also interpolate screen
local variables. (This can be overridden by supplying an explicit
scope argument to the Text displayable.)

Ren'Py isn't limited to interpolating simple variables. It can also
interpolate fields and components of tuples. So it's possible to have
code like::

    g "My first name is [player.names[0]]."

It's possible to apply formatting codes when displaying numbers. This
code will display a floating point number to two decimal places::

    $ percent = 100.0 * points / max_points
    g "I like you [percent:.2] percent!"

Ren'Py's string interpolation is taken from the :pep:`3101` string
formatting syntax. Ren'Py uses [ to introduce string formatting
because { was taken by text tags.

Along with the !s and !r conversion flags supported by Python, Ren'Py
supports a !q conversion flag. The !q conversion flag ensures that
text tags are properly quoted, so that displaying a string will not
introduce unwanted formatting constructs. For example::

    g "Don't pull a fast one on me, [playername!q]."


Styling and Text Tags
=====================

In Ren'Py, text gains style information in two ways. The first is from
the style that is applied to the entire block of text. Please see the
section about the :ref:`style system <styles>` for more details,
especially the section on :ref:`text style properties <text-style-properties>`.  

The second way is through text tags. Text tags are suitable for
styling a portion of text block, or a small fraction of the text
blocks in the program. If you find yourself applying the same text
tags to every line of text, consider using a style instead.

There are two text tags. Some text tags are self-closing, while others
require a closing tag. When multiple closing tags are used, they
should be closed last open, first closed order - Ren'Py will reject
incorrect nesting. For example::

    # This line is correct.
    "Plain {b}Bold {i}Bold-Italic{/i} Bold{/b} Plain"

    # This line is incorrect, and will cause an error or incorrect
    # behavior.
    "Plain {b}Bold {i}Bold-Italic{/b} Italic{/i} Plain"

Some text tags take an argument. In that case, the tag name is
followed by an equals sign (=), and the argument. The argument may
not contain the right-brace (}) character. The meaning of the
argument varies based on the text tag.

General Text Tags
-----------------

Tags that apply to all text are:

.. text-tag:: a

    The anchor tag creates a hyperlink between itself and its closing
    tag. While the behavior of the hyperlink is controlled by the
    :propref:`hyperlink_functions` style property, the default handler
    has the following behavior.

    * Hyperlinks are rendered using the ``style.hyperlink_text`` style. 

    * If the argument begins with the text ``"http://"``, clicking on
      it opens the url in a web browser. Otherwise, the argument is
      interpreted as a label, which is called in a new context. This
      allows hyperlinks to be used to define terms.

    * Apart from the change in style, there is no specific behavior
      when a hyperlink is hovered.

    ::

        label test:
    
            e "Why don't you visit {a=http://renpy.org}Ren'Py's home page{/a}?"

            e "The {a=define_trebuchet}trebuchet{/a} is at the gates."

            return
            
        label define_trebuchet:

            e "A trebuchet is a kind of siege engine."
            e "It uses a lever to fling things at targets."
            e "Like us!"
            
            return


.. text-tag:: b

    The bold tag renders the text between itself and its closing tag
    in a bold font. ::

        "An example of {b}bold test{/b}."

.. text-tag:: color

    The color text tag renders the text between itself and its closing
    tag in the specified color. The color should be in #rgb, #rgba,
    #rrggbb, or #rrggbbaa format. ::

        "{color=#f00}Red{/color}, {color=#00ff00}Green{color}, {color=#0000ffff}Blue{/color}"

.. text-tag:: cps

    The characters per second tag sets the speed of text display, for
    text between the tag and its closing tag. If the argument begins
    with an asterisk, it's taken as a multiplier to the current text
    speed. Otherwise, the argument gives the speed to show the text
    at, in characters per second. ::

        "{cps=20}Fixed Speed{/cps} {cps=*2}Double Speed{/cps}
        
.. text-tag:: font

    The font tag renders the text between itself and its closing tag
    in the specified font. The argument is the filename of the font to
    use. ::

        "Try out the {font=mikachan.ttf}mikachan font{/font}."

.. text-tag:: i

   The italics tag renders the text between itself and its closing tag
   in italics. ::

       "Visit the {i}leaning tower of Pisa{/i}."

.. text-tag:: k

   The kerning tag is a tag that adjust the kerning of characters
   between itself and its closing tag. It takes as an argument a
   floating point number giving the number of pixels of kerning to add
   to each kerning pair. (The number may be negative to decrease
   kerning.) ::

       "{k=-.5}Negative{/k} Normal {k=.5}Positive{/k}"
       
.. text-tag:: image

   The image tag is a self-closing tag that inserts an image into the
   text. The image should be the height of a single line of text. The
   argument should be either the image filename, or the name of an
   image defined with the image statement. ::

       g "Good to see you! {image=heart.png}"

.. text-tag:: s

   The strikethrough tag draws a line through text between itself and
   its closing tag. ::

       g "It's good {s}to see you{/s}."

.. text-tag:: rb

   The ruby bottom tag marks text between itself and its closing tag
   as ruby bottom text. See the section on :ref:`Ruby Text <ruby-text>` 
   for more information.

.. text-tag:: rt

   The ruby top tag marks text between itself and its closing tag as
   ruby top text. See the section on :ref:`Ruby Text <ruby-text>` for
   more information.
   
.. text-tag:: size

   The size tag changes the size of text between itself and its
   closing tag. The argument should be an integer, optionally preceded
   by + or -. If the argument is just an integer, the size is set to
   that many pixels high. Otherwise, the size is increased or
   decreased by that amount. ::

       "{size=+10}Bigger{/size} {size=-10}Smaller{/size} {size=24}24 px{/size}."

.. text-tag:: space

   The space tag is a self-closing tag that inserts horizontal space
   into a line of text. As an argument, it takes an integer giving the
   number of pixels of space to add. ::

       "Before the space.{space=30}After the space."
       
.. text-tag:: u

   The underline tag underlines the text between itself and its
   closing tag. ::

      g "It's good to {u}see{/u} you."

.. text-tag:: vspace

   The vspace tag is a self-closing tag that inserts vertical space
   between lines of text. As an argument, it takes an integer giving
   the number of pixels of space to add. ::

      "Line 1{vspace=30}Line 2"
       
        
Dialogue Text Tags
------------------

Text tags that only apply to dialogue are:

.. text-tag:: fast

    If the fast tag is displayed in a line of text, then all text
    before it is displayed instantly, even in slow text mode. The
    fast tag is a self-closing tag. ::

        g "Looks like they're{nw}"
        show trebuchet
        g "Looks like they're{fast} playing with their trebuchet again."

.. text-tag:: nw

    The no-wait tag is a self-closing tag that causes the current line
    of dialogue to automatically dismiss itself once the end of line
    has been displayed. ::

        g "Looks like they're{nw}"
        show trebuchet
        g "Looks like they're{fast} playing with their trebuchet again."

.. text-tag:: p

    The paragraph pause tag is a self-closing tag that terminates the
    current paragraph, and waits for the user to click to continue. If
    it is given an argument, the argument is interpreted as a number,
    and the wait automatically ends after that many seconds have
    passed. ::
        
        "Line 1{p}Line 2{p=1.0}Line 3"

.. text-tag:: w

    The wait tag is a self-closing tag that waits for the user to
    click to continue. If it is given an argument, the argument is
    interpreted as a number, and the wait automatically ends after
    that many seconds have passed. ::

        "Line 1{w} Line 1{w=1.0} Line 1"


User-Defined Text Tags
----------------------

Ren'Py also supports user-defined text tags. A user-defined text tag
is a text tag where the tag name is empty. In this case, the argument
is taken to be the name of a style. The text between this tag and the
closing tag has the following properties set to those defined in the
style:

* antialias
* font
* size
* bold
* italic
* underline
* strikethrough
* color
* black_color
* kerning

Slow Text Concerns
==================

Non-English Languages
=====================

Ruby Text
=========

Fonts
=====

Image-Based Fonts
-----------------


Text Displayable
================

