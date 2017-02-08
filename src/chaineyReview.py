import random
import nltk
import util_funcs

from nltk import word_tokenize
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

    meta = getMovieMeta(movieName)

    cast = meta.get("cast")
    crew = meta.get("crew")

    from nltk import tokenize
    sentences = tokenize.sent_tokenize(str)

    review = ""
    #create a list of names from cast and crew with their role / job
    #look for name of role, job or the name of the person (or one of their names) in each sentence
    #

    sentencesAboutPeople = []
    sid = SentimentIntensityAnalyzer()


    for sentence in sentences:
        #check if sentence contains a name of a member of cast or crew
        #if it does add it to a list of phrases discussing cast or crew members
        sent = sid.polarity_scores(sentence)
        for person in cast:
            name = person.get('name')
            role = person.get('character')
            if name in sentence or role in sentence:
                #print sentence, name, role

                sentencesAboutPeople.append([name, role, sentence, sent])

        for person in crew:
            name = person.get('name')
            job = person.get('job')
            if name in sentence or job in sentence:
                #print sentence, name, job
                sentencesAboutPeople.append([name, job, sentence, sent])

    #now we have a list of sentences that talk about someone, and are tagged with their sentiment polarity
    #we can use these to construct basic sentences that talk about the person's performance in the job (they did well, poorly, capably)
    #

    #http://www.nltk.org/howto/chunk.html
    #

    reception = sid.polarity_scores(str)
    if reception.get('pos') > reception.get('neg'):
        review += "Definitely one worth watching."
    else:
        review += "It's not worth seeing this film."

    print review

def getMovieMeta(movieName):
    import httplib
    import json
    conn = httplib.HTTPSConnection("api.themoviedb.org")

    payload = "{}"

    conn.request("GET", "/3/search/movie?api_key=16e6e2321c81b245dbae3e28e24f6b7e&query="+movieName, payload)
    res = conn.getresponse()
    searchData = res.read()
    searchData = json.loads(searchData)
    #print searchData
    movieId = str(searchData.get('results')[0].get('id'))

    #print "Movie ID: ", movieId
    #find first instance of id in the text and return it as it is the movie title \"id\"

    conn.request("GET", "/3/movie/"+ movieId + "/credits?api_key=16e6e2321c81b245dbae3e28e24f6b7e", payload)
    res = conn.getresponse()
    castData = res.read()

    castData = json.loads(castData)
    #print castData

    return castData

def generateSentence():
    #nouns with adjectives preceeding or following them
    #structure of a movie review generally touches upon themes, technical detials, individual performances and such.
    #begins with an introduction, often describing a memorable scene from the film.
    #so we can break the sentence generation down in to some of these things.
    #
    #one difficulty with generating sentences is that summary or discussion of characters in the film will use proper nouns and it may be difficult to tell them apart from the
    #actors performing in it. for this purpose we will build a dictionary of actors and members of staff and a dictionary of the characters played using the IMDB files if at all possible

    print 'something'

    #

def tagString(str):

    tokens = word_tokenize(str)
    print tokens
    return nltk.pos_tag(tokens)

#templateReview()
templateReview("Bridge+Of+Spies")
