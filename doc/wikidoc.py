import os
import os.path
import urllib
import sys

dir = '/home/tom/shinobu/home/home/tom/moin.renpy/data/pages/'
pages = [ ]
pagefns = [ ]

for name in os.listdir(dir):
    if not os.path.exists(dir + name + "/current"):
        continue

    name = name.replace("(2f)", "/")
    name = name.replace("(2e)", ".")
    name = name.replace("(26)", "&")
    name = name.replace("(27)", "'")
    name = name.replace("(2d)", "-")
    name = name.replace("(2c)", ",")
    
    if not (name.startswith("renpy/doc/reference") or 
            name.startswith("renpy/doc/tutorials/Quick") or
            name.startswith("renpy/doc/tutorials/TheQuestion")):

        continue

    if name == "renpy/doc/reference":
        continue
    
    pages.append(name)
    pagefns.append(name.replace("renpy/doc/", ""))

if "download" in sys.argv:

    for url, fn in zip(pages, pagefns):

        dir = os.path.dirname(fn)
        if not os.path.exists("mirror/" + dir):
            os.makedirs("mirror/" + dir)

        print url

        urllib.urlretrieve("http://www.renpy.org/wiki/" + url,
                            "mirror/" + fn + ".html")

    

from elementtree.ElementTree import ElementTree, Element, SubElement, parse, fromstring
from elementtidy import TidyHTMLTreeBuilder
XHTML = "{http://www.w3.org/1999/xhtml}"


def process(fn):

    print "Processing", fn
    
    if "This page does not exist yet" in file("mirror/" + fn + ".html").read():
        return
        
    dir = os.path.dirname(fn)
    if dir and not os.path.exists(dir):
        os.makedirs(dir)

    root = "../" * len(dir.split('/'))

    disclaimer = fromstring("""\
<div align="center">
<b>Reference Manual:</b>
(<a href="%(root)sreference/Reference_Manual.html">offline</a>
| <a href="http://www.renpy.org/wiki/renpy/doc/reference/">online</a>)
<b>Quickstart:</b>
(<a href="%(root)stutorials/Quickstart.html">offline</a>
| <a href="http://www.renpy.org/wiki/renpy/doc/tutorials/Quickstart">online</a>)
</div>
""" % locals())

                            
    tree = TidyHTMLTreeBuilder.parse("mirror/" + fn + ".html") 

    for elem in tree.getiterator():
        if elem.tag.startswith(XHTML):
            elem.tag = elem.tag[len(XHTML):]

    for div in tree.getroot().findall(".//div"):
        if div.get('id') == 'content':

            # Convert all hrefs.
            for a in div.findall(".//*"):
                if 'href' in a.attrib:
                    href = a.attrib['href']
                    if href.startswith("/wiki/renpy/doc/"):

                        href = href.replace("/wiki/renpy/doc/", root)
                        if "#" in href:
                            href = href.replace("#", ".html#")
                        else:
                            href = href + ".html"
                            
                    elif href[0] == '/': 
                        href = "http://www.renpy.org" + href
                    elif href.startswith('http:/'):
                        href = "http://www.renpy.org" + href[5:]
                        
                    a.attrib['href'] = href

            html = Element("html")
            head = SubElement(html, "head")
            SubElement(head, "link", rel="stylesheet", type="text/css", href=root + "screen.css")
            body = SubElement(html, "body")
            body.append(disclaimer)
            body.append(div)
            body.append(disclaimer)
                    
            ElementTree(html).write(fn + ".html")
            
for fn in pagefns:
    process(fn)

print "Did you download the latest documentation?"
