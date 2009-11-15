cdef extern from "fribidi/fribidi.h":
    int FRIBIDI_TYPE_LTR
    int FRIBIDI_TYPE_ON
    int FRIBIDI_TYPE_RTL
    int FRIBIDI_TYPE_WR
    int FRIBIDI_TYPE_WL
    
cdef extern object renpybidi_log2vis(object, int *)

WLTR = FRIBIDI_TYPE_WL
LTR = FRIBIDI_TYPE_LTR
ON = FRIBIDI_TYPE_ON
RTL = FRIBIDI_TYPE_RTL
WRTL = FRIBIDI_TYPE_WR

def log2vis(s, int direction=FRIBIDI_TYPE_ON):
       
    s = s.encode("utf8")
    s = renpybidi_log2vis(s, &direction)
    return s.decode("utf8"), direction

