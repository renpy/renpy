import sys

from sound import *

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

