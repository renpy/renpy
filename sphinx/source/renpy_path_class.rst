=========
RenpyPath
=========

Ren'Py has a `PathLike <https://docs.python.org/3/library/os.html#os.PathLike>`_
providing all path operations of
`PurePath <https://docs.python.org/3/library/pathlib.html#pure-paths>`_
some methods from `Path <https://docs.python.org/3/library/pathlib.html#pathlib.Path>`_,
and more convenience methods for Ren'Py file operations.
Unlike `pathlib <https://docs.python.org/3/library/pathlib.html>`_ classes
which work on physical filesystem files, :class:`RenpyPath` works on Ren'Py game files,

:class:`RenpyPath` files are discovered using Ren'Py's standard search method,
and may reside in the game directory, in an RPA archive, as an Android
asset, in a remote server, or in any additional location a plugin may
provide.

Few usage examples to get you started
-------------------------------------

**Find all Ren'Py valid image files in standard "images" directory:**

.. code-block:: python

    init python:
    	allowed_extensions = ("*.png", "*.jpg", "*.jpeg", "*.webp", "*.avif")
        for image_file in RenpyPath("images").files_matching(*allowed_extensions, case_sensitive=False):
            record_image(image_files)


**Find eileen's image files:**

.. code-block:: python

    init python:
    	eileen_prefix = 'eileen[_ ]'
        eileen_images = list(
            RenpyPath("images").files_matching(
                f"{eileen_prefix}*.png", f"{eileen_prefix}*.jpg", f"{eileen_prefix}*.jpeg", f"{eileen_prefix}*.webp", f"{eileen_prefix}*.avif",
                case_sensitive=False
            )
        )

**Find all volume directories of arc 1 which have a chapter 7:**

For example, if automating menus.

.. code-block:: python

    init python:
        for volume_chapter in RenpyPath("story/arc1").rglob("volume*/chapter7/"):
            volume_name = volume_chapter.parent.name
            print(f"arc1 has chapter1 in {volume_name}")


**Quickly find first bgm:**

.. code-block:: python

    init python:
        audio_dir = RenpyPath("audio")
        try:
            bgm_track_1 = next(audio_dir.files_matching("bgm_*.ogg", "bgm_*.opus"))
            renpy.audio.play(bgm_track_1)
        except StopIteration:
            renpy.notify("No bgm files exist")

**Create a file in the game directory relative to another:**

.. code-block:: python

    init python:
        commentary_path = RenpyPath("comments")
        (commentary_path / f'comment_{next_comment_number}.txt').as_path().write_text(comment)

**Read a file relative to the current script:**

.. code-block:: python

    init python:
        here, _line = RenpyPath.current_path_line()
        data_text = (here.parent / "my_data.txt").read_text()

**Exclude current script and its compiled file from builds:**

.. code-block:: python

    init python:
        here, _line = RenpyPath.current_path_line()
        here.rpy_path().build_classify(None)
        here.rpyc_path().build_classify(None)

**Replace loadable + open_file with RenpyPath:**

.. code-block:: python

    init python:
        with RenpyPath("data/data.bin").open("rb") as f:
            bindata = f.read()

**Read a JSON file:**

.. code-block:: python

    init python:
        import json
        with RenpyPath("data/config.json").open() as f:
            data = json.load(f)


.. include:: inc/renpy_path



Choosing between using :class:`RenpyPath` and :func:`list_files`
----------------------------------------------------------------

Use :func:`renpy.list_files` when you want a full flat listing.
Use :class:`RenpyPath` when you want to navigate a subset of directories or
perform tree-like operations over Ren'Py files.
