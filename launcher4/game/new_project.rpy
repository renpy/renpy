label new_project:
    
    python hide:
        
        project_name = ""
        
        while True:
        
            project_name = interface.input(
                _("PROJECT NAME"), 
                _("Please enter the name of your project:"),
                filename=True,
                cancel=Jump("front_page"),
                default=project_name)
            
            break
            
    jump front_page
    
    