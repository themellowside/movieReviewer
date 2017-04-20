import math
import random

# markov chain text generator

# first: take a parameter n (number of prefixes to a suffix)
#
# second: generate a table of all prefix suffix combinations


# third: chose words based on random rolls for that matrix


# -> [
#    [prefix, [suffix, count], [suffix2, count2], [suffix3, count3]]
#    [prefix2, [suffix, count], [suffix2, count2], [suffix3, count3]]
#    ]



def newText(lim, n, table, twitter):


    # for now just choose the first prefix without empty values
    ##
    twitter = True
    if twitter:
        idx0 = int (random.random() * len(table)+n)
    else:
        idx0 = n

    output = [] + table[idx0][0] ##PRETTY SURE THIS IS PASSING BY REFERENCE ONLY AND I DON'T KNOW WHY
    chainCount = 0
    hasSuffix = True
    executing = True
    while hasSuffix and len(" ".join(output)) < lim and executing: # while we haven't exceeded the limit or have a suffix to continue with
        suffixCount = len(table[idx0][1:]) # number of suffixes is every item in the table at idx0 past the first one
        if suffixCount == 1: # if we have one suffix there's only one potential word to continue the chain with
            output.append(table[idx0][1][0])
        else: # if we have more than one suffix we have to use weighted randomness to decide the next item in the chain
            totalSuffixes = 0
            for i in range(1, len(table[idx0])): # for each suffix, calculate the total weighting
                totalSuffixes += table[idx0][i][1]
            weight = random.random() * totalSuffixes # weight is number of suffixes (including duplicates) * rand 0, 1
            count = 0
            for i in range(1, len(table[idx0])): # now we count up including the weighting
                count += table[idx0][i][1]
                if weight < count: # if weight < count we've got a hit, and we choose this output
                    if(len(" ".join(output)) + len(table[idx0][i][0] + 1) < lim ):
                        output.append(table[idx0][i][0])
                    else:
                        executing = False
                    break

        newSuffix = output[len(output)-n:len(output)] # the new suffix
        #print "new suffix: ", newSuffix

        chainCount += 1
        # find the index of the latest prefix
        hasSuffix = False
        #print "checking for suffix"
        for i in range(0, len(table)):
            #print table[i][0], newSuffix
            if table[i][0] == newSuffix:
                idx0 = i
                hasSuffix = True
                #print "suffix found"
                break
    print
    print chainCount
    print output
    return " ".join(output)


def generateTable(text, n):
    chain = []
    textArray = text.split()
    #
    for i in range(0, len(textArray)):
        suffix = textArray[i]

        if i - n >= 0:
            prefix = textArray[i - n:i]

        else:
            prefix = []
            for j in range(n, 0, -1):
                if i - j < 0:
                    prefix.append([])
                else:
                    prefix.append(textArray[i - j])

        # if prefix already exists, add a suffix to it (unless the suffix already exists in which case increment its count by 1)


        prefixExists = False
        suffixExists = False
        for k in range(0, len(chain)):

            if chain[k][0] == prefix:
                prefixExists = True

                for m in range(1, len(chain[k])):
                    if (chain[k][m][0] == suffix):
                        #for list in chain:
                        #    print list
                        #print suffix, chain[k][m][0]

                        #print k,m
                        #print chain[k]
                        #print chain[k][m]
                        #print chain[k][m][1]
                        chain[k][m][1] += 1
                        suffixExists = True
                if not suffixExists:
                    chain[k].append([suffix, 1])

        if not prefixExists:
            chain.append([prefix, [suffix, 1]])

    return chain


def generateMultidocTable(docs, n):
    chain = []
    for doc in docs:

        if '@' not in doc:
            textArray = doc.split()
            #
            #
            for i in range(0, len(textArray)):
                suffix = textArray[i]

                if i - n >= 0:
                    prefix = textArray[i - n:i]

                else:
                    prefix = []
                    for j in range(n, 0, -1):
                        if i - j < 0:
                            prefix.append("")
                        else:
                            prefix.append(textArray[i - j])

                # if prefix already exists, add a suffix to it (unless the suffix already exists in which case increment its count by 1)


                prefixExists = False
                suffixExists = False
                for k in range(0, len(chain)):

                    if chain[k][0] == prefix:
                        prefixExists = True

                        for m in range(1, len(chain[k])):
                            if (chain[k][m][0] == suffix):
                                # for list in chain:
                                #    print list
                                # print suffix, chain[k][m][0]

                                # print k,m
                                # print chain[k]
                                # print chain[k][m]
                                # print chain[k][m][1]
                                chain[k][m][1] += 1
                                suffixExists = True
                        if not suffixExists:
                            chain[k].append([suffix, 1])

                if not prefixExists:
                    chain.append([prefix, [suffix, 1]])

    return chain


#text = "I am not a number, I am a man, I am a real man, and I am number one"

#n = 2

#chain = generateTable(text, n)

#for i in range(0, len(chain)):
#    print chain[i]

#print newText(1000, 2, chain)

