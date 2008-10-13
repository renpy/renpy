#!/bin/sh

rm -Rf spline_editor/*~
rm -Rf spline_editor/game/*~
rm -Rf spline_editor/game/*.rpyc
rm -Rf spline_editor/game/*.rpyb
rm -Rf spline_editor/game/saves

rm spline_editor.zip
zip -9r spline_editor.zip spline_editor -x \*.svn\* 



