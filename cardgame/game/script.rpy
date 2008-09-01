# You can place the script of your game in this file.

init:
    # Declare images below this line, using the image statement.
    # eg. image eileen happy = "eileen_happy.png"

    # Declare characters used by this game.
    $ e = Character('Eileen', color="#c8ffc8")

    image eileen happy = "eileen_happy.png"
    image eileen mad = "eileen_concerned.png"
    

# The game starts here.
label start:

    scene black
    show eileen happy

    e "Welcome to the card game engine!"
    
    scene expression "#292"
    
    python:

        t = Table(base="card/base.png", back="card/back.png")
        t.card(1, "card/1.png")
        t.card(2, "card/2.png")
        t.card(3, "card/3.png")
        t.card(4, "card/4.png")
        t.card(5, "card/5.png")

        s1 = t.stack(100, 100, yoff=20, click=True, drag=DRAG_BELOW, drop=True)        
        s2 = t.stack(200, 100, yoff=20, click=True, drag=DRAG_CARD, drop=True)
        s3 = t.stack(300, 100, yoff=20, click=True, drag=DRAG_BOTTOM, drop=True)
        s4 = t.stack(400, 100, yoff=20, click=True, drag=DRAG_STACK, drop=True)
        s5 = t.stack(700, 100, yoff=20, drop=True)


        s6 = t.stack(100, 500, drop=True)
        s7 = t.stack(200, 500, drop=True)
        s8 = t.stack(300, 500, drop=True)
        s9 = t.stack(400, 500, drop=True)
        
        s1.append(1)
        s1.append(2)
        s1.append(3)
        s1.append(4)
        s1.append(5)

        ui.layer("master")
        ui.add(t)
        ui.close()

        renpy.with_statement(dissolve)
        
        while True:

            ev = ui.interact()

            print ev.type
            
            if ev.type == "drag":

                if ev.drop_stack == s5:
                    renpy.show("eileen mad")
                    e("Hey! You can't drop things there!")
                    renpy.hide("eileen")
                    renpy.with_statement(moveoutright)
                elif ev.drop_stack == s6:
                    print "FACEDOWN"
                    for c in ev.drag_cards:
                        print c
                        t.set_faceup(c, False)
                elif ev.drop_stack == s7:
                    for c in ev.drag_cards:
                        t.set_faceup(c, True)
                elif ev.drop_stack == s8:
                    for c in ev.drag_cards:
                        t.set_rotate(c, 90)
                elif ev.drop_stack == s9:
                    for c in ev.drag_cards:
                        t.set_rotate(c, 0)
                        
                        
                else:
                    for c in ev.drag_cards:
                        ev.drop_stack.append(c)
                    

        

