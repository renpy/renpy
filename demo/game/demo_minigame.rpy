init:

    image bg pong field = "pong_field.png"

    python:

        class PongMinigame(object):

            def __init__(self):
                # The minigame object, initialized with the methods it calls
                # for various events.
                self.minigame = renpy.Minigame(self.render, self.event)

                # The sizes of some of the images.
                self.PADDLE_WIDTH = 8
                self.PADDLE_HEIGHT = 79
                self.BALL_WIDTH = 15
                self.BALL_HEIGHT = 15
                self.COURT_TOP = 108
                self.COURT_BOTTOM = 543

                # If the ball is stuck to the paddle.
                self.stuck = True
                
                # The positions of the two paddles.
                self.playery = (self.COURT_BOTTOM - self.COURT_TOP) / 2
                self.computery = self.playery

                # The speed of the computer.
                self.computerspeed = 350.0

                # The position, dental-position, and the speed of the
                # ball.
                self.bx = 88
                self.by = self.playery
                self.bdx = .5
                self.bdy = .5
                self.bspeed = 300.0

                # The time of the past render-frame.
                self.oldst = None

                # The winner.
                self.winner = None


            # Recomputes the position of the ball, handles bounces, and
            # draws the screen.
            def render(self, r, st):


                # Figure out the time elapsed since the previous frame.
                if self.oldst is None:
                    self.oldst = st
                    
                dtime = st - self.oldst
                self.oldst = st

                # Figure out where we want to move the ball to.
                speed = dtime * self.bspeed
                oldbx = self.bx

                if self.stuck:
                    self.by = self.playery
                else:                    
                    self.bx += self.bdx * speed
                    self.by += self.bdy * speed

                # Move the computer's paddle. It wants to go to self.by, but
                # may be limited by it's speed limit.
                cspeed = self.computerspeed * dtime
                if abs(self.by - self.computery) <= cspeed:
                    self.computery = self.by
                else:
                    self.computery += cspeed * (self.by - self.computery) / abs(self.by - self.computery)

                # Handle bounces.
                
                # Bounce off of top.
                ball_top = self.COURT_TOP + self.BALL_HEIGHT / 2                
                if self.by < ball_top:
                    self.by = ball_top + (ball_top - self.by)
                    self.bdy = -self.bdy
                    renpy.sound.play("pong_beep.wav", channel=0)
                    
                # Bounce off bottom.
                ball_bot = self.COURT_BOTTOM - self.BALL_HEIGHT / 2
                if self.by > ball_bot:
                    self.by = ball_bot - (self.by - ball_bot)
                    self.bdy = -self.bdy
                    renpy.sound.play("pong_beep.wav", channel=0)

                # This draws a paddle, and checks for bounces.                       
                def paddle(px, py, hotside):

                    pi = self.minigame.load_image("pong.png")
                    r.blit(pi, (int(px), int(py - self.PADDLE_HEIGHT / 2)))

                    if py - self.PADDLE_HEIGHT / 2 <= self.by <= py + self.PADDLE_HEIGHT / 2:

                        hit = False
                        
                        if oldbx >= hotside >= self.bx:
                            self.bx = hotside + (hotside - self.bx)
                            self.bdx = -self.bdx
                            hit = True
                            
                        elif oldbx <= hotside <= self.bx:
                            self.bx = hotside - (self.bx - hotside)
                            self.bdx = -self.bdx
                            hit = True
                            
                        if hit:
                            renpy.sound.play("pong_boop.wav", channel=1)
                            self.bspeed *= 1.10
                            
                # Draw the two paddles.
                paddle(68, self.playery, 68 + self.PADDLE_WIDTH)
                paddle(724, self.computery, 724)

                # Draw the ball.
                ball = self.minigame.load_image("pong_ball.png")
                r.blit(ball, (int(self.bx - self.BALL_WIDTH / 2),
                              int(self.by - self.BALL_HEIGHT / 2)))

                # Show the player names.
                player = self.minigame.render_text("Player",
                                                   style.default.font,
                                                   36,
                                                   "#fff")
                r.blit(player, (20, 25))

                # Show Eileen's name.
                eileen = self.minigame.render_text("Eileen",
                                                    style.default.font,
                                                    36,
                                                    "#fff")
                ew, eh = eileen.get_size()
                r.blit(eileen, (790 - ew, 25))
                
                # Show the "Click to Begin" label.
                if self.stuck:
                    ctb = self.minigame.render_text("Click to Begin",
                                                    style.default.font,
                                                    36,
                                                    "#fff")

                    cw, ch = ctb.get_size()
                    r.blit(ctb, (400 - cw / 2, 30)) 
                    
                
                # Check for a winner.
                if self.bx < -200:
                    self.winner = "eileen"

                    # Needed to ensure that event is called, noticing
                    # the winner.
                    self.minigame.timeout(0)

                elif self.bx > 1000:
                    self.winner = "player"
                    self.minigame.timeout(0)

                # Ask that we be re-rendered ASAP, so we can show the next
                # frame.
                self.minigame.redraw()

            # Handles events.
            def event(self, ev, x, y, st):

                import pygame

                # Mousebutton down == start the game by setting stuck to
                # false.
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    self.stuck = False
                    
                # Set the position of the player's paddle.
                y = max(y, self.COURT_TOP)
                y = min(y, self.COURT_BOTTOM)
                self.playery = y

                # If we have a winner, return him or her. Otherwise, ignore
                # the current event.
                if self.winner:
                    return self.winner
                else:
                    self.minigame.ignore_event()
            

label demo_minigame:

    e "The Minigame interface lets experienced pygame programmers extend Ren'Py with minigames."

    e "It's not for everyone, but it does allow for a change of pace."

    e "Now, why don't we play some pong?"

label demo_minigame_pong:

    # Put up the pong background, in the usual fashion.
    scene bg pong field

    # Run the pong minigame, and determine the winner.
    python:
        pm = PongMinigame()
        winner = pm.minigame.run()

    
    scene bg washington
    show eileen vhappy
        
    if winner == "eileen":
    
        e "I win!"

    else:

        e "You won! Congratulations."


    show eileen happy
        
    menu:
        e "Would you like to play again?"

        "Sure.":
            jump demo_minigame_pong
        "No thanks.":
            pass        

        
    e "You need to be careful about putting minigames in a visual novel, as not every visual novel player wants to be good at arcade games."

    return




            

            
        

                
