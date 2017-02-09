import random
import nltk
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

    f = open('input.txt', 'r')

    str = f.read()
    print "Suggested keyphrases:"
    r = rake.Rake("lib/RAKE/SmartStoplist.txt")
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
            if name in sentence or job in sentence:
                #print sentence, name, job
                for row in sentencesAboutCrew:
                    if row[0] == name and row[1] == job:
                        row[2].append([sentence,sent])
                        break
                sentencesAboutCrew.append([name, job, [[sentence, sent]]])
    introTemplates = loadTemplates('C:\Users\Thomas\PycharmProjects\movieReviewer\src\introtemplates.txt')
    outroTemplates = loadTemplates('C:\Users\Thomas\PycharmProjects\movieReviewer\src\outrotemplates.txt')
    sentenceTemplates = loadTemplates('C:\Users\Thomas\PycharmProjects\movieReviewer\src\simpletemplates.txt')

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

    review += generateSentence(intro, sentencesAboutCast, sentencesAboutCrew, movieName, genre, reception) + " "
    for sent in body:
        review += generateSentence(sent, sentencesAboutCast, sentencesAboutCrew, movieName, genre, reception) + " "
    review += generateSentence(outro, sentencesAboutCast, sentencesAboutCrew, movieName, genre, reception)
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

def generateSentence(sentence, castSent, crewSent, moviename, genre, sent):

    #picks an actor mentioned in the castSent
    if ('[director]' in sentence):
        print 'director'
    if ('[actor]' or '[actor2]' in sentence):
        print 'actor'
    if ('[crew]' in sentence):
        print 'crew'

    if ('[moviename]' in sentence):
        sentence = sentence.replace('[moviename]', moviename)
        print moviename
    if ('[genre]' in sentence):
        sentence = sentence.replace('[genre]', genre)
        if('[see]' in sentence):
            if(sent.get('pos') > sent.get('neg')):
                sentence = sentence.replace('[see]', 'watch')
            else:
                sentence = sentence.replace('[see]', 'avoid')


    return sentence

    #

def tagString(str):

    tokens = word_tokenize(str)
    print tokens
    return nltk.pos_tag(tokens)

#templateReview()
templateReview("Bridge Of Spies")
