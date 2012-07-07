init 1000000 python:
    import doc

    doc.scan_section("", renpy.store)
    doc.scan_section("renpy.", renpy)
    doc.scan_section("renpy.music.", renpy.music)
    doc.scan_section("theme.", theme)
    doc.scan_section("layout.", layout)
    doc.scan_section("define.", define)
    doc.scan_section("ui.", ui)
    doc.scan_section("im.", im)
    doc.scan_section("im.matrix.", im.matrix)
    doc.scan_section("build.", build)
    doc.scan_section("updater.", updater)

    doc.write_line_buffer()
    doc.write_keywords()
    
    
    raise SystemExit
    
