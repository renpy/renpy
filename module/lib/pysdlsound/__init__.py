import sys

from sound import *

try:
    import winmixer #@UnresolvedImport
    sys.modules['winmixer'] = sys.modules['pysdlsound.winmixer']
except:
    pass

try:
    import linmixer #@UnresolvedImport
    sys.modules['linmixer'] = sys.modules['pysdlsound.linmixer']
except:
    pass

