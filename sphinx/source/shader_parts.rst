:orphan:

Default Shader Parts
====================

Shader parts are used by :doc:`model` and :doc:`textshaders`. This file
contains an index of parts by priority, and the source of each shader
part.

Vertex Part Priorities
----------------------

How Ren'Py uses vertex part priorities:

* Priority 0 sets up gl_Position.
* Priority 10 is used to capture gl_Position in virtual or drawable coordinates before adjustment.
* Priorities 20-80 adjust gl_Position in virtual or drawable coordinates.
* Priority 90 is used to capture gl_Position in virtual or drawable coordinates after adjustment.
* Priority 100 transforms gl_Position to viewport coordinates.
* Priority 200 stores more information in varying variables, without touching gl_Position.

In order:

.. include:: inc/shadervertexpriorities

Fragment Part Priorities
------------------------

How Ren'Py uses fragment part priorities:

* Priority 200 determines an original color and stores it in gl_FragColor.
* Priority 300 multiplies that color with a second texture.
* Priority 325 stores alpha before the text shaders adjust it.
* Priority 350 applies text shaders that adjust alpha.
* Priority 375 can undo part of the effect of these text shaders.
* Priority 400 adjusts the color, applying Transform and displayable-based changes.
* Priority 500 adjusts the alpha channel, applying Transform and displayable-based changes.

In order:

.. include:: inc/shaderfragmentpriorities

.. highlight:: glsl

.. include:: inc/shadersource
