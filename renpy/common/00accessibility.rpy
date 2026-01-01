# Copyright 2004-2026 Tom Rothamel <pytom@bishoujo.us>
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

    ##########################################################################
    # Self-voicing

    # Strings used internally in Ren'Py.
    _("Self-voicing disabled.")
    _("Clipboard voicing enabled. ")
    _("Self-voicing enabled. ")

    _("bar")
    _("selected")
    _("viewport")
    _("horizontal scroll")
    _("vertical scroll")
    _("activate")
    _("deactivate")
    _("increase")
    _("decrease")


    # The character that's used for descriptive text.
    config.descriptive_text_character = None

    def alt(what, interact=True, **kwargs):
        """
        Uses the narrator to speak `what` if self-voicing is enabled.
        """

        if _preferences.self_voicing:

            c = config.descriptive_text_character

            if c is None:
                c = narrator

            return c(what, interact=interact, **kwargs)

    def alt_statement_name():
        if _preferences.self_voicing:
            return "say"
        else:
            return "say-condition-false"

    alt.statement_name = alt_statement_name
    del alt_statement_name

    # Old name for alt.
    sv = alt


init -1500 python:

    __font_transform_cache = { }
    "A map from a font name, base font, and list of substitutions to a FontGroup."

    def _font_transform(font, base_font, charset):
        key = (font, base_font, charset)
        rv = __font_transform_cache.get(key, None)

        if rv is not None:
            return rv

        rv = FontGroup()

        for r in charset.split():
            start, _, end = r.partition("-")
            start = int(start, 16)
            end = int(end, 16) if end else start

            rv.add(base_font, start, end)

        rv.add(font, None, None)

        store.__font_transform_cache[key] = rv
        return rv


init -1500 python hide:

    ##########################################################################
    # Font Transforms.

    store.__font_transform = { }

    def opendyslexic(f):

        # Generated with fc-query --format=%{charset} OpenDyslexic3-Regular.ttf
        # Cyrillic has been removed, as it's incomplete.
        charset = "20-7e a0-107 10a-113 116-11b 11e-123 126-12b 12e-133 136-137 139-148 14a-14d 150-15b 15e-16b 16e-17e 186 188-189 18e-192 194 197 19d 1a0-1a1 1a9 1ac 1af-1b4 1c0-1c3 1cd-1df 1e6-1e7 1fe-1ff 218-21b 228-22b 241-244 24b-24c 250-254 256-259 25b-25c 261-262 265 268 26a-26b 26f-270 272 274-276 279-27a 280-281 283 289-28a 28c-28f 294-295 298-299 29b-29c 29f 2a1-2a2 2c6-2c7 2d8-2dd 309 31b 323 326 32d 331 3b2 3b8 3c0 3c7 1e04-1e05 1e0c-1e0f 1e12-1e13 1e24-1e25 1e2e-1e2f 1e36-1e37 1e3c-1e3f 1e44-1e47 1e4a-1e4d 1e50-1e53 1e62-1e63 1e6c-1e71 1e80-1e85 1e92-1e93 1ea0-1ef9 2013-2014 2018-201a 201c-201e 2020-2022 2026 2030 2039-203a 203d 2044 20ac 2122 2126 215b-215e 2202 2206 220f 2211-2212 2219-221a 221e 222b 2248 2260 2264-2265 25ca 2c64 2c6d 2c72-2c73 2e18 fb01-fb02"
        return _font_transform(f, "_OpenDyslexic3-Regular.ttf", charset)

    config.font_transforms["opendyslexic"] = opendyslexic
    config.ftfont_scale["_OpenDyslexic3-Regular.ttf"] = .87
    config.ftfont_vertical_extent_scale["_OpenDyslexic3-Regular.ttf"] = .66

    def dejavusans(f):

        # Generated with fc-query --format=%{charset} DejaVuSans.ttf
        charset = "20-7e a0-2e9 2ec-2ee 2f3 2f7 300-34f 351-353 357-358 35a 35c-362 370-377 37a-37e 384-38a 38c 38e-3a1 3a3-525 531-556 559-55f 561-587 589-58a 5b0-5c3 5c6-5c7 5d0-5ea 5f0-5f4 606-607 609-60a 60c 615 61b 61f 621-63a 640-655 657 65a 660-670 674 679-6bf 6c6-6c8 6cb-6cc 6ce 6d0 6d5 6f0-6f9 7c0-7e7 7eb-7f5 7f8-7fa e3f e81-e82 e84 e87-e88 e8a e8d e94-e97 e99-e9f ea1-ea3 ea5 ea7 eaa-eab ead-eb9 ebb-ebd ec0-ec4 ec6 ec8-ecd ed0-ed9 edc-edd 10a0-10c5 10d0-10fc 1401-1407 1409-141b 141d-1435 1437-144a 144c-1452 1454-14bd 14c0-14ea 14ec-1507 1510-153e 1540-1550 1552-156a 1574-1585 158a-1596 15a0-15af 15de 15e1 1646-1647 166e-1676 1680-169c 1d00-1d14 1d16-1d23 1d26-1d2e 1d30-1d5b 1d5d-1d6a 1d77-1d78 1d7b 1d7d 1d85 1d9b-1dbf 1dc4-1dc9 1e00-1efb 1f00-1f15 1f18-1f1d 1f20-1f45 1f48-1f4d 1f50-1f57 1f59 1f5b 1f5d 1f5f-1f7d 1f80-1fb4 1fb6-1fc4 1fc6-1fd3 1fd6-1fdb 1fdd-1fef 1ff2-1ff4 1ff6-1ffe 2000-2064 206a-2071 2074-208e 2090-209c 20a0-20b5 20b8-20ba 20bd 20d0-20d1 20d6-20d7 20db-20dc 20e1 2100-2109 210b-2149 214b 214e 2150-2185 2189 2190-2311 2318-2319 231c-2321 2324-2328 232b-232c 2373-2375 237a 237d 2387 2394 239b-23ae 23ce-23cf 23e3 23e5 23e8 2422-2423 2460-2469 2500-269c 269e-26b8 26c0-26c3 26e2 2701-2704 2706-2709 270c-2727 2729-274b 274d 274f-2752 2756 2758-275e 2761-2794 2798-27af 27b1-27be 27c5-27c6 27e0 27e6-27eb 27f0-28ff 2906-2907 290a-290b 2940-2941 2983-2984 29ce-29d5 29eb 29fa-29fb 2a00-2a02 2a0c-2a1c 2a2f 2a6a-2a6b 2a7d-2aa0 2aae-2aba 2af9-2afa 2b00-2b1a 2b1f-2b24 2b53-2b54 2c60-2c77 2c79-2c7f 2d00-2d25 2d30-2d65 2d6f 2e18 2e1f 2e22-2e25 2e2e 4dc0-4dff a4d0-a4ff a644-a647 a64c-a64d a650-a651 a654-a657 a662-a66e a68a-a68d a694-a695 a708-a716 a71b-a71f a722-a72b a730-a741 a746-a74b a74e-a753 a756-a757 a764-a767 a780-a783 a789-a78e a790-a791 a7a0-a7aa a7f8-a7ff ef00-ef19 f000-f003 f400-f426 f428-f441 f6c5 fb00-fb06 fb13-fb17 fb1d-fb36 fb38-fb3c fb3e fb40-fb41 fb43-fb44 fb46-fb4f fb52-fba3 fbaa-fbad fbd3-fbdc fbde-fbdf fbe4-fbe9 fbfc-fbff fe00-fe0f fe20-fe23 fe70-fe74 fe76-fefc feff fff9-fffd 10300-1031e 10320-10323 1d300-1d356 1d538-1d539 1d53b-1d53e 1d540-1d544 1d546 1d54a-1d550 1d552-1d56b 1d5a0-1d5d3 1d7d8-1d7eb 1ee00-1ee03 1ee05-1ee1f 1ee21-1ee22 1ee24 1ee27 1ee29-1ee32 1ee34-1ee37 1ee39 1ee3b 1ee61-1ee62 1ee64 1ee67-1ee6a 1ee6c-1ee72 1ee74-1ee77 1ee79-1ee7c 1ee7e 1f030-1f093 1f0a0-1f0ae 1f0b1-1f0be 1f0c1-1f0cf 1f0d1-1f0df 1f42d-1f42e 1f431 1f435 1f600-1f623 1f625-1f62b 1f62d-1f640"
        return _font_transform(f, "DejaVuSans.ttf", charset)

    config.font_transforms["dejavusans"] = dejavusans

screen _accessibility_audio():

    grid 2 1:
        xfill True
        spacing gui._scale(40)

        vbox:

            label _("Self-Voicing")

            if renpy.variant("touch"):
                text _("Self-voicing support is limited when using a touch screen.")

            textbutton _("Off"):
                action Preference("self voicing", "disable")
                style_suffix "radio_button"

            textbutton _("Text-to-speech"):
                action Preference("self voicing", "enable")
                style_suffix "radio_button"

            textbutton _("Clipboard"):
                action Preference("clipboard voicing", "enable")
                style_suffix "radio_button"

            textbutton _("Debug"):
                action Preference("debug voicing", "enable")
                style_suffix "radio_button"

            label _("Voice Volume")

            side "c r":

                spacing gui._scale(10)

                bar value Preference("voice volume") yalign 0.5

                textbutton _("Reset"):
                    alt "reset voice volume"
                    action Preference("voice volume", 1.0)

            label _("Self-Voicing Volume Drop")

            side "c r":
                spacing gui._scale(10)

                bar value Preference("self voicing volume drop") yalign 0.5

                textbutton _("Reset"):
                    alt "reset self voicing volume drop"
                    action Preference("self voicing volume drop", 0.5)

        vbox:

            label _("Mono Audio")

            textbutton _("Enable"):
                action Preference("mono audio", "enable")
                style_suffix "radio_button"

            textbutton _("Disable"):
                action Preference("mono audio", "disable")
                style_suffix "radio_button"

screen _accessibility_text():

    grid 2 1:
        xfill True
        spacing gui._scale(40)

        vbox:

            label _("Font Override")

            textbutton _("Default"):
                action Preference("font transform", None)
                style_suffix "radio_button"

            textbutton _("DejaVu Sans"):
                action Preference("font transform", "dejavusans")
                style_suffix "radio_button"

            textbutton _("Opendyslexic"):
                action Preference("font transform", "opendyslexic")
                style_suffix "radio_button"

            label _("High Contrast Text")

            textbutton _("Enable"):
                action Preference("high contrast text", "enable")
                style_suffix "radio_button"

            textbutton _("Disable"):
                action Preference("high contrast text", "disable")
                style_suffix "radio_button"

        vbox:

            label _("Text Size Scaling")

            side "c r":
                spacing gui._scale(10)

                bar value Preference("font size") yalign 0.5

                textbutton _("Reset"):
                    alt "reset font size"
                    action Preference("font size", 1.0)

            label _("Line Spacing Scaling")

            side "c r":
                spacing gui._scale(10)

                bar value Preference("font line spacing") yalign 0.5

                textbutton _("Reset"):
                    alt "reset font line spacing"
                    action Preference("font line spacing", 1.0)

            label _("Kerning")

            side "c r":
                spacing gui._scale(10)

                bar value Preference("font kerning") yalign 0.5

                textbutton _("Reset"):
                    alt "reset font kerning"
                    action Preference("font kerning", 0.0)


screen _accessibility():
    layer config.interface_layer
    zorder 2000
    modal True

    default page = "audio"

    frame:
        style_group ""
        alt _("Accessibility Menu. Use up and down arrows to navigate, and enter to activate buttons and bars.")
        yfill False

        has side "c b":
            spacing gui._scale(10)
            xfill True

        viewport:
            scrollbars "vertical"
            mousewheel True
            viewport_yfill False


            vbox:

                hbox:
                    xfill True

                    hbox:
                        spacing gui._scale(25)

                        textbutton _("Self-Voicing and Audio"):
                            style_suffix "big_radio_button"
                            action SetScreenVariable("page", "audio")

                        textbutton _("Text"):
                            style_suffix "big_radio_button"
                            action SetScreenVariable("page", "text")

                    textbutton _("Return"):
                        action Hide("_accessibility")
                        style_suffix "big_radio_button"
                        xalign 1.0

                if page == "audio":
                    use _accessibility_audio()
                elif page == "text":
                    use _accessibility_text()

        text _("The options on this menu are intended to improve accessibility. They may not work with all games, and some combinations of options may render the game unplayable. This is not an issue with the game or engine. For the best results when changing fonts, try to keep the text size the same as it originally was.")
