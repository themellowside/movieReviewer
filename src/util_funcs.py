#collection of functions i might need to call a lot somewhere

def stripNonAscii(str):
    newStr = ""
    for c in str:
        if(ord(c) < 128):
            newStr = newStr + c

    return newStr