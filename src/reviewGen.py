from chaineyReview import *


def generateReview(filmtitle):
    content = determineContent(filmtitle)
    structuredContent = structureDocument(content)
    aggregatedDoc = aggregateDocument(structuredContent)
    aggDocWLex = lexicalChoice(aggregatedDoc)
    docWReferringExp = generateReferringExpression(aggDocWLex)
    return realiseDocument(docWReferringExp)

def determineContent(filmtitle):
    plotsummary, sentencesAboutCast, sentencesAboutCrew, sentencesAboutDirector, meta, genre, reception = getContent(filmTitle)
    content = []
    #content will be a series of opinions and statements relating to actors, directors, the film in general, a plot synopsis, the genre of the movie,
    ## and other things to flesh out the review in order to make it more like a review text than a list of sentiment tagged points

    #
    #one such content could be
    #subject verb adjective
    #


    return content

def structureDocument(content):
    #this method takes the content and decides where to make statements about what, semi-stochastically

    #because the structure of a movie review is sort of generated along with the content this section wil

    structure = []
    return structure

def aggregateDocument(document):
    #this method looks for pieces of content which can be concatenated into a single sentrence
    return document

def lexicalChoice(document):
    #chooses words related to sentiment and other vocabulary to make the text sound more original
    return document

def generateReferringExpression(document):
    #also known as anaphora
    #this is sort of cyclic - needs to have content determination and lexical choice

    #inserts referring expressions regarding the document
    return document

def realiseDocument(document):
    #converst structured document into text (hopefully this is mostly verbatim)
    return text
