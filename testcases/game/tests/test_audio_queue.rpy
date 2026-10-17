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

    def audio_queue_test_loop_spec():
        channel = renpy.audio.audio.get_channel("music")
        filename = AudioData(audio.queue_first.data, "<loop 0.0005625>first.wav")
        first, start, end, volume = channel.split_filename(filename, False)
        assert start == 0.0
        loop, start, end, volume = channel.split_filename(filename, True)
        assert start == 27 / 48000
        assert end == -1
        assert first.data == loop.data == audio.queue_first.data

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
    testcase loop_filename:
        $ audio_queue_test_loop_spec()

    testcase delayed_queue:
        run Start("audio_queue_test_delayed")
        pause until screen "main_menu"
