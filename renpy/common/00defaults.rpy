# Copyright 2004-2013 Tom Rothamel <pytom@bishoujo.us>
# See LICENSE.txt for license details.

init -1500 python:

    # basics: If not None, the default value of the fullscreen
    # preference when the game is first run.
    config.default_fullscreen = None

    # basics: If not None, the default value of the text_cps
    # preference when the game is first run.
    config.default_text_cps = None

    # If not None, the default value of afm_time
    config.default_afm_time = None

    # If not None, the default value of afm_enable
    config.default_afm_enable = False

    # If not None, the default language to use.
    config.default_language = None

    # If not None, the default value of wait_voice
    config.default_wait_for_voice = True

    # If not None, the default value of voice_sustain
    config.default_voice_sustain = False


init 1500 python:

    if not persistent._set_preferences:
        persistent._set_preferences = True

        if config.default_fullscreen is not None:
            _preferences.fullscreen = config.default_fullscreen

        if config.default_text_cps is not None:
            _preferences.text_cps = config.default_text_cps

        if config.default_afm_time is not None:
            _preferences.afm_time = config.default_afm_time

        if config.default_language is not None:
            _preferences.language = config.default_language

        if config.default_wait_for_voice is not None:
            _preferences.wait_voice = config.default_wait_for_voice

        if config.default_voice_sustain is not None:
            _preferences.voice_sustain = config.default_voice_sustain

    if config.default_afm_enable is not None:
        _preferences.afm_enable = config.default_afm_enable
        _preferences.using_afm_enable = True
    else:
        _preferences.afm_enable = True
        _preferences.using_afm_enable = False


init -1500 python:
    def _imagemap_auto_function(auto_param, variant):
        rv = auto_param % variant

        if renpy.loadable(rv):
            return rv
        else:
            return None

    config.imagemap_auto_function = _imagemap_auto_function

init -1500 python:

    # Hyperlink functions. Duplicated in _errorhandling.rpym.
    def hyperlink_styler(target):
        return style.hyperlink_text

    def hyperlink_function(target):
        if target.startswith("http:"):
            try:
                import webbrowser
                webbrowser.open(target)
            except:
                pass
        else:
            renpy.call_in_new_context(target)

    style.default.hyperlink_functions = (hyperlink_styler, hyperlink_function, None)

init -1500:
    image text = renpy.ParameterizedText(style="centered_text")
    image vtext = renpy.ParameterizedText(style="centered_vtext")

