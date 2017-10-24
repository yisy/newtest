#-*- encoding=UTF-8 -*-
from newtest import db,login_manager
from datetime import datetime

class Comment(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    content = db.Column(db.String(1024))
    image_id = db.Column(db.Integer,db.ForeignKey('image.id'))
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    status = db.Column(db.Integer)

    def __init__(self,content,image_id,user_id,status):
        self.content = content
        self.image_id = image_id
        self.user_id = user_id
        self.status = status

    def __repr(self):
        return '<Comment %d %s %d %d %d >' %(self.id, self.content,self.image_id,self.user_id,self.status)

class Image(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_id  = db.Column(db.Integer,db.ForeignKey('user.id'))
    url = db.Column(db.String(70))
    created_time = db.Column(db.DateTime)
    comments = db.relationship('Comment')

    def __init__(self,url,user_id):
        self.user_id = user_id 
        self.url = url
        self.created_time = datetime.now()

    def __repr__(self):
        return '<Image %d %d %s %s >' %(self.id, self.user_id, self.url, self.created_time)


class User(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(20),unique=True)
    password = db.Column(db.String(32))
    slat = db.Column(db.String(32))
    head_url = db.Column(db.String(170))
    images = db.relationship('Image',backref='user',lazy='dynamic')
    comments = db.relationship('Comment')

    def __init__(self,username,password,slat=''):
        self.username = username
        self.password = password
        self.head_url = 'http://www.baidu.com'
        self.slat = slat

    def __repr__(self):
        return '<User %d %s>' %(self.id, self.username)

   
    # @property
    def is_authenticated(self):
        return  True
    
    # @property
    def is_active(self):
        return True

    # @property
    def is_anonymous(self):
        return False

    # @property
    def get_id(self):
        return self.id

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
