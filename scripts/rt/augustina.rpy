default evil = False

layeredimage augustina:

    always "augustina_base"

    attribute whatever null

    group outfit auto

    group eyes auto:
        attribute open default

    group eyebrows auto:
        attribute normal default

    group mouth auto:
        pos (100, 100)
        attribute smile default

    if evil:
        "augustina_glasses_evil"
    else:
        "augustina_glasses"
