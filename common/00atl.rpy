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
        return trans.xpos

    @atl_setter
    def xpos(trans, value):
        trans.xpos = value

    @atl_getter
    def xanchor(trans):
        return trans.xanchor

    @atl_setter
    def xanchor(trans, value):
        trans.xanchor = value

    @atl_getter
    def xalign(trans):
        return float(trans.xpos)

    @atl_setter
    def xalign(trans, value):
        trans.xpos = value
        trans.xanchor = value

    # Y getters and setters.
            
    @atl_getter
    def ypos(trans):
        return trans.ypos

    @atl_setter
    def ypos(trans, value):
        trans.ypos = value

    @atl_getter
    def yanchor(trans):
        return trans.yanchor

    @atl_setter
    def yanchor(trans, value):
        trans.yanchor = value

    @atl_getter
    def yalign(trans):
        return float(trans.ypos)

    @atl_setter
    def yalign(trans, value):
        trans.ypos = value
        trans.yanchor = value
        
        
    

    
