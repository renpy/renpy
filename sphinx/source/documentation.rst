=============
Documentation
=============

Ren'Py's documentation is built with `Sphinx <https://www.sphinx-doc.org>`_.
Documentation is written in reStructuredText files found in :file:`sphinx/source`,
and generated documentation found in function :ref:`docstrings <docstring>`
scattered throughout the code.

When editing the engine, it's important to keep the documentation
up to date.

This page covers the most common directives, roles, and fields used,
as well as the custom tags written specifically for Ren'Py.

Useful Resources:

* `reStructuredText Primer <https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html#rst-primer>`_
* `Directives <https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html>`_
* `Roles <https://www.sphinx-doc.org/en/master/usage/restructuredtext/roles.html>`_
* `Referencing <https://www.sphinx-doc.org/en/master/usage/referencing.html>`_


.. _docstring:

Docstrings
==========

Documentation can be generated from docstrings scattered throughout the code.

.. warning::

    Do not edit the files in :file:`sphinx/source/inc` directly, as they will be overwritten.

Docstrings may include tags on the first few lines:

\:doc: `section` `kind`
    Indicates that this function should be documented. `section` gives
    the name of the include file the function will be documented in, while
    `kind` indicates the kind of object to be documented (one of ``function``,
    ``method`` or ``class``. If omitted, `kind` will be auto-detected.
\:name: `name`
    The name of the function to be documented. Function names are usually
    detected, so this is only necessary when a function has multiple aliases.
\:args: `args`
    This overrides the detected argument list. It can be used if some arguments
    to the function are deprecated.

Example:

.. code-block:: python

    def warp_speed(factor, transwarp=False):
        """
        :doc: warp
        :name: renpy.warp_speed
        :args: (factor)

        Exceeds the speed of light.
        """

        renpy.engine.warp_drive.engage(factor)


Blocks
======
.. rst:directive:: note

    .. list-table::
        :stub-columns: 1

        *
            - Example
            - .. code-block:: rst

                .. note::

                    Here's a little bit of information for you.

        *
            - Result
            - .. note::

                Here's a little bit of information for you.


.. rst:directive:: seealso

    .. list-table::
        :stub-columns: 1

        *
            - Example
            - .. code-block:: rst

                .. seealso::

                    You should also see the following page:

        *
            - Result
            - .. seealso::

                You should also see the following page:


.. rst:directive:: warning

    Marks a section as something the reader should keep in mind. May include
    pitfalls, bugs, or weird interactions with other things.

    .. list-table::
        :stub-columns: 1

        *
            - Example
            - .. code-block:: rst

                .. warning::

                    This is something you should keep in mind.

        *
            - Result
            - .. warning::

                This is something you should keep in mind.


Inline Formatting
=================
.. rst:role:: abbr

    Creates an abbreviation whose full meaning can be seen by hovering it with the cursor.

    .. list-table::
        :stub-columns: 1

        *
            - Example
            - .. code-block:: rst

                The :abbr:`CLI (Command Line Interface)` is a way to run Ren'Py commands
                without having to use the launcher.

        *
            - Result
            - The :abbr:`CLI (Command Line Interface)` is a way to run Ren'Py commands
              without having to use the launcher.


.. rst:role:: dfn

    Used for keyword definitions.

    .. list-table::
        :stub-columns: 1

        *
            - Example
            - .. code-block:: rst

                :dfn:`idle`
                    Used when the displayable is neither focused nor selected.

        *
            - Result
            - :dfn:`idle`
                Used when the displayable is neither focused nor selected.


.. rst:role:: file

    Used to mark the text as being a filename or part of a file name.

    .. list-table::
        :stub-columns: 1

        *
            - Example
            - .. code-block:: rst

                You can find settings in :file:`options.rpy`.

        *
            - Result
            - You can find settings in :file:`options.rpy`.


References
==========

.. rst:role:: doc

    Refers to a page of documentation. Do not include the `.rst` extension at the end.

    By default it will use the page title as the displayed text.

    .. list-table::
        :stub-columns: 1

        *
            - Example
            - .. code-block:: rst

                :doc:`updater`

        *
            - Result
            - :doc:`updater`

    In order to change the displayed text, do the following:

    .. list-table::
        :stub-columns: 1

        *
            - Example
            - .. code-block:: rst

                :doc:`Ren'Py Updater <updater>`

        *
            - Result
            - :doc:`Ren'Py Updater <updater>`



.. rst:role:: ref

    References any arbitrary part of a document. Makes use of standard reStructuredText labels.
    The label name must be unique for this to work. When defining the label, it MUST start with an undecore.

    .. Comment: Sadly the reference doesn't work here. Not sure why.

    .. list-table::
        :stub-columns: 1

        *
            - Example
            - .. code-block:: rst

                .. _my-reference-label:

                Section to cross-reference
                --------------------------

                This is the text of the section.

                It refers to the section itself, see :ref:`my-reference-label`.


External links
==============

.. rst:role:: ghbug

    Create a hyperlink to a `Ren'Py GitHub issue <https://github.com/renpy/renpy/issues>`_ with the specified number.

    .. list-table::
        :stub-columns: 1

        *
            - Example
            - .. code-block:: rst

                :ghbug:`51`: The slow_done callback was not called after a rollback.

        *
            - Result
            - :ghbug:`51`: The slow_done callback was not called after a rollback.


.. rst:role:: lpbug

    (Obselete) Create a hyperlink to a `Ren'Py LaunchPad issue <https://launchpad.net/renpy>`_ with the specified number.

    .. list-table::
        :stub-columns: 1

        *
            - Example
            - .. code-block:: rst

                :lpbug:`647686`, a regression that prevented sounds from looping
                properly.

        *
            - Result
            - :lpbug:`647686`, a regression that prevented sounds from looping
              properly.


.. rst:role:: pep

    Create a hyperlink to a `Python Enhancement Proposal (PEP) <https://peps.python.org/>`_ with the specified number.

    .. list-table::
        :stub-columns: 1

        *
            - Example
            - .. code-block:: rst

                Ren'Py's string formatting is taken from the
                :pep:`3101` string formatting syntax.

        *
            - Result
            - Ren'Py's string formatting is taken from the
              :pep:`3101` string formatting syntax.




Custom Directives and Roles
===========================

.. rst:directive:: describe

    Creates a full-width box that contains some text. This is the base
    component for later elements, such as ``option``, ``screen-property``, and so on.

    ``describe`` does not create any indices or references, but the derivative classes do.

    .. note ::

        This is the block that's used primarily on this page. The example may appear
        different since it is indented in the source code.

    .. list-table::
        :stub-columns: 1

        *
            - Example
            - .. code-block:: rst

                .. describe:: <basedir>

                    In the commands below, <basedir> refers to the
                    path to the project directory.

        *
            - Result
            - .. describe:: <basedir>

                | In the commands below, <basedir> refers to the
                | path to the project directory.


.. rst:directive:: option
.. rst:role:: option

    Used for :doc:`cli` arguments.

    .. list-table::
        :stub-columns: 1

        *
            - Example
            - .. code-block:: rst

                .. option:: --demo_option

                    If given, displays a help message

                    * [Demo Reference] :option:`--demo_option`
                    * [Real Reference] :option:`--launch`

        *
            - Result
            - .. option:: --demo_option

                If given, displays a help message

                * [Demo Reference] :option:`--demo_option`
                * [Real Reference] :option:`--launch`


.. rst:directive:: screen-property
.. rst:role:: scpref

    Used for :doc:`Screen Properties <screens>`.

    .. list-table::
        :stub-columns: 1

        *
            - Example
            - .. code-block:: rst

                .. screen-property:: demo_screen_property

                    :type: str
                    :default: None

                    This property does nothing

                    * [Demo Reference] :scpref:`demo_screen_property`
                    * [Real Reference] :scpref:`zorder`

        *
            - Result
            - .. screen-property:: demo_screen_property

                :type: str
                :default: None

                This property does nothing

                * [Demo Reference] :scpref:`demo_screen_property`
                * [Real Reference] :scpref:`zorder`


.. rst:directive:: style-property
.. rst:role:: propref

    Used for :doc:`style_properties`.

    .. list-table::
        :stub-columns: 1

        *
            - Example
            - .. code-block:: rst

                .. style-property:: demo_style_property str

                    :default: #000000

                    This controls the color of the displayable.

                    * [Demo Reference] :propref:`demo_style_property`
                    * [Real Reference] :propref:`xpos`

        *
            - Result
            - .. style-property:: demo_style_property str

                :default: #000000

                This controls the color of the displayable.

                * [Demo Reference] :propref:`demo_style_property`
                * [Real Reference] :propref:`xpos`


.. rst:directive:: text-tag
.. rst:role:: tt

    Used for :doc:`Text Tags <text>`.

    .. list-table::
        :stub-columns: 1

        *
            - Example
            - .. code-block:: rst

                .. text-tag:: demo_text_tag

                    This text tag does nothing.

                    * [Demo Reference] :tt:`demo_text_tag`
                    * [Real Reference] :tt:`font`

        *
            - Result
            - .. text-tag:: demo_text_tag

                    This text tag does nothing.

                    * [Demo Reference] :tt:`demo_text_tag`
                    * [Real Reference] :tt:`font`


.. rst:directive:: transform-property
.. rst:role:: tpref

    Used for :doc:`transform_properties`.

    .. list-table::
        :stub-columns: 1

        *
            - Example
            - .. code-block:: rst

                .. transform-property:: demo_transform_property

                    :type: float
                    :default: 0

                    This property controls nothing.

                    * [Demo Reference] :tpref:`demo_transform_property`
                    * [Real Reference] :tpref:`xpos`

        *
            - Result
            - .. transform-property:: demo_transform_property

                :type: float
                :default: 0

                This property controls nothing.

                * [Demo Reference] :tpref:`demo_transform_property`
                * [Real Reference] :tpref:`xpos`


Code
====

.. rst:directive:: exception
.. rst:role:: exc

    Used to define exceptions.

    .. list-table::
        :stub-columns: 1

        *
            - Example
            - .. code-block:: rst

                .. exception:: InvalidShapeException

                    Raised if a shape is not a regular polygon.

                    * [Demo Reference] :exc:`InvalidShapeException`
                    * [Real Reference] :exc:`renpy.IgnoreEvent`

        *
            - Result
            - .. exception:: InvalidShapeException

                Raised if a shape is not a regular polygon.

                * [Demo Reference] :exc:`InvalidShapeException`
                * [Real Reference] :exc:`renpy.IgnoreEvent`


.. rst:directive:: function
.. rst:role:: func

    .. list-table::
        :stub-columns: 1

        *
            - Example
            - .. code-block:: rst

                .. function:: DemoCircleArea(radius)

                    :param float radius: The radius of the circle to calculate.

                    * [Demo Reference] :func:`DemoCircleArea`
                    * [Real Reference] :func:`style.rebuild`

        *
            - Result
            - .. function:: DemoCircleArea(radius)

                :param float radius: The radius of the circle to calculate.

                * [Demo Reference] :func:`DemoCircleArea`
                * [Real Reference] :func:`style.rebuild`


.. rst:directive:: var
.. rst:role:: var

    .. list-table::
        :stub-columns: 1

        *
            - Example
            - .. code-block:: rst

                .. var:: demo_variable

                    This is a dummy variable that does nothing.

                    * [Demo Reference] :var:`demo_variable`
                    * [Real Reference] :var:`gui.bar_size`

        *
            - Result
            - .. var:: demo_variable

                This is a dummy variable that does nothing.

                * [Demo Reference] :var:`demo_variable`
                * [Real Reference] :var:`gui.bar_size`


Class, Method, and Attribute
----------------------------

All three of these are usually defined with :ref:`docstrings <docstring>`.

.. rst:directive:: class
.. rst:role:: class

    Used to define a class.

.. rst:directive:: attribute
.. rst:role:: attr

    Used to define an attribute within a class. Cannot be used in isolation, must be within a class.

.. rst:directive:: method
.. rst:role:: meth

    Used to define a method within a class. Cannot be used in isolation, must be within a class.

    .. list-table::
        :stub-columns: 1

        *
            - Example
            - .. code-block:: rst

                .. class:: DemoClass
                    * [Demo Reference] :class:`DemoClass`
                    * [Real Reference] :class:`Transform`

                    .. attribute:: demo_radius

                        :type: float
                        The radius of the circle

                        * [Demo Reference] :attr:`demo_radius`
                        * [Real Reference] :attr:`Transform.hide_request`

                    .. attribute:: demo_color

                        :type: str
                        The color of the circle

                    .. method:: demo_area()

                        :return: The area of the circle
                        :rtype: float

                        * [Demo Reference] :meth:`DemoClass.demo_area`
                        * [Real Reference] :meth:`Transform.update`

                    .. method:: demo_repaint(color)

                        :param str color: The new color of the circle

        *
            - Result
            - .. class:: DemoClass

                * [Demo Reference] :class:`DemoClass`
                * [Real Reference] :class:`Transform`

                .. attribute:: demo_radius

                    :type: float
                    The radius of the circle

                    * [Demo Reference] :attr:`demo_radius`
                    * [Real Reference] :attr:`Transform.hide_request`

                .. attribute:: demo_color

                    :type: str
                    The color of the circle

                .. method:: demo_area()

                    :return: The area of the circle
                    :rtype: float

                    * [Demo Reference] :meth:`DemoClass.demo_area`
                    * [Real Reference] :meth:`Transform.update`

                .. method:: demo_repaint(color)

                    :param str color: The new color of the circle
