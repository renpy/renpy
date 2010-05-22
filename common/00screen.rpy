# Screen system support.

init python:

    class SetField(Action):
        def __init__(self, obj, var, value):
            self.object = obj
            self.var = var
            self.value = value
        
        def __call__(self):
            setattr(self.object, self.var, self.value)
            renpy.restart_interaction()

        def get_selected(self):
            return getattr(self.object, self.var) == self.value
        
