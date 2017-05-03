class Clause:
    'Class to define a clause within a sentence'
    #for the case of a movie review I find that nearly every statement is declarative which helps to simplify the problem of defining a clause

    verb = ""
    obj = ""
    subject = ""
    adjective = ""
    adverb = ""

    def __init__(self, verb, obj="", subject="", adjective="", adverb=""):
        self.verb = verb
        self.subject = subject
        self.obj = obj
        self.adjective = adjective
        self.adverb = adverb

    def getContents(self):
        return self.verb, self.obj, self.subject, self.adjective, self.adverb



# clause = Clause(verb="was", subject="Tom Hardy", adjective = "good")
# subClause = Clause(verb = "as", subject = "Bane")
# verb, obj, subject, adjective, adverb = clause.getContents()
# print subject, verb, adjective

