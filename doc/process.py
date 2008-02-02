#!/usr/bin/python2.4

import sys
import os.path

# import xml.etree.ElementTree as elementtree
# sys.modules['elementtree'] = elementtree

from elementtree.ElementTree import ElementTree, Element, SubElement, tostring, fromstring
from elementtidy import TidyHTMLTreeBuilder

# Removes everyhing we don't care about from the wikipages.
def remove_crap(n):

    classes = n.attrib.get("class", "").split()
    
    if "editsection" in classes:
        return None
    if "printfooter" in classes:
        return None    
    if "magnify" in classes:
        return None

    
    id = n.attrib.get("id", None)

    if "catlinks" == id:
        return None

    newchildren = [ ]
    for i in n:
        i = remove_crap(i)
        if i is not None:
            newchildren.append(i)

    n[:] = newchildren

    if n.tag == "a" and not n.text:
        n.text = "SPACE REMOVE ME PLEASE"
        
    return n
    
def process(src, dst, nav):

    if nav:
        nav = fromstring(nav)
    
    base = "../" * (len(dst.split('/')) - 1)

    if dst.startswith("./"):
        base = ""
    
    tree = TidyHTMLTreeBuilder.parse(src)

    XHTML = "{http://www.w3.org/1999/xhtml}"

    for elem in tree.getiterator():
        if elem.tag.startswith(XHTML):
            elem.tag = elem.tag[len(XHTML):]

    by_id = dict()

    for n in tree.getiterator():
        if "id" in n.attrib:
            by_id[n.attrib["id"]] = n

    html = Element("html")
    head = SubElement(html, "head")
    title = SubElement(head, "title")
    title.text = tree.findtext(".//title")
    head = SubElement(head, "link", rel="stylesheet", href=base + "shared.css")
    head = SubElement(head, "link", rel="stylesheet", href=base + "monobook.css")
    head = SubElement(head, "link", rel="stylesheet", href=base + "common.css")
    head = SubElement(head, "link", rel="stylesheet", href=base + "monobook2.css")
    head = SubElement(head, "link", rel="stylesheet", href=base + "docs.css")
    
    body = SubElement(html, "body")
    # gw = SubElement(body, "div", id="globalWrapper")
    # cc = SubElement(gw, "div", id="column-content")
    # content = SubElement(cc, "div", id="content")

    bc = by_id['bodyContent']
    body.append(bc)

    bc.remove(by_id['siteSub'])
    bc.remove(by_id['contentSub'])
    bc.remove(by_id['jump-to-nav'])

    for n in bc.findall(".//a"):
        if "href" in n.attrib:
            href = n.attrib['href']

            if href.startswith("/wiki/Image:") or href.startswith("/w/"):
                n.attrib['href'] = 'http://www.renpy.org' + href
                continue

            if href.startswith("#"):
                continue
            
            if href.startswith("http:"):
                continue
            
            href = href.replace("/wiki/renpy/doc/", base)

            if "#" in href:
                href.replace("#", ".html#")
            else:
                href += ".html"

            n.attrib['href'] = href

    for n in bc.findall(".//img"):
        src = n.attrib["src"]
        src = base + "images" + src[src.rfind("/"):]
        n.attrib["src"] = src


    if nav:
        hr = Element("hr")
        bc[:] = [ nav ] + list(bc) + [ hr, nav ]
    
    html = remove_crap(html)        

    doc = tostring(html)
    doc = doc.replace("SPACE REMOVE ME PLEASE", "")
    file(dst, "w").write(doc)
    
    
def process_dir(src, dst, nav):
    try:
        os.makedirs(dst)
    except:
        pass

    for fn in os.listdir(src):
        if os.path.isdir(src + "/" + fn):
            continue

        if fn.endswith(".1"):
            continue
        
        process(src + "/" + fn, dst + "/" + fn + ".html", nav)

nav = '<p class="docnav"><a href="../index.html">documentation index</a></p>'
process_dir("www.renpy.org/wiki/renpy/doc/tutorials", "tutorials", nav) 

nav = '<p class="docnav"><a href="../index.html">documentation index</a> &#x25e6; <a href="Reference_Manual.html">reference manual</a> &#x25e6; <a href="Function_Index.html">function index</a></p>'
process_dir("www.renpy.org/wiki/renpy/doc/reference", "reference", nav) 

nav = '<p class="docnav"><a href="../../index.html">documentation index</a> &#x25e6; <a href="../Reference_Manual.html">reference manual</a> &#x25e6; <a href="../Function_Index.html">function index</a></p>'
process_dir("www.renpy.org/wiki/renpy/doc/reference/functions", "reference/functions", nav) 

nav = ''
process_dir("www.renpy.org/wiki/renpy/doc/", ".", nav) 
