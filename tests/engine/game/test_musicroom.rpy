init python:

    mr_track = ""

    mr = MusicRoom(stop_action=SetVariable("mr_track", "Stopped"))

    mr.add("sound/1.ogg", True, SetVariable("mr_track", "1"))
    mr.add("sound/2.ogg", True, SetVariable("mr_track", "2"))
    mr.add("sound/3.ogg", True, SetVariable("mr_track", "3"))
    mr.add("sound/4.ogg", True, SetVariable("mr_track", "4"))
    mr.add("sound/5.ogg", True, SetVariable("mr_track", "5"))


screen music_room:
    tag menu

    frame:

        has vbox

        text "[mr_track]"

        textbutton "1" action mr.Play("sound/1.ogg")
        textbutton "2" action mr.Play("sound/2.ogg")
        textbutton "3" action mr.Play("sound/3.ogg")
        textbutton "4" action mr.Play("sound/4.ogg")
        textbutton "5" action mr.Play("sound/5.ogg")

        hbox:
            textbutton "Next" action mr.Next()
            textbutton "Previous" action mr.Previous()
            textbutton "RandomPlay" action mr.RandomPlay()
            textbutton "TogglePlay" action mr.TogglePlay()


        hbox:
            text "Loop"
            textbutton "Yes" action mr.SetLoop(True)
            textbutton "No" action mr.SetLoop(False)
            textbutton "Toggle" action mr.ToggleLoop()
        hbox:
            text "Single Track"
            textbutton "Yes" action mr.SetSingleTrack(True)
            textbutton "No" action mr.SetSingleTrack(False)
            textbutton "Toggle" action mr.ToggleSingleTrack()
        hbox:
            text "Shuffle"
            textbutton "Yes" action mr.SetShuffle(True)
            textbutton "No" action mr.SetShuffle(False)
            textbutton "Toggle" action mr.ToggleShuffle()

        textbutton "Return" action Return()


