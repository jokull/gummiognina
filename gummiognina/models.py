# encoding=utf-8

import hashlib, datetime, itertools, locale

from flask import url_for

from gummiognina.classtools import cached_property
from gummiognina.extensions import db

locale.setlocale(locale.LC_ALL, "is_IS.UTF-8") # To print nice dates

class Person(db.Model):
    """
    `Person` entities that are real users have a person. 
    Person is the place to store logins.
    """
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.datetime.now)
    active = db.Column(db.Boolean, nullable=False, default=True, index=True)
    
    email = db.Column(db.String(250), index=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    
    instagram_access_token = db.Column(db.String, default='')
    instagram_id = db.Column(db.String, default='')
    name = db.Column(db.String(255))
    picture = db.Column(db.String)
    
    pins = db.relationship('Photo', backref="person", lazy='dynamic')
    
    def __init__(self, **kwargs):
        if not self.id and 'password' in kwargs:
            self.set_password(password)
        for key, value in kwargs.iteritems():
            setattr(self, key, value)
    
    def validate_password(self, password):
        """The given password is hashed and compared against the one
        stored in the database.  Returns True if they are equal, else
        False.
        """
        hashed_password = self._hash_password(password)
        return self.password == hashed_password and self.activated
    
    def set_password(self, raw_pass):
        """Set a new password for the account.  The raw password
        will be stored in hashed form and will not be reversible.
        """
        self.password = self._hash_password(raw_pass)

    def set_random_password(self, length=6, allowed_chars='abcdefghjkmnpqrstuvwxyz23456789'):
        "Generates a random password with the given length and given allowed_chars"
        # Note that default value of allowed_chars does not have "I" or letters
        # that look like it -- just to avoid confusion.
        from random import choice
        random_password = ''.join([choice(allowed_chars) for i in range(length)])
        self.set_password(random_password)
        return random_password

    def _hash_password(self, raw_pass):
        return hashlib.sha512(raw_pass).hexdigest()
    
    def get_picture_url(self):
        if self.picture:
            return self.picture
        return url_for('.static', 'images/emptyperson.png')
    
    @cached_property
    def json(self):
        return dict(id=self.id,
                    instagram_id=self.instagram_id,
                    name=self.name,
                    picture_url=self.get_picture_url(),
                    email=self.email)
    
    """
    Methods Flask-Login expects
    """
    
    def is_authenticated(self):
        return True
    
    def is_active(self):
        return self.active
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return unicode(self.id)
    
    def get_instagram(self):
        return Graph(self.instagram_access_token)
        
    @classmethod
    def create(cls, clean_data):
        
        instagram_access_token = clean_data.pop('instagram_access_token')
        person = cls(**dict(clean_data))
        person.instagram_access_token = instagram_access_token
        person.password = ""
        
        return person


class Photo(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.datetime.now)
    lat = db.Column(db.String, index=True)
    lng = db.Column(db.String, index=True)
    # person_id = db.Column(db.Integer, db.ForeignKey('person.id'), index=True)
    date = db.Column(db.Date, index=True)
    
    @cached_property
    def json(self):
        return dict(id=self.id, 
                    lat=self.lat,
                    lng=self.lng,
                    # person=self.person.json,
                    date=str(self.date),
                    date_locale=self.date.strftime(u'%d. %B %Y'))









