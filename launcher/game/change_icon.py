# Copyright 2004-2019 Tom Rothamel <pytom@bishoujo.us>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


# http://www.csn.ul.ie/~caolan/publink/winresdump/winresdump/doc/pefile.html
# Contains a reasonable description of the format.

from __future__ import print_function

import struct
import sys
import array
import pefile  # @UnresolvedImport

# This class performs various operations on memory-loaded binary files,
# including modifications.


class BinFile(object):

    def set_u32(self, addr, value):
        self.a[addr+0] = (value >> 0) & 0xff
        self.a[addr+1] = (value >> 8) & 0xff
        self.a[addr+2] = (value >> 16) & 0xff
        self.a[addr+3] = (value >> 24) & 0xff

    def u32(self):
        addr = self.addr
        rv = self.a[addr]
        rv |= self.a[addr+1] << 8
        rv |= self.a[addr+2] << 16
        rv |= self.a[addr+3] << 24
        self.addr += 4
        return rv

    def u16(self):
        addr = self.addr
        rv = self.a[addr]
        rv |= self.a[addr+1] << 8
        self.addr += 2
        return rv

    def u8(self):
        rv = self.a[self.addr]
        self.addr += 1
        return rv

    def name(self):
        c = self.u16()

        rv = u""
        for _i in range(c):
            rv += unichr(self.u16())

        return rv

    def seek(self, addr):
        self.addr = addr

    def tostring(self):
        return self.a.tostring()

    def substring(self, start, len):  # @ReservedAssignment
        return self.a[start:start+len].tostring()

    def __init__(self, data):
        self.a = array.array(b'B')
        self.a.fromstring(data)

##############################################################################
# These functions parse data out of the file. In these functions, offset is
# relative to the start of the file.

# The virtual address of the resource segment.
resource_virtual = 0

# This parses a data block out of the resources.


def parse_data(bf, offset):
    bf.seek(offset)
    data_offset = bf.u32()
    data_len = bf.u32()
    code_page = bf.u32()
    bf.u32()

    l = [ ]

    bf.seek(data_offset - resource_virtual)
    for _i in range(data_len):
        l.append(chr(bf.u8()))

    return (code_page, b"".join(l))

# This parses a resource directory.


def parse_directory(bf, offset):

    bf.seek(offset)
    char = bf.u32()  # @UnusedVariable
    timedate = bf.u32()  # @UnusedVariable
    major = bf.u16()  # @UnusedVariable
    minor = bf.u16()  # @UnusedVariable
    n_named = bf.u16()
    n_id = bf.u16()

    entries = [ ]

    for _i in range(n_named + n_id):
        entries.append((bf.u32(), bf.u32()))

    rv = { }

    for name, value in entries:

        if name & 0x80000000:
            bf.seek((name & 0x7fffffff))
            name = bf.name()

        if value & 0x80000000:
            value = parse_directory(bf, value & 0x7fffffff)
        else:
            value = parse_data(bf, value)

        rv[name] = value

    return rv


##############################################################################
# This utility function displays the tree of resources that have been loaded.
def show_resources(d, prefix):

    if not isinstance(d, dict):
        print(prefix, "Codepage", d[0], "length", len(d[1]))
        return

    for k in d:
        print(prefix, k)
        show_resources(d[k], prefix + "  ")

##############################################################################
# These functions repack the resources into a new resource segment. Here,
# the offset is relative to the start of the resource segment.


class Packer(object):

    def pack(self, d):
        self.data = b""
        self.data_offset = 0

        self.entries = b""
        self.entries_offset = 0

        head = self.pack_dict(d, 0)

        self.data = b""
        self.data_offset = len(head) + len(self.entries)

        self.entries = b""
        self.entries_offset = len(head)

        return self.pack_dict(d, 0) + self.entries + self.data

    def pack_name(self, s):
        rv = self.data_offset + len(self.data)

        l = len(s)
        s = s.encode("utf-16le")
        self.data += struct.pack("<H", l) + s + b"\0\0"

        return rv

    def pack_tuple(self, t):
        codepage, data = t

        rv = len(self.entries) + self.entries_offset

        if len(self.data) % 2:
            self.data += b"P"

        daddr = len(self.data) + self.data_offset

        self.entries += struct.pack("<IIII", daddr + resource_virtual, len(data), codepage, 0)
        self.data += data

        # if len(self.data) % 1 == 1:
        #    self.data += 'P'

        return rv

    def pack_dict(self, d, offset):
        name_entries = sorted((a, b) for a, b in d.iteritems() if isinstance(a, unicode))
        id_entries = sorted((a, b) for a, b in d.iteritems() if isinstance(a, int))

        rv = struct.pack("<IIHHHH", 0, 0, 4, 0, len(name_entries), len(id_entries))

        offset += len(rv) + (len(name_entries) + len(id_entries)) * 8

        rest = b""

        for (name, value) in name_entries + id_entries:
            if isinstance(name, unicode):
                name = 0x80000000 | self.pack_name(name)

            if isinstance(value, dict):
                addr = offset | 0x80000000
                packed = self.pack_dict(value, offset)
                offset += len(packed)
                rest += packed
            else:
                addr = self.pack_tuple(value)

            rv += struct.pack("<II", name, addr)

        return rv + rest

##############################################################################
# This loads in an icon file, and returns a dictionary that is suitable for
# use in the resources of an exe file.


def load_icon(fn):
    f = BinFile(file(fn, "rb").read())

    f.seek(0)
    f.u16()
    f.u16()
    count = f.u16()

    rv = { }
    rv[3] = { }

    group = struct.pack("HHH", 0, 1, count)

    for i in range(count):
        width = f.u8()
        height = f.u8()
        colors = f.u8()
        reserved = f.u8()
        planes = f.u16()
        bpp = f.u16()
        size = f.u32()
        offset = f.u32()

        addr = f.addr
        f.seek(offset + 16)
        if not f.u32():
            f.set_u32(offset + 20, 0)

        rv[3][i + 1] = { 0 : (1252, f.substring(offset, size)) }

        group += struct.pack("BBBBHHIH", width, height, colors, reserved,
                             planes, bpp, size, i + 1)

        f.seek(addr)

    rv[14] = { 1 : { 0 : (1252, group) } }

    return rv


##############################################################################
# This is the main function that should be called externally, that copies over
# the icons.
def change_icons(oldexe, icofn):
    global resource_virtual

    pe = pefile.PE(oldexe)

    for s in pe.sections:
        if s.Name == b".rsrc\0\0\0":
            rsrc_section = s
            break
    else:
        raise Exception("Couldn't find resource section.")

    base = rsrc_section.PointerToRawData
    resource_virtual = rsrc_section.VirtualAddress

    physize = rsrc_section.SizeOfRawData
    virsize = rsrc_section.Misc_VirtualSize

    f = file(oldexe, "rb")
    f.seek(base)
    data = f.read(physize)
    f.close()

    bf = BinFile(data)

    resources = parse_directory(bf, 0)
    # show_resources(resources, "")
    resources.update(load_icon(icofn))
    # show_resources(resources, "")

    rsrc = Packer().pack(resources)

    alignment = pe.OPTIONAL_HEADER.SectionAlignment

    # print("Alignment is", alignment)

    if len(rsrc) % alignment:
        pad = alignment - (len(rsrc) % alignment)
        padding = b"RENPYVNE" * (pad / 8 + 1)
        padding = padding[:pad]
        rsrc += padding

    newsize = len(rsrc)

    rsrc_section.Misc_VirtualSize += newsize - virsize
    rsrc_section.Misc_PhysicalAddress += newsize - virsize
    rsrc_section.Misc += newsize - virsize
    rsrc_section.SizeOfRawData += newsize - physize

    pe.OPTIONAL_HEADER.SizeOfInitializedData += newsize - physize

    # Resource size.
    pe.OPTIONAL_HEADER.DATA_DIRECTORY[2].Size += newsize - virsize

    # Compute the total size of the image.
    total_size = 0

    for i in pe.sections:

        sec_size = i.Misc_VirtualSize
        sec_size = sec_size - (sec_size % alignment) + alignment

        total_size += sec_size

    pe.OPTIONAL_HEADER.SizeOfImage = total_size

    return pe.write()[:base] + rsrc

if __name__ == "__main__":

    f = file(sys.argv[3], "wb")
    f.write(change_icons(sys.argv[1], sys.argv[2]))
    f.close()
