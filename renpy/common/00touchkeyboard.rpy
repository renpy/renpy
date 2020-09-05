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
    class _TouchWebTextInput(Action, DictEquality):
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
    class _TouchWebKeyBackspace(Action, DictEquality):
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
    class _TouchWebKeyReturn(Action, DictEquality):
        """
         Simulate return
         """

        def __call__(self):
            import pygame_sdl2

            # avoid loop when K_RETURN activates our button
            renpy.exports.hide_screen('_touchwebkeyboard', layer='screens')
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

    transform _touchwebkeyboard:
        alpha 0.5
        xalign 0.5

    style _touchwebkeyboard_button:
        color "#fff"
        hover_background "#f00"
        #xalign 0.5

    style _touchwebkeyboard_button_text:
        outlines [ (absolute(3), "#000", absolute(0), absolute(0)) ]
        size 50
        min_width 50
        text_align 0.5

    screen _touch_keyboard:
        zorder 100
        style_prefix "_touchwebkeyboard"

        hbox:
            at _touchwebkeyboard

            grid 5 9:
                textbutton "A" action _TouchWebTextInput('A')
                textbutton "B" action _TouchWebTextInput('B')
                textbutton "C" action _TouchWebTextInput('C')
                textbutton "D" action _TouchWebTextInput('D')
                textbutton "E" action _TouchWebTextInput('E')

                textbutton "F" action _TouchWebTextInput('F')
                textbutton "G" action _TouchWebTextInput('G')
                textbutton "H" action _TouchWebTextInput('H')
                textbutton "I" action _TouchWebTextInput('I')
                textbutton "J" action _TouchWebTextInput('J')

                textbutton "K" action _TouchWebTextInput('K')
                textbutton "L" action _TouchWebTextInput('L')
                textbutton "M" action _TouchWebTextInput('M')
                textbutton "N" action _TouchWebTextInput('N')
                textbutton "O" action _TouchWebTextInput('O')

                textbutton "P" action _TouchWebTextInput('P')
                textbutton "Q" action _TouchWebTextInput('Q')
                textbutton "R" action _TouchWebTextInput('R')
                textbutton "S" action _TouchWebTextInput('S')
                textbutton "T" action _TouchWebTextInput('T')

                textbutton "U" action _TouchWebTextInput('U')
                textbutton "V" action _TouchWebTextInput('V')
                textbutton "W" action _TouchWebTextInput('W')
                textbutton "X" action _TouchWebTextInput('X')
                textbutton "Y" action _TouchWebTextInput('Y')

                textbutton "Z" action _TouchWebTextInput('Z')
                textbutton "[" action _TouchWebTextInput('[')
                textbutton "]" action _TouchWebTextInput(']')
                textbutton "␣" action _TouchWebTextInput(' ')
                textbutton "_" action _TouchWebTextInput('_')

                textbutton "0" action _TouchWebTextInput('0')
                textbutton "1" action _TouchWebTextInput('1')
                textbutton "2" action _TouchWebTextInput('2')
                textbutton "3" action _TouchWebTextInput('3')
                textbutton "4" action _TouchWebTextInput('4')

                textbutton "5" action _TouchWebTextInput('5')
                textbutton "6" action _TouchWebTextInput('6')
                textbutton "7" action _TouchWebTextInput('7')
                textbutton "8" action _TouchWebTextInput('8')
                textbutton "9" action _TouchWebTextInput('9')

                textbutton "/" action _TouchWebTextInput('/')
                textbutton "=" action _TouchWebTextInput('=')
                textbutton "@" action _TouchWebTextInput('@')
                textbutton "<" action _TouchWebTextInput('<')
                textbutton ">" action _TouchWebTextInput('>')

            null width 30

            grid 5 9:
                textbutton "a"  action _TouchWebTextInput('a')
                textbutton "b"  action _TouchWebTextInput('b')
                textbutton "c"  action _TouchWebTextInput('c')
                textbutton "d"  action _TouchWebTextInput('d')
                textbutton "e"  action _TouchWebTextInput('e')

                textbutton "f"  action _TouchWebTextInput('f')
                textbutton "g"  action _TouchWebTextInput('g')
                textbutton "h"  action _TouchWebTextInput('h')
                textbutton "i"  action _TouchWebTextInput('i')
                textbutton "j"  action _TouchWebTextInput('j')

                textbutton "k"  action _TouchWebTextInput('k')
                textbutton "l"  action _TouchWebTextInput('l')
                textbutton "m"  action _TouchWebTextInput('m')
                textbutton "n"  action _TouchWebTextInput('n')
                textbutton "o"  action _TouchWebTextInput('o')

                textbutton "p"  action _TouchWebTextInput('p')
                textbutton "q"  action _TouchWebTextInput('q')
                textbutton "r"  action _TouchWebTextInput('r')
                textbutton "s"  action _TouchWebTextInput('s')
                textbutton "t"  action _TouchWebTextInput('t')

                textbutton "u"  action _TouchWebTextInput('u')
                textbutton "v"  action _TouchWebTextInput('v')
                textbutton "w"  action _TouchWebTextInput('w')
                textbutton "x"  action _TouchWebTextInput('x')
                textbutton "y"  action _TouchWebTextInput('y')

                textbutton "z"  action _TouchWebTextInput('z')
                textbutton "{{" action _TouchWebTextInput('{')
                textbutton "}"  action _TouchWebTextInput('}')
                textbutton "|"  action _TouchWebTextInput('|')
                textbutton "~"  action _TouchWebTextInput('~')

                textbutton "!"  action _TouchWebTextInput('!')
                textbutton "#"  action _TouchWebTextInput('#')
                textbutton "$"  action _TouchWebTextInput('$')
                textbutton "%"  action _TouchWebTextInput('%')
                textbutton "&"  action _TouchWebTextInput('&')

                textbutton "("  action _TouchWebTextInput('(')
                textbutton ")"  action _TouchWebTextInput(')')
                textbutton "*"  action _TouchWebTextInput('*')
                textbutton "+"  action _TouchWebTextInput('+')
                textbutton "-"  action _TouchWebTextInput('-')

                textbutton ":"  action _TouchWebTextInput(':')
                textbutton ";"  action _TouchWebTextInput(';')
                null
                textbutton "←"  action _TouchWebKeyBackspace()
                textbutton "⏎" action _TouchWebKeyReturn()
