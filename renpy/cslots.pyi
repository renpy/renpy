
class Object:

    _cslot_count: int
    "The number of slots in this class and all of its parents."

    def _compress(self) -> None:
        """
        Compresses the slots of this object.
        """

    def _decompress(self) -> None:
        """
        Decompresses the slots of this object.
        """

    def _kill(self) -> None:
        """
        This 'kills' the object, by removing all references from it to other objects,
        and setting all slots to the default, breaking reference cycles.
        """


class Slot[T]:

    number: int
    "A number assigned to this slot."

    default_value: T
    "The default value of this slot."

    intern: bool
    "If true, the value of this slot should be interned."

    def __init__(self, default_value: T, intern: bool=False) -> None:
        """
        A slot that stores a value in a CObject.

        `default_value`
            The default value of this slot.

        `intern`
            If true, this slot is a string that should be interned before being assigned
            to the cslot.
        """

    def __get__(self, instance : Object, owner: type) -> T:
        """
        Gets the value of a slot.
        """

    def __set__(self, instance : Object, value: T) -> None:
        """
        Sets the value of a slot.
        """


class IntegerSlot:

    number: int
    "A number assigned to this slot."

    default_value: int
    "The default value of this slot."

    def __init__(self, default_value: int,) -> None:
        """
        A slot that stores a value in a CObject.

        `default_value`
            The default value of this slot.

        """

    def __get__(self, instance : Object, owner: type) -> int:
        """
        Gets the value of a slot.
        """

    def __set__(self, instance : Object, value: int) -> None:
        """
        Sets the value of a slot.
        """


def cobject_size() -> int:
    """
    Returns the size of a CObject.
    """
