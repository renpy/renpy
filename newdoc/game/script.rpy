init 1000000 python:
    import doc

    doc.scan_section("", store)
    doc.scan_section("renpy.", renpy)
    doc.scan_section("theme.", theme)
    doc.scan_section("layout.", layout)
    doc.scan_section("define.", define)
    doc.scan_section("ui.", ui)
    doc.scan_section("im.", im)

    doc.write_line_buffer()

    
    raise SystemExit
    
