import cslots

class C1(cslots.Object):
    s1 = cslots.Slot(1)
    s2 = cslots.Slot(2)

    def __init__(self, s1, s2):
        self.s1 = 1
        self.s2 = 2

class C2(C1):

    s3 = cslots.Slot(3)
    s4 = cslots.Slot(4)

    def __init__(self, s1, s2, s3, s4):
        super().__init__(s1, s2)
        self.s3 = s3
        self.s4 = s4



def test_cslots_import():
    assert cslots

def test_cslots_object_size():
    assert cslots.cobject_size() == 32


def test_slot_count():
    assert C1._cslot_count == 2
    assert C2._cslot_count == 4


def test_slots():

    class C1(cslots.Object):
        s1 = cslots.Slot(1)
        s2 = cslots.Slot(2)

    i1 = C1()

    assert i1.s1 == 1

    i1.s1 = 2
    assert i1.s1 == 2

    i1.s1 = 1
    assert i1.s1 == 1

    assert i1.s2 == 2

    i1.s2 = 3
    assert i1.s2 == 3

    i1.s2 = 2
    assert i1.s2 == 2
