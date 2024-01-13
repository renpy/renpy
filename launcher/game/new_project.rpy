# Copyright 2004-2024 Tom Rothamel <pytom@bishoujo.us>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

init python:
    import shutil
    import os
    import time
    import re


label new_project:

    if persistent.projects_directory is None:
        call choose_projects_directory

    if persistent.projects_directory is None:
        $ interface.error(_("The projects directory could not be set. Giving up."))

    if PY2:
        $ interface.info(_("Warning : you are using Ren'Py 7. It is recommended to start new projects using Ren'Py 8 instead."))

    python:
        new_project_language = __("{#language name and font}")
        gui_kind = "new_gui_project"

        # When translating this, feel free to replace [new_project_language] with the translation of your language.
        interface.info(_("You will be creating an [new_project_language]{#this substitution may be localized} language project. Change the launcher language in preferences to create a project in another language."), cancel=Jump("front_page"))

    python:
        if project.manager.templates:
            gui_kind, gui_template_path = interface.choice(
                _("Please select a template project to use."),
                [ ( ("new_gui_project", None), _("Do not use a template project.") ) ] +
                [ ( ("new_template_project", p.path ), p.name) for p in project.manager.templates ],
                ("new_gui_project", None),
                cancel=Jump("front_page"),
            )

    python:
        project_name = ""
        while True:
            project_name = interface.input(
                _("PROJECT NAME"),
                _("Please enter the name of your project:"),
                allow=interface.PROJECT_LETTERS,
                cancel=Jump("front_page"),
                default=project_name,
            )

            project_name = project_name.strip()
            if not project_name:
                interface.error(_("The project name may not be empty."), label=None)
                continue

            project_dir = os.path.join(persistent.projects_directory, project_name)

            if project.manager.get(project_name) is not None:
                interface.error(_("[project_name!q] already exists. Please choose a different project name."), project_name=project_name, label=None)
                continue

            if os.path.exists(project_dir):
                interface.error(_("[project_dir!q] already exists. Please choose a different project name."), project_dir=project_dir, label=None)
                continue
            break

    jump expression gui_kind
