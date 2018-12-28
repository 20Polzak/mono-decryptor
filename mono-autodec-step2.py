# Monodecryptor from likely dictionary
from string import ascii_lowercase as alpha
from cryptotools import sanitize
from operator import itemgetter

def mono_autodec(msg, bigDict):
    '''monodecrypt(msg, bigDict) -> str
    Returns the autodecrypted version of a monoalphabetic substitution cipher
    bigDict[ciphertextletter] = list((plaintextCandidate1, confidenceLvl1), ...)'''

    msg = sanitize(msg)

    listTuples = [(key, bigDict[key][0][0], bigDict[key][0][1]) for key in alpha]

    singDict = {}


    # Get the best values
    bestValues = {key: bigDict[key].pop(0) for key in alpha}

    # Correct if duplicates are found
    bestValues2 = {}
    for i in bestValues:
        currentBest = bestValues.pop(i)
        while currentBest[0] in [v[0] for v in bestValues.values()]:
            
