init python:
    def audio_queue_test_tone(duration, name):
        import io
        import struct
        import wave

        data = io.BytesIO()
        with wave.open(data, "wb") as output:
            output.setparams((2, 2, 48000, 0, "NONE", "not compressed"))
            output.writeframes(struct.pack("<hh", 10000, 10000) * round(duration * 48000))

        return AudioData(data.getvalue(), name)

define audio.queue_first = audio_queue_test_tone(0.4, "first.wav")
define audio.queue_second = audio_queue_test_tone(0.8, "second.wav")


label audio_queue_test_delayed:
    play music audio.queue_first noloop
    $ renpy.pause(0.1, hard=True)
    queue music audio.queue_second noloop
    $ renpy.pause(0.5, hard=True)
    $ assert renpy.music.get_playing("music") == audio.queue_second
    stop music
    return


testsuite audio_queue:
    testcase delayed_queue:
        run Start("audio_queue_test_delayed")
        pause until screen "main_menu"
