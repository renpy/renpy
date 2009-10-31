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
            vp = Viewport(ct, child_size=(2000, 2000), ymaximum=120, draggable=True, mousewheel=True)
            w = Window(vp, background = "#fffc", right_padding=0, bottom_padding=0, yminimum=0)
            return example_transform(w)

image example = __Example()
        
                
init python hide:

    import os.path
    import re
    
    # A list of files we will be scanning.
    files = [ ]
    
    for i in os.listdir(config.gamedir):
        if i.endswith(".rpy"):
            files.append(os.path.join(config.gamedir, i))

    for fn in files:

        f = file(fn, "r")

        open_examples = set()
        
        for l in f:

            l = l.rstrip()
            
            m = re.match("\s*#begin (\w+)", l)
            if m:
                example = m.group(1)

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
            
