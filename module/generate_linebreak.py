# encoding: utf-8

# Based on: http://www.unicode.org/Public/UNIDATA/LineBreak.txt
# Based on: http://unicode.org/reports/tr14/#PairBasedImplementation

import re

breaking = """OP    CL    CP    QU    GL    NS    EX    SY    IS    PR    PO    NU    AL    ID    IN    HY    BA    BB    B2    ZW    CM    WJ    H2    H3    JL    JV    JT 
OP    ^    ^    ^    ^    ^    ^    ^    ^    ^    ^    ^    ^    ^    ^    ^    ^    ^    ^    ^    ^    @    ^    ^    ^    ^    ^    ^
CL    _    ^    ^    %    %    ^    ^    ^    ^    %    %    _    _    _    _    %    %    _    _    ^    #    ^    _    _    _    _    _
CP    _    ^    ^    %    %    ^    ^    ^    ^    %    %    %    %    _    _    %    %    _    _    ^    #    ^    _    _    _    _    _
QU    ^    ^    ^    %    %    %    ^    ^    ^    %    %    %    %    %    %    %    %    %    %    ^    #    ^    %    %    %    %    %
GL    %    ^    ^    %    %    %    ^    ^    ^    %    %    %    %    %    %    %    %    %    %    ^    #    ^    %    %    %    %    %
NS    _    ^    ^    %    %    %    ^    ^    ^    _    _    _    _    _    _    %    %    _    _    ^    #    ^    _    _    _    _    _
EX    _    ^    ^    %    %    %    ^    ^    ^    _    _    _    _    _    _    %    %    _    _    ^    #    ^    _    _    _    _    _
SY    _    ^    ^    %    %    %    ^    ^    ^    _    _    %    _    _    _    %    %    _    _    ^    #    ^    _    _    _    _    _
IS    _    ^    ^    %    %    %    ^    ^    ^    _    _    %    %    _    _    %    %    _    _    ^    #    ^    _    _    _    _    _
PR    %    ^    ^    %    %    %    ^    ^    ^    _    _    %    %    %    _    %    %    _    _    ^    #    ^    %    %    %    %    %
PO    %    ^    ^    %    %    %    ^    ^    ^    _    _    %    %    _    _    %    %    _    _    ^    #    ^    _    _    _    _    _
NU    %    ^    ^    %    %    %    ^    ^    ^    %    %    %    %    _    %    %    %    _    _    ^    #    ^    _    _    _    _    _
AL    %    ^    ^    %    %    %    ^    ^    ^    _    _    %    %    _    %    %    %    _    _    ^    #    ^    _    _    _    _    _
ID    _    ^    ^    %    %    %    ^    ^    ^    _    %    _    _    _    %    %    %    _    _    ^    #    ^    _    _    _    _    _
IN    _    ^    ^    %    %    %    ^    ^    ^    _    _    _    _    _    %    %    %    _    _    ^    #    ^    _    _    _    _    _
HY    _    ^    ^    %    _    %    ^    ^    ^    _    _    %    _    _    _    %    %    _    _    ^    #    ^    _    _    _    _    _
BA    _    ^    ^    %    _    %    ^    ^    ^    _    _    _    _    _    _    %    %    _    _    ^    #    ^    _    _    _    _    _
BB    %    ^    ^    %    %    %    ^    ^    ^    %    %    %    %    %    %    %    %    %    %    ^    #    ^    %    %    %    %    %
B2    _    ^    ^    %    %    %    ^    ^    ^    _    _    _    _    _    _    %    %    _    ^    ^    #    ^    _    _    _    _    _
ZW    _    _    _    _    _    _    _    _    _    _    _    _    _    _    _    _    _    _    _    ^    _    _    _    _    _    _    _
CM    %    ^    ^    %    %    %    ^    ^    ^    _    _    %    %    _    %    %    %    _    _    ^    #    ^    _    _    _    _    _
WJ    %    ^    ^    %    %    %    ^    ^    ^    %    %    %    %    %    %    %    %    %    %    ^    #    ^    %    %    %    %    %
H2    _    ^    ^    %    %    %    ^    ^    ^    _    %    _    _    _    %    %    %    _    _    ^    #    ^    _    _    _    %    %
H3    _    ^    ^    %    %    %    ^    ^    ^    _    %    _    _    _    %    %    %    _    _    ^    #    ^    _    _    _    _    %
JL    _    ^    ^    %    %    %    ^    ^    ^    _    %    _    _    _    %    %    %    _    _    ^    #    ^    %    %    %    %    _
JV    _    ^    ^    %    %    %    ^    ^    ^    _    %    _    _    _    %    %    %    _    _    ^    #    ^    _    _    _    %    %
JT    _    ^    ^    %    %    %    ^    ^    ^    _    %    _    _    _    %    %    %    _    _    ^    #    ^    _    _    _    _    %
"""

other_classes = " PITCH AI BK CB CR LF NL SA SG SP XX"

lines = breaking.split("\n")

print "# This is generated code. Do not edit."
print

# A map from character class to the number that represents it.
cl = { }

for i, j in enumerate((lines[0] + other_classes).split()):
    print "cdef char BC_{} = {}".format(j, i)
    cl[j] = i
    
rules = [ ]

for l in lines[1:]:
    for c in l.split()[1:]:        
        rules.append(c)

print
print "cdef char *break_rules = \"" + "".join(rules) + "\""

cc = [ 'XX' ] * 65536

for l in file("LineBreak.txt"):
    m = re.match("(\w+)\.\.(\w+);(\w\w)", l)
    if m:
        start = int(m.group(1), 16)
        end = int(m.group(2), 16)
        
        if start > 65535:
            continue 
        
        if end > 65535:
            end = 65535
        
        for i in range(start, end + 1):
            cc[i] = m.group(3)
            
        continue
    
    m = re.match("(\w+);(\w\w)", l)
    if m:
        start = int(m.group(1), 16)        

        if start > 65535:
            continue
        
        cc[start] = m.group(2)            
        continue
    
print "cdef char *break_classes = \"" + "".join("\\x%02x" % cl[i] for i in cc) + "\""
            
            