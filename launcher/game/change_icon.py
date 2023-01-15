# Copyright 2004-2023 Tom Rothamel <pytom@bishoujo.us>
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
from renpy.compat import bchr, chr, str, PY2

import struct
import sys
import array
import pefile


# This class performs various operations on memory-loaded binary files,
# including modifications.

class BinFile(object):

    def set_u32(self, addr, value):
        self.a[addr + 0] = (value >> 0) & 0xff
        self.a[addr + 1] = (value >> 8) & 0xff
        self.a[addr + 2] = (value >> 16) & 0xff
        self.a[addr + 3] = (value >> 24) & 0xff

    def u32(self):
        addr = self.addr
        rv = self.a[addr]
        rv |= self.a[addr + 1] << 8
        rv |= self.a[addr + 2] << 16
        rv |= self.a[addr + 3] << 24
        self.addr += 4
        return rv

    def u16(self):
        addr = self.addr
        rv = self.a[addr]
        rv |= self.a[addr + 1] << 8
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
            rv += chr(self.u16())

        return rv

    def seek(self, addr):
        self.addr = addr

    def tostring(self):
        if PY2:
            return self.a.tostring() # type: ignore
        else:
            return self.a.tobytes()

    def substring(self, start, len): # @ReservedAssignment
        if PY2:
            return self.a[start:start + len].tostring() # type: ignore
        else:
            return self.a[start:start + len].tobytes()

    def __init__(self, data):
        self.a = array.array('B')

        if PY2:
            self.a.fromstring(data) # type: ignore
        else:
            self.a.frombytes(data)

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
        l.append(bchr(bf.u8()))

    return (code_page, b"".join(l))

# This parses a resource directory.


def parse_directory(bf, offset):

    bf.seek(offset)
    char = bf.u32() # @UnusedVariable
    timedate = bf.u32() # @UnusedVariable
    major = bf.u16() # @UnusedVariable
    minor = bf.u16() # @UnusedVariable
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
        name_entries = sorted((a, b) for a, b in d.items() if isinstance(a, str))
        id_entries = sorted((a, b) for a, b in d.items() if isinstance(a, int))

        rv = struct.pack("<IIHHHH", 0, 0, 4, 0, len(name_entries), len(id_entries))

        offset += len(rv) + (len(name_entries) + len(id_entries)) * 8

        rest = b""

        for (name, value) in name_entries + id_entries:
            if isinstance(name, str):
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
    f = BinFile(open(fn, "rb").read())

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

        #rv[3][i + 1] = { 0 : (1252, f.substring(offset, size)) }
        #I do not have justification for the 0x0409 entry ID, other than copying what other files do. Same for codepage of 0
        rv[3][i + 1] = { 1033 : (0, f.substring(offset, size)) }

        group += struct.pack("BBBBHHIH", width, height, colors, reserved,
                             planes, bpp, size, i + 1)

        f.seek(addr)

    #rv[14] = { 1 : { 0 : (1252, group) } }
    rv[14] = { 1 : { 1033 : (0, group) } }

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

    f = open(oldexe, "rb")
    basedata = f.read(base)
    data = f.read(physize)

    #Symbol table, I could not understand so well
    #  Some analysis and the little I could find on how the symbol tables were layed out show that the PE table is in two sections. One is
    # a list of NumberOfSymbols*(18 bytes) symbol entries, followed immediately by a string table who's length is specified in the 4 bytes following the symbol structure list
    #Again, the information *seems* to indicate that this will always follow the entire block of all sections (so be at the end of the file)


    ######
    # As a related note, apparently this flag has been deprecated, but appears to be set (I think ..) in the renpy.exe that is used to build from..
    # no idea of a consequence, just an observation
    # https://docs.microsoft.com/en-us/windows/win32/debug/pe-format#characteristics , see "IMAGE_FILE_LINE_NUMS_STRIPPED" :
    #	COFF line numbers have been removed. This flag is deprecated and should be zero.
    # In renpy.exe, this 2-byte  flag is @ 0x096 and 0x097  in little-endian
    ######

    f.close()

    bf = BinFile(data)

    resources = parse_directory(bf, 0)
    # show_resources(resources, "")
    resources.update(load_icon(icofn))
    # show_resources(resources, "")

    rsrc = Packer().pack(resources)

    newExactSize = len(rsrc)

    #From note about flags above regarding image flags. These two should be 0
    pe.FILE_HEADER.Characteristics = pe.FILE_HEADER.Characteristics & (~pefile.IMAGE_CHARACTERISTICS["IMAGE_FILE_LINE_NUMS_STRIPPED"])
    pe.FILE_HEADER.Characteristics = pe.FILE_HEADER.Characteristics & (~pefile.IMAGE_CHARACTERISTICS["IMAGE_FILE_LOCAL_SYMS_STRIPPED"])

    #Per docs, symbol table can just be removed
    #https://docs.microsoft.com/en-us/windows/win32/debug/pe-format#coff-file-header-object-and-image  see "PointerToSymbolTable"  and  "NumberOfSymbols "

    pe.FILE_HEADER.PointerToSymbolTable = 0
    pe.FILE_HEADER.NumberOfSymbols = 0

    #####
    # Alignment requirements as I understand them
    #
    # SectionAlignment (misnomer.. 'memory' alignment) = 4096
    # FileAlignment = 512
    #
    #  Section, SizeOfRawData = multiple of FileAlignment   (On Disk size)
    #  Scetion, VirtualSize   is  NOT aligned to any specific number, and rwdata may be > than this due to its alignment requirement  (In memory size)
    #
    #  the resource section should be padded out to meet the alignment requirement of  SizeOfRawData = multiple of FileAlignment  (So, in the file, since on disk)
    #
    #####
    #  RVA table virt address and size = that in the section header
    #
    #####
    # SizeOfImage  must be aligned to SectionAlignment  (memory alignment)
    #   There is NO padding needed, the image size number simply needs to be aligned to >= the

    memoryalignment = pe.OPTIONAL_HEADER.SectionAlignment
    filealignment = pe.OPTIONAL_HEADER.FileAlignment

    rsrc_section.Misc_VirtualSize = newExactSize
    rsrc_section.Misc_PhysicalAddress = newExactSize
    rsrc_section.Misc = newExactSize

    #Size of resource section (and pointer, but we're not changing anything 'above' resource) is the same as virtual address in the section table
    # https://docs.microsoft.com/en-us/windows/win32/debug/pe-format#optional-header-data-directories-image-only
    pe.OPTIONAL_HEADER.DATA_DIRECTORY[2].Size = rsrc_section.Misc_VirtualSize


    #Alignment for raw data
    if len(rsrc) % filealignment:
        pad = filealignment - (len(rsrc) % filealignment)
        padding = b"\0" * (pad)
        padding = padding[:pad]
        rsrc += padding
    rsrc_section.SizeOfRawData = len(rsrc)


    #Image size is the memory size of all sections + all headers, padded to memory alignment.
    #There's alread a header size, and this isn't changing headers, so just add.
    #imageSize = pe.OPTIONAL_HEADER.ImageBase + pe.OPTIONAL_HEADER.SizeOfHeaders
    imageSize = pe.OPTIONAL_HEADER.SizeOfHeaders
    for s in pe.sections:
        sectionSize = s.Misc_VirtualSize
        #Align every section, so add padding to size
        pad = 0
        if sectionSize % memoryalignment:
            pad = memoryalignment - (sectionSize % memoryalignment)
        imageSize += (sectionSize + pad)
    pad = 0
    if imageSize % memoryalignment:
        pad = memoryalignment - (imageSize % memoryalignment)
    pe.OPTIONAL_HEADER.SizeOfImage = imageSize + pad


    #The symbol table is simply left off. Its size DOES factor into ImageSize, but we didn't calculate it above, so fine
    #Correctly checksum the file. The entire file is involved in the calculation, so a new PE object must be generated for the calculation to work against
    newFile = pe.write()[:base] + rsrc
    newpe = pefile.PE(data=bytes(newFile))
    newpe.OPTIONAL_HEADER.CheckSum = newpe.generate_checksum()

    return bytes(newpe.write())


if __name__ == "__main__":

    f = open(sys.argv[3], "wb")
    f.write(change_icons(sys.argv[1], sys.argv[2]))
    f.close()
