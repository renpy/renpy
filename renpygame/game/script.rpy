init:
    $ config.screen_width = 640
    $ config.screen_height = 480

    $ theme.roundrect()

    $ import main
    $ import sys
    
label start:

    "Ready for a danmaku game?"

    python:
        for i in sys.modules:
            print i

        print
        print sys.meta_path

    
    $ main.main()

    "Game over, man, game over."
