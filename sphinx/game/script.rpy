init 1000000 python:
    import doc
    import shaderdoc

    shaderdoc.shaders()

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
    doc.scan_section("gui.", gui)
    doc.scan_section("layeredimage.", layeredimage)
    doc.scan_section("Matrix.", Matrix)

    doc.write_line_buffer()
    doc.write_keywords()

    doc.scan_docs()
    doc.write_reserved(doc.builtins, "source/inc/reserved_builtins", False)
    doc.write_reserved(store, "source/inc/reserved_renpy", True)

    doc.write_pure_const()

    doc.write_easings(_warper)

    doc.write_tq()

    doc.check_dups()

    console_commands = _console.help(None, True)
    console_commands = "\n\n".join(console_commands.split("\n"))
    f = open("source/inc/console_commands", "w")
    f.write(console_commands)
    f.close()

    raise SystemExit
