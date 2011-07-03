==============================================
Gallery, Scene Gallery, and Music Room Actions
==============================================


Music Room
==========

A music room is a screen that allows the user to select and play music
tracks from the game. These tracks may start off locked when the user
first begins playing a particular game, and will be unlocked as the
user listens to the music while playing the game. While Ren'Py doesn't
ship with a pre-defined music room, it does provide a number of
actions that can be used by screens to easily implement a custom music
room.

A music room is managed by the MusicRoom class. There can be more than
one MusicRoom instance in a game, allowing a game to have multiple
music rooms. Creating a music room consists of the following four
steps:

1. Create an instance of MusicRoom. The MusicRoom constructor takes
   parameters to control the channel on which music is played back,
   and how long it takes to fade music out and back in.

2. Add music files to the instance.

3. Create a screen that uses the MusicRoom instance to create actions
   for buttons, imagebuttons, or hotspots. These actions can pick a
   track, the next or previous track, or stop and start the music.

   Note that the actions used are members of a MusicRoom instance,
   so if the MusicRoom instance is named ``mr``, then
   ``mr.Play("track1.ogg")`` is how you'd use the play action.

4. Add the music room screen to a main or extras screen.

Here's an example of the first three steps::

    init python:
        
        # Step 1. Create a MusicRoom instance.
        mr = MusicRoom(fadeout=1.0)
        
        # Step 2. Add music files.
        mr.add("track1.ogg", always_unlocked=True)
        mr.add("track2.ogg")
        mr.add("track3.ogg")
        
        
    # Step 3. Create the music room screen.
    screen music_room:
    
        tag menu
    
        frame:
            has vbox
                
            # The buttons that play each track.
            textbutton "Track 1" action mr.Play("track1.ogg")
            textbutton "Track 2" action mr.Play("track2.ogg")
            textbutton "Track 3" action mr.Play("track3.ogg")
            
            null height 20
        
            # Buttons that let us advance tracks.
            textbutton "Next" action mr.Next()
            textbutton "Previous" action mr.Previous()
            
            null height 20
            
            # The button that lets the user exit the music room.
            textbutton "Main Menu" action ShowMenu("main_menu")
            
        # Start the music playing on entry to the music room.
        on "replace" action mr.Play()
        
        # Restore the main menu music upon leaving.
        on "replaced" action Play("music", "track1.ogg")

Step 4 will vary based on how your game is structured, but one way of
accomplishing it is to add the following line::

        textbutton "Music Room" action ShowMenu("music_room")

to the main menu screen.

Using the :func:`Preferences` function, especially
``Preferences("music volume")``, it's possible to include a volume
slider on the music screen.

.. include:: inc/music_room

