init python in navigation:
    import store.interface as interface
    import store.project as project

label navigation:
    
    python in navigation:
        interface.processing(_("Ren'Py is scanning the project..."))
        
        dump_worked = project.current.update_dump()
        
        if not dump_worked:
            interface.info(_("Ren'Py was unable to scan your project.\nScript navigation will be limited."))
        
        interface.info("Made it here.")
