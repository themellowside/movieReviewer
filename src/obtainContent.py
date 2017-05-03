
import random
import nltk

import util_funcs

from nltk import word_tokenize

from nltk import tokenize
from nltk.sentiment import SentimentIntensityAnalyzer
from unidecode import unidecode
import httplib
import json

import requests
from bs4 import BeautifulSoup

from nltk.sentiment import SentimentIntensityAnalyzer

from getAssocWord import *


def getContent(movieName):
    synopsis, reviews = scrapeIMDB(movieName.replace(" ", "+"))
    from summa import summarizer
    if len(synopsis) > 0:
        plotsummary = summarizer.summarize(synopsis, ratio=0.05)
    reviewCorpora = ""
    for review in reviews:
        reviewCorpora += review

    meta, genre = getMovieMeta(movieName.replace(" ", "+"))

    cast = meta.get("cast")
    crew = meta.get("crew")

    sentences = tokenize.sent_tokenize(reviewCorpora)

    # create a list of names from cast and crew with their role / job
    # look for name of role, job or the name of the person (or one of their names) in each sentence
    #

    sid = SentimentIntensityAnalyzer()
    reception = sid.polarity_scores(reviewCorpora)

    sentencesAboutCast = []
    sentencesAboutCrew = []
    sentencesAboutDirector = []
    for sentence in sentences:
        # check if sentence contains a name of a member of cast or crew
        # if it does add it to a list of phrases discussing cast or crew members
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
                    # print sentence, name, role

                    for row in sentencesAboutCast:
                        if row[0] == name and row[1] == role:
                            row[2].append([sentence, sent])
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
                if (dirAppended):
                    break

            else:

                crewappended = False
                for assocname in assocnames:
                    if assocname in sentence:
                        # print sentence, name, role
                        crewExists = False
                        for row in sentencesAboutCrew:
                            if row[0] == name and row[1] == job:
                                row[2].append([sentence, sent])
                                crewExists = True
                                break
                        if not crewExists:
                            sentencesAboutCrew.append([name, job, [[sentence, sent]]])

                        crewappended = True

                    if crewappended:
                        break
    return plotsummary, sentencesAboutCast, sentencesAboutCrew, sentencesAboutDirector, meta, genre, reception

def getAdditionalContent(movieName, castNames, director):
    #this is for the nlg system, obtains additional data that could later be used to improve the template system too I suppose
    import ast

    #grab cast id and crew id
    #https://api.themoviedb.org/3/search/person?api_key=16e6e2321c81b245dbae3e28e24f6b7e&query=[name1]%20[name2]
    iDNameRoles = []
    for castName in castNames:
        iDNameRoles.append([getPersonID(castName[0]), castName, 'cast', castName[1]])

    iDNameRoles.append([getPersonID(director), director, 'director', 'director'])
    pastCollaborations = []

    for combination in getCombinations(iDNameRoles, []):
        #print combination
        id1 = 0
        id2 = 0
        if combination[0][2] == 'director':
            id1 = combination[0][0]
            id2 = combination[1][0]
        else:
            id1 = combination[1][0]
            id2 = combination[0][0]
        pastWorks = pastMovieIncidence(movieName, id1, id2)
        if len(pastWorks) > 0:
            pastCollaborations.append([combination[0][1], combination[1][1], pastWorks])

    return pastCollaborations

def getCombinations(remaining, combinations):
    #get all combinations of each individual with no repetitions

    if len(remaining) > 0:
        first = remaining[0]
        remainingClone = remaining[1:]
        for remaining in remainingClone:
            combinations.append([first, remaining])
        return getCombinations(remainingClone, combinations)

    return combinations

def pastMovieIncidence(movieName, id1, id2):
    payload = "{}"
    conn = httplib.HTTPSConnection("api.themoviedb.org")

    conn.request("GET", "/3/discover/movie?api_key=16e6e2321c81b245dbae3e28e24f6b7e&with_cast="+str(id1)+ "&with_people="+str(id2),
                 payload)

    res = conn.getresponse()
    searchData = res.read()
    searchData = json.loads(searchData)
    filmNames = []

    for result in searchData.get('results'):
        if result.get('title') != movieName:
            filmNames.append(result.get('title'))


    return filmNames

def getPersonID(name):
    conn = httplib.HTTPSConnection("api.themoviedb.org")
    payload = "{}"
    rep = name.replace(" ", "%20")
    rep = unidecode(rep)
    #print rep
    conn.request("GET",
                 "https://api.themoviedb.org/3/search/person?api_key=16e6e2321c81b245dbae3e28e24f6b7e&query=" + rep,
                 payload)

    res = conn.getresponse()
    searchData = res.read()
    searchData = json.loads(searchData)
    return searchData.get('results')[0].get('id')

def scrapeIMDB(title):
    id = getimdbID(title)
    synopsis = scrapeSynopsis(id)
    #print synopsis
    revs = scrapeMovieReviews(id, 2)
    return synopsis, revs

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


def getAssociatedWords(names):
    assocNames = []
    disallowed = ['the', 'man', 'woman', 'from', 'uncredited', 'boy', 'girl', 'staff', '(uncredited)', 'for']
    for name in names:
        subnames = name.split(" ")

        for subname in subnames:
            if len(subname) > 2 and subname not in disallowed:
                assocNames.append(subname)
    return assocNames

#print getAdditionalContent("The Wolf of Wall Street", ["Leonardo DiCaprio", "Jonah Hill"], "Martin Scorsese")

