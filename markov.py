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
    
    def __repr__(self)::
        if (len(self.solution)) == 0:
            self.make()
        output = self.solution[0].word2
        for ind in range(0, len(self.solution)-1):
            output += self.solution[ind].nextWord
    
    def make(self):
        #TODO refactor from local/markov
    
    def makeFromLog(self):
        #TODO
    
    def makeIntoLog(self):
        #TODO
        
    def trace(self):
        #TODO helper function for makeIntoLog

def markov():
    #spits out a chain
    chain = Chain()
    chain.make()
    return chain