numbers = {'0':'zero', '1':'one', '2':'two', '3':'three', '4':'four', '5':'five', '6':'six', '7':'seven', '8':'eight', '9':'nine'}

def genOneLine(textName):
    fHand = open(textName,'r')
    txt = ""
    for line in fHand:
        txt += line.strip()
    fHand.close()
    return txt

def sanitizeDown(text):
    out = ''
    for c in text.lower():
        if c >= 'a' and c <= 'z':
            out += c
        elif c in numbers.keys():
            out += numbers[c]
    return out

f = open("simpText.txt",'w')
f.write(sanitizeDown(genOneLine("encrypted.txt")))
f.close()
print("done")