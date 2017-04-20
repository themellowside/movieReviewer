from markov import *
import time

from twython import Twython, TwythonError
import json

def runTombot():
    executing = True
    counter = 0
    filmsFile = file('C:\Users\Thomas\Documents\CSY3\FYP\\reviewer\movieReviewer\src\\reviewedFilms.txt', mode='r')
    filmsList = filmsFile.read().splitlines()
    films =[]
    for film in filmsList:
        films.append(film.split('*'))
    print films
    while executing:

        API_KEY = 'Y7cCYDF2Nfs141Zd5SWTY5rrq'
        API_SECRET_KEY = 'xeJVtg1kcVnCvndeuLMiGFurgijDomciki7vwdlagnxqYqSgHd'

        ACCESS_TOKEN = '319558171-P5bk8YupTGPmvXTq8Qlg8fWa7crIGS7Skw0pmEbB'
        ACCESS_TOKEN_SECRET = 'U4hCqSl7ERhF7Ttk5Wl2pDYggPohf0BS4BaC3FSRrNfEB'

        try:
            twitter = Twython(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

            # now, generate a tweet advertising our generated movie reviews
            # essentially from a template of texts that say such things as "read our review of [moviename] here: [link]"

            # tweet = newText(5 + int(random.random() * 27), 1, chain, True)
            tweet = generateText(twitter, films)

            print "Generated tweet: ", tweet
            twitter.update_status(status=tweet)

            time.sleep(3600)  # Delay for half an hour





        except TwythonError as e:
            print e

        try:
            twitter = Twython(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

            # now, generate a tweet advertising our generated movie reviews
            # essentially from a template of texts that say such things as "read our review of [moviename] here: [link]"
            advert = generateAdvert(films)
            print "Generated ad: ", advert
            twitter.update_status(status=advert)
            time.sleep(3600)  # Delay for half an hour


        except TwythonError as e:
            print e



        #for i in range(1, 7):
            #time.sleep(300)  # Delay for half an hour
            #print("Waiting...", i*5 , 'minutes so far')

def generateText(twitter, films):


    film = films[int(random.random()*len(films))][0]

    #list of terms to search twitter for in order to gather a corpus


    searchTerms = [film, "saw " + film,  film +" movie", film + " film", "#" + film.replace(" ", "")]

    searchStrings = []

    for searchTerm in searchTerms:

        search = twitter.search(q=searchTerm, result_type='recent').get('statuses')

        for status in search:
            text = status.get('text')
            text = stripHandles(text)
            text = stripTags(text)
            text = stripURL(text)

            searchStrings.append(text)

        #
        # for tweet in user_timeline:
        #     user_timeline_strings.append(tweet.get('text'))
        #
        # for tweet in user_timeline_second:
        #     user_timeline_strings.append(tweet.get('text'))

        print searchStrings

    chain = generateMultidocTable(searchStrings, 1)
    tweet = newText(144, 1, chain, True)
    return tweet

def generateAdvert(reviews):

    #list of films?



    chosenAdvert = int(random.random()*len(reviews))

    reviewURL = reviews[chosenAdvert][1]
    movieTitle = reviews[chosenAdvert][0]

    #how can you advertise a movie review?
    #read our review of [title] here: [link]
    #Check our our thoughs on [title] here: [link]

    introTexts = ["Read our review of ", "Read our review for ", "Check our our review of ", "See what we thought of ", "Have a look at our thoughts on ", "Take a look at our review of "]
    locationTexts = [" here: ", " at "]

    introtext = introTexts[int(random.random()*len(introTexts))]
    locationtext = locationTexts[int(random.random()*len(locationTexts))]

    advert = introtext + movieTitle + locationtext + reviewURL + " #" + movieTitle.replace(" ", "")

    return advert

def stripHandles(inp):

    foundHandle = False
    oup = ""
    for i in range(0, (len(inp))):
        if inp[i] == '@':
            foundHandle = True

        elif inp[i] == ' ':
            foundHandle = False

        if foundHandle == False:
            oup += inp[i]
    return oup

def stripTags(inp):
    foundTag = False
    oup = ""
    for i in range(0, (len(inp))):
        if inp[i] == '#':
            foundTag = True

        elif inp[i] == ' ':
            foundTag = False

        if foundTag == False:
            oup += inp[i]

    return oup

def stripURL(inp):
    foundURL = False
    oup = ""
    for i in range(0, (len(inp))):
        if i + 8 < len(inp):
            if inp[i:i+8] == 'https://':
                foundURL = True

        if foundURL == False:
            oup += inp[i]

        elif inp[i] == ' ':
            foundURL = False

    return oup

runTombot()

#print list_timeline

