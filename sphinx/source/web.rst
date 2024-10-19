Web / HTML5
===========

Ren'Py supports running games in a web browser. This is done by with a
version of Ren'Py that has been compiled to WebAssembly, allowing as much
as possible of Ren'Py to run in the browser. This page will explain
some of the limitations of running inside a browser, help you design your
game to run well, and explain how to build your game for the web.

Limitations
-----------

Like all games running inside a web browser, Ren'Py games have a number of
limitations on them. Some of these are imposed by the sandbox in the browser,
while others have been chosen to reduce the amount of data that needs to be
downloaded before a game can start.

Some limitations are:

* Video is played back using the browser's built-in video playback. This
  limits the formats that can be played back to those supported by the web
  browser, and only :func:`renpy.movie_cutscene` is supported.

* Audio playback may use the browsers audio format, which is fast, or may
  use Ren'Py's built in audio playback, which is slower, but supports more
  formats. See the section below.

* The web port doesn't support multi-threading, so functions like
  :func:`renpy.invoke_in_thread` and the Python ``threading`` module are not
  supported. This can also limit the performance of some games - on desktop
  and mobile Ren'Py, images can be preloaded in the background, but on the web
  port this is not possible, and so image loading may cause framerate glitches.

* Networking is not supported. This might be surprising, but the browser
  sandbox prevents Ren'Py from making arbitrary network requests. This means
  that sockets and the requests library will return errors when run inside
  the web browser.

* Live2D is not supported.

In addition, there are some limitations that can be caused by where you host
your game. Some hosting providers limit the size of a game and the number
of files that can be included as part of a project. As an example,
`itch.io <https://itch.io/docs/creators/html5#zip-file-requirements>`_ documents
these limits. Browsers provide other limits - files that are greater than 50MB
in size won't be cached, which means big files will be downloaded every time
your game is run.

Supported Browsers
------------------

We try to keep Ren'Py running in recent versions of evergreen browsers
like Chrome, Edge, Firefox, and Safari, as well as the mobile versions of
these browsers on iOS and Android. Ren'Py may work in other browsers, but
it depends on the browser's support for WebAssembly and other features
required by Ren'Py.

Ren'Py does require many modern web features, and so won't run if these
features are blocked or disabled.

While we try to keep Ren'Py running, Ren'Py can push the edge of what
a browser is capable of, and so it's possible that changes to the browsers
will render them incapable of running games. We work with browser vendors
to ensure the browsers keep working, but it's possible that a change to
the browser will require your game to be updated.

Packaging your Game
-------------------

Ren'Py games can be packaged for the web by using the "Web (Beta)" section
of the Launcher. This has four main options in it.

Build Web Application
    This will package your game for the web. This will create a web.zip
    file containing your entire game, and a folder that contains each of
    the individual files that make up your game. (Actually running the game
    from this folder isn't supported, as the game needs to be hosted by
    a web server.)

Build and Open in Browser
    This will package your game for the web, and then open it in a local
    web browser for testing purposes. This will run a web server on your
    computer that serves the game, and then open a browser that accesses
    that web server.

    This is the usual way to test your game.

Open in Browser
    This will open a local web browser that accesses a web server on your
    computer, without the full build process.

Open build Directory
    This opens the folder containing the files produced by the build process.


Generated folders
-----------------
Say, your project is in the renpy/projects/main/yourproject folder. Then you
will find a new renpy/projects/main/yourproject-1.0-dists folder. This folder
contains a yourproject-1.0-web subfolder, and this subfolder's zipped version,
a yourproject-1.0-web.zip file.

Uploading your Game
-------------------

Once you've built your game, you'll need to upload it to a public web
server. For game hosting services like itch.io, you'll need to upload
the web.zip file, which contains all of the files. For other hosting
options, you'll need to upload every file in the generated web directory.

If you're hosting the game yourself, you'll want to make sure your web
server serves .wasm files using the application/wasm MIME type. Doing
so will make the game load faster, and prevent a warning from happening.

Some web hosts may reject the game.zip file. In that case, rename it to
game.data, and edit index.html to change game.zip to game.data.

.. _web-presplash:

Presplash
---------

The Web platform natively uses a default presplash image. To override it, you can supply
an image named `web-presplash`, `.jpg`, `.png` or `.webp`, and it will replace
the default.

The `.webp` format allows for an animated presplash image, if that's required.

Icon
---------

The Web page icon can be customized by putting an image file with the name `web-icon.png`
in the base directory of your project. This image must have a minimum resolution of
512x512 and its width and height must be equal.
If no custom image is given, the default Ren'Py icon is used.

Progressive Downloading
-----------------------

Ren'Py supports a progressive download feature, which is configured by
editing the file named ``progressive_download.txt`` in the base directory
of your project. If this file doesn't exist, it will be created when you
package your game for the web the first time. The default contents of this
file is::

    # RenPyWeb progressive download rules - first match applies"
    # '+' = progressive download, '-' = keep in game.data (default)
    # See https://www.renpy.org/doc/html/build.html#classifying-and-ignoring-files for matching
    #
    # +/- type path
    - image game/gui/**
    + image game/**
    + music game/audio/**
    + voice game/voice/**

This file determines which files are downloaded before the game starts,
and which are downloaded when required. Lines beginning with a # are
comments. Lines beginning with a - match files that should be downloaded
where the game begins - usually files that are used in the opening screen.
Lines beginning with a + match files that should be downloaded as needed.

The second column determines the type of file, and how Ren'Py treats these
files. The types are:

image
    Image files are replaced by a pixellated version of the image, and
    then replaced with the full image when the image is loaded. In many
    cases, Ren'Py can predict the image and load it before the full image
    is needed, so the pixellated image will only be seen when this load
    can't finish in time.

    If the full image never loads, it's likely that the wrong data is on
    the web server.

music
    Music files are replaced by silence, and then play when loading finishes.

voice
    Voice files are replaced by silence, and then play when loading finishes.

Finally, the last columns is the path to match.


Audio and Video
---------------

Due to limitations in the browser intended to stop advertisements from
playing audio, sound and music files won't play until the user clicks
inside the game at least once.

Ren'Py has two ways to play audio files. The first is to use the webaudio
system inside the browser, and then second is to use its own audio playback
system. The webaudio system is faster, but on Safari, the OGG format is not
supported.

The :var:`config.webaudio_required_types` variable controls which audio system
is used, by probing the browser for the types it supports. If your game
uses only mp3 this can be changed using ::

    define config.webaudio_required_types = [ "audio/mpeg" ]

Playing back video is also supported. There are two variables that control
it:

:var:`config.web_video_base`
    This is a URL that's appended to to the movie filename to get the full URL
    to play the movie from. It can include directories in it, so
    "https://share.renpy.org/movies-for-mygame/" would also be fine.

    This is useful if you want to host the movies on a different server
    than the rest of your game.

:var:`config.web_video_prompt`
    On Mobile Safari on iOS, by default, the player will need to click to play
    a movie with sound. This variable gives the message that's used to prompt
    players to click.

There's one more Safari-related feature. Since Safari doesn't support modern
formats like webm, the webvideo support has a fallback. A URL with the extension
replaced with .mp4 will be tried if the first fails. On Safari, what will happen
is that https://share.renpy.org/oa4_launch.webm will be tried and fail as unsupported,
and then https://share.renpy.org/oa4_launch.mp4 will be tried if it exists.


Javascript
----------

Ren'Py can run Javascript, using three functions in the ``emscripten``
module. This module is available as :var:`renpy.emscripten` when
running on the web platform. When not running on the web platform,
renpy.emscripten is False.


.. function:: renpy.emscripten.run_script(script)

    Runs the given Javascript script. This does not return a result.

.. function:: renpy.emscripten.run_script_int(script)

    Runs the given Javascript script, and returns its result as an integer.

.. function:: renpy.emscripten.run_script_string(script)

    Runs the given Javascript script, and returns its result as a string.

You can add Javascript functions to your game by editing the ``web/index.html``
file, and including the scripts that Ren'Py will call. Note that this file
may be replaced when Ren'Py is updated.

Javascript can also call into Ren'Py using the window.renpy_exc, window.renpy_get,
and window.renpy_set functions. For the documentation of these functions, please
read ``web/renpy-pre.js``.


Hamburger Menu
--------------

The hamburger menu is a menu that appears in the top left corner of the game.
It has three options:

Import saves
    This lets the user upload Ren'Py save files and persistent data into
    the web browser.

Export saves
    This allows the user to download a zip file with their save games and
    persistent data. This file can be uploaded into a different web browser,
    saved for backup, or even unzipped and loaded into a desktop game.

Ren'Py log
    This downloads the Ren'Py log, which contains debugging output.
