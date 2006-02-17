# This is the annoying readback mode. I implemented this because
# people asked for it, not because I like it. I'd prefer you use
# rollback, which is better in every way.

# To use readback, drop this file into your game directory. Readback
# will take over when rollback no longer works, so you'll also need to
# either reduce config.hard_rollback_limit or set
# config.rollback_enabled to false.

init -100:
     $ config.hard_rollback_limit = 1

# Readback works by replacing the default Character and Menu objects
# with ones that record what is said in a readback buffer. The user
# can then go back, and what has been said will be shown to them
# again. Images and the like will not change... if you want that, use
# rollback. Heck, use rollback anyway. :-P

# The number of lines of readback can be changed by assigning an
# integer to the readback_limit variable. But leaving it None will
# leave the entire game in the buffer. As this is actually fairly
# memory-efficent, you should probably leave it as None.

# Readback uses two styles, readback_dialogue and
# readback_thought. Change them to change the color and look of
# read-back text. 

# If you want to add your own message, as narration, to the readback
# buffer, you can do it by calling the readback function or having
# the readback character say it:

#    $ readback('A message for readbackers only.')
#    readback "A similar message."

# Note: When using Readback, you can no longer use a string for a
# character's name. All dialogue must be routed through Character
# objects, if it is to show up in the readback buffer. This limitation
# will be fixed in a future version of Ren'Py.

init -100:

    python:

        # The limit of the number of readbacks to keep. None means no limit.
        readback_limit = None

        # Set this to true to print out the contents of the readback
        # buffer when it is saved. 
        readback_debug = False

        # Readback styles.
        style.create('readback_dialogue', 'say_dialogue', '')
        style.create('readback_thought', 'say_thought', '')

        style.readback_dialogue.color = (255, 128, 128, 255)
        style.readback_thought.color = (255, 128, 128, 255)


        # No user-servicable parts below this line. ######################

        # The readback buffer is a doubly-linked list of readback
        # objects. 
        class Readback(object):
            def __init__(self, obj, args):
                self.older = None
                self.newer = None
                self.obj = obj
                self.args = args

            def show(self):
                self.obj.readback(*self.args)


        readback_oldest = None
        readback_newest = None
        readback_count = 0


        # This saves a readback entry to the readback buffer.
        def readback_save(obj, *args):

            store.readback_count += 1

            if readback_limit and readback_count > readback_limit:
                store.readback_count -= 1
                readback_oldest.newer.older = None
                store.readback_oldest = readback_oldest.newer
            
            rb = Readback(obj, args)

            
            if readback_newest:
                readback_newest.newer = rb
            else:
                store.readback_oldest = rb
                
            rb.older = readback_newest

            store.readback_newest = rb


            if readback_debug:

                print "---- Readback Buffer ----"

                rb = readback_oldest
                while rb:
                    print rb.obj, rb.args
                    rb = rb.newer
                

        # The rest of this file is replacing the default objects and
        # functions with versions that save things in the readback
        # buffer.
        
        # Save the old character object.
        readback_OldCharacter = Character
        readback_oldmenu = menu

        class Character(readback_OldCharacter):

            def __init__(self, who,
                         readback_style='readback_dialogue',
                         **kwargs):
                
                readback_OldCharacter.__init__(self, who, **kwargs)
                self.readback_style = readback_style
                
            def __call__(self, what, **kwargs):

                if not self.check_condition():
                    return

                readback_OldCharacter.__call__(self, what, **kwargs)

            def store_readback(self, who, what):
                readback_save(self, who, what)

            def readback(self, who, what):
                self.function(who, what,
                              who_style=self.who_style,
                              what_style=self.readback_style,
                              window_style=self.window_style,
                              interact=False,
                              all_at_once=True,
                              **self.properties)
    
        class Sayer(object):
            def __call__(self, who, what):
                renpy.display_say(who, what)
                readback_save(self, who, what)

            def readback(self, who, what):
                renpy.display_say(who, what,
                                  what_style='readback_dialogue',
                                  all_at_once=True,
                                  interact=False)
                
        
        narrator = Character(None, what_style='say_thought')
        say = Sayer()

        def readback(what):
            narrator.store_readback(None, what)
            
        def menu(menuitems):
            rv = readback_oldmenu(menuitems)

            text = '\n'.join([ l for l, v in menuitems
                               if v is None or v == rv ])

            readback(text)

            return rv

        # This stuff is involved in entering the readback mode.
        
        def readback_mode():
            # Try rollback, first.
            renpy.rollback()

            # If we made it here, we're into readback mode. So let's
            # go there now. 
            
            renpy.call_in_new_context("readback")

        # Add in the readback function.
        config.underlay.append(renpy.Keymap(rollback=readback_mode))


# This label is called in a new context, when the user succesfully
# enters Readback mode.
label readback:

    # If we have an empty readback buffer, go home.
    if not readback_newest:
        return

    python hide:

        rb = readback_newest

        while True:
            
            rb.show()

            ui.add(renpy.Keymap(rollback=lambda : "older",
                                rollforward=lambda : "newer",
                                dismiss=lambda : "dismiss",
                                ))

            res = ui.interact()

            if res == "newer":
                rb = rb.newer
                if not rb:
                    break

            elif res == "older":
                if rb.older:
                    rb = rb.older

            elif res == "dismiss":
                break

    return
    

        
