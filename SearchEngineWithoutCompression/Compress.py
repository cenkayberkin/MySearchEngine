"""Author Mehmet Cenk Ayberkin"""
from collections import deque

def toGaps(l):
    z = zip(l[:-1],l[1:])
    m = map(lambda p: int(p[1]) - int(p[0]),z)
    result  = [int(l[0])] + m
    return result

def fromGaps(l):
    res = []
    beginValue = 0
    for i in l:
        beginValue += int(i)
        res.append(beginValue)
    return res
    
def vb_encode_num(num): 
    bytes = deque([])
    while True:
        bytes.appendleft(num % 128)
        if num < 128:
            break
        num = num / 128 
    bytes[len(bytes) - 1] += 128
    return list(bytes)

def vb_encode(arr):
    bytestream = []
    for n in arr:
        ebytes = vb_encode_num(n)
        bytestream.extend(ebytes)
    return bytestream

def vb_decode(bytestream):
    numbers = []
    n = 0
    for i in range(0,len(bytestream)):
        if ord(bytestream[i]) < 128:
            n = 128 * n + ord(bytestream[i])
        else:
            n = 128 * n + (ord(bytestream[i]) - 128)
            numbers.append(n)
            n = 0 
    return numbers

"""
fHandler = open('OutDir/D1','rb')
for i in range(0,200):
    line = fHandler.readline()
    line = line.rstrip('\n')
    li = line.split('|')
    r = vb_decode(li[2])
    finalResult = fromGaps(r)
    print li[0] + "|"+ li[1] + "|" + str(finalResult)
"""

"""
l = [0,1,3,4,5,6,10]

#first gap it then encode it.
def WritePostings(l):
    gapped = toGaps(l)
    a =  vb_encode(gapped)
    encodedString = "".join(map(chr,a)) + "\n"
    fHandler = open('test1','wb')
    fHandler.write("1|5|" + encodedString)
    fHandler.close()

#decoding
def ReadPostings():
    fOpener = open('test1','rb')
    line = fOpener.readline()
    line = line.rstrip('\n')
    li = line.split('|')
    r = vb_decode(li[2])
    finalResult = fromGaps(r)
    for z in finalResult:
        print z

WritePostings(l)
ReadPostings()
    """