# # Should we debug the equality operations?
# config.debug_equality = False

class DictEquality(object):
    """
    Declares two objects equal if their types are the same, and
    their internal dictionaries are equal.
    """

    def __eq__(self, o):

        try:
            if self is o:
                return True

            if _type(self) is _type(o):
                return (self.__dict__ == o.__dict__)

            return False

        except:
            # if config.debug_equality:
            #     raise

            return False

    def __ne__(self, o):
        return not (self == o)

class FieldEquality(object):
    """
    Declares two objects equal if their types are the same, and
    the listed fields are equal.
    """

    # The lists of fields to use.
    equality_fields = [ ]
    identity_fields = [ ]

    def __eq__(self, o):

        try:

            if self is o:
                return True

            if _type(self) is not _type(o):
                return False

            for k in self.equality_fields:
                if self.__dict__[k] != o.__dict__[k]:
                    return False

            for k in self.identity_fields:
                if self.__dict__[k] is not o.__dict__[k]:
                    return False

            return True

        except:

            # if config.debug_equality:
            #     raise

            return False

    def __ne__(self, o):
        return not (self == o)
