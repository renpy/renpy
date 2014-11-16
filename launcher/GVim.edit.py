#coding=utf-8
'''
GVim Support for Ren'Py Launcher



Copyright (c) 2014 Civa Lin 林雪凡 <larinawf@gmail.com>
(blog: http://blog.civa.me)

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

import renpy
import os
import sys
import subprocess

def which(program):
    '''Test Program exist or not. If exist, return program absolute path.

        usage:
            >>> which('hg')

        program - Both "absolute path" (/usr/bin/xxx) & "only filename" (xxx)
                  are work.

        return ==> None if not exist, else return the program's absolute path.
        '''
    def is_exe(filename):
        return os.path.isfile(filename) and os.access(filename, os.X_OK)
    dirname = os.path.dirname(program)
    if dirname:
        if is_exe(program):
            return program
    else:
        for path in os.environ['PATH'].split(os.pathsep):
            exe_filename = os.path.join(path, program)
            if is_exe(exe_filename):
                return exe_filename
            elif sys.platform.startswith('win'): # windows
                if is_exe(exe_filename + '.exe'):
                    return exe_filename + '.exe'
    return None # test failed


class Editor(renpy.editor.Editor):
    '''Gedit Editor'''

    def begin(self, new_window = False, **kwargs):
        '''Collect variable'''
        self.var = {'new_window': new_window}
        self.exe = which('gvim')
        self.env = dict(os.environ)

    def end(self, **kwargs):
        '''Recycle Data'''
        pass

    def open(self, filename, line = None, **kwargs):
        '''Open'''
        # cmd init
        if self.var['new_window']: # New Window
            cmd = [self.exe,]
            self.var['new_window'] = False # open new window at first time
            if line:
                cmd.append('+{}'.format(line))
        else:
            cmd = [self.exe, '--remote-tab-silent']
            if line:
                cmd.append('+{}'.format(line))
        # loadfile
        cmd.append(filename)
        subprocess.Popen(cmd, env = self.env).wait()
