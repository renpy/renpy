# This is supposed to be run on Windows! In Cygwin!

if test "x$1" = "x"; then
   echo Need release name.
   exit -1
fi

rm -Rf build dist "/tmp/$1.zip"
cp run_game.py console.py

cmd /c build_exe.bat 

# strip dist/*.dll dist/lib/*.pyd dist/lib/*.dll dist/lib/*.exe

python distribute.py "../$1" demo2

export CYGWIN=smbntsec
cd ..

chmod +x "$1/run_game.py"
chmod +x "$1/tools/add_from"
chmod +x "$1/tools/archiver"
chmod +x "$1/tools/dump_text"
chmod +x "$1/tools/run_dse"

zip -X9 -r "/tmp/$1.zip" "$1"

unset CYGWIN

cp "/tmp/$1.zip" "$1.zip"