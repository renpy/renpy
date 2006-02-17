import xml.dom.minidom
import sys

def escape(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;")

def transform_children(node):

    rv = [ ]

    for n in node.childNodes:
        rv.append(transform(n))

    return ''.join(rv)


def transformElement(node):

    attributes = ' '.join(['%s="%s"' % (k, escape(v)) for k,v in node.attributes.items()])

    tag = node.tagName


    # Otherwise, the default.
    return "<%s %s>%s</%s>" % (node.tagName, attributes,
                               transform_children(node), node.tagName)
    
    

def transform(node):

    if node.nodeType == node.ELEMENT_NODE:
        return transformElement(node)
    else:
        return escape(str(node))

def main():

    dom = xml.dom.minidom.parse(sys.argv[1])

    print transform(dom.documentElement)

if __name__ == "__main__":
    main()
