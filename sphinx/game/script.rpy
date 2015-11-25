init 1000000 python:
    import doc
    import __builtin__

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
    doc.scan_section("iap.", iap)
    doc.scan_section("achievement.", achievement)

    doc.write_line_buffer()
    doc.write_keywords()

    doc.scan_docs()
    doc.write_reserved(__builtin__, "source/inc/reserved_builtins", False)
    doc.write_reserved(store, "source/inc/reserved_renpy", True)

    doc.write_pure_const()

    doc.write_easings(_warper)

    raise SystemExit

