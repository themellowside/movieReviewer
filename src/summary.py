from summa import summarizer

f = open('/Users/tom/Documents/CSY3/FYP/movieReviewer/src/synopsis.txt', 'r')

str = f.read()

print summarizer.summarize(str)