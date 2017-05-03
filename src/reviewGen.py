from chaineyReview import *


def generateReview(filmtitle):
    content = determineContent(filmtitle)
    structuredContent = structureDocument(content)
    aggregatedDoc = aggregateDocument(structuredContent)
    aggDocWLex = lexicalChoice(aggregatedDoc)
    docWReferringExp = generateReferringExpression(aggDocWLex)
    return realiseDocument(docWReferringExp)

def determineContent(filmtitle):

    plotsummary, sentencesAboutCast, sentencesAboutCrew, sentencesAboutDirector, meta, genre, reception = getContent(filmtitle)
    content = {}

    #content will be a series of opinions and statements relating to actors, directors, the film in general, a plot synopsis, the genre of the movie,
    ## and other things to flesh out the review in order to make it more like a review text than a list of sentiment tagged points

    #
    #one such content could be
    #subject verb adjective
    #
    #pick the most mentioned crew between 0 and 3 members inclusively.
    #pick the most mentioned cast between 0 and 4 members inclusively - keep track of how mentioned they are as this is relevant in content structure
    #talk about director obviously - obtain overall sentiment and some adjectives + adverbs to use
    #
    #print sentencesAboutCast
    #genre - talk about how it relates to other films within the genre

    #can we get previous roles in movies from actors?
    #can we get previous films by director + their reception?
    content['title'] = filmtitle
    content['summary'] = plotsummary
    content['genre'] = genre
    content['reception'] = reception

    totalCast = len(sentencesAboutCast)
    talkableCast = []

    if totalCast > 4:

        while len(talkableCast) <= 4:
            mostMentions = 0
            mostMentioned = []
            for castMemb in sentencesAboutCast:
                mentions = len(castMemb[2])
                if mentions > mostMentions and castMemb not in talkableCast:
                    mostMentions = mentions
                    mostMentioned = castMemb

            talkableCast.append(mostMentioned)
    else:
        for cast in sentencesAboutCast:
            talkableCast.append(cast)


    totalCrew = len(sentencesAboutCrew)
    talkableCrew = []

    if totalCrew > 3:

        while len(talkableCrew) <= 3:
            mostMentions = 0
            mostMentioned = []
            for crewMemb in sentencesAboutCrew:
                mentions = len(crewMemb[2])
                if mentions > mostMentions and crewMemb not in talkableCrew:
                    mostMentions = mentions
                    mostMentioned = crewMemb

            talkableCrew.append(mostMentioned)
    else:
        for crew in sentencesAboutCrew:
            talkableCrew.append(crew)

    castNames = []
    for cast in talkableCast:
        #print cast
        castNames.append([cast[0], cast[1]])

    content['previous'] = getAdditionalContent(filmtitle, castNames, sentencesAboutDirector[0])
    content['noteworthyCast'] = talkableCast
    content['noteworthyCrew'] = talkableCrew
    content['director'] = sentencesAboutDirector
    #take the names of the cast members and see if they have any incidence in past movies
    #print content.get('noteworthyCrew')
    #print content
    return content

def structureDocument(content):
    #this method takes the content and decides where to make statements about what, semi-stochastically

    #because the structure of a movie review is sort of generated along with the content this section wil

    structure = []

    plotSummary = []


    ##STRUCTURE INTRO##
    #introductory sentence - essentially pos or neg
    #needs: title, genre, reception, lead actor and director
    intro = structureIntro(content)

    #add opening sentence, pick randomly from the rest of what is necessary to include
    plotSummary.append(content.get('summary'))
    ##STRUCTURE PSUMM##
    #add plot summary text?


    ##STRUCTURE MAINBODY##
    #Pick a topic, sentiment, and adjectives/adverbs related to it
    #repeat this multiple times - related clauses need to be grouped however
    #order of assessment of each member of cast + crew should have most influential at the beginning? - make that choice
    #mention people who have worked together previously together also (if applicable)
    mainbody = structureBody(content)

    ##STRUCTURE OUTRO##
    #Use general sentiment and pick the most mentioned person to talk about again
    #Closing sentence
    outro = structureOutro(content)

    for int in intro:
        structure.append(int)
    structure.append(plotSummary)
    for main in mainbody:
        structure.append(main)
    for out in outro:
        structure.append(out)

    #print structure
    return structure

def structureIntro(content):
    # make a bunch of statements defining film + actors / roles

    intro = []
    introTopics = []
    topics = ['filmname', 'sentiment', 'director', 'mostRelevantActor']

    while len(topics) > 0:
        topicidx = int(len(topics) * random.random())
        topic = topics[topicidx]
        topics.remove(topic)
        introTopics.append(topic)

        # for topic in optionalTopics:
        #     if random.random() > 0.75:
        #         intro.append(topic)

    for subject in introTopics:
        if subject == 'filmname':
            intro.append(['filmname', content.get('title')])
            intro.append(['optional genre', content.get('genre')])
            intro.append(['optional film sentiment', content.get('reception')])

        elif subject == 'director':
            intro.append(['director', content.get('director')])
            intro.append(['optional director sentiment', content.get('director')])
        elif subject == 'mostRelevantActor':
            intro.append(['actor role', content.get('noteworthyCast')[0]])
            intro.append(['optional actor sentiment', content.get('noteworthyCast')[0]])
            intro.append(['optional second actor', content.get('noteworthyCast')[1]])

    return intro

def structureOutro(content):
    #make a bunch of statements about whether or not the film is worth seeing
    topics = ['sentiment', 'mostRelevantActor', 'director', 'genre']
    outroTopics = []
    outro = []

    while len(topics) > 0:

        topicidx = int(len(topics) * random.random())
        topic = topics[topicidx]
        topics.remove(topic)
        outroTopics.append(topic)

    for subject in outroTopics:
        if subject == 'sentiment':
            outro.append(['film sentiment', content.get('title'), content.get('reception')])
        elif subject == 'mostRelevantActor':
            outro.append(['actor sentiment', content.get('noteworthyCast')[0]])
        elif subject == 'director':
            outro.append(['closing optional director sentiment', content.get('director')])
        elif subject == 'genre':
            outro.append(['closing genre sentiment', content.get('genre'), content.get('reception')])

    return outro

def structureBody(content):
    #make a bunch of statements in an orderly fashion i guess
    topics = ['cast', 'director', 'crew', 'past']

    #start with past roles - group people together from them
    #talk about rest of cast and crew and director after that
    #these are the only 'factual' things we can mention - will add random template context-free stuff later stage
    body = []
    previous = content.get('previous')
    pair = []
    from random import shuffle

    if len(previous) > 0:
        #pick a random pair to mention
        pair = previous[int(random.random() * len(previous))]
        cast = content.get('noteworthyCast')
        firstSent = []
        secondSent = []
        for member in cast:
            if member[0] == pair[0][0]:
                firstSent = member
            elif member[0] == pair[1][0]:
                secondSent = member

        clausePairs = [[['second role', pair[1]], ['second sentiment', secondSent]], [['first role', pair[0]], ['first sentiment', firstSent]], [['pair past work comparison', content.get('reception')], ['pair past work', previous]]]

        shuffle(clausePairs)

        for clausePair in clausePairs:
            for clause in clausePair:
                body.append(clause)

    remainingClausePairs = []

    for crew in content.get('noteworthyCrew'):
        cs = [['crew role', crew],['crew sentiment', crew]]
        shuffle(cs)
        remainingClausePairs.append(cs)
    for cast in content.get('noteworthyCast'):
        if cast[0] == pair[0][0] or cast[0] == pair[1][0]:
            cas = [['cast role', cast],['cast sentiment', cast]]
            shuffle(cas)
            remainingClausePairs.append(cas)

    if content.get('director')[0] == pair[0][0] or content.get('director')[0] == pair[1][0]:
        remainingClausePairs.append(['director sentiment', content.get('director')])

    for clausePair in remainingClausePairs:
        #print clausePair
        for clause in clausePair:
            body.append(clause)

    return body

def aggregateDocument(document):
    #this method looks for pieces of content which can be concatenated into a single sentrence
    #look through statements and see where they can be combined
    agg = []
    #print document
    #print 'printing document structure'

    #for doc in document:
        #print doc[0]
    #print
    #print

    dociter = iter(range(0, len(document)))
    for i in dociter:
        ###aggregation of main body clauses###

        if document[i][0] == 'first sentiment':
            if document[i+1][0] == 'first role':
                next(dociter, None)
                agg.append(['first sent role', document[i][1]])

        elif document[i][0] == 'first role':
            if document[i+1][0] == 'first sentiment':
                next(dociter, None)
                agg.append(['first role sent', document[i+1][1]])

        elif document[i][0] == 'second sentiment':
            if document[i+1][0] == 'second role':
                next(dociter, None)
                agg.append(['second sent role', document[i][1]])

        elif document[i][0] == 'second role':
            if document[i+1][0] == 'second sentiment':
                next(dociter, None)
                #print document[i+1]
                agg.append(['second role sent', document[i+1][1]])

        elif document[i][0] == 'pair past work':
            if document[i+1][0] == 'pair past work comparison':
                next(dociter, None)
                #print document[i]
                #print document[i+1]

                agg.append(['pair past work comparison', document[i][1], document[i+1][1]])

        elif document[i][0] == 'pair past work comparison':
            if document[i+1][0] == 'pair past work':
                next(dociter, None)
                #print document[i]
                #print document[i+1]
                agg.append(['comparison pair past work', document[i][1], document[i+1][1]])


        elif document[i][0] == 'cast sentiment':
            if document[i+1][0] == 'cast role':
                next(dociter, None)
                agg.append(['cast sent role', document[i][1]])

        elif document[i][0] == 'cast role':
            if document[i+1][0] == 'cast sentiment':
                next(dociter, None)
                agg.append(['cast role sent', document[i][1]])

        elif document[i][0] == 'crew sentiment':
            if document[i+1][0] == 'crew role':
                next(dociter, None)
                agg.append(['crew sent role', document[i][1]])

        elif document[i][0] == 'crew role':
            if document[i+1][0] == 'crew sentiment':
                next(dociter, None)
                agg.append(['crew role sent', document[i][1]])


        #### aggregation of intro clauses ####

        elif document[i][0] == 'actor role':

            stri = 'actor role'
            actor = document[i][1]
            second = []

            if document[i + 1][0] == 'optional actor sentiment':
                next(dociter, None)
                stri = stri + ' ' + 'sentiment'

            elif document[i + 1][0] == 'optional second actor':
                next(dociter, None)
                stri = stri + ' ' + 'second'
                second = document[i + 1][1]

            if document[i + 2][0] == 'optional actor sentiment':
                next(dociter, None)
                stri = stri+ ' ' + 'sentiment'

            elif document[i + 2][0] == 'optional second actor':
                next(dociter, None)
                stri = stri + ' ' + 'second'
                second = document[i + 2][1]

            agg.append([stri, actor, second])



        elif document[i][0] == 'director':
            if document[i+1][0] == 'optional director sentiment':
                agg.append(['intro director sentiment', document[i][1]])
                next(dociter, None)
            else:
                agg.append(['intro director'], [i][1])


        elif document[i][0] == 'filmname':
            stri = 'filmname'
            title = document[i][1]
            genre = ''
            sentiment = []
            if document[i + 1][0] == 'optional genre':
                next(dociter, None)
                stri = stri + ' ' + 'genre'
                genre = document[i+1][1]

            elif document[i+1][0] == 'optional film sentiment':
                next(dociter, None)
                stri = stri + ' ' + 'sentiment'
                sentiment = document[i+1][1]

            if document[i + 2][0] == 'optional genre':
                next(dociter, None)
                stri = stri + ' ' + 'genre'
                genre = document[i+2][1]

            elif document[i+2][0] == 'optional film sentiment':
                next(dociter, None)
                stri = stri + ' ' + 'sentiment'
                sentiment = document[i + 2][1]

            agg.append([stri, title, genre, sentiment])

        #### aggregation of outro clauses ####


        elif document[i][0] == 'closing optional director sentiment' or document[i][0] == 'actor sentiment' or document[i][0] == 'closing genre sentiment' or document[i][0] == 'film sentiment':

            agg.append([document[i][0], document[i][1]])
            stri = ''
            directorsent =[]
            actorsent = []
            genre = ''
            filmname = ''
            reception = []
            firstItem = True
            for j in range(i, len(document)):

                if firstItem == True:
                    firstItem = False
                else:
                    stri = stri + ' '

                if document[j][0] == 'closing optional director sentiment':
                    stri = stri + 'directorsent'
                    directorsent = document[j][1]
                    next(dociter, None)

                elif document[j][0] == 'actor sentiment':
                    stri = stri + 'actorsent'
                    actorsent = document[j][1]
                    next(dociter, None)

                elif document[j][0] == 'closing genre sentiment':
                    stri = stri + 'genre'
                    genre = document[j][1]
                    reception = document[j][2]
                    next(dociter, None)

                elif document[j][0] == document[j][0] == 'film sentiment':
                    stri = stri + 'film'
                    filmname = document[j][1]
                    reception = document[j][2]
                    next(dociter, None)
                    # pass on the plot summary

            agg.append([stri, filmname, genre, directorsent, actorsent, reception])


    return agg

def lexicalChoice(document):

    #chooses words related to sentiment and other vocabulary to make the text sound more original
    lchoice = []

    for doc in document:
        if type(doc) != str:

            lchoice.append(fulfil(doc))
        else:
            lchoice.append(doc)

    print 'printing text-ified document structure'
    for lc in lchoice:
        print lc

    return lchoice

def fulfil(doc):
    #choose words to fill in the structure with
    ff =[]



    #### MAIN BODY HANDLING ####

    if doc[0] == 'cast role sent':
        pol = getSentRating(doc[1])

        adv = getAssocWord(doc[1], 'adverb')
        asPart = asParticle[int(random.random()*len(asParticle))]

        if random.random() > 0.5:
            if pol == 'neg':
                pos = int(random.random()*len(posCastPhrases))
                additional = posCastPhrases[pos]
                ff.append([doc[1][0], asPart, doc[1][1], adv, additional])
                del(posCastPhrases[pos])

            else:

                pos = int(random.random() * len(negCastPhrases))
                additional = negCastPhrases[pos]
                ff.append([doc[1][0], asPart, doc[1][1], adv, additional])
                del (negCastPhrases[pos])
        else:
            ff.append([doc[1][0], asPart, doc[1][1], adv])

    elif doc[0] == 'cast sent role':
        pol = getSentRating(doc[1])

        adj = getAssocWord(doc[1], 'adjective')

        asPart = asParticle[int(random.random()*len(asParticle))]

        if random.random() > 0.5:
            if pol == 'neg':
                pos = int(random.random()*len(posCastPhrases))
                additional = posCastPhrases[pos]
                ff.append([additional, doc[1][0], adj, asPart, doc[1][1]])
                del(posCastPhrases[pos])

            else:

                pos = int(random.random() * len(negCastPhrases))
                additional = negCastPhrases[pos]
                ff.append([additional, doc[1][0], adj, asPart, doc[1][1]])
                del (negCastPhrases[pos])
        else:
            ff.append([doc[1][0], adj, asPart, doc[1][1]])


    ##

    if doc[0] == 'crew role sent':
        pol = getSentRating(doc[1])

        adv = getAssocWord(doc[1], 'adverb')
        asPart = asParticle[int(random.random()*len(asParticle))]

        if random.random() > 0.5:
            if pol == 'neg':
                pos = int(random.random()*len(posCrewPhrases))
                additional = posCrewPhrases[pos]
                ff.append([doc[1][0], asPart, doc[1][1], adv, additional])
                del(posCrewPhrases[pos])

            else:

                pos = int(random.random() * len(negCrewPhrases))
                additional = negCrewPhrases[pos]
                ff.append([doc[1][0], asPart, doc[1][1], adv, additional])
                del (negCrewPhrases[pos])
        else:
            ff.append([doc[1][0], asPart, doc[1][1], adv])

    elif doc[0] == 'crew sent role':
        pol = getSentRating(doc[1])

        adj = getAssocWord(doc[1], 'adjective')

        asPart = asParticle[int(random.random()*len(asParticle))]

        if random.random() > 0.5:
            if pol == 'neg':
                pos = int(random.random()*len(posCrewPhrases))
                additional = posCrewPhrases[pos]
                ff.append([additional, doc[1][0], adj, asPart, doc[1][1]])
                del(posCrewPhrases[pos])

            else:

                pos = int(random.random() * len(negCrewPhrases))
                additional = negCrewPhrases[pos]
                ff.append([additional, doc[1][0], adj, asPart, doc[1][1]])
                del (negCrewPhrases[pos])
        else:
            ff.append([doc[1][0], adj, asPart, doc[1][1]])


    ##
    elif doc[0] == 'first role sent':
        #pol = getSentRating(doc[1])


        adv = getAssocWord(doc[1], 'adverb')
        ff.append([doc[1][0], 'plays', doc[1][1], adv])
    elif doc[0] == 'first sent role':
        #pol = getSentRating(doc[1])

        adj = getAssocWord(doc[1], 'adjective')
        asPart = asParticle[int(random.random()*len(asParticle))]

        ff.append([doc[1][0], adj, asPart, doc[1][1]])
    elif doc[0] == 'second role sent':
        #pol = getSentRating(doc[1])


        adv = getAssocWord(doc[1], 'adverb')
        ff.append([doc[1][0], 'plays', doc[1][1], adv])

    elif doc[0] == 'second sent role':
        #pol = getSentRating(doc[1])

        adj = getAssocWord(doc[1], 'adjective')

        asPart = asParticle[int(random.random()*len(asParticle))]
        ff.append([doc[1][0], adj, asPart, doc[1][1]])

    elif doc[0] == 'pair past work comparison':

        name1 = doc[1][0][0][0]
        name2 = doc[1][0][1][0]
        movie = doc[1][0][2][0]
        con = conj[int(random.random()*len(conj))]

        sentPol = doc[2]
        sent = 'neg'
        if sentPol.get('pos') > sentPol.get('neg'):
            comp = posComparativeSentimentPhrases[int(random.random()*len(posComparativeSentimentPhrases))]
            ff.append([name1, 'and', name2, 'haveWorkedOn', movie, con, comp])
        else:
            comp = negComparativeSentimentPhrases[int(random.random()*len(negComparativeSentimentPhrases))]

            ff.append([name1, 'and', name2, 'haveWorkedOn', movie, con, comp])



    elif doc[0] == 'comparison pair past work':

        name1 = doc[2][0][0][0]
        name2 = doc[2][0][1][0]
        movie = doc[2][0][2][0]

        sentPol = doc[1]
        sent = 'neg'
        if sentPol.get('pos') > sentPol.get('neg'):
            comp = posComparativeSentimentPhrases[int(random.random() * len(posComparativeSentimentPhrases))]
            ff.append([comp, movie, 'features', name1, 'and', name2])
        else:
            comp = negComparativeSentimentPhrases[int(random.random() * len(negComparativeSentimentPhrases))]
            ff.append([comp, movie, 'features', name1, 'and', name2])


    #### INTRO HANDLING ####
    # filmname genre sentiment
    #actor role sentiment second
    #intro director sentiment

    elif 'filmname' in doc[0]:

        sections = doc[0].split(' ')
        sentence = []
        sentPol = doc[3]
        sent = 'neg'
        if sentPol.get('pos') > sentPol.get('neg'):
            sent = 'pos'

        for section in sections:
            if section == 'filmname':
                sentence.append(doc[1])
                sentence.append('is')
            elif section == 'genre':
                sentence.append('a')
                sentence.append(doc[2])

        ff.append(sentence)

    elif 'actor role' in doc[0]:

        sections = doc[0].split(' ')
        sentence = []
        #print 'PRINTING ACTOR STUFF'
        #print doc
        fSent = getSentRating(doc[1])
        #sSent = getSentRating(doc[2])

        for section in sections:
            if section == 'actor':
                sentence.append('starring')
                sentence.append(doc[1][0])
            elif section == 'role':
                sentence.append('as')
                sentence.append(doc[1][1])
            elif section == 'second':
                sentence.append('and')
                sentence.append(doc[2][0])

        ff.append(sentence)
    elif 'intro' in doc[0]:

        sections = doc[0].split(' ')
        sentence = []
        sent = getSentRating(doc[1])
        for section in sections:
            if section == 'director':
                sentence.append('directed by')
                sentence.append(doc[1][0])
            elif section == 'sentiment':
                if sent == 'pos':
                    sentence.append(introPosDirectorSentimentPhrases[int(random.random()*len(introPosDirectorSentimentPhrases))])
                else:
                    sentence.append(introNegDirectorSentimentPhrases[int(random.random()*len(introNegDirectorSentimentPhrases))])

        ff.append(sentence)

    #### OUTRO HANDLING ####
    # actorsent
    # directorsent
    # genre
    # film

    elif 'directorsent' in doc[0]:
        #[['genre', 'film', 'directorsent', 'actorsent']]
        #print doc
        sections = doc[0].split(' ')
        sentence = []

        dirSent = getSentRating(doc[3])
        actSent = getSentRating(doc[4])
        genSent = 'neg'
        if doc[5].get('pos') > doc[5].get('neg'):
            genSent = 'pos'

        for section in sections:
            if section == 'genre':
                if genSent == 'pos':

                    sentence.append(posOutroGenreSentimentPhrases[int(random.random()*len(posOutroGenreSentimentPhrases))])
                else:
                    sentence.append(negOutroGenreSentimentPhrases[int(random.random()*len(negOutroGenreSentimentPhrases))])

                sentence.append(doc[2])

            elif section == 'film':
                sentence.append(doc[1])
                if genSent == 'pos':

                    sentence.append(
                        posOutroFilmSentimentPhrases[int(random.random() * len(posOutroFilmSentimentPhrases))])
                else:
                    sentence.append(
                        negOutroFilmSentimentPhrases[int(random.random() * len(negOutroFilmSentimentPhrases))])


            elif section == 'directorsent':
                sentence.append(doc[3][0])

                if dirSent == 'pos':

                    sentence.append(
                        posOutroDirectorSentimentPhrases[int(random.random() * len(negOutroDirectorSentimentPhrases))])
                else:
                    sentence.append(
                        negOutroDirectorSentimentPhrases[int(random.random() * len(negOutroDirectorSentimentPhrases))])


            elif section == 'actorsent':
                sentence.append(doc[4][0])
                if genSent == 'pos':

                    sentence.append(
                        posOutroActorSentimentPhrases[int(random.random() * len(negOutroActorSentimentPhrases))])
                else:
                    sentence.append(
                        negOutroActorSentimentPhrases[int(random.random() * len(negOutroActorSentimentPhrases))])

        ff.append(sentence)
    return ff

def generateReferringExpression(document):
    #also known as anaphora
    #this is sort of cyclic - needs to have content determination and lexical choice

    #inserts referring expressions regarding the document, also add some templated particles/speech elements to seem more personable
    #first, given a list of names, replace names and insert things to names to make them referring to earlier sentences.
    #Also, handle capital letters, full stops
    return document

def realiseDocument(document):
    #converst structured document into text (hopefully this is mostly verbatim)

    text = ""
    for sentence in document:
        if len(sentence) > 0:
            for word in sentence[0]:
                text = text + ' ' + word


    return text


 ### Main Body Phrase Collection ####

posCastPhrases = ['in one of the best works of their career','in a career defining performance', ', giving a career defining performance', ', really breating life into the role', ', selling the role perfectly', ', in a memorable performance']
negCastPhrases = ['in one of the worst works of their career',', giving a forgettable performance', ', has really embarassed theirself in this role', 'and is not worth writing home about']
posCrewPhrases = ['doing an excellent job','in a career defining performance', ', giving a career defining performance', ', really breating life into the role', ', selling the role perfectly', ', in a memorable performance']
negCrewPhrases = ['in one of the worst works of their career',', giving a forgettable performance', ', has really embarassed theirself in this role', 'and is not worth writing home about']



haveWorkedOn = ['have worked together previously in', 'have appeared together before in', 'have worked together on']
asParticle = ['in the role of', 'as', 'plays the part of', 'is', 'has been cast as', 'is cast as', 'plays']
conj = ['where', 'in which']

posComparativeSentimentPhrases = ['in a much less memorable movie', 'in a far less competent movie']

negComparativeSentimentPhrases = ['in a much better movie than this']

####Intro Phrase Handling####
introPosDirectorSentimentPhrases = ['in the defining work of his career', 'as a true project of passion', 'and is probably his most striking work']
introNegDirectorSentimentPhrases = ['provides a poor effort', 'doesn\'t quite hit the mark', 'has seemingly turned up for the pay-cheque']




####Outro Phrase Handling####
posOutroFilmSentimentPhrases = ['delivers a unique experience', 'is a true classic', 'is worth coming to the cinema for', 'deserves your attention']
posOutroGenreSentimentPhrases = ['fans of the genre will love this', 'this is a truly great']
posOutroActorSentimentPhrases = ['carries this movie to greatness', 'really makes this movie worthwhile', 'is so watchable', 'gives a standout performance']
posOutroDirectorSentimentPhrases = ['has delivered', 'deserves recognition for this', 'has created a work of art']

negOutroFilmSentimentPhrases = ['is not worth watching', 'is ultimately a bit underwhelming', 'is not worth coming to the cinema for', 'could be left until it comes out online']
negOutroGenreSentimentPhrases = ['fans of the genre might enjoy this', 'you could probably watch this if you like any old']
negOutroActorSentimentPhrases = ['sells this movie short', 'really makes this movie hard to bare', 'is very hard to like', 'gives an underwhelming performance']
negOutroDirectorSentimentPhrases = ['has not delivered', 'is going to have to make up for this', 'has missed the mark']



print generateReview("Pulp Fiction")


