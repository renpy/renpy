try () { "$@" || exit 1; }

try python setup.py clean --all
try python setup.py install_lib -d $PYTHONPATH
