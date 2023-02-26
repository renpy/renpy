# Disable the director until the director example enables it.
default _director_enable = False

python early hide:



    import shutil
    fn1 = os.path.join(renpy.config.gamedir, "tutorial_director.rpym")
    fn2 = os.path.join(renpy.config.gamedir, "tutorial_director.rpy")

    try:

        if not renpy.session.get("director", False):
            shutil.copy(fn1, fn2)

        store.director_readonly = False

    except Exception:

        store.director_readonly = True
