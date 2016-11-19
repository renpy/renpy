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

在移动平台，比如Android and iOS, 当:var:`config.hw_video` 值为true时硬件视频解码就能默认开启。编码速度通常都很快，但能支持的视频格式取决于平台。

视频的可展示性和视频精灵元素
------------------------------------

视频的可展示性能够令视频在 Ren'Py 允许展示的地方显现出来。例如，视频可以作为菜单背景来展示，或者是充当背景。视频的可展示型同样可以用于定义视频精灵元素，这是由两个视频元素共同渲染出来的。第一个视频元素提供了精灵的颜色。第二个视频元素是一个遮罩视频，提供了透明通道，当不透明全满时为白色，当透明度为满时为黑色。

受视频可展示性控制的视频会自动循环播放的。

视频可展示性有三个特别重要的参数，其中的两个时经常用到。

`channel`
    一段字符串，它表明了播放视频所在的频道的名称。

    此参数必须给定，千万 *不要* 在默认的"movie" 中遗漏它,并且不要和声音频道的名称一样。名称不要和同一时间给定频道播放的视频重名。如果指定的频道没有注册过的话，会自动使用 :func:`renpy.music.register_channel` 来进行注册。

`play`
    一段字符串，给定的视频文件的文件名。

    此参数必须给定。

`mask`
    一段字符串，作为透明度遮罩的视频文件的名称。

以下是视频精灵的一个示例::

    image eileen movie = Movie(channel="eileen", play="eileen_movie.webm", mask="eileen_mask.webm")

可以使用 show 语句来显示视频精灵，它会自动地开始视频播放。当可显示性被隐藏时，它就会自动停止视频播放。 ::

    show eileen movie

    e "I'm feeling quite animated today."

    hide eileen

    e "But there's no point on wasting energy when I'm not around."

视频可展示性也可以作为屏幕的一部分来使用，在 init 时期给定并创建(例如，作为 image 语句的一部分。) ::


    image main_menu = Movie(channel="main_menu", play="main_menu.ogv")

    screen main_menu:
        add "main_menu"
        textbutton "Start" action Start() xalign 0.5 yalign 0.5

多个视频可展示性或者视频精灵可以在屏幕中显示一次，为了迁就系统的性能并保持相同的帧率。当视频以不同的帧率被播放时，Ren'Py 的行为时不确定的，比如会有明显的掉帧现象。


Python Functions
----------------

.. include:: inc/movie_cutscene
.. include:: inc/movie
