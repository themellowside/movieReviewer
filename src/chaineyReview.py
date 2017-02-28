import random
import nltk
from rope.base.pyobjectsdef import _AssignVisitor

import util_funcs

from nltk import word_tokenize
from nltk import tokenize
from nltk.sentiment import SentimentIntensityAnalyzer

from lib.RAKE import rake
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


def templateReview(movieName):

    f = open('input.txt', 'r')
    #f = open('/Users/tom/Documents/CSY3/FYP/movieReviewer/src/input.txt', 'r')

    str = f.read()
    str = util_funcs.stripNonAscii(str)

    meta, genre = getMovieMeta(movieName.replace(" ", "+"))

    cast = meta.get("cast")
    crew = meta.get("crew")


    sentences = tokenize.sent_tokenize(str)

    review = ""
    #create a list of names from cast and crew with their role / job
    #look for name of role, job or the name of the person (or one of their names) in each sentence
    #

    sentencesAboutPeople = []
    sid = SentimentIntensityAnalyzer()
    reception = sid.polarity_scores(str)

    sentencesAboutCast=[]
    sentencesAboutCrew=[]
    sentencesAboutDirector = []
    for sentence in sentences:
        #check if sentence contains a name of a member of cast or crew
        #if it does add it to a list of phrases discussing cast or crew members
        sent = sid.polarity_scores(sentence)
        for person in cast:
            name = person.get('name')
            role = person.get('character')
            if name in sentence or role in sentence:
                #print sentence, name, role
                for row in sentencesAboutCast:
                    if row[0] == name and row[1] == role:
                        row[2].append([sentence,sent])
                        break
                sentencesAboutCast.append([name, role, [[sentence, sent]]])

        for person in crew:
            name = person.get('name')
            job = person.get('job')
            if job == 'Director':
                if len(sentencesAboutDirector) == 0:
                    sentencesAboutDirector =[name, job, [[sentence, sent]]]
                    break
                else:
                    sentencesAboutDirector[2].append([sentence, sent])
                    break

            elif name in sentence or job in sentence:
                #print sentence, name, job
                for row in sentencesAboutCrew:
                    if row[0] == name and row[1] == job:
                        row[2].append([sentence,sent])
                        break
                sentencesAboutCrew.append([name, job, [[sentence, sent]]])
    introTemplates = loadTemplates('C:\Users\Thomas\PycharmProjects\movieReviewer\src\introtemplates.txt')
    #introTemplates = loadTemplates('/Users/tom/Documents/CSY3/FYP/movieReviewer/src/introtemplates.txt')

    outroTemplates = loadTemplates('C:\Users\Thomas\PycharmProjects\movieReviewer\src\outrotemplates.txt')
    #outroTemplates = loadTemplates('/Users/tom/Documents/CSY3/FYP/movieReviewer/src/outrotemplates.txt')

    sentenceTemplates = loadTemplates('C:\Users\Thomas\PycharmProjects\movieReviewer\src\simpletemplates.txt')
    #sentenceTemplates = loadTemplates('/Users/tom/Documents/CSY3/FYP/movieReviewer/src/simpletemplates.txt')

    intro = introTemplates[int(random.random()*len(introTemplates))]
    outro = outroTemplates[int(random.random()*len(outroTemplates))]

    bodylen = int(random.random() * len(sentenceTemplates)-2) +2

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

    review += generateSentence(intro, sentencesAboutDirector, sentencesAboutCast, sentencesAboutCrew, movieName, genre, reception) + " "
    for sentence in body:
        #print sentence
        review += generateSentence(sentence, sentencesAboutDirector, sentencesAboutCast, sentencesAboutCrew, movieName, genre, reception) + " "
    review += generateSentence(outro, sentencesAboutDirector, sentencesAboutCast, sentencesAboutCrew, movieName, genre, reception)
    print review

def loadTemplates(filepath):
    ##loads templates from txt file
    templateFile = file(filepath, mode='r')
    templateList = templateFile.read().splitlines()
    return templateList

def getMovieMeta(movieName):
    import httplib
    import json
    import ast
    conn = httplib.HTTPSConnection("api.themoviedb.org")

    payload = "{}"

    conn.request("GET", "/3/search/movie?api_key=16e6e2321c81b245dbae3e28e24f6b7e&query="+movieName, payload)
    res = conn.getresponse()
    searchData = res.read()
    searchData = json.loads(searchData)
    #print searchData
    movieId = str(searchData.get('results')[0].get('id'))
    #print str(searchData.get('results')[0])
    genreIDs = str(searchData.get('results')[0].get('genre_ids'))
    #print "Movie ID: ", movieId
    #find first instance of id in the text and return it as it is the movie title \"id\"

    conn.request("GET", "/3/movie/"+ movieId + "/credits?api_key=16e6e2321c81b245dbae3e28e24f6b7e", payload)
    res = conn.getresponse()
    castData = res.read()

    castData = json.loads(castData)
    conn.request("GET", "/3/genre/movie/list?api_key=16e6e2321c81b245dbae3e28e24f6b7e", payload)
    res = conn.getresponse()
    genreData = res.read()
    genreData = json.loads(genreData)

    genreList = genreData.get('genres')
    genreString = ""
    genreIDs = ast.literal_eval(genreIDs)
    for genreItem in genreList:

        if genreItem.get('id') == genreIDs[0]:
            genreString = genreItem.get('name')

    #print castData
    #print genreData.get('genres')[0].get('name')
    #print genreString
    return castData, genreString

def generateSentence(sentence, directorSent, castSent, crewSent, moviename, genre, sentiment):

    #completes the template sentence passed into the function
    #print sentiment
    if '[director]' in sentence:
        director = directorSent[0]
        sentence = sentence.replace('[director]', director)
        if '[directoradverb]' in sentence:
            sentence = sentence.replace('[directoradverb]',selectWord(directorSent, 'adverb'))
        if '[directoradjective]' in sentence:
            sentence = sentence.replace('[directoradjective]',selectWord(directorSent, 'adjective'))
        if '[directornot]' in sentence:
            if(getSentRating(directorSent) == 'pos'):
                sentence = sentence.replace('[directornot]', '')
            else:
                sentence = sentence.replace('[directornot]', 'not')

    if '[actor]' in sentence:
        #pick an actor from the ones talked about and use sentiment (For now) to describe performance
        #print castSent
        #for now we also chose the actor randomly but can replace this with the most frequently mentioned ones in the future

        chosenIdx = int(len(castSent) * random.random())
        chosen = castSent[chosenIdx]
        actor = chosen[0]
        role = chosen[1]
        casent = chosen[2]
        #print castSent
        #print "casent:", casent
        sentence = sentence.replace('[actor]', actor)
        sentence = sentence.replace('[role]', role)
        if '[actoradverb]' in sentence:
            #print "casent:", casent[0]
            #print "directorSent:", directorSent[0]
            sentence = sentence.replace('[actoradverb]', selectWord(casent, 'adverb'))

        if '[actoradjective]' in sentence:
            #print "casent:", casent[0]
            #print "directorSent:", directorSent[0]
            sentence = sentence.replace('[actoradjective]',selectWord(casent, 'adjective'))

        if '[actornot]' in sentence:
            if(getSentRating(sentiment) == 'pos'):
                sentence = sentence.replace('[actornot]', '')
            else:
                sentence = sentence.replace('[actornot]', 'not')

        if '[actor2]' in sentence:
            if len(castSent) ==1:
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
        crsent = chosen[2]
        sentence = sentence.replace('[job]', role)
        sentence = sentence.replace('[crew]', crew)
        #print crewSent
        if '[crewadverb]' in sentence:
            sentence = sentence.replace('[crewadverb]',selectWord(crsent, 'adverb'))
        if '[crewadjective]' in sentence:
            sentence = sentence.replace('[crewadjective]',selectWord(crsent, 'adjective'))



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

    #

def getSentRating(sent):
    #works out whether or not there is an overall positive or negative sentiment across all sentences in the list passed
    #returns either pos or negative
    print sent
    polarityCount = 0
    for sentence in sent:
        #print "sentence:", sentence
        if sentence[1].get('pos') > sentence[1].get('neg'):
            polarityCount += 1
    if polarityCount > len(sent):
        return 'pos'
    else:
        return 'neg'


def selectWord(sent, type):
    #selects an adjective or adverb that describes the given sentences
    #print "select word sent: ",sent
    #print "running select word sent on: ", sent[0]
    pol = getSentRating(sent)


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



def tagString(str):

    tokens = word_tokenize(str)
    #print tokens
    return nltk.pos_tag(tokens)

#templateReview()
templateReview("Bridge Of Spies")
#chaineyReview()