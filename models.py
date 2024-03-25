
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()


def connect_db(app):
    """Connect database with flaskapp"""
    with app.app_context():
     db.app = app
     db.init_app(app)
     db.create_all()


class User(db.Model):
    """Create User"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    username= db.Column(
        db.String(20),
        nullable=False,
        unique=True,
    )

    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)



    @classmethod
    def register(cls, username, password, first_name, last_name, email):
        """Registering a user, hashing their password"""

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        user = cls(
            username=username,
            password=hashed_utf8,
            first_name=first_name,
            last_name=last_name,
            email=email
        )

        db.session.add(user)
        db.session.commit()
        return user
    
    @classmethod
    def authenticate(cls, username, password):
        """Validate if user exists and password is correct"""

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False
        

class Favorite(db.Model):
    """Favorited images for users"""
    
    __tablename__ = 'favorites'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    image_url = db.Column(db.String(200), nullable=False)

    # Relationship with User model
    user = db.relationship("User", backref="favorites")        
        