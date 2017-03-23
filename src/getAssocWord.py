##given a list of words
##take all of the adjectives OR adverbs depending on the given param (adj or adv)
##find the word most similar to all other words
##return it as the summarative word (?)
import nltk

#nltk.download('wordnet')

from nltk.corpus import wordnet

dog = wordnet.synset('dog')
cat = wordnet.synset('cat')



print wordnet.synsets('dog')

def posTagSentences(sentences):
    #returns a list of sentences that are tagged in part of speech

def getAllOfType(type, taggedSent):
    #returns a list of all words of a certain type (adjective and adverb will be used)

def chooseWordOfType(type, sentences):
    #tags sentences, gets all words of that type and then picks a word of that type that is most summarative of them all
