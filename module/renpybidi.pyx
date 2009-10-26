cdef extern from "fribidi/fribidi.h":
    int FRIBIDI_PAR_LTR
    int FRIBIDI_PAR_WLTR
    int FRIBIDI_PAR_ON
    int FRIBIDI_PAR_WRTL
    int FRIBIDI_PAR_RTL
    
cdef extern object renpybidi_log2vis(object, int *)

LTR = FRIBIDI_PAR_LTR
WLTR = FRIBIDI_PAR_WLTR
ON = FRIBIDI_PAR_ON
WRTL = FRIBIDI_PAR_WRTL
RTL = FRIBIDI_PAR_RTL

def log2vis(s, int direction=FRIBIDI_PAR_ON):
       
    s = s.encode("utf8")
    s = renpybidi_log2vis(s, &direction)
    return s.decode("utf8"), direction

