from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import requests
import time

import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
db = SQLAlchemy(app)

class Log(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nonce = db.Column(db.String(20))
    created_at = db.Column(db.String(50))
    links = db.Column(db.String(4000))

    def __init__(self, nonce, created_at, links):
        self.nonce = nonce
        self.created_at = created_at
        self.links = links

class CardSource(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    card = db.Column(db.String(200))
    cardSet = db.Column(db.String(100))

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
    next_word = db.Column(db.String(50))
    source_id = db.Column(db.Integer)

    def __init__(self, word1, word2, next_word, cardId):
        self.word1 = word1
        self.word2 = word2
        self.next_word = next_word
        self.source_id = cardId
    
    def __repr__(self):
        output = ""
        output += self.word1 + " "
        output += self.word2 + " "
        output += self.next_word + " "
        return output

def main():

    db.drop_all()
    db.session.commit()
    db.create_all()
    db.session.commit()

    db.drop(Link)
    db.drop(CardSource)
    db.session.commit()
    db.create_all()
    db.session.commit()

    pageNumber = 1
    while(True):
        URL = "https://api.scryfall.com/cards/?page=" + str(pageNumber)

        r = requests.get(url = URL)
        data = r.json()
        cards = data["data"]

        for card in cards:
            if card["lang"] == "en" and "flavor_text" in card:
                flavorText = "SOL " + card["flavor_text"] + " EOL"
                cardName = card["name"]
                cardSet = card["set_name"]

                #print(flavorText + " " + cardName + " " + cardSet)

                newCard = CardSource(cardName, cardSet)
                db.session.add(newCard)
                db.session.commit()

                words = flavorText.split(" ")
                eol = words.index("EOL")
                for i in range(0, eol-1):
                    key1 = words[i]
                    key2 = words[i+1]
                    word = words[i+2]
                    link = Link(key1, key2, word, newCard.id)
                    #print(key1 + " " + key2 + " " + word)
                    db.session.add(link)
                
                db.session.commit()
        pageNumber += 1
        if pageNumber%10 == 0:
            print(str(pageNumber) + " pages read")
        if not data["has_more"]:
            break
        
        time.sleep(1)
    

if __name__ == "__main__":
    main()