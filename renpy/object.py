class Object(object):
    """
    Our own base class. Contains methods to simplify serialization.
    """

    nosave = [ ]

    def __getstate__(self):
        rv = vars(self).copy()

        for f in self.nosave:
            if rv.has_key(f):
                del rv[f]

        return rv


    def after_setstate(self):
        """
        Called after a deserialization has occured.
        """

        return


    def __setstate__(self, new_dict):
        self.__dict__ = new_dict
        self.after_setstate()
