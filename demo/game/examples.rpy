# This file is responsible for displaying code examples. It expects to see
# comments like #begin foo and #end foo a the start of lines. The code is
# then used to create example fragments.
#
# When we see:
#
# show example foo bar
#
# We concatenate fragements foo and bar, higlight them, wrap them into a
# viewport, button and transform, and display them to the user.

transform example_transform:
    ypos 450 yanchor 1.0 xpos 0 xanchor 0
    alpha 0
    on hover:
        linear .25 alpha 1.0
    on idle:
        linear .25 alpha .25
    on hide:
        linear .25 alpha 0
        


init python:

    # This maps from example name to the text of the fragment.    
    examples = { }

    class __Example(object):
        """
         When parameterized, this displays an example window, containing
         example text from blocks with those parameters.
         """

        def parameterize(self, name, args):

            # Collect the examples we use.            
            lines1 = [ ]
            
            for i in args:
                if i not in examples:
                    raise Exception("Unknown example %r." % i)
                lines1.extend(examples[i])


            # Strip off doubled blank lines.
            last_blank = False
            lines = [ ]
            
            for i in lines1:

                if not i and last_blank:
                    continue

                last_blank = not i

                lines.append(i)
            
            # Join them into a single string.
            code = "\n".join(lines)

            ct = Text(code, size=14, color="#000")
            vp = Viewport(ct, ymaximum=120, draggable=True, mousewheel=True)
            b = Button(vp,
                       clicked=ui.returns(None),
                       background = "#fffc",
                       )
            return example_transform(b)

image example = __Example()
        
                
init python hide:

    import os.path
    import re
    
    # A list of files we will be scanning.
    files = [ ]
    
    for i in os.listdir(config.gamedir):
        if i.endswith(".rpy"):
            files.append(os.path.join(config.gamedir, i))

    d = os.path.join(config.gamedir, "../../the_question/game")
    for i in os.listdir(d):
        if i.endswith(".rpy"):
            files.append(os.path.join(d, i))
        
            
    for fn in files:

        f = file(fn, "r")

        open_examples = set()
        
        for l in f:

            l = l.rstrip()
            
            m = re.match("\s*#begin (\w+)", l)
            if m:
                example = m.group(1)
                print example, fn

                if example in examples:
                    raise Exception("Example %r is defined in two places.", example)

                open_examples.add(example)
                examples[example] = [ ]

                continue

            m = re.match("\s*#end (\w+)", l)
            if m:
                example = m.group(1)

                if example not in open_examples:
                    raise Exception("Example %r is not open.", example)

                open_examples.remove(example)
                continue

            for i in open_examples:
                examples[i].append(l)

        if open_examples:
            raise Exception("Examples %r remain open at the end of %r" % (open_examples, fn))

        f.close()
            
