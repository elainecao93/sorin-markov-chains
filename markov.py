from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import random
import requests
import string
import os
from init import Link, Log, CardSource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
db = SQLAlchemy(app)

class Chain():

    def __init__(self):
        self.solution = []
    
    def __repr__(self):
        if (len(self.solution)) == 0:
            self.make()
        output = self.solution[0].word2
        for ind in range(0, len(self.solution)-1):
            output += " " + self.solution[ind].next_word
        return output
    
    def make(self):
        self.solution = []
        possibleFirstElems = Link.query.filter_by(word1="SOL").all()
        firstElem = random.choice(possibleFirstElems)
        self.solution.append(firstElem)
        while (True):
            lastElem = self.solution[-1]
            possibleNextElems = Link.query.filter_by(word1=lastElem.word2, word2=lastElem.next_word).all()
            nextElem = random.choice(possibleNextElems)
            self.solution.append(nextElem)
            if nextElem.next_word == "EOL":
                break
        return None
    
    def makeFromLog(self, log):
        return None #TODO
    
    def makeIntoLog(self):
        return None #TODO
        
    def trace(self):
        output = ""
        first = True
        for elem in self.solution:
            if not first:
                output += "\n"
            first = False
            output += str(elem.id) + " " + str(elem.source_id)
        return output

def markov():
    #spits out a chain
    chain = Chain()
    chain.make()
    return chain