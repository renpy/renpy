class Curry(object):
    """
    Stores a callable and some arguments. When called, calls the
    callable with the stored arguments and the additional arguments
    supplied to the call.
    """

    __doc__ = property(fget=lambda self : self.callable.__doc__)

    def __init__(self, callable, *args, **kwargs):
        self.callable = callable
        self.args = args
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        return self.callable(*(self.args + args),
                             **dict(self.kwargs.items() + kwargs.items()))

    def __repr__(self):
        return "<curry " + repr(vars(self)) + ">"

def curry(fn):
    """
    Takes a callable, and returns something that, when called, returns
    something that when called again, calls the function. So
    basically, the thing returned from here when called twice does the
    same thing as the function called once.
    """
    
    return Curry(Curry, fn)
