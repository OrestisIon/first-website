
import email
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from flask_login import UserMixin
# create the database interface
db = SQLAlchemy()

 
        
user_group= db.Table('user_group',
        db.Column('user_id',db.Integer, db.ForeignKey('users.id')),
        db.Column('group_id', db.Integer, db.ForeignKey('groups.id'))  
)       
# a model of a user for the database
class User(UserMixin, db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(20), unique=False, nullable=False)
    password = db.Column(db.String(60), unique=False, nullable=False)
    friends= db.relationship('Friend', backref='author', lazy=True)
    following = db.relationship('Group', secondary=user_group, backref='followers')
    def __init__(self, username,email, password):
        self.username=username
        self.email=email
        self.password=password
        
class Group(db.Model):
    __tablename__='groups'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.Text(),unique=True)
    def __init__(self,name):
        self.name=name 

    
class GroupBill(db.Model):
    __tablename__='groupbills'
    id=db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())
    amount=db.Column(db.Float, unique=False, nullable=False)
    balance=db.Column(db.Float, unique=False, nullable=False)
    authorID=db.Column(db.Integer, unique=False, nullable=False)
    user_counter=db.Column(db.Integer, unique=False, nullable=False)
    bills= db.relationship('Bill', backref='main', lazy=True)    
    
    def __init__(self, name,amount,currentID):
        self.name=name
        self.amount=amount
        self.balance=amount
        self.user_counter=1
        self.authorID=currentID
# a model of a list for the database
# it refers to a user
class Bill(db.Model):
    __tablename__='bills'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())
    amount=db.Column(db.Float, unique=False, nullable=False)
    isPaid=db.Column(db.Boolean, unique=False, nullable=False)
    isNew=db.Column(db.Boolean, unique=False, nullable=False)
    user_id = db.Column(db.Integer,unique=False, nullable=False)
    group_id=db.Column(db.Integer,unique=False, nullable=False)
    groupbill_id=db.Column(db.Integer, db.ForeignKey('groupbills.id'))  # this ought to be a "foreign key"
    
    def __init__(self, name, user_id,groupbill_id,group_id,amount):
        self.name=name
        self.user_id = user_id
        self.group_id=group_id
        self.isPaid=False
        self.amount=amount
        self.groupbill_id=groupbill_id
        self.isNew=True
        

class Friend(db.Model):
    __tablename__='friends'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(20), unique=False, nullable=False)
    username=db.Column(db.String(20), unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # this ought to be a "foreign key"
    
    def __init__(self,username, email, user_id):
        self.username=username
        self.email=email
        self.user_id = user_id
        
def dbinit():
    user_list = [
        User(username="Felicia",email="felicia@gmail.com" ,password=generate_password_hash("1234")),
        User(username="Maria",email="maria@gmail.com", password=generate_password_hash("1234" )),
        User(username="George",email="george@gmail.com", password=generate_password_hash("1234" )),
        User(username="Orestis",email="1@gmail.com" ,password=generate_password_hash("1234")),
        User(username="Nicos",email="2@gmail.com", password=generate_password_hash("1234" )),
        User(username="Mary",email="3@gmail.com", password=generate_password_hash("1234" )),
        User(username="Liza",email="4@gmail.com" ,password=generate_password_hash("1234")),
        User(username="Daniel",email="5@gmail.com", password=generate_password_hash("1234" )),
        User(username="Marios",email="6@gmail.com", password=generate_password_hash("1234" )),
        User(username="Polis",email="7@gmail.com" ,password=generate_password_hash("1234")),
        User(username="Giota",email="8@gmail.com", password=generate_password_hash("1234" )),
        User(username="John",email="9@gmail.com", password=generate_password_hash("1234" ))
        ]
    db.session.add_all(user_list)
    db.session.commit()

    # find the id of the user Felicia
    felicia_id = User.query.filter_by(email="felicia@gmail.com").first().id
    george_id = User.query.filter_by(email="george@gmail.com").first().id

    all_friends = [
        Friend("George","george@gmail.com",felicia_id),
        Friend(username="Felicia",email="felicia@gmail.com",user_id=george_id),
        Friend("Polis","7@gmail.com",2),
        Friend("Polis","7@gmail.com",3),
        Friend("Polis","7@gmail.com",4),
        Friend("Polis","7@gmail.com",5),
        Friend("Polis","7@gmail.com",6),
        Friend("Nicos","2@gmail.com",2),
        Friend("Nicos","2@gmail.com",3),
        Friend("Nicos","2@gmail.com",4),
        Friend("Nicos","2@gmail.com",5),
        Friend("Nicos","2@gmail.com",6),
        ]
    db.session.add_all(all_friends)
    # commit all the changes to the database file
    db.session.commit()
    zgroup=Group("ZGROUP")
    db.session.add(zgroup)
    all_groups = [
        Group('AGROUP'),
        Group('Dimotiko'),
        Group('Warwick'),
        Group('Egroup')
        ]
    db.session.add_all(all_groups)
    db.session.commit()
    zgroup=Group.query.filter_by(name="ZGROUP").first()
    groupa=Group.query.filter_by(name="AGROUP").first()
    nicos=User.query.filter_by(id=1).first()
    user2=User.query.filter_by(id=2).first()
    user3=User.query.filter_by(id=3).first()
    user4=User.query.filter_by(id=4).first()
    user5=User.query.filter_by(id=5).first()
    nicos.following.append(zgroup)
    user2.following.append(zgroup)
    user5.following.append(zgroup)
    user5.following.append(groupa)
    user3.following.append(zgroup)
    user2.following.append(groupa)
    user2.following.append(zgroup)
    user4.following.append(groupa)
    nicos.following.append(groupa)
    db.session.commit()
    
    
    