import inspect
import re
import collections


# A map from filename to a list of lines that are supposed to go into
# that file.
line_buffer = collections.defaultdict(list)


def scan(name, o):

    # The type of object we're dealing with.
    doc_type = "function"

    # The section it's going into.
    section = None

    # The formatted arguments.
    args = None
    
    # Get the function's docstring.
    doc = inspect.getdoc(o)

    if not doc:
        return

    # Break up the doc string, scan it for specials.
    lines = [ ]

    for l in doc.split("\n"):
        m = re.match(r':doc: *(\w+) *(\w+)?', l)
        if m:
            section = m.group(1)

            if m.group(2):
                doc_type = m.group(2)

            continue

        m = re.match(r':args: *(.*)', l)
        if m:
            args = m.group(1)
            continue

        m = re.match(r':name: *(\S+)', l)
        if m:
            if name != m.group(1):
                return

        
        lines.append(l)

    if section is None:
        return


    if args is None:
    
        # Get the arguments.
        if inspect.isclass(o):
            init = getattr(o, "__init__", None)
            if not init:
                return

            try:
                args = inspect.getargspec(init)
            except:
                args = None
        elif inspect.isfunction(o):
            args = inspect.getargspec(o)
        else:
            return

        # Format the arguments.
        if args is not None:
            
            args = inspect.formatargspec(*args)
            args = args.replace("(self, ", "(")
        else:
            args = "()"
            

    # Put it into the line buffer.
    lb = line_buffer[section]

    lb.append(".. %s:: %s%s" % (doc_type, name, args))

    for l in lines:
        lb.append("    " + l)

    lb.append("")



def scan_section(name, o):
    """
    Scans object o. Assumes it has the name name.
    """

    for n in dir(o):
        scan(name + n, getattr(o, n))
            

def write_line_buffer():

    for k, v in line_buffer.iteritems():

        print "Generating", k
        
        f = file("source/inc/" + k, "w")
        
        print >>f, ".. Automatically generated file - do not modify."
        print >>f

        for l in v:
            print >>f, l
        
        f.close()
