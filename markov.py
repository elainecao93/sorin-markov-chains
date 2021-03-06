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

MAX_TWEET_LENGTH = 280

class Chain():

    def __init__(self):
        self.solution = []
    
    def __repr__(self):
        if (len(self.solution)) == 0:
            self.make()
        output = ""
        first = True
        for elem in self.solution:
            if not first:
                output += " "
            first = False
            output += elem.word2
        if output.count("\"")%2==1:
            output += "\""
        return output
    
    def make(self, ensure_length = False):
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
        
        if ensure_length:
            length = 0
            for elem in self.solution:
                length += len(elem.word2) + 1
            if length > 280:
                return self.make()
        
        #check to see that its not just a copy
        orig_id = self.solution[0].source_id
        for elem in self.solution:
            if elem.source_id != orig_id:
                return None
        self.make()
    
    def makeFromLog(self, log):
        self.solution = []
        log = log.split("\n")
        for elem in log:
            link_id = elem.split(" ")[0]
            link = Link.query.filter_by(id=link_id).first()
            self.solution.append(link)

    def makeIntoLog(self):
        output = ""
        first = True
        for elem in self.solution:
            if not first:
                output += "\n"
            first = False
            output += str(elem.id) + " " + str(elem.source_id)
        return output
    
    def fullTrace(self):
        output = []
        for elem in self.solution:
            card_source = CardSource.query.filter_by(id=elem.source_id).first()
            output += (elem.word2, card_source.card, card_source.cardSet)
        return output

def markov(ensure_length = False):
    #spits out a chain
    chain = Chain()
    chain.make(ensure_length)
    return chain