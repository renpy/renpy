
# http://www.csn.ul.ie/~caolan/publink/winresdump/winresdump/doc/pefile.html
# Contains a reasonable description of the format.

import struct
import sys
import array

# The starting point of the resource segment in the file.
RESOURCE_BASE=0x3400

# The virtual memory location the resource segment is loaded
# to.
RESOURCE_VIRTUAL=0x6000

# Locations in the file where we need to patch in the resource
# segment length.
RESOURCE_LENGTH_PATCHES = [ 0x018c ]

# Locations in the file where we need to patch in the padded
# resource segment length.
RESOURCE_PADDED_PATCHES = [ 0x280 ]

# A location in the file that will be checked to be sure it matches
# RESOURCE_BASE.
CHECK_ADDRESS = 0x284

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
        for i in range(c):
            rv += unichr(self.u16())

        return rv
    
    def seek(self, addr):
        self.addr = addr

    def tostring(self):
        return self.a.tostring()

    def substring(self, start, len):
        return self.a[start:start+len].tostring()
    
    def __init__(self, fn):
        data = open(fn, "rb").read()
        self.a = array.array('B')
        self.a.fromstring(data)

##############################################################################
# These functions parse data out of the file. In these functions, offset is
# relative to the start of the file.

# This parses a data block out of the resources.
def parse_data(offset):
    pe.seek(RESOURCE_BASE + offset)
    data_offset = pe.u32()
    data_len = pe.u32()
    code_page = pe.u32()
    pe.u32()

    l = [ ]

    pe.seek(data_offset + RESOURCE_BASE - RESOURCE_VIRTUAL)
    for i in range(data_len):
        l.append(chr(pe.u8()))

    return (code_page, "".join(l))

# This parses a resource directory.
def parse_directory(offset):

    pe.seek(RESOURCE_BASE + offset)
    char = pe.u32()
    timedate = pe.u32()
    major = pe.u16()
    minor = pe.u16()
    n_named = pe.u16()
    n_id = pe.u16()

    entries = [ ]
    
    for i in range(n_named + n_id):
        entries.append((pe.u32(), pe.u32()))

    rv = { }

    for name, value in entries:

        if name & 0x80000000:
            pe.seek((name & 0x7fffffff) + RESOURCE_BASE)
            name = pe.name()

        if value & 0x80000000:
            value = parse_directory(value & 0x7fffffff)
        else:
            value = parse_data(value)

        rv[name] = value
            
    return rv 


##############################################################################
# This utility function displays the tree of resources that have been loaded.
def show_resources(d, prefix):

    if not isinstance(d, dict):
        print prefix, "Codepage", d[0], "length", len(d[1])
        return
        
    for k in d:
        print prefix, k
        show_resources(d[k], prefix + "  ")

##############################################################################
# These functions repack the resources into a new resource segment. Here,
# the offset is relative to the start of the resource segment.
        
def repack_name(s):
    l = len(s)
    s = s.encode("utf-16le")
    return struct.pack("<H", l) + s + "\0\0"

def repack_tuple(o, offset):
    codepage, data = o
    # print "REPACK OFFSET IS", offset
    return struct.pack("<IIII", offset + 16 + RESOURCE_VIRTUAL, len(data), codepage, 0) + data

def repack_dict(o, offset):
    name_entries = sorted((a, b) for a, b in o.iteritems() if isinstance(a, unicode))
    id_entries = sorted((a, b) for a, b in o.iteritems() if isinstance(a, int))

    rv = struct.pack("<IIHHHH", 0, 0, 4, 0, len(name_entries), len(id_entries))

    offset += len(rv) + (len(name_entries) + len(id_entries)) * 8

    rest = ""
    
    for (name, value) in name_entries + id_entries:
        if isinstance(name, unicode):
            packed = repack_name(name)
            name = 0x80000000 | offset
            offset += len(packed)
            rest += packed

            pad = 8 - (offset % 8)
            offset += pad
            rest += "RENPYVNE"[:pad]
            
        addr = offset
        if isinstance(value, dict):
            addr = addr | 0x80000000
            
        rv += struct.pack("<II", name, addr)

        if isinstance(value, dict):
            packed = repack_dict(value, offset)
        elif isinstance(value, tuple):
            packed = repack_tuple(value, offset)

        offset += len(packed)
        rest += packed

        if offset % 8:        
            pad = 8 - (offset % 8)
            offset += pad
            rest += "RENPYVNE"[:pad]
        
    return rv + rest
        
##############################################################################
# This loads in an icon file, and returns a dictionary that is suitable for
# use in the resources of an exe file.
def load_icon(fn):
    f = BinFile(fn)

    f.seek(0)
    f.u16()
    f.u16()
    count = f.u16()

    rv = { }
    
    for i in range(count):
        width = f.u8()
        height = f.u8()
        colors = f.u8()
        reserved = f.u8()
        planes = f.u16()
        bpp = f.u16()
        size = f.u32()
        offset = f.u32()

        rv[i + 1] = { 0 : (1252, f.substring(offset, size)) }

    return rv


##############################################################################
# This is the main function that should be called externally, that copies over
# the icons.
def change_icons(oldexe, icofn):
    global pe
    pe = BinFile(oldexe)

    # Check that RESOURCE_BASE is still valid.
    pe.seek(CHECK_ADDRESS)
    if pe.u32() != RESOURCE_BASE:
        raise Exception("RESOURCE_BASE is no longer correct. Please check all relocations.")

    resources = parse_directory(0)
    # show_resources(resources, "")
    resources[3] = load_icon(icofn)
    # show_resources(resources, "")
    
    rsrc = repack_dict(resources, 0)
    rsrc_len = len(rsrc)

    if len(rsrc) % 0x1000:
        pad = 0x1000 - (len(rsrc) % 0x1000)
        padding = "RENPYVNE" * (pad / 8 + 1)
        padding = padding[:pad]
        rsrc += padding

    padded_len = len(rsrc)

    for addr in RESOURCE_LENGTH_PATCHES:
        pe.set_u32(addr, rsrc_len)

    for addr in RESOURCE_PADDED_PATCHES:
        pe.set_u32(addr, padded_len)

    return pe.tostring()[:RESOURCE_BASE] + rsrc
    
if __name__ == "__main__":

    f = file(sys.argv[3], "wb")
    f.write(change_icons(sys.argv[1], sys.argv[2]))
    f.close()
    
