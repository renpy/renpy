import sys
import pickle

from cslots import Object, Slot, IntegerSlot

class C1(Object):
    str1 : str|None = None
    int1 : int = 0

    def __init__(self, str1=None, int1=1):
        self.str1 = str1
        self.int1 = int1

class C2(C1):
    str2 : str|None = None
    int2 : int = 0

    def __init__(self, str1=None, int1=0, str2=None, int2=0):
        self.str1 = str1
        self.int1 = int1
        self.str2 = str2
        self.int2 = int2


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

    def expect_size(o, values, indexes):
        assert sys.getsizeof(o) == 32 + 8 * values + indexes

    o = C2()

    o.str1 = "hello"
    o.int1 = 42
    o.str2 = "world"
    o.int2 = 43
    expect_size(o, 4, 4)

    o._compress()

    assert o.str1 == "hello"
    assert o.int1 == 42
    assert o.str2 == "world"
    assert o.int2 == 43
    expect_size(o, 4, 4)

    o = C2()

    o.str2 = "world"
    o.int2 = 43

    o._compress()

    assert o.str1 is None
    assert o.int1 == 0
    assert o.str2 == "world"
    assert o.int2 == 43
    expect_size(o, 2, 4)

    o = C2()
    o.str1 = "hello"

    o._compress()

    assert o.str1 == "hello"
    assert o.int1 == 0
    assert o.str2 is None
    assert o.int2 == 0
    expect_size(o, 1, 1)


def test_decompress():

    def expect_size(o, values, indexes):
        assert sys.getsizeof(o) == 32 + 8 * values + indexes

    o = C2()

    o.str1 = "hello"
    o.int1 = 42
    o.str2 = "world"
    o.int2 = 43
    expect_size(o, 4, 4)

    o._compress()
    o._decompress()

    assert o.str1 == "hello"
    assert o.int1 == 42
    assert o.str2 == "world"
    assert o.int2 == 43
    expect_size(o, 4, 4)

    o = C2()

    o.str2 = "world"
    o.int2 = 43

    o._compress()
    o._decompress()

    assert o.str1 is None
    assert o.int1 == 0
    assert o.str2 == "world"
    assert o.int2 == 43
    expect_size(o, 4, 4)

    o = C2()
    o.str1 = "hello"

    o._compress()
    o._decompress()

    assert o.str1 == "hello"
    assert o.int1 == 0
    assert o.str2 is None
    assert o.int2 == 0
    expect_size(o, 4, 4)


def test_kill():

    o = C2()

    o.str1 = "hello"
    o.int1 = 42
    o.str2 = "world"
    o.int2 = 43

    o._kill()

    assert o.str1 is None
    assert o.int1 == 0
    assert o.str2 is None
    assert o.int2 == 0

    o = C2()

    o.str2 = "world"
    o.int2 = 43

    o._compress()
    o._kill()

    assert o.str1 is None
    assert o.int1 == 0
    assert o.str2 is None
    assert o.int2 == 0


def test_pickle():
    o = C2()

    o.str1 = "hello"
    o.int1 = 42
    o.str2 = "world"
    o.int2 = 43

    o = pickle.loads(pickle.dumps(o))

    assert o.str1 == "hello"
    assert o.int1 == 42
    assert o.str2 == "world"
    assert o.int2 == 43

    o = C2()

    o.str2 = "world"
    o.int2 = 43

    o = pickle.loads(pickle.dumps(o))

    assert o.str1 is None
    assert o.int1 == 0
    assert o.str2 == "world"
    assert o.int2 == 43

    o = C2()
    o.str1 = "hello"

    o = pickle.loads(pickle.dumps(o))

    assert o.str1 == "hello"
    assert o.int1 == 0
    assert o.str2 is None
    assert o.int2 == 0



def test_pickle_compressed():
    o = C2()

    o.str1 = "hello"
    o.int1 = 42
    o.str2 = "world"
    o.int2 = 43

    o._compress()

    o = pickle.loads(pickle.dumps(o))

    assert o.str1 == "hello"
    assert o.int1 == 42
    assert o.str2 == "world"
    assert o.int2 == 43

    o = C2()

    o.str2 = "world"
    o.int2 = 43

    o._compress()
    o = pickle.loads(pickle.dumps(o))

    assert o.str1 is None
    assert o.int1 == 0
    assert o.str2 == "world"
    assert o.int2 == 43

    o = C2()
    o.str1 = "hello"

    o._compress()
    o = pickle.loads(pickle.dumps(o))

    assert o.str1 == "hello"
    assert o.int1 == 0
    assert o.str2 is None
    assert o.int2 == 0
