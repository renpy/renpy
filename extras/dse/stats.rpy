init -100:
    python:

        # This class encapsulates a statistic in DSE. Instances of
        # this class have two properties, .value and .maxvalue. The
        # .value property is clamped to ensure that it is always in
        # the range 0 - .maxvalue, inclusive.
        #
        # 
        class Stat(object):
            
            #name: string intended to describe the stat in game (e.g. "Intelligence")
            #startvalue: value the stat starts out with
            #maxvalue: highest value this stat can reach
            def __init__(self, name, startvalue, maxvalue):
                
                self.name=name
                self.__value=startvalue
                self.__maxvalue=maxvalue

            def __int__(self):
                return self.__value
            
            def __str__(self):
                return str(self.__value)
            
            #sets value and ensures it is within boundaries
            #0-maxvalue, inclusive.
            def set(self, new_value):
                self.__value = new_value
                self.__value = min(self.__value, self.__maxvalue)
                self.__value = max(self.__value, 0)
                
            #sets maxvalue and ensures value is within the new boundaries
            def set_max(self, new_value):
                self.__maxvalue = new_value
                self.set(self.__value)

            # Set up properties so the user can directly access value
            # and maxvalue, and set or set_max is called when they are
            # updated.

            value = property(fget = lambda self : self.__value,
                             fset = set)

            maxvalue = property(fget = lambda self : self.__maxvalue,
                                fset = set_max)
            
            #allow comparisons to integer
            def __cmp__(self, other):
                #correctly raises exception if we try to compare to anything not castable to integer
                cmp_to = int(other)
                return cmp(self.__value, cmp_to)

            # Renders this Stat into the stats window.
            def render(self):
                ui.hbox()
                ui.text(self.name, minwidth=150)
                ui.bar(600, 20, self.__maxvalue, self.__value, ypos=0.5, yanchor='center')
                ui.close()

label stats_show:

    python hide:

        # This is the window that the stats are kept in, if any.
        ui.window(xpos=0,
                  ypos=0,
                  xanchor='left',
                  yanchor='top',
                  xfill=True,
                  yminimum=0)

        ui.vbox()

        ui.text('Statistics')
        ui.null(height=10)

        for i in shown_stats:
            i.render()
            
        ui.close()

    return
