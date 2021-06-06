from Application import db, login_mang, app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as ser
from sqlalchemy import and_

@login_mang.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    #img = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    notes = db.relationship('Note', backref='author', lazy=True)
    tags = db.relationship('Tag', backref='author1', lazy=True)
    file = db.relationship('File', backref='author2', lazy=True)


    def get_reset_token(self,expires_sec=1800):
        s = ser(app.config['SECRET_KEY'], expires_sec)
        return s.dump({'user_id':self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = ser(app.config['SECRET_KEY'])
        try:
            user_id = s.load(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text, unique=False, nullable=True)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tags = db.relationship('TagNoteLink', backref='tags', lazy=True)
    path = db.Column(db.String(100), nullable=True)

    @staticmethod
    def getByTag(tag):

        try:
            ids = [n.note for n in TagNoteLink.query.filter_by(tag=Tag.query.filter_by(name=tag).first().name)]
        except:
            ids = []
        return db.session.query(Note).filter(Note.name.in_(ids))



class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    notes = db.relationship('TagNoteLink', backref='notes', lazy=True)

class TagNoteLink(db.Model):
    note = db.Column(db.Integer, db.ForeignKey('note.name'), nullable=False, primary_key=True)
    tag = db.Column(db.Integer, db.ForeignKey('tag.name'), nullable=False, primary_key=True)

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    path = db.Column(db.String(100), nullable=True)


