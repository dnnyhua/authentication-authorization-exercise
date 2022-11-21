from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """ Connect this database to provided Flask app. """

    db.app = app
    db.init_app(app)


class User(db.Model):

    __tablename__ = 'users'

    username = db.Column(db.String(20), primary_key=True, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    # cascade all,delete so that when the user is deleted all of the feedbacks are deleted too
    feedback = db.relationship('Feedback', backref='users', cascade="all,delete")
    


    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(password)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        # return instance of user w/username and hashed pwd
        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)
    # end_register


    # start_authenticate
    @classmethod
    def authenticate(cls, username, pwd):
        """ 
        Validate that user exists & password is correct.
        Return user if valid; else return False.

        """

        # Get user based on username
        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            return u
        
        else: 
            return False
    
    # end_authenticate


class Feedback(db.Model):

    __tablename__ = 'feedbacks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(20), db.ForeignKey('users.username'), nullable=False)

    



        