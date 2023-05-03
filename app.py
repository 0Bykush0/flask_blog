from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = True
app.config['SECRET_KEY'] = 'secret_key'

db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String())
    created_on = db.Column(db.Date, default=datetime.utcnow(), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

    def __init__(self, title, description, user_id):
        self.title = title
        self.description = description
        self.user_id = user_id


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(30))
    registered_on = db.Column(db.Date, default=datetime.utcnow(), nullable=False)

    def __init__(self, name, email, username, password):
        self.name = name
        self.email = email
        self.username = username
        self.password = password


with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@app.route("/", methods=['POST', 'GET'])
def home():
    return render_template("home.html")


@app.route("/about", methods=['POST', 'GET'])
def about():
    if 'logged_in' in session and session['logged_in']:
        username = session['username']
        print(username)
        return render_template("about.html")
    else:
        return redirect('/login')


@app.route("/articles", methods=['POST', 'GET'])
@login_required
def articles():
    if 'logged_in' in session and session['logged_in']:
        username = session['username']
        user_id = session['user_id']
        projects = Article.query.filter(Article.user_id == user_id).all()
        print()
        return render_template("articles.html", username=username, projects=projects)


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        name = request.form.get('Full_Name')
        username = request.form.get('username')
        mail = request.form.get('email')
        password = request.form.get("password")
        user = Users(username=username, name=name, email=mail, password=password)
        db.session.add(user)
        db.session.commit()
        print(user, "Registered successfully")
        return redirect('/login')
    return render_template('register.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = Users.query.filter_by(username=request.form.get('username')).first()
        password = Users.query.filter_by(password=request.form.get('password')).first()
        if user:
            if password:
                login_user(user)
                print("login successful")
                session['username'] = user.username
                session['user_id'] = user.id
                session['logged_in'] = True
                return redirect('/articles')
            else:
                print("login failed, Wrong password")
        else:
            print("login failed, nonexistent user")
    return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)
