import sys
from cslots import Object, Slot, cobject_size

class C1(Object):
    str1 : Slot[str|None] = Slot(None)
    int1 : Slot[int] = Slot(0)

    def __init__(self, str1=None, int1=1):
        self.str1 = str1
        self.int1 = int1

class C2(C1):
    str2 : Slot[str|None] = Slot(None)
    int2 : Slot[int] = Slot(0)

    def __init__(self, str1=None, int1=0, str2=None, int2=0):
        self.str1 = str1
        self.int1 = int1
        self.str2 = str2
        self.int2 = int2


def test_cslots_object_size():
    assert cobject_size() == 32


def test_slot_count():
    assert C1._cslot_count == 2
    assert C2._cslot_count == 4

def test_slots():

    o = C2()

    assert o.str1 is None
    assert o.int1 == 0
    assert o.str2 is None
    assert o.int2 == 0

    o.str1 = "hello"
    o.int1 = 42
    o.str2 = "world"
    o.int2 = 43

    assert o.str1 == "hello"
    assert o.int1 == 42
    assert o.str2 == "world"
    assert o.int2 == 43

    o.str1 = None
    o.int1 = 0
    o.str2 = None
    o.int2 = 0

    assert o.str1 is None
    assert o.int1 == 0
    assert o.str2 is None
    assert o.int2 == 0


def test_compress():

    o = C2()

    o.str1 = "hello"
    o.int1 = 42
    o.str2 = "world"
    o.int2 = 43

    o._compress()

    assert o.str1 == "hello"
    assert o.int1 == 42
    assert o.str2 == "world"
    assert o.int2 == 43



    o = C2()

    o.str2 = "world"
    o.int2 = 43

    o._compress()

    assert o.str1 is None
    assert o.int1 == 0
    assert o.str2 == "world"
    assert o.int2 == 43



    o = C2()
    o.str1 = "hello"

    o._compress()

    assert o.str1 == "hello"
    assert o.int1 == 0
    assert o.str2 is None
    assert o.int2 == 0
