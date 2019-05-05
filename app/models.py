from werkzeug.security import generate_password_hash,check_password_hash
from . import login_manager
from datetime import datetime
from flask_login import UserMixin
from app import db


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    
class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True, index = True)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String()) 
    pass_secure = db.Column(db.String(255))
    providers = db.relationship('Providers',backref = 'author',lazy = 'dynamic') 

    @property
    def password(self):
        raise AttributeError("You can't read the password attribute")

    @password.setter
    def password(self,password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)

    def save_user(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'User{self.username}'

class Providers(db.Model):
    __tablename__='providers'

    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.String(2550))
    date_posted = db.Column(db.DateTime, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    reviews = db.relationship('Reviews', backref = 'author', lazy = True) 

    def save_provider(self):
        db.session.add(self)
        db.session.commit()
    

    def __repr__(self):
        return f'Providers{self.title}'


class Reviews(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer,primary_key = True)
    review = db.Column(db.String(255))
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    provider_id = db.Column(db.Integer,  db.ForeignKey("providers.id"))

    def save_review(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'Review{self.review}'


    @classmethod
    def get_reviews(cls,id):
        reviews = Review.query.filter_by(providers_id=id).all()
        return reviews
        
    @classmethod
    def clear_reviews(cls):
        Review.all_reviews.clear()

    @classmethod
    def get_reviews(cls,id):

        response = []


        for review in cls.all_reviews:
            if review.provider_id == id:
                response.append(review)

        return response

class Caterers(db.Model):
    __tablename__='caterers'

    id = db.Column(db.Integer,primary_key=True)
    location = db.Column(db.String(255))
    company = db.Column(db.String(255))
    service = db.Column(db.String(2550))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    reviews_id = db.Column(db.Integer,db.ForeignKey('reviews.id')) 

    def save_caterer(self):
        db.session.add(self)
        db.session.commit()
    

    def __repr__(self):
        return f'Caterers({self.company},{self.service})'

class Grounds(db.Model):
    __tablename__='grounds'

    id = db.Column(db.Integer,primary_key=True)
    location = db.Column(db.String(255))
    company = db.Column(db.String(255))
    service = db.Column(db.String(2550))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    reviews_id = db.Column(db.Integer,db.ForeignKey('reviews.id')) 

    def save_ground(self):
        db.session.add(self)
        db.session.commit()
    

    def __repr__(self):
        return f'Grounds({self.company},{self.service})'

class Cars(db.Model):
    __tablename__='cars'

    id = db.Column(db.Integer,primary_key=True)
    location = db.Column(db.String(255))
    company = db.Column(db.String(255))
    service = db.Column(db.String(2550))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    reviews_id = db.Column(db.Integer,db.ForeignKey('reviews.id'))
    

    def save_car(self):
        db.session.add(self)
        db.session.commit()
    

    def __repr__(self):
        return f'Cars({self.company},{self.service})'

class Photography(db.Model):
    __tablename__='photography'

    id = db.Column(db.Integer,primary_key=True)
    location = db.Column(db.String)
    company = db.Column(db.String(255))
    service = db.Column(db.String(2550))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    reviews_id = db.Column(db.Integer,db.ForeignKey('reviews.id')) 

    def save_photograph(self):
        db.session.add(self)
        db.session.commit()
    

    def __repr__(self):
        return f'Photography({self.company},{self.service})'

class Tents(db.Model):
    __tablename__='tents'

    id = db.Column(db.Integer,primary_key=True)
    location = db.Column(db.String)
    company = db.Column(db.String(255))
    service = db.Column(db.String(2550))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    reviews_id = db.Column(db.Integer,db.ForeignKey('reviews.id')) 

    def save_tent(self):
        db.session.add(self)
        db.session.commit()
    

    def __repr__(self):
        return f'Tents({self.company},{self.service})'

class Songs(db.Model):
    __tablename__='songs'

    id = db.Column(db.Integer,primary_key=True)
    location = db.Column(db.String)
    company = db.Column(db.String(255))
    service = db.Column(db.String(2550))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    reviews_id = db.Column(db.Integer,db.ForeignKey('reviews.id')) 
    providers = db.Column(db.Integer,db.ForeignKey('providers.id'))
    # providers = db.relationship('Providers',backref = 'author',lazy = 'dynamic') 

    def save_song(self):
        db.session.add(self)
        db.session.commit()
    

    def __repr__(self):
        return f'Songs({self.company},{self.service})'


