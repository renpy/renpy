Template Projects
=================

It's possible to to create a template project that can be used to create
new projects. This can be used to make it easy for creators to begin
making a game with, for example, a gui you develop, rather than the
default gui that comes with Ren'Py.

If at least one template project is present on a creator's computer,
when creating a new game they will be given the option to select a
template project. If they do, the template project will be copied into
the new project, and the following changes will be made:

* The :var:`config.name`, :var:`config.save_directory`, and
  :var:`build.name` variables will be set to the name of
  the new project.

* The tl directory will be removed, and replaced with default translations
  taken from the launcher.

* If translatable strings or comments are found matching those in the launcher,
  the translations will be copied into the new project.

This usually makes an acceptable starting point for new projects.


Creating a Template Project
---------------------------

To create a template project, you need to create a Ren'Py project, then
add a project.json file to it. This file should contain the following
text::

    { "type" : "template" }

Save it, then refresh the launcher, and you should be able to use
your template.


Distributing a Template Project
-------------------------------

You can distribute a template project by zipping it up manually. (You
should not use the Distribute command.) It might make sense to delete
the ``game/saves`` and ``game/cache`` directories before zipping it
up, though this is not required.

The end user can unzip the template project into their projects
directory, then refresh the launcher to make it available.
