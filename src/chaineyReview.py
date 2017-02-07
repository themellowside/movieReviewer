import random

from nltk.sentiment import SentimentIntensityAnalyzer

from lib.RAKE import rake
#http://www.nltk.org/book/ch06.html#ref-document-classify-extractor

#sentences = rake.split_sentences(open('/Users/tom/Documents/CSY3/FYP/movieReviewer/src/res/movie_reviews/neg/cv000_29416.txt', 'r').read())

#for i in range(0, len(sentences)):
#    print sentences[i], sid.polarity_scores(sentences[i])



def chaineyReview():
    f = open('/Users/tom/Documents/CSY3/FYP/movieReviewer/src/input.txt', 'r')

    str = f.read()
    print "Suggested keyphrases:"
    sid = SentimentIntensityAnalyzer()
    r = rake.Rake("/Users/tom/Documents/CSY3/FYP/movieReviewer/src/lib/RAKE/SmartStoplist.txt")
    keywords = r.run(str)
    print keywords
    print "Reception of the film:"
    reception = sid.polarity_scores(str)
    print "Pos:", reception.get('pos'), "Neg:", reception.get('neg')

    import markov

    print markov.newText(300, 2, markov.generateTable(str, 2), False)
    if reception.get('pos') > reception.get('neg'):
        print "Definitely one worth watching."
    else:
        print "It's not worth seeing this film."

def templateReview():
