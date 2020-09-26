1. Download mingw-get-inst from http://www.mingw.org/wiki/Getting_Started
   . Install C, C++, MSYS, and the developer environment.

2. To ensure compatibility with Python 2.7, the compiler specs need to
   be changed to use msvcr90, and to include a manifest file that causes
   the right version of the library to be used.

   A sample file for GCC 4.7.0 is included in the windows
   directory of the renpy-deps distribution. Otherwise, you have to use
   ``gcc -dumpspecs`` to get a specs file, and then edit it.

   If you want to make the changes yourself (say, because you need to
   use a future GCC), the important changes are to the following
   sections:

   libgcc
      change -lmoldname to -lmoldname90, change -lmsvcrt to -lmsvcr90

   endfile
      add crt_resource.o%s just before crtend.o%s.

   cc1plus
      add -D__MSVCRT_VERSION__=0x0900 -D_USE_32BIT_TIME_T

   cpp
     add -D__MSVCRT_VERSION__=0x0900 -D_USE_32BIT_TIME_T

3. Copy the specs file and crt_resource.o to the directory with
   crtbegin.o in it. (For example, C:\MinGW\lib\gcc\mingw32\4.7.0\)

3. Edit C:\MinGW\include\_mingw.h, and add the line::

     #undef __STRICT_ANSI___

   at the start. The msvcr90 headers do not seem to work when
   ``STRICT_ANSI`` is defined. Cancelling it seems to be the fix.

4. Untar directx-devel.tar.gz over in C:\MinGW.

5. Install Python 2.7.

6. Download distribute_setup.py, and run it to install distribute.

7. Run easy_install-script.py (in the Python scripts directory) to
   install rsa.

8. Download and install py2exe.

9. Edit /Python27/Lib/cygwinccompiler.py to remove all of the uses
   of "-mno-cygwin". This option is no longer supported by MinGW,
   and causes a failure.


When these steps are done, put /python27 and /mingw/bin in your PATH,
and run build.sh from renpy-deps. Then run setup.py in the modules
directory of Ren'Py to build the ren'py modules.
