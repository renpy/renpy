python early:

    def music_play_parse(l):
        print "Parsing music play."

        filename = l.simple_expression()
        if l is None:
            renpy.error("expected a music filename.")

        if not l.eol():
            renpy.error("expecting the end of the line.")

        return dict(filename=filename)
        
        
    def music_play_predict(parsed):
        print "Predicting music play."

    def music_play_execute(parsed):
        print "Executing music play."

    def music_play_lint(parsed):
        print "Linting music play."
        renpy.error("Ceci ne pas une lint.")
        
    renpy.statements.register('music play',
                              parse=music_play_parse,
                              execute=music_play_execute,
                              predict=music_play_predict,
                              lint=music_play_lint)

    print "Registered statement."

                              
