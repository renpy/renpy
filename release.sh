# This is supposed to be run on Windows! In Cygwin!

if test "x$1" = "x"; then
   echo Need release name.
   exit -1
fi

rm -Rf build dist
cp run_game.py console.py

cmd /c build_exe.bat 

python distribute.py ../$1 demo2
cd ..
zip -9 -r $1.zip $1

