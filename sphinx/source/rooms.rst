=============================================
Image Gallery, Music Room, and Replay Actions
=============================================

.. _image-gallery:

Image Gallery
-------------

A image gallery is a screen that allows the player to unlock images,
and then view those images. The screen has one or more buttons associated
with it, and each button has one or more associated images. Buttons and
images also have conditions that determine if they have unlocked.

Image galleries are managed by instances of the Gallery class. A
single instance of the gallery class may be shared between multiple
image gallery screens.

A gallery has one or more buttons associated with it, a button has one
or more images associated with it, and each image has one or more displayables
associated with it. Conditions can be assigned to buttons and images. A button
is unlocked when all of the conditions associated with it are satisfied and
at least one image associated with that button is unlocked. An image is unlocked
when all associated conditions are satisfied.

Creating an image gallery consists of the following four steps.

1. Create an instance of Gallery.

2. Add buttons and images to that gallery, along with conditions that
   determine if the buttons and images they belong to are unlocked. This
   is also a multi-step process.

   1. Declare a new button by calling :meth:`Gallery.button`.

   2. Optionally, add one or more unlock conditions to the button by
      calling :meth:`Gallery.unlock` or :meth:`Gallery.condition`.

   3. Declare an image by calling :meth:`Gallery.image` with one or more
      displayables as arguments. Or call the convenience method
      :meth:`Gallery.unlock_image` instead.

   4. Optionally, call :meth:`Gallery.transform` to associate
      transforms with the displayables.

   5. Optionally, add one or more unlock conditions to the image by
      calling :meth:`Gallery.unlock`, :meth:`Gallery.condition`,
      or :meth:`Gallery.allprior`.

   Additional images can be added to a button by repeating steps 3-5,
   while additional buttons can be added to the gallery by repeating
   all five steps.

3. Create an image gallery screen. The screen should display a background,
   and should contain navigation that allows the user to show other
   image galleries, or to return to the main or extras menu.

4. Add a way to display the image gallery screen to the main or extras menu.

Here's an example::

    init python:

        # Step 1. Create the gallery object.
        g = Gallery()

        # Step 2. Add buttons and images to the gallery.

        # A button with an image that is always unlocked.
        g.button("title")
        g.image("title")

        # A button that contains an image that automatically unlocks.
        g.button("dawn")
        g.image("dawn1")
        g.unlock("dawn1")

        # This button has multiple images associated with it. We use unlock_image
        # so we don't have to call both .image and .unlock. We also apply a
        # transform to the first image.
        g.button("dark")
        g.unlock_image("bigbeach1")
        g.transform(slowpan)
        g.unlock_image("beach1 mary")
        g.unlock_image("beach2")
        g.unlock_image("beach3")

        # This button has a condition associated with it, allowing the game
        # to choose which images unlock.
        g.button("end1")
        g.condition("persistent.unlock_1")
        g.image("transfer")
        g.image("moonpic")
        g.image("girlpic")
        g.image("nogirlpic")
        g.image("bad_ending")

        g.button("end2")
        g.condition("persistent.unlock_2")
        g.image("library")
        g.image("beach1 nomoon")
        g.image("bad_ending")

        # The last image in this button has an condition associated with it,
        # so it will only unlock if the user gets both endings.
        g.button("end3")
        g.condition("persistent.unlock_3")
        g.image("littlemary2")
        g.image("littlemary")
        g.image("good_ending")
        g.condition("persistent.unlock_3 and persistent.unlock_4")

        g.button("end4")
        g.condition("persistent.unlock_4")
        g.image("hospital1")
        g.image("hospital2")
        g.image("hospital3")
        g.image("heaven")
        g.image("white")
        g.image("good_ending")
        g.condition("persistent.unlock_3 and persistent.unlock_4")

        # The final two buttons contain images that show multiple pictures
        # at the same time. This can be used to compose character art onto
        # a background.
        g.button("dawn mary")
        g.unlock_image("dawn1", "mary dawn wistful")
        g.unlock_image("dawn1", "mary dawn smiling")
        g.unlock_image("dawn1", "mary dawn vhappy")

        g.button("dark mary")
        g.unlock_image("beach2", "mary dark wistful")
        g.unlock_image("beach2", "mary dark smiling")
        g.unlock_image("beach2", "mary dark vhappy")

        # The transition used when switching images.
        g.transition = dissolve

    # Step 3. The gallery screen we use.
    screen gallery:

        # Ensure this replaces the main menu.
        tag menu

        # The background.
        add "beach2"

        # A grid of buttons.
        grid 3 3:

            xfill True
            yfill True

            # Call make_button to show a particular button.
            add g.make_button("dark", "gal-dark.png", xalign=0.5, yalign=0.5)
            add g.make_button("dawn", "gal-dawn.png", xalign=0.5, yalign=0.5)
            add g.make_button("end1", "gal-end1.png", xalign=0.5, yalign=0.5)

            add g.make_button("end2", "gal-end2.png", xalign=0.5, yalign=0.5)
            add g.make_button("end3", "gal-end3.png", xalign=0.5, yalign=0.5)
            add g.make_button("end4", "gal-end4.png", xalign=0.5, yalign=0.5)

            add g.make_button("dark mary", "gal-dark_mary.png", xalign=0.5, yalign=0.5)
            add g.make_button("dawn mary", "gal-dawn_mary.png", xalign=0.5, yalign=0.5)
            add g.make_button("title", "title.png", xalign=0.5, yalign=0.5)


        # The screen is responsible for returning to the main menu. It could also
        # navigate to other gallery screens.
        textbutton "Return" action Return() xalign 0.5 yalign 0.5

Step 4 will vary based on how your game is structured, but one way of
accomplishing it is to add the following line::

        textbutton "Gallery" action ShowMenu("gallery")

to the main menu screen.

.. include:: inc/gallery


.. _music-room:

Music Room
----------

A music room is a screen that allows the user to select and play music
tracks from the game. These tracks may start off locked when the user
first begins playing a particular game, and will be unlocked as the
user listens to the music while playing the game.

A music room is managed by an instance of the MusicRoom class. There
can be more than one MusicRoom instance in a game, allowing a game to
have multiple music rooms. Creating a music room consists of the
following four steps:

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

4. Add the music room screen to the main menu, or an extras menu.

Here's an example::

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


.. _replay:

Replay
------

Ren'Py also includes the ability to replay a sequence from inside the
main or game menu. This can be used to create a "sequence gallery", or
memory gallery that allows the player to repeat important sequence.
After the sequence finishes, Ren'Py returns to where the replay was launched.

Sequence replay is also possible using the :func:`Start` action. The
difference between the two modes are:

* A replay can be launched from any screen while Start can only be
  used in the main menu or screens shown by the main menu.

* When a replay finishes, control returns to the point where the
  replay was invoked. That point can be inside the main or game
  menu, for example. If a game is in progress when replay is called,
  game state is preserved.

* Saving is disabled while in replay mode. Reloading, which requires
  saving, is also disabled.

* While in replay mode, a call to :func:`renpy.end_replay` will end
  the replay. In normal mode, end_replay does nothing.

To take advantage of the replay mode, a sequence should begin with a label,
and end with a call to :func:`renpy.end_replay`. The sequence should make
no assumption as to the state of the layers or variables, which can be
very different in normal and replay mode (except those set through the
`scope` parameter when entering replay). When a replay begins, the label
is invoked from a black screen.

For example::

        "And finally, I met the wizard himself."

    label meaning_of_life:

        scene revelation

        "Mage" "What is the meaning of life, you say?"

        "Mage" "I've thought about it long and hard. A long time, I've
                spent pondering that very thing."

        "Mage" "And I'll say - the answer - the meaning of life
                itself..."

        "Mage" "Is forty-three."

        $ renpy.end_replay()

        "Mage" "Something like that, anyway."

With the sequence defined like that, the replay can be invoked with the
Replay action::

    textbutton "The meaning of life" action Replay("meaning_of_life")

There is one store variable used by replay mode:

.. var:: _in_replay

    When in replay mode, this is sent to the label at which replay
    mode was started - the label that was called, not the one the
    call originated from. Outside of replay mode, this is None.

In addition, :var:`config.enter_replay_transition` and
:var:`config.exit_replay_transition` are used when entering and exiting
replay mode, respectively. :var:`config.replay_scope` adds variables
to the cleaned store when entering a replay, and by default sets
:var:`_game_menu_screen` to cause right-clicking in a replay to
default to showing the preferences screen.

The following variables and actions are used in replay mode:

.. include:: inc/replay
