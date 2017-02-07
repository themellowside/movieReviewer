from markov import *
import time

from twython import Twython, TwythonError
import json

def getUserTimeLineAfter(i):
    return

def runTombot():
    while True:

        API_KEY = 'Y7cCYDF2Nfs141Zd5SWTY5rrq'
        API_SECRET_KEY = 'xeJVtg1kcVnCvndeuLMiGFurgijDomciki7vwdlagnxqYqSgHd'

        ACCESS_TOKEN = '319558171-P5bk8YupTGPmvXTq8Qlg8fWa7crIGS7Skw0pmEbB'
        ACCESS_TOKEN_SECRET = 'U4hCqSl7ERhF7Ttk5Wl2pDYggPohf0BS4BaC3FSRrNfEB'

        twitter = Twython(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

        try:
            twitter = Twython(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

            user_timeline = twitter.get_user_timeline(screen_name='nullBaa', count=200, include_rts=False,
                                                      trim_user=True, contributor_details=False)
            since = user_timeline[len(user_timeline)-1].get('id')

            user_timeline_strings = []

            user_timeline_second = user_timeline = twitter.get_user_timeline(screen_name='nullBaa', count=200, include_rts=False,
                                                      trim_user=True, contributor_details=False, since=since)


            for tweet in user_timeline:
                user_timeline_strings.append(tweet.get('text'))

            for tweet in user_timeline_second:
                user_timeline_strings.append(tweet.get('text'))


            chain = generateMultidocTable(user_timeline_strings, 1)
            # for c in chain:
            #    print c
            tweet = newText(5 + int(random.random() * 27), 1, chain, True)
            print "Generated tweet: ", tweet
            twitter.update_status(status=tweet)
        except TwythonError as e:
            print e
        for i in range(1, 7):

            time.sleep(300)  # Delay for half an hour
            print("Waiting...", i*5 , 'minutes so far')


runTombot()


#print list_timeline

