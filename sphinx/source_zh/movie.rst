.. _movie:

Movie
=====

Ren'Py兼容 libav (已包含)的使用并使用
视频编码器来播放视频:

* VP9
* VP8
* Theora
* MPEG 4 part 2 (包含 Xvid and DivX)
* MPEG 2
* MPEG 1

还有以下的音频编码器:

* OPUS
* Vorbis
* MP3
* MP2
* PCM

以下容器格式之中:

* WebM
* Matroska
* Ogg
* Avi
* 各种不同的 MPEG 流.

(要留意以上某些格式的使用可能需要专利许可。当你对此有疑问时，特别是在制作商业游戏的情况下，我们推荐你使用VP9, VP8, 或者 Theora, Opus 或者 Vorbis, 和 WebM, Matroska, 或者 Ogg。)

视频能够全屏播放，在displayable之中也是. 全屏视频播放会更有效率

全屏视频
-----------------

全屏播放视频最简单并且最有效率的方法是使用 renpypy.movie_cutscene 函数。这个函数会播放视频直到视频完结或者玩家点击解除视频。 ::

        $ renpy.movie_cutscene("On_Your_Mark.webm")

在移动平台，比如Android and iOS, 当:var:`config.hw_video` 值为true时硬件视频解码就能默认开启。This is generally
much faster, but the list of supported movie formats depends on the
platform.

Movie Displayables and Movie Sprites
------------------------------------

The Movie displayable can be used to display a movie anywhere Ren'Py can
show a displayable. For example, a movie can be displayed as the background
of a menu screen, or as a background.

The Movie displayable can also be used to define a movie sprite, which is
a sprite that is backed by two movies. The primary movie provides the
color of the sprite. A second movie, the mask movie, provides the alpha
channel, with white being full opacity and black being full transparency.

Movies played by the Movie displayable loop automatically.

There are three very important parameters to the Movie displayable, two of
which should always be provided.

`channel`
    A string giving the name of the channel that the movie will be played on.

    This must always be provided, and should never
    *not* be left at the default of "movie", and should not be the name
    of an audio channel. Names should be chosen such that only one
    Movie will be displaying on a given channel at the same time. Channels
    provided will be automatically registered using :func:`renpy.music.register_channel`,
    if not already registered.

`play`
    A string giving the name of a movie file to play.

    This should always be provided.

`mask`
    A string giving the name of a movie file to use as an alpha mask.

Here's an example of defining a movie sprite::

    image eileen movie = Movie(channel="eileen", play="eileen_movie.webm", mask="eileen_mask.webm")

The movie sprite can be shown using the show statement, which automatically starts the
movie playing. It will be automatically stopped when the displayable is hidden. ::

    show eileen movie

    e "I'm feeling quite animated today."

    hide eileen

    e "But there's no point on wasting energy when I'm not around."

A Movie displayable can also be used as part of a screen, provided it is created
during the init phase (for example, as part of an image statement.) ::


    image main_menu = Movie(channel="main_menu", play="main_menu.ogv")

    screen main_menu:
        add "main_menu"
        textbutton "Start" action Start() xalign 0.5 yalign 0.5

Multiple movie displayables or sprites can be displayed on the screen at once,
subject to system performance, and provided all share the same framerate. The
behavior of Ren'Py when displaying movies with different framerates is
undefined, but will likely include a significant amount of frame drop.


Python Functions
----------------

.. include:: inc/movie_cutscene
.. include:: inc/movie
