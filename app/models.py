
from . import db
from werkzeug.security import generate_password_hash
from datetime import datetime
class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80))
    password = db.Column(db.String(128))


    def __init__(self, email, password):
        self.email = email
        self.password = generate_password_hash(password, method='pbkdf2:sha256')
        
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicodedata(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<User %r>' % (self.username)
    

class Book(db.Model):
    __tablename__ = 'book'
    bookid = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255))
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%A %b %d, %Y")
    dateuploaded = db.Column(db.String(255), default=formatted_datetime)

    def __init__(self, filename):
        self.filename = filename

    def __repr__(self):
        return '<Book %r>' % self.filename