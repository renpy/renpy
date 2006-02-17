init:
    image black = Solid((0, 0, 0, 255))

label main_menu:

    $ renpy.renpy.style.write_docs("doc/styles.xml")
    $ renpy.renpy.style.write_hierarchy("doc/style_heirarchy.xml")
    $ raise "foo"
    
