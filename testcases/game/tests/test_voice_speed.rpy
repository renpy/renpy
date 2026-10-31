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


# Use a filename so the ordinary voice statement also exercises voice filename formatting.
define audio.voice_speed__tone = "sound/5.ogg"

label voice_speed__say:
    $ _voice_speed__advanced = False
    voice audio.voice_speed__tone
    "A voiced line waits for playback to finish."
    $ _voice_speed__advanced = True
    $ preferences.afm_enable = False
    "Playback finished."
    return

label voice_speed__checkpoint:
    $ _voice_speed__value = "before"
    "Before the checkpoint."
    $ _voice_speed__value = "after"
    "After the checkpoint."
    return


testsuite voice_speed:
    setup:
        $ _test.voice_speed_old_preferences = (preferences.voice_speed, preferences.afm_enable, preferences.afm_time, preferences.wait_voice, preferences.text_cps)
        $ _test.voice_speed_old_timeout = _test.timeout
        $ _test.timeout = 5.0

    before testcase:
        run Preference("voice speed", 1.0)
        $ preferences.afm_enable = False
        $ preferences.text_cps = 0
        $ preferences.wait_voice = True

    after testcase:
        run Stop("voice")
        if not screen "main_menu":
            run MainMenu(confirm=False, save=False)

    teardown:
        $ preferences.voice_speed, preferences.afm_enable, preferences.afm_time, preferences.wait_voice, preferences.text_cps = _test.voice_speed_old_preferences
        $ _test.timeout = _test.voice_speed_old_timeout
        $ renpy.unlink_save("_test_voice_speed")

    testcase auto_forward_waits_for_voice:
        parameter speed = [0.5, 1.5, 3.0]
        run Preference("voice speed", speed)
        $ preferences.afm_time = 0.1
        $ preferences.afm_enable = True
        run Start("voice_speed__say")
        assert eval renpy.get_voice_speed() == speed
        assert eval renpy.sound.is_playing(channel="voice") timeout 2.0
        pause 0.15
        assert eval not _voice_speed__advanced
        assert eval _voice_speed__advanced timeout 4.0
        assert eval not renpy.sound.is_playing(channel="voice")

    testcase replay_uses_new_speed:
        run Preference("voice speed", 3.0)
        run Start("voice_speed__say")
        assert eval renpy.sound.is_playing(channel="voice") timeout 2.0
        run Preference("voice speed", 0.5)
        run VoiceReplay()
        pause 0.2
        assert eval renpy.sound.is_playing(channel="voice")
        assert eval 0.0 < renpy.music.get_pos(channel="voice") < 0.3

    testcase live_speed_keeps_position:
        run Start("voice_speed__say")
        assert eval renpy.sound.is_playing(channel="voice") timeout 2.0
        pause 0.1
        $ _test.voice_live_before = renpy.music.get_pos(channel="voice") or 0.0
        run Preference("voice speed", 0.5)
        assert eval renpy.audio.renpysound.get_playback_speed(renpy.audio.audio.get_channel("voice").number) == 0.5 timeout 1.0
        assert eval (renpy.music.get_pos(channel="voice") or 0.0) >= _test.voice_live_before - 0.02
        pause 0.2
        assert eval renpy.sound.is_playing(channel="voice")
        run Preference("voice speed", 3.0)
        assert eval renpy.audio.renpysound.get_playback_speed(renpy.audio.audio.get_channel("voice").number) == 3.0 timeout 1.0
        assert eval (renpy.music.get_pos(channel="voice") or 0.0) >= _test.voice_live_before - 0.02

    testcase character_sample_uses_speed:
        run Preference("voice speed", 0.5)
        run PlayCharacterVoice("voice_speed_test", audio.voice_speed__tone)
        pause 0.2
        assert eval renpy.sound.is_playing(channel="voice")
        assert eval 0.0 < renpy.music.get_pos(channel="voice") < 0.3

    testcase slider:
        $ _test.voice_speed_slider = Preference("voice speed").get_adjustment()
        $ _test.voice_speed_slider.change(1.5)
        assert eval renpy.get_voice_speed() == 2.0

    testcase developer_slider_range:
        $ _test.voice_speed_slider = Preference("voice speed", range=(0.125, 8.0)).get_adjustment()
        $ _test.voice_speed_slider.change(0.0)
        assert eval renpy.get_voice_speed() == 0.125
        $ _test.voice_speed_slider.change(7.875)
        assert eval renpy.get_voice_speed() == 8.0

    testcase save_and_rollback_keep_player_preference:
        run Preference("voice speed", 1.5)
        run Start("voice_speed__checkpoint")
        assert eval _voice_speed__value == "before"
        run Function(renpy.save, "_test_voice_speed")
        run Preference("voice speed", 2.0)
        advance
        assert eval _voice_speed__value == "after"
        run Rollback()
        assert eval _voice_speed__value == "before"
        assert eval renpy.get_voice_speed() == 2.0
        run Function(renpy.load, "_test_voice_speed")
        assert eval _voice_speed__value == "before"
        assert eval renpy.get_voice_speed() == 2.0
