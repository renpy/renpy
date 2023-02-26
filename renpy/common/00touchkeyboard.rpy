# Copyright 2020 Sylvain Beucler
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

init -1500 python:

    import pygame_sdl2

    @renpy.pure
    class _TouchKeyboardTextInput(Action, DictEquality):
        """
        Simulate text input
        """

        def __init__(self, char):
            self.char = char

        def __call__(self):
            import pygame_sdl2
            pygame_sdl2.event.post(pygame_sdl2.event.Event(
                pygame_sdl2.TEXTINPUT,
                text=self.char))

    @renpy.pure
    class _TouchKeyboardBackspace(Action, DictEquality):
        """
         Simulate backspace
         """

        def __call__(self):
            pygame_sdl2.event.post(pygame_sdl2.event.Event(
                pygame_sdl2.KEYDOWN,
                key=pygame_sdl2.K_BACKSPACE,
                scancode=pygame_sdl2.K_BACKSPACE,
                unicode='', mod=0, repeat=False,
            ))
            pygame_sdl2.event.post(pygame_sdl2.event.Event(
                pygame_sdl2.KEYUP,
                key=pygame_sdl2.K_BACKSPACE,
                scancode=pygame_sdl2.K_BACKSPACE,
                unicode='', mod=0, repeat=False,
            ))

    @renpy.pure
    class _TouchKeyboardReturn(Action, DictEquality):
        """
         Simulate return
         """

        def __call__(self):
            import pygame_sdl2

            # avoid loop when K_RETURN activates our button
            renpy.exports.hide_screen('_touch_keyboard', layer='screens')
            renpy.restart_interaction()

            pygame_sdl2.event.post(pygame_sdl2.event.Event(
                pygame_sdl2.KEYDOWN,
                key=pygame_sdl2.K_RETURN,
                scancode=pygame_sdl2.K_RETURN,
                unicode='', mod=0, repeat=False,
            ))
            pygame_sdl2.event.post(pygame_sdl2.event.Event(
                pygame_sdl2.KEYUP,
                key=pygame_sdl2.K_RETURN,
                scancode=pygame_sdl2.K_RETURN,
                unicode='', mod=0, repeat=False,
            ))

init -1500:

    transform _touch_keyboard:
        mesh True
        alpha 0.6
        xalign 0.5

    style _touch_keyboard_button:
        hover_background "#f00"

    style _touch_keyboard_button_text:
        color "#fff"
        font "DejaVuSans.ttf"
        outlines [ (absolute(3), "#000", absolute(0), absolute(0)) ]
        size gui._scale(55)
        min_width gui._scale(55)
        textalign 0.5

    screen _touch_keyboard:
        zorder 1100
        style_prefix "_touch_keyboard"

        hbox:
            at _touch_keyboard

            grid 7 7:
                textbutton "A" action _TouchKeyboardTextInput('A')
                textbutton "B" action _TouchKeyboardTextInput('B')
                textbutton "C" action _TouchKeyboardTextInput('C')
                textbutton "D" action _TouchKeyboardTextInput('D')
                textbutton "E" action _TouchKeyboardTextInput('E')
                textbutton "F" action _TouchKeyboardTextInput('F')
                textbutton "G" action _TouchKeyboardTextInput('G')

                textbutton "H" action _TouchKeyboardTextInput('H')
                textbutton "I" action _TouchKeyboardTextInput('I')
                textbutton "J" action _TouchKeyboardTextInput('J')
                textbutton "K" action _TouchKeyboardTextInput('K')
                textbutton "L" action _TouchKeyboardTextInput('L')
                textbutton "M" action _TouchKeyboardTextInput('M')
                textbutton "N" action _TouchKeyboardTextInput('N')

                textbutton "O" action _TouchKeyboardTextInput('O')
                textbutton "P" action _TouchKeyboardTextInput('P')
                textbutton "Q" action _TouchKeyboardTextInput('Q')
                textbutton "R" action _TouchKeyboardTextInput('R')
                textbutton "S" action _TouchKeyboardTextInput('S')
                textbutton "T" action _TouchKeyboardTextInput('T')
                textbutton "U" action _TouchKeyboardTextInput('U')

                textbutton "V" action _TouchKeyboardTextInput('V')
                textbutton "W" action _TouchKeyboardTextInput('W')
                textbutton "X" action _TouchKeyboardTextInput('X')
                textbutton "Y" action _TouchKeyboardTextInput('Y')
                textbutton "Z" action _TouchKeyboardTextInput('Z')
                null
                null

                textbutton "+" action _TouchKeyboardTextInput('+')
                textbutton "-" action _TouchKeyboardTextInput('-')
                textbutton "0" action _TouchKeyboardTextInput('0')
                textbutton "1" action _TouchKeyboardTextInput('1')
                textbutton "2" action _TouchKeyboardTextInput('2')
                textbutton "3" action _TouchKeyboardTextInput('3')
                textbutton "4" action _TouchKeyboardTextInput('4')

                textbutton "*" action _TouchKeyboardTextInput('*')
                textbutton "/" action _TouchKeyboardTextInput('/')
                textbutton "5" action _TouchKeyboardTextInput('5')
                textbutton "6" action _TouchKeyboardTextInput('6')
                textbutton "7" action _TouchKeyboardTextInput('7')
                textbutton "8" action _TouchKeyboardTextInput('8')
                textbutton "9" action _TouchKeyboardTextInput('9')


                textbutton "#" action _TouchKeyboardTextInput('#')
                textbutton "$" action _TouchKeyboardTextInput('$')
                textbutton "=" action _TouchKeyboardTextInput('=')
                textbutton "<" action _TouchKeyboardTextInput('<')
                textbutton ">" action _TouchKeyboardTextInput('>')
                textbutton "_" action _TouchKeyboardTextInput('_')
                null

            null width 30

            grid 7 7:
                textbutton "a"  action _TouchKeyboardTextInput('a')
                textbutton "b"  action _TouchKeyboardTextInput('b')
                textbutton "c"  action _TouchKeyboardTextInput('c')
                textbutton "d"  action _TouchKeyboardTextInput('d')
                textbutton "e"  action _TouchKeyboardTextInput('e')
                textbutton "f"  action _TouchKeyboardTextInput('f')
                textbutton "g"  action _TouchKeyboardTextInput('g')

                textbutton "h"  action _TouchKeyboardTextInput('h')
                textbutton "i"  action _TouchKeyboardTextInput('i')
                textbutton "j"  action _TouchKeyboardTextInput('j')
                textbutton "k"  action _TouchKeyboardTextInput('k')
                textbutton "l"  action _TouchKeyboardTextInput('l')
                textbutton "m"  action _TouchKeyboardTextInput('m')
                textbutton "n"  action _TouchKeyboardTextInput('n')

                textbutton "o"  action _TouchKeyboardTextInput('o')
                textbutton "p"  action _TouchKeyboardTextInput('p')
                textbutton "q"  action _TouchKeyboardTextInput('q')
                textbutton "r"  action _TouchKeyboardTextInput('r')
                textbutton "s"  action _TouchKeyboardTextInput('s')
                textbutton "t"  action _TouchKeyboardTextInput('t')
                textbutton "u"  action _TouchKeyboardTextInput('u')

                textbutton "v"  action _TouchKeyboardTextInput('v')
                textbutton "w"  action _TouchKeyboardTextInput('w')
                textbutton "x"  action _TouchKeyboardTextInput('x')
                textbutton "y"  action _TouchKeyboardTextInput('y')
                textbutton "z"  action _TouchKeyboardTextInput('z')
                null
                null

                textbutton "|"  action _TouchKeyboardTextInput('|')
                textbutton "~"  action _TouchKeyboardTextInput('~')
                textbutton "%"  action _TouchKeyboardTextInput('%')
                textbutton "&"  action _TouchKeyboardTextInput('&')
                textbutton "@"  action _TouchKeyboardTextInput('@')
                textbutton "("  action _TouchKeyboardTextInput('(')
                textbutton ")"  action _TouchKeyboardTextInput(')')


                textbutton "."  action _TouchKeyboardTextInput('.')
                textbutton "!"  action _TouchKeyboardTextInput('!')
                textbutton ":"  action _TouchKeyboardTextInput(':')
                textbutton ";"  action _TouchKeyboardTextInput(';')
                textbutton "\"" action _TouchKeyboardTextInput('\"')
                null
                null

                textbutton "␣"  action _TouchKeyboardTextInput(' ')
                null
                null
                textbutton "←"  action _TouchKeyboardBackspace()
                null
                null
                textbutton "⏎"  action _TouchKeyboardReturn()
