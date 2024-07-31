python early:
    config.generating_documentation = True

init 1000000 python:
    import doc
    import shaderdoc
    import renpy_json

    del object.__init__

    srcdir = 'source'
    if os.path.isdir('sphinx') and os.path.split(os.getcwd())[-1] == 'renpy':
        srcdir = os.path.join('sphinx', 'source') # ran from renpy/. cwd using sphinx in-game project

    incdir = os.path.join(srcdir, 'inc')

    shaderdoc.shaders(incdir=incdir)
    shaderdoc.textshaders(incdir=incdir)

    doc.scan_section("", renpy.store)
    doc.scan_section("renpy.", renpy)
    doc.scan_section("renpy.music.", renpy.music)
    doc.scan_section("renpy.audio.filter.", renpy.audio.filter)
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
    doc.scan_section("achievement.steam.", _renpysteam)

    doc.write_line_buffer(incdir=incdir)
    doc.write_keywords(srcdir=srcdir)

    doc.scan_docs(srcdir=srcdir, incdir=incdir)
    doc.write_reserved(doc.builtins, os.path.join(incdir, "reserved_builtins"), False)
    doc.write_reserved(store, os.path.join(incdir, "reserved_renpy"), True)

    doc.write_pure_const(incdir=incdir)

    doc.write_easings(_warper, incdir=incdir)

    doc.write_tq(srcdir=srcdir)

    doc.check_dups()

    console_commands = _console.help(None, True).replace("\n ", "\n\n* ")
    with open(os.path.join(incdir, "console_commands"), "w") as f:
        f.write(console_commands)

    renpy_json.main()

    raise SystemExit
