init python in navigation:
    import store.interface as interface
    import store.project as project
    from store import persistent

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
        "label" : _("Navigate Labels"),
    }
     
    for i in KINDS:
        persistent.navigation_sort.setdefault(i, "by-file")

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
            
            g = groups.get(group, None)
            if g is None:
                groups[group] = g = [ ]
                
            g.append((name, filename, line))
            
        for g in groups.values():
            if sort == "natural":
                g.sort(key=lambda a : a[2].lower())
            else:
                g.sort(key=lambda a : a[0].lower())
                
        rv = list(groups.items())
        rv.sort()

        return rv

screen navigation:
    
    frame:
        style_group "l"
        style "l_root"
        
        window:
    
            has vbox
    
            frame style "l_label":
                has hbox xfill True
                text "[title]" style "l_label_text"
                frame:
                    style "l_alternate"
                    style_group "l_small"
                    
                    has hbox
                    
                    text _("Order: ")
                    textbutton _("alphabetical")
                    text " | "
                    textbutton _("by-file")
                    text " | "
                    textbutton _("natural")
        
            
            add HALF_SPACER
            text "Blah Blah Blah."

            add SPACER
            add SEPARATOR

            frame style "l_indent":

                viewport:
                    mousewheel True
                    scrollbars "vertical"
                    
                    vbox:
                        style_group "l_navigation"

                        for group_name, group in groups:
                        
                            if group_name is not None:
                                add HALF_SPACER
                                text group_name bold True
                                
                            hbox:
                                box_wrap True
                                
                                for name, filename, lin in group:
                                    textbutton name
                                
                        

    
                



label navigation:
    
    python in navigation:
        interface.processing(_("Ren'Py is scanning the project..."))
        
        dump_worked = project.current.update_dump()
        
        
label navigation_loop:
    
    python in navigation:
        
        kind = persistent.navigation        

        groups = group_and_sort(kind)
        title = KINDS[kind]
        
        renpy.call_screen("navigation", title=title, groups=groups)
        

