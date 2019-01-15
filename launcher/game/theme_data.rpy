# Copyright 2004-2019 Tom Rothamel <pytom@bishoujo.us>
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

init python in theme_data:

    def __PerformScreenOperations(lines, file_picker_rows=5, file_picker_cols=2):

        import re

        x = 0
        correct_section = False

        while x < len(lines):
            l = lines[x]

            m = re.match(r'^screen\s+\w+\s*:\s*$', l)
            if m:
                correct_section = False

            m = re.match(r'^screen\s+file_picker\s*:\s*$', l)
            if m:
                correct_section = True

            if correct_section:
                m = re.match(r'^\s+\$\s*columns\s*=\s*(\d+)\s*$', l)
                if m:
                    l = l.replace(str(m.group(1)), str(file_picker_cols))
                m = re.match(r'^\s+\$\s*rows\s*=\s*(\d+)\s*$', l)
                if m:
                    l = l.replace(str(m.group(1)), str(file_picker_rows))

            lines[x] = l

            x = x + 1

        return lines

    def roundrect_screen_ops(lines):
        return __PerformScreenOperations(lines)

    def awt_screen_ops(lines):
        return __PerformScreenOperations(lines, file_picker_rows=3)




    # theme name -> (color scheme name -> code that implements it)
    THEME = { }

    # The set of theme functions.
    THEME_FUNCTIONS = set()

    # theme name -> function name to call to munge screens.rpy as appropriate
    # for that theme.
    THEME_SCREEN_OPERATIONS = { }

    # Color schemes that work (technically - some are eye-melting) with the
    # roundrect-style themes.
    ROUNDRECT_SCHEMES = {
        'Basic Blue': {'disabled': '#404040',
                       'disabled_text': '#c8c8c8',
                       'frame': '#6496c8',
                       'gm_root': '#dcebff',
                       'label': '#ffffff',
                       'mm_root': '#dcebff',
                       'widget': '#003c78',
                       'widget_hover': '#0050a0',
                       'widget_selected': '#ffffc8',
                       'widget_text': '#c8ffff'},
        'Bloody Mary': {'disabled': '#400000',
                        'disabled_text': '#260000',
                        'frame': '#400808',
                        'gm_root': '#000000',
                        'label': '#ffffff',
                        'mm_root': '#000000',
                        'widget': '#000000',
                        'widget_hover': '#830000',
                        'widget_selected': '#ffffff',
                        'widget_text': '#C2C2C2'},
        'Colorblind': {'disabled': '#898989',
                       'disabled_text': '#666666',
                       'frame': '#252525',
                       'gm_root': '#393939',
                       'label': '#c2c2c2',
                       'mm_root': '#393939',
                       'widget': '#898989',
                       'widget_hover': '#464646',
                       'widget_selected': '#F2F2F2',
                       'widget_text': '#CCCCCC'},
        'Cotton Candy': {'disabled': '#C8AFA1',
                         'disabled_text': '#E1D4C9',
                         'frame': '#FCF5F2',
                         'gm_root': '#D0B4BA',
                         'label': '#805C40',
                         'mm_root': '#D0B4BA',
                         'widget': '#ECC7D0',
                         'widget_hover': '#E1D4C9',
                         'widget_selected': '#805C40',
                         'widget_text': '#805C40'},
        'Creamsicle': {'disabled': '#FFECBF',
                       'disabled_text': '#ffffff',
                       'frame': '#FFECBF',
                       'gm_root': '#FDF5E3',
                       'label': '#502F13',
                       'mm_root': '#FDF5E3',
                       'widget': '#D96B00',
                       'widget_hover': '#FD9B1C',
                       'widget_selected': '#ffffff',
                       'widget_text': '#FCE6B1'},
        'Dramatic Flesh': {'disabled': '#ab6038',
                           'disabled_text': '#BF7C51',
                           'frame': '#49271b',
                           'gm_root': '#2a201f',
                           'label': '#ffffff',
                           'mm_root': '#2a201f',
                           'widget': '#BF7C51',
                           'widget_hover': '#dda570',
                           'widget_selected': '#ffffff',
                           'widget_text': '#E5DFDF'},
        'Easter Baby': {'disabled': '#DDE9FF',
                        'disabled_text': '#A6AFBF',
                        'frame': '#CCF8DC',
                        'gm_root': '#FBF9DF',
                        'label': '#698071',
                        'mm_root': '#FBF9DF',
                        'widget': '#F5D4EE',
                        'widget_hover': '#F0DDFF',
                        'widget_selected': '#000000',
                        'widget_text': '#698071'},
        'Favorite Jeans': {'disabled': '#919994',
                           'disabled_text': '#B6BFB9',
                           'frame': '#6f7571',
                           'gm_root': '#b0b8ba',
                           'label': '#ffffff',
                           'mm_root': '#b0b8ba',
                           'widget': '#8699a7',
                           'widget_hover': '#9eb1ad',
                           'widget_selected': '#ffffff',
                           'widget_text': '#dcdfd6'},
        'Fine China': {'disabled': '#ADB9CC',
                       'disabled_text': '#DFBA14',
                       'frame': '#ADB9CC',
                       'gm_root': '#F7F7FA',
                       'label': '#39435E',
                       'mm_root': '#F7F7FA',
                       'widget': '#6A7183',
                       'widget_hover': '#1A2B47',
                       'widget_selected': '#E3E3E4',
                       'widget_text': '#C9C9CB'},
        'First Valentines': {'disabled': '#F8F2D0',
                             'disabled_text': '#BFA1A1',
                             'frame': '#F8F2D0',
                             'gm_root': '#D98989',
                             'label': '#5D1010',
                             'mm_root': '#D98989',
                             'widget': '#F09898',
                             'widget_hover': '#D6C5BB',
                             'widget_selected': '#B31E1E',
                             'widget_text': '#593131'},
        'Ice Queen': {'disabled': '#F0F2F2',
                      'disabled_text': '#FBFBFB',
                      'frame': '#ffffff',
                      'gm_root': '#E6E6E6',
                      'label': '#D9D9D9',
                      'mm_root': '#E6E6E6',
                      'widget': '#D9D9D9',
                      'widget_hover': '#F0F2F2',
                      'widget_selected': '#737373',
                      'widget_text': '#ffffff'},
        'Mocha Latte': {'disabled': '#614D3A',
                        'disabled_text': '#80654D',
                        'frame': '#926841',
                        'gm_root': '#1A140E',
                        'label': '#F1EBE5',
                        'mm_root': '#1A140E',
                        'widget': '#4D3B29',
                        'widget_hover': '#996E45',
                        'widget_selected': '#ffffff',
                        'widget_text': '#B99D83'},
        'Muted Horror': {'disabled': '#73735C',
                         'disabled_text': '#8C8C70',
                         'frame': '#555544',
                         'gm_root': '#1A0001',
                         'label': '#1A0001',
                         'mm_root': '#1A0001',
                         'widget': '#777777',
                         'widget_hover': '#73735C',
                         'widget_selected': '#000000',
                         'widget_text': '#404033'},
        'Old Polaroid': {'disabled': '#A89E7D',
                         'disabled_text': '#CCC097',
                         'frame': '#49403E',
                         'gm_root': '#A84A3E',
                         'label': '#ffffff',
                         'mm_root': '#A84A3E',
                         'widget': '#A89E7D',
                         'widget_hover': '#8DB6B9',
                         'widget_selected': '#ffffff',
                         'widget_text': '#49403E'},
        'Really Red': {'disabled': '#404040',
                       'disabled_text': '#c8c8c8',
                       'frame': '#e17373',
                       'gm_root': '#ffd0d0',
                       'label': '#ffffff',
                       'mm_root': '#ffd0d0',
                       'widget': '#963232',
                       'widget_hover': '#c83232',
                       'widget_selected': '#ffffc8',
                       'widget_text': '#ffffff'},
        'Summer Sky': {'disabled': '#6074BF',
                       'disabled_text': '#7383BF',
                       'frame': '#6074BF',
                       'gm_root': '#B4CDD4',
                       'label': '#94C7D4',
                       'mm_root': '#B4CDD4',
                       'widget': '#F2E6AA',
                       'widget_hover': '#FCFCA4',
                       'widget_selected': '#1A5766',
                       'widget_text': '#7DA8B3'},
        'Swamp Critter': {'disabled': '#A2521D',
                          'disabled_text': '#753D00',
                          'frame': '#797C1C',
                          'gm_root': '#B09D5A',
                          'label': '#ffffff',
                          'mm_root': '#B09B4F',
                          'widget': '#753D00',
                          'widget_hover': '#B19A48',
                          'widget_selected': '#ffffff',
                          'widget_text': '#CCCAC2'},
        'Urban Sprawl': {'disabled': '#8F0000',
                         'disabled_text': '#333333',
                         'frame': '#8F0000',
                         'gm_root': '#000000',
                         'label': '#ffffff',
                         'mm_root': '#000000',
                         'widget': '#333333',
                         'widget_hover': '#000000',
                         'widget_selected': '#ffffff',
                         'widget_text': '#6C8A2F'},
        'Victorian Gingerbread': {'disabled': '#7A674F',
                                  'disabled_text': '#664F33',
                                  'frame': '#BF8A73',
                                  'gm_root': '#695640',
                                  'label': '#F2EDC4',
                                  'mm_root': '#695640',
                                  'widget': '#7A674F',
                                  'widget_hover': '#BDA77D',
                                  'widget_selected': '#FDFBEE',
                                  'widget_text': '#F2EDC4'},
        'Watermelon Pie': {'disabled': '#FABF46',
                           'disabled_text': '#FFE06D',
                           'frame': '#C3CD91',
                           'gm_root': '#F7F7C5',
                           'label': '#FCFCD7',
                           'mm_root': '#F7F7C5',
                           'widget': '#FFE06D',
                           'widget_hover': '#E38A4F',
                           'widget_selected': '#996600',
                           'widget_text': '#FAA700'},
        'White Chocolate': {'disabled': '#614D3A',
                            'disabled_text': '#80654D',
                            'frame': '#926841',
                            'gm_root': '#FBF9EA',
                            'label': '#F1EBE5',
                            'mm_root': '#FBF9EA',
                            'widget': '#33271C',
                            'widget_hover': '#ECE7C4',
                            'widget_selected': '#ffffff',
                            'widget_text': '#B99D83'},
        'Winter Mint': {'disabled': '#426143',
                        'disabled_text': '#819981',
                        'frame': '#245536',
                        'gm_root': '#e5f1e5',
                        'label': '#ffffff',
                        'mm_root': '#e5f1e5',
                        'widget': '#7AA27B',
                        'widget_hover': '#A3C7A3',
                        'widget_selected': '#ffffff',
                        'widget_text': '#CDE0CE'},
       'Mint Chocolate': {'disabled': '#ffe69c',
                       'disabled_text': '#ddbc7e',
                       'frame': '#8ab395',
                       'gm_root': '#7a4229',
                       'label': '#7a4229',
                       'mm_root': '#7a4229',
                       'widget': '#ffe69c',
                       'widget_hover': '#f5c153',
                       'widget_selected': '#7a4229',
                       'widget_text': '#b5743a'},
       'Parachute Pants': {'disabled': '#53c7bb',
                       'disabled_text': '#97d7bd',
                       'frame': '#457b9f',
                       'gm_root': '#37397f',
                       'label': '#cce2ae',
                       'mm_root': '#37397f',
                       'widget': '#53c7bb',
                       'widget_hover': '#97d7bd',
                       'widget_selected': '#37397f',
                       'widget_text': '#457b9f'},
       'Strawberry Orchard': {'disabled': '#b3c292',
                       'disabled_text': '#525748',
                       'frame': '#d8ebae',
                       'gm_root': '#e7f3cb',
                       'label': '#525748',
                       'mm_root': '#e7f3cb',
                       'widget': '#525748',
                       'widget_hover': '#f45c73',
                       'widget_selected': '#ffce95',
                       'widget_text': '#e7f3cb'},
       'Grape Jelly': {'disabled': '#81859a',
                       'disabled_text': '#5e2862',
                       'frame': '#8ea9b0',
                       'gm_root': '#5e2862',
                       'label': '#ffffff',
                       'mm_root': '#5e2862',
                       'widget': '#c45693',
                       'widget_hover': '#5e2862',
                       'widget_selected': '#e59eae',
                       'widget_text': '#ffffff'},
       'Dreamscape': {'disabled': '#966077',
                       'disabled_text': '#c75f77',
                       'frame': '#836177',
                       'gm_root': '#c75f77',
                       'label': '#fefab6',
                       'mm_root': '#c75f77',
                       'widget': '#77a493',
                       'widget_hover': '#8accb3',
                       'widget_selected': '#c75f77',
                       'widget_text': '#ffffff'},
       'Unrequited Love': {'disabled': '#dbe4dd',
                       'disabled_text': '#bd9ca9',
                       'frame': '#fffeed',
                       'gm_root': '#b38698',
                       'label': '#23000e',
                       'mm_root': '#b38698',
                       'widget': '#7fa1b3',
                       'widget_hover': '#b38698',
                       'widget_selected': '#fffeed',
                       'widget_text': '#ffffff'},

       'Watermelon': {'disabled': '#f9cdad',
                       'disabled_text': '#fc9d9a',
                       'frame': '#f9cdad',
                       'gm_root': '#83af9b',
                       'label': '#fe4365',
                       'mm_root': '#83af9b',
                       'widget': '#fc9d9a',
                       'widget_hover': '#fe4365',
                       'widget_selected': '#e5fcc2',
                       'widget_text': '#ffffff'},
       'City Lights': {'disabled': '#638e89',
                       'disabled_text': '#594f4f',
                       'frame': '#547980',
                       'gm_root': '#594f4f',
                       'label': '#e5fcc2',
                       'mm_root': '#594f4f',
                       'widget': '#45ada8',
                       'widget_hover': '#2e5860',
                       'widget_selected': '#e5fcc2',
                       'widget_text': '#9de0ad'},
       'Vampire Bite': {'disabled': '#971140',
                       'disabled_text': '#bd4b40',
                       'frame': '#bd1550',
                       'gm_root': '#490a3d',
                       'label': '#f8ca00',
                       'mm_root': '#490a3d',
                       'widget': '#e97f02',
                       'widget_hover': '#f5a240',
                       'widget_selected': '#490a3d',
                       'widget_text': '#bd1550'},
        'Underground Rave': {'disabled': '#57cdff',
                       'disabled_text': '#717be5',
                       'frame': '#04b4ff',
                       'gm_root': '#cd249b',
                       'label': '#000000',
                       'mm_root': '#cd249b',
                       'widget': '#8833ce',
                       'widget_hover': '#cd249b',
                       'widget_selected': '#b6d754',
                       'widget_text': '#000000'},
       'Tree Frog': {'disabled': '#ffffff',
                       'disabled_text': '#1c140d',
                       'frame': '#cbe86b',
                       'gm_root': '#ffffff',
                       'label': '#1c140d',
                       'mm_root': '#ffffff',
                       'widget': '#1c140d',
                       'widget_hover': '#86827e',
                       'widget_selected': '#f2e9e1',
                       'widget_text': '#cbe86b'},
       'Sun Kissed': {'disabled': '#ffffff',
                       'disabled_text': '#ec4c51',
                       'frame': '#f0874d',
                       'gm_root': '#f8c821',
                       'label': '#ffffff',
                       'mm_root': '#f8c821',
                       'widget': '#ec4c51',
                       'widget_hover': '#dc454a',
                       'widget_selected': '#f8c821',
                       'widget_text': '#ffffff'},
       'Vintage Faded': {'disabled': '#b17d6f',
                       'disabled_text': '#8c4e3d',
                       'frame': '#ab7464',
                       'gm_root': '#935844',
                       'label': '#f7d3c8',
                       'mm_root': '#935844',
                       'widget': '#8c4e3d',
                       'widget_hover': '#734032',
                       'widget_selected': '#fcf5ed',
                       'widget_text': '#e2b9ad'},
       'Vintage': {'disabled': '#883e35',
                       'disabled_text': '#b86258',
                       'frame': '#b86258',
                       'gm_root': '#a24637',
                       'label': '#ffffff',
                       'mm_root': '#a24637',
                       'widget': '#6c2921',
                       'widget_hover': '#832f26',
                       'widget_selected': '#ffc7c0',
                       'widget_text': '#fff4eb'},
       'Earth Tones': {'disabled': '#12612f',
                       'disabled_text': '#2c6e44',
                       'frame': '#00551f',
                       'gm_root': '#6b4a27',
                       'label': '#ffffff',
                       'mm_root': '#568153',
                       'widget': '#ad8c31',
                       'widget_hover': '#568153',
                       'widget_selected': '#f2edc4',
                       'widget_text': '#ffffff'},
       'Kindergarten': {'disabled': '#1ca4b2',
                       'disabled_text': '#22d5b3',
                       'frame': '#22d5b3',
                       'gm_root': '#ffeca6',
                       'label': '#ffffff',
                       'mm_root': '#ffeca6',
                       'widget': '#1781b1',
                       'widget_hover': '#12678e',
                       'widget_selected': '#f2edc4',
                       'widget_text': '#fdfbee'},
       'Phone Operator': {'disabled': '#929292',
                       'disabled_text': '#ababab',
                       'frame': '#d2d2d2',
                       'gm_root': '#59667a',
                       'label': '#343e4d',
                       'mm_root': '#59667a',
                       'widget': '#59667a',
                       'widget_hover': '#343e4d',
                       'widget_selected': '#bed4f6',
                       'widget_text': '#ffffff'},
                        }

    ROUNDRECT_VARIANTS = [
        ("Roundrect", "roundrect"),
        ("Bordered", "bordered"),
        ("Diamond", "diamond"),
        ("Regal", "regal"),
        ("Austen", "austen"),
        ("TV", "tv"),
        ("3D", "threeD"),
        ("Glow", "glow"),
        ("Marker", "marker"),
        ("Crayon", "crayon"),
       ]

    ROUNDRECT_CODE = """theme.%(function)s(
        ## Theme: %(theme)s
        ## Color scheme: %(scheme)s

        ## The color of an idle widget face.
        widget = "%(widget)s",

        ## The color of a focused widget face.
        widget_hover = "%(widget_hover)s",

        ## The color of the text in a widget.
        widget_text = "%(widget_text)s",

        ## The color of the text in a selected widget. (For
        ## example, the current value of a preference.)
        widget_selected = "%(widget_selected)s",

        ## The color of a disabled widget face.
        disabled = "%(disabled)s",

        ## The color of disabled widget text.
        disabled_text = "%(disabled_text)s",

        ## The color of informational labels.
        label = "%(label)s",

        ## The color of a frame containing widgets.
        frame = "%(frame)s",

        ## The background of the main menu. This can be a color
        ## beginning with '#', or an image filename. The latter
        ## should take up the full height and width of the screen.
        mm_root = "%(mm_root)s",

        ## The background of the game menu. This can be a color
        ## beginning with '#', or an image filename. The latter
        ## should take up the full height and width of the screen.
        gm_root = "%(gm_root)s",

        ## If this is True, the in-game window is rounded. If False,
        ## the in-game window is square.
        rounded_window = False,

        ## And we're done with the theme. The theme will customize
        ## various styles, so if we want to change them, we should
        ## do so below.
        )"""

    for theme, function in ROUNDRECT_VARIANTS:
        THEME[theme] = { }
        THEME_FUNCTIONS.add(function)
        THEME_SCREEN_OPERATIONS[theme] = roundrect_screen_ops

        for scheme, colors in ROUNDRECT_SCHEMES.iteritems():
            subs = dict(colors)
            subs["function"] = function
            subs["theme"] = theme
            subs["scheme"] = scheme

            THEME[theme][scheme] = ROUNDRECT_CODE % (subs)

    AWT_CODE = """theme.a_white_tulip(
        ## Theme: A White Tulip
        ## Scheme %(scheme)s

        ## The color of an idle widget face.
        widget = "%(widget)s",

        ## The color of a focused widget face.
        widget_hover = "%(widget_hover)s",

        ## The color of the text in a selected widget. (For
        ## example, the current value of a preference.)
        widget_selected = "%(widget_selected)s",

        ## The color of a disabled widget face.
        disabled = "%(disabled)s",

        ## The color of a frame containing widgets.
        frame = "%(frame)s",

        ## The background of the main menu. This can be a color
        ## beginning with '#', or an image filename. The latter
        ## should take up the full height and width of the screen.
        mm_root = "%(mm_root)s",

        ## The background of the game menu. This can be a color
        ## beginning with '#', or an image filename. The latter
        ## should take up the full height and width of the screen.
        gm_root = "%(gm_root)s",

        ## The fonts used by this theme. The default fonts may not be
        ## suitable for non-English languages.
        regular_font = "_theme_awt/Quicksand-Regular.ttf",
        bold_font = "_theme_awt/Quicksand-Bold.ttf",

        ## And we're done with the theme. The theme will customize
        ## various styles, so if we want to change them, we should
        ## do so below.
        )"""

    THEME["A White Tulip"] = { }
    THEME_FUNCTIONS.add("a_white_tulip")
    THEME_SCREEN_OPERATIONS["A White Tulip"] = awt_screen_ops


    for scheme, colors in ROUNDRECT_SCHEMES.iteritems():
        subs = dict(colors)
        subs["scheme"] = scheme

        THEME["A White Tulip"][scheme] = AWT_CODE % (subs)

    THEME["A White Tulip"]["A White Tulip"] = AWT_CODE % dict(
            scheme = "A White Tulip",
            widget = "#c1c6d3",
            widget_hover = "#d7dbe5",
            widget_text = "#6b6b6b",
            widget_selected = "#c1c6d3",
            disabled = "#b4b4b4",
            disabled_text = "#6b6b6b",
            label = "#6b6b6b",
            frame = "#9391c9",
            mm_root = "#ffffff",
            gm_root = "#ffffff",
    )

