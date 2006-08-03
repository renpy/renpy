import sys

from sound import *

try:
    import nativemidi
    sys.modules['nativemidi'] = sys.modules['pysdlsound.nativemidi']
except:
    pass

try:
    import winmixer
    sys.modules['winmixer'] = sys.modules['pysdlsound.winmixer']
except:
    pass

try:
    import linmixer
    sys.modules['linmixer'] = sys.modules['pysdlsound.linmixer']
except:
    pass

