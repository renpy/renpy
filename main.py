import renpy.game
import optparse

if __name__ == "__main__":

    op = optparse.OptionParser()
    op.add_option('--game', dest='game', default='game',
                  help='The directory the game is in.')


    options, args = op.parse_args()
    
    renpy.game.main(options.game)
