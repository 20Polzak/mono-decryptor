from operator import itemgetter
from graphs import di_Freq, tri_Freq
alpha = "abcdefghijklmnopqrstuvwxyz"
eng_Freq = {"a": 8.167, "b": 1.492, "c": 2.782, "d": 4.253, "e": 12.702, "f": 2.228, "g": 2.015, "h": 6.094, "i": 6.966, "j": 0.153, "k": 0.772, "l": 4.025,
    "m": 2.406, "n": 6.749, "o": 7.507, "p": 1.929, "q": 0.095, "r": 5.987, "s": 6.327, "t": 9.056, "u": 2.758, "v": 0.978, "w": 2.360, "x": 0.150, "y": 1.974, "z": 0.074}
text = open("simpText.txt",'r').read()

def findGraphs(phr, gap): # note: returns raw count
    '''findGraphs(str, gap) -> dict
    gap = n-graph letter count
    returns raw count of graph frequencies'''
    sortedGraphs = {}
    for k in range(len(phr)- gap + 1):
        currGraph = phr[k:k+gap]
        if not currGraph in sortedGraphs.keys():
            sortedGraphs[currGraph] = phr.count(currGraph)
    tupleGraphs = sorted(sortedGraphs.items(), key=itemgetter(1))
    tupleGraphs.reverse()
    return tupleGraphs

def mapGraphs(subGraphs, engGraphs):
    '''mapGraphs(subGraphs, engGraphs) -> list(tuple(encrypted letter, plaintext candidate))
    Returns the possible letter combos based on n-gram frequency'''
    engGraphs = sorted(engGraphs.items(), key=itemgetter(1))
    engGraphs.reverse()
    print(len(engGraphs))
    graphPairs = [ (subGraphs[x][0].lower(), engGraphs[x][0].lower()) for x in range(min(len(engGraphs), len(subGraphs)))]
    indivSubs = []
    print(graphPairs[:500])
    for pair in graphPairs:
        for charPos in range(len(pair[0])):
            charCombo = (pair[0][charPos], pair[1][charPos])
            if charCombo not in indivSubs:
                indivSubs.append(charCombo)
    return indivSubs # [(encrypted letter, plaintext candidate)]

def genFinalDict(encryptedText):
    '''genFinalDict(encryptedText) -> dict(chr:[(chr, int), ...],...)
    Generates a final dictionary compiling the invididual letter frequencies with
    the n-gram frequencies'''
    encryptedFrequencies = findGraphs(encryptedText,1)
    editableDict = {tupleGraph[0]: {x: 0 for x in alpha} for tupleGraph in encryptedFrequencies}
    bigDict = {tupleGraph[0]: [] for tupleGraph in encryptedFrequencies}
    allMaps = mapGraphs(encryptedFrequencies, eng_Freq)
    encryptedFrequencies = findGraphs(encryptedText,2) # Digraph frequencies
    allMaps.extend(mapGraphs(encryptedFrequencies, di_Freq))
    # encryptedFrequencies = findGraphs(encryptedText,3) # Trigraphs
    # allMaps += mapGraphs(encryptedFrequencies, tri_Freq)
    for mapPair in allMaps:
        editableDict[mapPair[0]][mapPair[1]] += 1
    for encryptedLetterDict in editableDict.keys():
        for plainCandidate in editableDict[encryptedLetterDict].keys():
            if editableDict[encryptedLetterDict][plainCandidate] > 1:
                bigDict[encryptedLetterDict] += [(plainCandidate, editableDict[encryptedLetterDict][plainCandidate])]
        bigDict[encryptedLetterDict].sort(key=itemgetter(1))
        bigDict[encryptedLetterDict].reverse()
    for encryptedLetter in bigDict.keys():
        print(encryptedLetter)
        print(bigDict[encryptedLetter])

if __name__ == '__main__':
    genFinalDict(text)
