from lib.RAKE import rake
from obtainContent import *
from getAssocWord import *


#http://www.nltk.org/book/ch06.html#ref-document-classify-extractor

#sentences = rake.split_sentences(open('/Users/tom/Documents/CSY3/FYP/movieReviewer/src/res/movie_reviews/neg/cv000_29416.txt', 'r').read())

#for i in range(0, len(sentences)):
#    print sentences[i], sid.polarity_scores(sentences[i])
#This product uses the TMDb API but is not endorsed or certified by TMDb.
#Any use of the TMDb logo in your application shall be less prominent than the logo or mark that primarily describes the application and your use of the TMDb logo shall not imply any endorsement by TMDb.


def chaineyReview():
    #nltk.download('vader_lexicon')

    #f = open('input.txt', 'r')
    f = open('/Users/tom/Documents/CSY3/FYP/movieReviewer/src/input.txt', 'r')

    str = f.read()
    print "Suggested keyphrases:"
    #r = rake.Rake("lib/RAKE/SmartStoplist.txt")
    r = rake.Rake("/Users/tom/Documents/CSY3/FYP/movieReviewer/src/lib/RAKE/SmartStoplist.txt")

    keywords = r.run(str)
    print keywords
    print "Reception of the film:"

    sid = SentimentIntensityAnalyzer()
    reception = sid.polarity_scores(str)
    print "Pos:", reception.get('pos'), "Neg:", reception.get('neg')

    import markov

    print markov.newText(300, 2, markov.generateTable(str, 2), False)
    if reception.get('pos') > reception.get('neg'):
        print "Definitely one worth watching."
    else:
        print "It's not worth seeing this film."




def templateReview(movieName, withWordnet):

    plotsummary, sentencesAboutCast, sentencesAboutCrew, sentencesAboutDirector, meta, genre, reception = getContent(movieName)

    review = ""



    introTemplates = loadTemplates('C:\Users\Thomas\Documents\CSY3\FYP\\reviewer\movieReviewer\src\introtemplates.txt')
    #introTemplates = loadTemplates('/Users/tom/Documents/CSY3/FYP/movieReviewer/src/introtemplates.txt')

    outroTemplates = loadTemplates('C:\Users\Thomas\Documents\CSY3\FYP\\reviewer\movieReviewer\src\outrotemplates.txt')
    #outroTemplates = loadTemplates('/Users/tom/Documents/CSY3/FYP/movieReviewer/src/outrotemplates.txt')

    sentenceTemplates = loadTemplates('C:\Users\Thomas\Documents\CSY3\FYP\\reviewer\movieReviewer\src\simpletemplates.txt')
    #sentenceTemplates = loadTemplates('/Users/tom/Documents/CSY3/FYP/movieReviewer/src/simpletemplates.txt')

    intro = introTemplates[int(random.random()*len(introTemplates))]
    outro = outroTemplates[int(random.random()*len(outroTemplates))]

    bodylen = int(random.random() * len(sentenceTemplates)-4) +4

    body = []

    for i in range(bodylen, 0, -1):
        pos = int(i * random.random())
        #print pos, len(sentenceTemplates)

        body.append(sentenceTemplates[pos])
        del sentenceTemplates[pos]
    #now we have a list of sentences that talk about someone, and are tagged with their sentiment polarity
    #we can use these to construct basic sentences that talk about the person's performance in the job (they did well, poorly, capably)
    #


    #http://www.nltk.org/howto/chunk.html
    #
    print intro
    review += generateSentence(intro, sentencesAboutDirector, sentencesAboutCast, sentencesAboutCrew, movieName, genre, reception, withWordnet) + " "

    print review
    review += plotsummary + " "
    for sentence in body:
        #print sentence
        review += generateSentence(sentence, sentencesAboutDirector, sentencesAboutCast, sentencesAboutCrew, movieName, genre, reception, withWordnet) + " "
    review += generateSentence(outro, sentencesAboutDirector, sentencesAboutCast, sentencesAboutCrew, movieName, genre, reception, withWordnet)
    print review

    #print "Sentences about director:", sentencesAboutDirector
    #print "Sentences about cast:", sentencesAboutCast
    #print getAssociatedWords(["Tom Hanks", "Woody (voice)"])
    #print "Sentences about crew:", sentencesAboutCrew

def loadTemplates(filepath):
    ##loads templates from txt file
    templateFile = file(filepath, mode='r')
    templateList = templateFile.read().splitlines()
    return templateList



def generateSentence(sentence, directorSent, castSent, crewSent, moviename, genre, sentiment, withWordNet):

    #completes the template sentence passed into the function
    #print sentiment
    if '[director]' in sentence:
        director = directorSent[0]
        sentence = sentence.replace('[director]', director)
        if '[directoradverb]' in sentence:
            sentence = sentence.replace('[directoradverb]',selectWord(directorSent, 'adverb', withWordNet))
        if '[directoradjective]' in sentence:
            sentence = sentence.replace('[directoradjective]',selectWord(directorSent, 'adjective', withWordNet))
        if '[directornot]' in sentence:
            #print "sentiment", sentiment
            #print "directorSent", directorSent
            if(getSentRating(directorSent) == 'pos'):
                sentence = sentence.replace('[directornot]', '')
            else:
                sentence = sentence.replace('[directornot]', 'not')

    if '[actor]' in sentence:
        #pick an actor from the ones talked about and use sentiment (For now) to describe performance
        #print castSent
        #for now we also chose the actor randomly but can replace this with the most frequently mentioned ones in the future
        #print "cast sent : " , castSent
        chosenIdx = int(len(castSent) * random.random())
        chosen = castSent[chosenIdx]
        actor = chosen[0]
        role = chosen[1]
        #print castSent
        #print "casent:", casent
        sentence = sentence.replace('[actor]', actor)
        sentence = sentence.replace('[role]', role)
        print castSent
        if '[actoradverb]' in sentence:
            #print "casent:", casent[0]
            #print "directorSent:", directorSent[0]
            sentence = sentence.replace('[actoradverb]', selectWord(chosen, 'adverb', withWordNet))

        if '[actoradjective]' in sentence:
            #print "casent:", casent[0]
            #print "directorSent:", directorSent[0]
            sentence = sentence.replace('[actoradjective]', selectWord(chosen, 'adjective', withWordNet))

        if '[actornot]' in sentence:

            if sentiment.get('pos') > sentiment.get('neg'): #check directorSent vs sentiment for formatting issues
                sentence = sentence.replace('[actornot]', '')
            else:
                sentence = sentence.replace('[actornot]', 'not')

        if '[actor2]' in sentence:
            if len(castSent) == 1:
                return "" #no second actor
            chosenIdx2 = int(len(castSent) * random.random())
            while(chosenIdx == chosenIdx2):
                chosenIdx2 = int(len(castSent) * random.random())

            secondChosen = castSent[chosenIdx2]
            secondActor = secondChosen[0]
            secondRole = secondChosen[1]
            secondsent = secondChosen[2]
            sentence = sentence.replace('[actor2]', secondActor)
            sentence = sentence.replace('[role2]', secondRole)

    if '[crew]' in sentence:
        chosen = crewSent[int(len(crewSent) * random.random())]
        crew = chosen[0]
        role = chosen[1]

        sentence = sentence.replace('[job]', role)
        sentence = sentence.replace('[crew]', crew)
        #print crewSent
        if '[crewadverb]' in sentence:
            sentence = sentence.replace('[crewadverb]',selectWord(chosen, 'adverb', withWordNet))
        if '[crewadjective]' in sentence:
            sentence = sentence.replace('[crewadjective]',selectWord(chosen, 'adjective', withWordNet))



    if '[moviename]' in sentence:
        sentence = sentence.replace('[moviename]', moviename)
        if '[movieadjective]' in sentence:
            if sentiment.get('pos') > sentiment.get('neg'):
                sentence = sentence.replace('[movieadjective]', 'excellent')
            else:
                sentence = sentence.replace('[movieadjective]', 'un-enjoyable')

        if '[movieadverb]' in sentence:
            if sentiment.get('pos') > sentiment.get('neg'):
                sentence = sentence.replace('[movieadverb]', 'excellently')
            else:
                sentence = sentence.replace('[movieadverb]', 'un-enjoyably')


    if '[genre]' in sentence:
        sentence = sentence.replace('[genre]', genre)

    if '[moviesee]' in sentence:
        if sentiment.get('pos') > sentiment.get('neg'):
            sentence = sentence.replace('[moviesee]', 'watch')
        else:
            sentence = sentence.replace('[moviesee]', 'avoid')

    return sentence

def getSentRating(sent):
    #works out whether or not there is an overall positive or negative sentiment across all sentences in the list passed
    #returns either pos or negative
    #print "printing sent:", sent


    polarityCount = 0
    for sentence in sent[2]:
        #print "sentence:", sentence

        if sentence[1].get('pos') > sentence[1].get('neg'):
            polarityCount += 1
    if polarityCount > int(len(sent)/2):
        return 'pos'
    else:
        return 'neg'

def selectWord(sent, type, withWordNet):
    #selects an adjective or adverb that describes the given sentences
    #print "select word sent: ",sent
    #print "running select word sent on: ", sent[0]
    pol = getSentRating(sent)
    #print sent
    if withWordNet:

        return getAssocWord(sent, type)

    else:
        if type == 'adjective':
            if pol == 'pos':
                return 'good'
            else:
                return 'poor'

        elif type == 'adverb':
            if pol == 'pos':
                return 'well'
            else:
                return 'poorly'



#templateReview()
#templateReview("Sing", withWordnet=True)
#chaineyReview()

