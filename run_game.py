import renpy.game
import optparse
import traceback
import os
import sys

# Extra things used for distribution.
import encodings.utf_8
import encodings.zlib_codec

# The version of Ren'Py in use.
version = 'Renpy 4 Preview Release 1'


if __name__ == "__main__":

    op = optparse.OptionParser()
    op.add_option('--game', dest='game', default='game',
                  help='The directory the game is in.')


    options, args = op.parse_args()

    try:
        renpy.game.main(options.game)
    except Exception, e:

        f = file("traceback.txt", "wU")

        print >>f, "I'm sorry, but an exception occured while executing your Ren'Py"
        print >>f, "script."
        print >>f

        traceback.print_exc()
        traceback.print_exc(None, f)

        print
        print >>f

        print renpy.game.exception_info
        print >>f, renpy.game.exception_info

        print >>f
        print >>f, "Ren'Py Version:", version

        f.close()

        try:
            os.startfile('traceback.txt')
        except:
            pass
        

        

    
