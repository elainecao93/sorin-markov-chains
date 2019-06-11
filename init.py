from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
db = SQLAlchemy(app)

class Log(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nonce = db.Column(db.String(20))
    created_at = db.Column(db.String(50))
    links = db.Column(db.String(200))
    

class CardSource(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    card = db.Column(db.String(100))
    cardSet = db.Column(db.String(100))
    #links = db.relationship("Link", backref="source")

    def __init__(self, card, cardSet):
        self.card = card
        self.cardSet = cardSet
    
    @staticmethod
    def getId(card, cardSet):
        source = CardSource.query.filter_by(card = card).filter_by(cardSet = cardSet).first()

        if not source:
            return 0
        return source.id

class Link(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    word1 = db.Column(db.String(50))
    word2 = db.Column(db.String(50))
    nextWord = db.Column(db.String(50))
    #source_id = db.Column(db.Integer, db.ForeignKey("CardSource.id"))
    source_id = db.Column(db.Integer)

    def __init__(self, word1, word2, nextWord, card, cardSet):
        self.word1 = word1
        self.word2 = word2
        self.nextWord = nextWord
        id = CardSource.getId(card, cardSet)
        if id == 0:
            newSource = CardSource(card, cardSet)
            db.session.add(newSource)
            id = newSource.id
        self.source_id = id
    
    def __repr__(self):
        output = ""
        output += self.word1 + " "
        output += self.word2 + " "
        output += self.nextWord + " "
        return output

def main():
    #Testcases
    db.drop_all()
    db.create_all()
    db.session.commit()

    newLink = Link("a", "b", "c", "1", "2")
    db.session.add(newLink)
    db.session.commit()

    #TODO refactor scrape.py into this
    

if __name__ == "__main__":
    main()