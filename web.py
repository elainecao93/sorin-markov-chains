from flask import Flask
from init import Link, Log, CardSource
from flask_sqlalchemy import SQLAlchemy
import os
import markov
import post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['DEBUG'] = True

db = SQLAlchemy(app)

@app.route("/")
def index():

    #Testcase
    output = "<p>" + str(markov.markov()) + "</p>"
    return output

@app.route("/i/love/bronson")
def postToTwitter():    
    chain = post.postFromWeb()
    return str(chain)

#TODO refactor post.py into this

if __name__ == "__main__":
    app.run()