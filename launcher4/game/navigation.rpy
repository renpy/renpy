init python in navigation:
    import store.interface as interface
    import store.project as project
    import store.editor as editor
    from store import persistent, Action
    

    # The last navigation screen we've seen. This is the scree we try to go
    # to the next time we enter navigation. (We may not be able to go there,
    # if the screen is empty.)
    if persistent.navigation is None:
        persistent.navigation = "label"
    
    # A map from a kind of information, to how we should sort it. Possible 
    # sorts are alphabetical, by-file, natural.
    if persistent.navigation_sort is None:
        persistent.navigation_sort = { }
    
    # A map from kind of label to the name of that kind.
    KINDS = { 
        "file" : _("Navigate Files"),
        "label" : _("Navigate Labels"),
        "define" : _("Navigate Defines"),
        "transform" : _("Navigate Transforms"),
        "screen" : _("Navigate Screens"),
        "callable" : _("Navigate Callables"),
        }

    # A map from kind name to adjustment.
    adjustments = { }

    for i in KINDS:
        persistent.navigation_sort.setdefault(i, "by-file")
        adjustments[i] = ui.adjustment()

    def group_and_sort(kind):
        """
        This is responsible for pulling navigation information of the 
        appropriate kind out of project.current.dump, grouping it, 
        and sorting it.
        
        This returns a list of (group, list of (name, filename, line)). The 
        group may be a string or None.
        """
        
        sort = persistent.navigation_sort[kind]
        
        name_map = project.current.dump.get("location", {}).get(kind, { })
        
        groups = { }
        
        for name, loc in name_map.items():
            filename, line = loc
            
            
            if sort == "alphabetical":
                group = None
            else:
                group = filename
                if group.startswith("game/"):
                    group = group[5:]
            
            g = groups.get(group, None)
            if g is None:
                groups[group] = g = [ ]
                
            g.append((name, filename, line))
            
        for g in groups.values():
            if sort == "natural":
                g.sort(key=lambda a : a[2])
            else:
                g.sort(key=lambda a : a[0].lower())
                
        rv = list(groups.items())
        rv.sort()

        return rv

    def group_and_sort_files():
        
        rv = [ ]
        
        for fn in project.current.script_files():
            shortfn = fn
            if shortfn.startswith("game/"):
                shortfn = fn[5:]
                
            rv.append((shortfn, fn, None))
            
        rv.sort()
        
        return [ (None, rv) ]

    class ChangeKind(Action):
        """
        Changes the kind of thing we're navigating over.
        """
        
        def __init__(self, kind):
            self.kind = kind
            
        def get_selected(self):
            return persistent.navigation == self.kind

        def __call__(self):
            if persistent.navigation == self.kind:
                return
                
            persistent.navigation = self.kind
            renpy.jump("navigation_loop")

    class ChangeSort(Action):
        
        def __init__(self, sort):
            self.sort = sort
            
        def get_selected(self):
            return persistent.navigation_sort[persistent.navigation] == self.sort
            
        def __call__(self):
            if self.get_selected():
                return
            
            persistent.navigation_sort[persistent.navigation] = self.sort
            renpy.jump("navigation_loop")

screen navigation:
    
    frame:
        style_group "l"
        style "l_root"
        
        window:
    
            has vbox
    
            frame style "l_label":
                has hbox xfill True
                text "[title]" style "l_label_text"
                
                
                if persistent.navigation != "file":
                
                    frame:
                        style "l_alternate"
                        style_group "l_small"
                        
                        has hbox
                        
                        text _("Order: ")
                        textbutton _("alphabetical") action navigation.ChangeSort("alphabetical")
                        text " | "
                        textbutton _("by-file") action navigation.ChangeSort("by-file")
                        text " | "
                        textbutton _("natural") action navigation.ChangeSort("natural")
            
            
            add HALF_SPACER
            
            frame style "l_indent":
                hbox:
                    spacing HALF_INDENT
                    text _("Category:")
                    
                    textbutton _("files") action navigation.ChangeKind("file")
                    textbutton _("labels") action navigation.ChangeKind("label")
                    textbutton _("defines") action navigation.ChangeKind("define")
                    textbutton _("transforms") action navigation.ChangeKind("transform")
                    textbutton _("screens") action navigation.ChangeKind("screen")
                    textbutton _("callables") action navigation.ChangeKind("callable")
                    

            add SPACER
            add SEPARATOR

            frame style "l_indent_margin":

                if groups:

                    viewport:
                        mousewheel True
                        scrollbars "vertical"
                        yadjustment navigation.adjustments[persistent.navigation]

                        vbox:
                            style_group "l_navigation"

                            for group_name, group in groups:
                            
                                if group_name is not None:
                                    text group_name
                                    
                                hbox:
                                    box_wrap True
                                    
                                    for name, filename, line in group:
                                        textbutton name action editor.Edit(filename, line)

                                if group_name is not None:
                                    add SPACER

                else:
                    
                    fixed:
                        text _("The list of names is empty."):
                            xalign 0.5
                            yalign 0.5


    textbutton _("Back") action Jump("front_page") style "l_left_button"
    textbutton _("Launch Project") action project.Launch() style "l_right_button"

label navigation:
    
    python in navigation:
        interface.processing(_("Ren'Py is scanning the project..."))
        
        dump_worked = project.current.update_dump()
        
        
label navigation_loop:
    
    python in navigation:
        
        kind = persistent.navigation        

        if kind == "file":
            groups = group_and_sort_files()
        else:
            groups = group_and_sort(kind)
            
        title = KINDS[kind]        
        renpy.call_screen("navigation", title=title, groups=groups)
        

