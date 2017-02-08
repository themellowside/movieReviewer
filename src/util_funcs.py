#collection of functions i might need to call a lot somewhere

def stripNonAscii(str):
    newStr = ""
    for c in str:
        if(ord(c) < 128):
            newStr = newStr + c

    return newStr

def getSentencesIncluding (sentences):
    #splits a long string of sentences into sentences
    import ntlk.data

    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')