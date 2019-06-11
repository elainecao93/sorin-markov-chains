from flask import Flask
from init import Link, Log, CardSource
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['DEBUG'] = True

db = SQLAlchemy(app)

@app.route("/")
def index():
    elem = Link.query.first()
    print(elem)
    print(type(elem))

if __name__ == "__main__":
    app.run()