import random
import nltk

import util_funcs

from nltk import word_tokenize
from nltk import tokenize
from nltk.sentiment import SentimentIntensityAnalyzer

from lib.RAKE import rake

import httplib
import json

import requests
from bs4 import BeautifulSoup

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

    
    synopsis, reviews = scrapeIMDB(movieName.replace(" ", "+"))
    from summa import summarizer
    plotsummary = summarizer.summarize(synopsis)
    reviewCorpora = ""
    for review in reviews:
        reviewCorpora += review
    
    meta, genre = getMovieMeta(movieName.replace(" ", "+"))

    cast = meta.get("cast")
    crew = meta.get("crew")


    sentences = tokenize.sent_tokenize(reviewCorpora)
    
    review = ""
    #create a list of names from cast and crew with their role / job
    #look for name of role, job or the name of the person (or one of their names) in each sentence
    #

    sentencesAboutPeople = []
    sid = SentimentIntensityAnalyzer()
    reception = sid.polarity_scores(reviewCorpora)

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
            assocnames = []
            assocnames.append(name)
            assocnames.append(role)
            assocnames = getAssociatedWords(assocnames)

            castappended = False
            castExists = False
            for assocname in assocnames:
                if assocname in sentence:
                    #print sentence, name, role

                    for row in sentencesAboutCast:
                        if row[0] == name and row[1] == role:
                            row[2].append([sentence,sent])
                            castExists = True
                            break
                    if not castExists:
                        sentencesAboutCast.append([name, role, [[sentence, sent]]])

                    castappended = True

                if castappended:
                    break


        for person in crew:
            name = person.get('name')
            job = person.get('job')
            assocnames = []
            assocnames.append(name)
            assocnames = getAssociatedWords(assocnames)
            assocnames.append(job)
            if job == 'Director':
                dirAppended = False

                for assocname in assocnames:
                    if assocname in sentence:
                        if len(sentencesAboutDirector) == 0:
                            sentencesAboutDirector = [name, job, [[sentence, sent]]]
                            dirAppended = True
                            break
                        else:
                            sentencesAboutDirector[2].append([sentence, sent])
                            dirAppended = True
                            break
                if(dirAppended):
                    break

            else:
                crewappended = False
                for assocname in assocnames:
                    if assocname in sentence:
                        #print sentence, name, job
                        for row in sentencesAboutCrew:
                            if row[0] == name and row[1] == job:
                                row[2].append([sentence,sent])
                                crewappended = True
                                break
                    if crewappended:
                        break

                sentencesAboutCrew.append([name, job, [[sentence, sent]]])
    #introTemplates = loadTemplates('C:\Users\Thomas\Documents\CSY3\FYP\\reviewer\movieReviewer\src\introtemplates.txt')
    introTemplates = loadTemplates('/Users/tom/Documents/CSY3/FYP/movieReviewer/src/introtemplates.txt')

    #outroTemplates = loadTemplates('C:\Users\Thomas\Documents\CSY3\FYP\\reviewer\movieReviewer\src\outrotemplates.txt')
    outroTemplates = loadTemplates('/Users/tom/Documents/CSY3/FYP/movieReviewer/src/outrotemplates.txt')

    #sentenceTemplates = loadTemplates('C:\Users\Thomas\Documents\CSY3\FYP\\reviewer\movieReviewer\src\simpletemplates.txt')
    sentenceTemplates = loadTemplates('/Users/tom/Documents/CSY3/FYP/movieReviewer/src/simpletemplates.txt')

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
    review += plotsummary
    for sentence in body:
        #print sentence
        review += generateSentence(sentence, sentencesAboutDirector, sentencesAboutCast, sentencesAboutCrew, movieName, genre, reception) + " "
    review += generateSentence(outro, sentencesAboutDirector, sentencesAboutCast, sentencesAboutCrew, movieName, genre, reception)
    print review

    print "Sentences about director:", sentencesAboutDirector
    print "Sentences about cast:", sentencesAboutCast
    print getAssociatedWords(["Tom Hanks", "Woody (voice)"])

def loadTemplates(filepath):
    ##loads templates from txt file
    templateFile = file(filepath, mode='r')
    templateList = templateFile.read().splitlines()
    return templateList

def getMovieMeta(movieName):

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
        print "cast sent : " , castSent
        chosenIdx = int(len(castSent) * random.random())
        chosen = castSent[chosenIdx]
        actor = chosen[0]
        role = chosen[1]
        #print castSent
        #print "casent:", casent
        sentence = sentence.replace('[actor]', actor)
        sentence = sentence.replace('[role]', role)
        if '[actoradverb]' in sentence:
            #print "casent:", casent[0]
            #print "directorSent:", directorSent[0]
            sentence = sentence.replace('[actoradverb]', selectWord(chosen, 'adverb'))

        if '[actoradjective]' in sentence:
            #print "casent:", casent[0]
            #print "directorSent:", directorSent[0]
            sentence = sentence.replace('[actoradjective]',selectWord(chosen, 'adjective'))

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
            sentence = sentence.replace('[crewadverb]',selectWord(chosen, 'adverb'))
        if '[crewadjective]' in sentence:
            sentence = sentence.replace('[crewadjective]',selectWord(chosen, 'adjective'))



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

def getimdbID(title):
    #http://www.omdbapi.com/

    # using the omdb api i can gather the imdb title id and then use this to construct the url

    import ast
    conn = httplib.HTTPSConnection("www.omdbapi.com")

    payload = "{}"

    conn.request("GET", "/?t=" + title + "&r=json", payload)
    res = conn.getresponse()
    searchData = res.read()
    searchData = json.loads(searchData)
    # print searchData
    # print searchData
    id = str(searchData.get('imdbID'))
    #print id
    return id

def scrapeSynopsis(imdbID):
    # http://www.imdb.com/title/[id]/synopsis it is formatted like so. then i can parse the html and extract the synopsis
    #scrapes imdb's synopsis page for movie title


    synopsis = ""
    #conn = httplib.HTTPSConnection("www.imdb.com")

    #payload = "{}"
    #conn.request("GET", "/title/" + imdbID + "/synopsis", payload)
    #conn.request("GET", "/title/" + "moonlight" + "/synopsis", payload)

    #res = conn.getresponse()
    #searchData = res.read()
    #synopsis text starts at: <div id="swiki.2.1">

    #print "trying: http://www.imdb.com/title/" + imdbID + "/synopsis"
    r = requests.get('http://www.imdb.com/title/' + imdbID + "/synopsis")
    #print r
    #doctext = r.text

    soup = BeautifulSoup(r.text, 'html.parser')
    text = soup.find(id="swiki.2.1").get_text()

    return text
    # print searchData
    # print searchData
    #return searchData


def scrapeMovieReviews(imdbID, lim):
    #same method as above, scrapes a bunch of movie reviews off of imdb, for now anyway. other movie sites may prove more accessibler
    reviews = []
    illegalStrings = []
    illegalStrings.append("*** This review may contain spoilers ***")
    illegalStrings.append("Add another review")
    illegalStrings.append("Find showtimes, watch trailers, browse photos, track your Watchlist and rate your favorite movies and TV shows on your phone or tablet!")
    for i in range(0, lim):

        #print "trying: http://www.imdb.com/title/" + imdbID + "/reviews?start=" + str(i*10)

        r = requests.get('http://www.imdb.com/title/' + imdbID + "/reviews?start=" + str(i*10))
        # print r
        #print r.text
        soup = BeautifulSoup(r.text, 'html.parser')

        text = soup.findAll('p')
        count = 0
        for t in text:
            string = t.get_text().replace("\n", " ").replace(u"\'", "")
            if count > 10:
                if string not in illegalStrings:
                    reviews.append(string)


            count += 1

    #print reviews
    return reviews

def getAssociatedWords(names):
    assocNames = []
    for name in names:
        subnames = name.split(" ")

        for subname in subnames:
            if len(subname) > 2:
                assocNames.append(subname)
    return assocNames


def scrapeIMDB(title):
    id = getimdbID(title)
    synopsis = scrapeSynopsis(id)
    #print synopsis
    revs = scrapeMovieReviews(id, 1)
    return synopsis, revs


#templateReview()
templateReview("Toy Story")
#chaineyReview()

