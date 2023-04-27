from flask import Flask, render_template
from article_data import Articles
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = True

db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String())
    created_on = db.Column(db.Date, default=datetime.utcnow(), nullable=False)

    def __init__(self, title, description, created_on):
        self.title = title
        self.description = description
        self.created_on = created_on


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    username = db.Column(db.String(100))
    password = db.Column(db.String(30))
    registered_on = db.Column(db.Date, default=datetime.utcnow(), nullable=False)

    def __init__(self, name, email, username, password, registered_on):
        self.name = name
        self.email = email
        self.username = username
        self.password = password
        self.registered_on = registered_on


with app.app_context():
    db.create_all()

Articles = Articles()


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route('/articles')
def articles():
    return render_template('articles.html', articles=Articles)


@app.route('/article/<string:id>/')
def display_article(id):
    return render_template('article.html', id=id)


if __name__ == "__main__":
    app.run(debug=True)
