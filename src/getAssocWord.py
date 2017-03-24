##given a list of words
##take all of the adjectives OR adverbs depending on the given param (adj or adv)
##find the word most similar to all other words
##return it as the summarative word (?)
import nltk

#nltk.download('wordnet')

from nltk.corpus import wordnet


from nltk import pos_tag

def posTagSentences(sentences):
    #returns a list of sentences that are tagged in part of speech
    #take sentences, pos tag them all
    print sentences
    sents = sentences[2]
    tagged_sents = []
    for sent in sents:
        #print sent
        tagged_sents.append(nltk.pos_tag(sent[0]))

    return tagged_sents

def getAllOfType(type, taggedSent):
    #returns a list of all words of a certain type (adjective and adverb will be used)
    #jj = adjective
    #rb = adverb
    alloftype = []
    for sent in taggedSent:
        if type == "adverb":
            print sent
        elif type == "adjective":
            print sent

    return alloftype

def chooseWordOfType(wordsOfType):
    #tags sentences, gets all words of that type and then picks a word of that type that is most summarative of them all
    return wordsOfType[0]

def getAssocWord(sentences, type):

    sentences = posTagSentences(sentences)
    wordsOfType = getAllOfType(type, sentences)
    return chooseWordOfType(wordsOfType)