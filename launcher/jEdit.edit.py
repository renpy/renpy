import os
import renpy
import subprocess

class Editor(renpy.editor.Editor):

    def begin(self, new_window=False, **kwargs):
        
        args = [ ]
        
        mydir = os.path.dirname(__file__)
        jar = os.path.join(mydir, "../jedit/jedit.jar")
        
        # My Java does not like having non-ASCII characters in jar paths. 
        # Using relpath won't guarantee those characters won't exist - but it 
        # makes them less likely in common use cases.
        jar = os.path.relpath(jar)

        if renpy.windows:
            args = [ "javaw.exe", "-jar", jar ]
        else:
            args = [ "java", "-jar", jar ]
        
        if new_window:
            args.append("-newplainview")
        else:
            args.append("-reuseview")
    
        self.arguments = args
    
    def open(self, filename, line=None, **kwargs):
        filename = renpy.exports.fsencode(filename)
        self.arguments.append(filename)
        
        if line is not None:
            self.arguments.append("+line:{0}".format(line))

    def end(self, **kwargs):
        print self.arguments
        subprocess.Popen(self.arguments)
        
