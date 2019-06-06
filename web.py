from flask import Flask

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/")
def index():
    return "Coming soon..."

if __name__ == "__main__":
    app.run()