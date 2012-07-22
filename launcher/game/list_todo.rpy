# Copyright 2004-2012 Tom Rothamel <pytom@bishoujo.us>
# See LICENSE.txt for license details.

define TODO_ADJUSTMENT = ui.adjustment()

init python:

    def create_todo_list():

        todos = [ ]

        gamedir = project.current.unelide_filename("game")
        files = os.listdir( gamedir )
        print files
        for f in files:
            if f.endswith(".rpy"):
                data = file( project.current.unelide_filename("game/" + f) )
                l = 0
                for line in data:
                    l += 1
                    m = re.match(".*#\s+[Tt][Oo][Dd][Oo]\s+(.*)", line)
                    if m is not None:
                        todos.append( (f, l, m.group(1)) )

        return todos

    class SelectTodo(Action):
        def __init__(self, value):
            self.value = value
            
        def __call__(self):
            e = renpy.editor.editor
            
            fn = project.current.unelide_filename("game/" + self.value[0])
            e.begin(True)
            e.open(fn, line=self.value[1])
            e.end()

screen todo_list:
    
    frame:
        style_group "l"
        style "l_root"
        
        window:
    
            has vbox

            label _("TODO list")
            
            add HALF_SPACER

            viewport:
                yadjustment TODO_ADJUSTMENT
                mousewheel True
                use todo_list_buttons

    textbutton _("Back") action Jump("front_page") style "l_left_button"

screen todo_list_buttons:

    vbox:
        
        $ todos = create_todo_list()
        
        if todos:
        
            for i in todos:
            
                $ buttext = u"%s (%s, line %d)" % (i[2], i[0], i[1])

                textbutton "[buttext]":
                    action SelectTodo(i)
                    style "l_list"
            
            null height 12

label todo:

    call screen todo_list
    jump todo_screen
    
