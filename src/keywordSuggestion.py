from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *

from lib.RAKE import rake


f = open('src/input.txt', 'r')

str = f.read()

r = rake.Rake("src/lib/RAKE/SmartStoplist.txt")

print r.run(str)
