from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os,sys
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
basedir = os.path.abspath(os.path.dirname(__file__))

db_uri = 'sqlite:///' + os.path.join(basedir, 'test.db')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r %r>' % (self.username , self.email)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),
        nullable=False)
    category = db.relationship('Category',
        backref=db.backref('posts', lazy=True))

    user_id = db.Column(db.Integer , db.ForeignKey('user.id'),
        nullable=False)
    user = db.relationship('User' ,
        backref = db.backref('users'),lazy=True)

    def __init__(self, title, body, category, pub_date=None):
        self.title = title
        self.body = body
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date
        self.category = category

    def __repr__(self):
        return '<Post %r %r>' % (self.title,self.category)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % self.name

# run  only when the db is not created
def create_db():
    db.create_all()
    admin = User(username='admin', email='admin@example.com')
    guest = User(username='guest', email='guest@example.com')
    db.session.add(admin)
    db.session.add(guest)
    cat1 = Category('humor')
    cat2 = Category('action')
    db.session.add(cat1)
    db.session.add(cat2)
    # this writes to the DB file
    db.session.commit()
    print User.query.all()
    print User.query.filter_by(username='admin').first()
    print Category.query.all()
    print Category.query.filter_by(name='humor').first()

def test_rel_once():
    py = Category(name='Python')
    Post(title='Hello Python!', body='Python is pretty cool', category=py)
    p = Post(title='Snakes', body='Ssssssss')
    py.posts.append(p)
    db.session.add(py)


#test_db_create()
#test_rel_once()

def new_fn():
    print "new fn"