import renpy

nodes = [ ]

def got_node(n):
    nodes.append(n)

    if isinstance(n, renpy.ast.Say):
        print n.what

renpy.config.searchpath = [ 'moonlight' ]

renpy.script.Script(got_node)

print "Script consists of %d nodes." % len(nodes)
print "Script consists of %d say nodes." % len([ n for n in nodes if isinstance(n, renpy.ast.Say)])
print "Script consists of %d menu nodes." % len([ n for n in nodes if isinstance(n, renpy.ast.Menu)])
