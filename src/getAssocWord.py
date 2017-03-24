##given a list of words
##take all of the adjectives OR adverbs depending on the given param (adj or adv)
##find the word most similar to all other words
##return it as the summarative word (?)
import nltk
from nltk.corpus import wordnet

import random
from nltk import pos_tag
from nltk import word_tokenize

def posTagSentences(sentences):
    #returns a list of sentences that are tagged in part of speech
    #take sentences, pos tag them all
    print sentences
    sents = sentences[2]
    tagged_sents = []

    for sent in sents:
        #print sent
        #print sent
        #print sent[0]
        tagged_sents.append(nltk.pos_tag(word_tokenize(sent[0])))

    #print "tagged sents: ", tagged_sents
    return tagged_sents

def getAllOfType(type, taggedSent):
    #returns a list of all words of a certain type (adjective and adverb will be used)
    #jj = adjective
    #rb = adverb
    alloftype = []
    for sent in taggedSent:
        for word in sent:
            #print word
            if type == "adverb" and word[1] == "RB":
                alloftype.append(word[0])
            elif type == "adjective" and word[1] == "JJ":
                alloftype.append(word[0])

    return alloftype

def chooseWordOfType(wordsOfType):
    #tags sentences, gets all words of that type and then picks a word of that type that is most summarative of them all
    print wordsOfType

    return wordsOfType[int(random.random()*len(wordsOfType))]

def getAssocWord(sentences, type):

    sentences = posTagSentences(sentences)
    wordsOfType = getAllOfType(type, sentences)
    word = chooseWordOfType(wordsOfType)
    print word
    return word