# This contains the default interpolators, getters and setters used by ATL.
# Note that this all goes into the private ATL namespace, not the namespace
# used by everything else.

python early hide:

    # Interpolators.
    
    @atl_interpolator
    def linear(t, a, b):
        return a + t * (b - a)


    # X getters and setters.

    @atl_getter
    def xpos(trans):
        if trans.xpos is not None:
            return trans.xpos
        else:
            return 0
        
    @atl_setter
    def xpos(trans, value):
        trans.xpos = value

    @atl_getter
    def xanchor(trans):
        if trans.xanchor is not None:
            return trans.xanchor
        else:
            return 0
        
    @atl_setter
    def xanchor(trans, value):
        trans.xanchor = value

    @atl_getter
    def xalign(trans):
        if trans.xpos is not None:
            return float(trans.xpos)
        else:
            return 0.0
        
    @atl_setter
    def xalign(trans, value):
        trans.xpos = value
        trans.xanchor = value

    # Y getters and setters.
            
    @atl_getter
    def ypos(trans):
        if trans.ypos is not None:
            return trans.ypos
        else:
            return 0
        
    @atl_setter
    def ypos(trans, value):
        trans.ypos = value
        
    @atl_getter
    def yanchor(trans):
        if trans.yanchor is not None:        
            return trans.yanchor
        else:
            return 0
    
    @atl_setter
    def yanchor(trans, value):
        trans.yanchor = value

    @atl_getter
    def yalign(trans):
        if trans.ypos is not None:
            return float(trans.ypos)
        else:
            return 0.0

    @atl_setter
    def yalign(trans, value):
        trans.ypos = value
        trans.yanchor = value
    
