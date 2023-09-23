# import SQLAlchemy
import email
from operator import sub
from pickle import FALSE
from tkinter.messagebox import ABORT
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from werkzeug import security
from flask_login import LoginManager, login_user, current_user, logout_user, login_required, UserMixin
# create the Flask app
from flask import Flask, render_template, request , redirect, url_for,flash, jsonify 
from markupsafe import escape

app = Flask(__name__)

# select the database filename
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///splitnator.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = '123'

# set up a 'model' for the data you want to store
from db_schema import db, User, Bill,GroupBill, Friend,Group,user_group, dbinit

# init the database so it can connect with our app
db.init_app(app)

# change this to False to avoid resetting the database every time this app is restarted
resetdb = True
if resetdb:
    with app.app_context():
        # drop everything, create all the tables, then put some data into the tables
        db.drop_all()
        db.create_all()
        dbinit()

login_manager= LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    if current_user.is_authenticated:
        newbills=Bill.query.filter_by(user_id=current_user.id, isNew=True)
        return render_template('index.html')
    return redirect('/login')

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return render_template('index.html')
    if request.method=='POST':
        email=escape(request.form['email'])
        password=escape(request.form['password'])
        user= User.query.filter_by(email=email).first()
        if user is None:
            return "<p>User doesn't exist<p>"
        if not security.check_password_hash(user.password, password):
            return "<p>Password is wrong<p>"
        login_user(user)
        return "ok"
    if request.method=="GET":
        return render_template("login.html")

@app.route('/newbills', methods=['GET','POST'])
@login_required
def newbills():
    bills=Bill.query.filter_by(user_id=current_user.id, isNew=True).first()
    if bills is None:
        return "no"
    return "<p>You have new bills<p>"

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect('/')
    if request.method=='GET':
        return render_template('register.html')
    if request.method=='POST':
        username= escape(request.form['username'])
        email= escape(request.form['email'])
        password= escape(request.form['password'])
        newuser=User(username=username, email=email, password=security.generate_password_hash(password))
        db.session.add(newuser)
        db.session.commit()
        return redirect('/login')
    
@app.route('/bills', methods=['GET','POST'])
@login_required
def bills():
    bills=[]
    userbills= Bill.query.filter_by(user_id=current_user.id).all()
    return render_template("showbills.html", bills=userbills)

@app.route('/addbill', methods=['GET','POST'])
@login_required
def addbill():
    if request.method=='POST':
        name=escape(request.form['billname'])
        amount=escape(request.form['amount'])
        groupbill=GroupBill.query.filter_by(name=name,authorID=current_user.id).first()
        if groupbill is None:
            newgroupbill= GroupBill(name=name,amount=amount,currentID=current_user.id)
            db.session.add(newgroupbill)
            db.session.commit()
            groupbill=GroupBill.query.filter_by(name=name,amount=amount,authorID=current_user.id).first()
            if groupbill is None:
                return "fail2"
            return str(groupbill.id)
        return "fail1"
    if request.method=='GET':
        groups=current_user.following
        return render_template('addbill.html',groups=groups)
    
       
@app.route('/friends', methods=['GET','POST'])
@login_required
def friends():
    friends= Friend.query.filter_by(user_id=current_user.id)
    return render_template("showfriends.html", friends=friends)

@app.route('/addfriend', methods=['GET','POST'])
@login_required
def addfriend():
    if not current_user.is_authenticated:
        return redirect('/')
    if request.method=='POST':
        email=escape(request.form['email'])
        if email is None:
            return redirect ('/addfriend')
        user= User.query.filter_by(email=email).first()
        if user is None:
            return redirect('/addfriend')
        newFriend= Friend(username=user.username,email=email, user_id=current_user.id)
        db.session.add(newFriend)
        db.session.commit()
        return redirect('/friends')
    if request.method=='GET':
        return render_template('addfriend.html')

@app.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/addgroup_tobill', methods=['GET','POST'])
@login_required
def addgroup_tobill():
    if request.method=='POST':
        group_id=escape(request.form['group_id'])
        groupbill_id=escape(request.form['bill_id'])
        group=Group.query.filter_by(id=group_id).first()
        users=group.followers
        if users is None:
            return "Group is empty"
        groupbill=GroupBill.query.filter_by(id=groupbill_id).first()
        newamount=groupbill.amount/len(users)
        for entry in users:
            newBill=Bill(name=groupbill.name, user_id=entry.id,groupbill_id=groupbill.id, group_id=group_id, amount=newamount) 
            db.session.add(newBill)
            db.session.commit()
        return ("ok");
         
@app.route('/paybill', methods=['GET','POST'])
@login_required
def paybill():    
     groupbill_id=request.args.get('groupbill_id')
     #The logged in user can only pay their bills, and noone else's
     bill=Bill.query.filter_by(groupbill_id=groupbill_id,user_id=current_user.id).first()
     if bill is None:
         return redirect('/bills')
     if bill.isPaid==False:
        bill.isPaid=True
        db.session.commit()
        groupbill=GroupBill.query.filter_by(id=groupbill_id).first()
        groupbill.balance-=bill.amount
        db.session.commit()
        bill.amount=0
        db.session.commit()
        return redirect('/bills')
     if bill.isPaid==True:
        return redirect('/bills')
        
@app.route('/pendingbills', methods=['GET','POST'])
@login_required
def pendingbills():
    bills= Bill.query.filter_by(user_id=current_user.id, isPaid=False)
    return render_template("showbills.html", bills=bills)

@app.route('/billdetails', methods=['GET','POST'])
@login_required
def billdetails():
    if request.method=='GET':
        userspaid=[]
        users_not_paid=[]
        groupbill_id=int(escape(request.args.get('groupbill_id')))
        bill=Bill.query.filter_by(user_id=current_user.id, groupbill_id=groupbill_id).first()
        #In case a user tries to access bills details that is not included
        if bill is None:
            return('/')
        #mark that the users has seen this bill at least once
        if bill.isNew==True:
            bill.isNew=False
            db.session.commit()
        groupbill=GroupBill.query.filter_by(id=groupbill_id).first()
        bills=Bill.query.filter_by(groupbill_id=groupbill_id).all()
        creator=User.query.filter_by(id=groupbill.authorID).first()
        return render_template("billdetails.html",bill=bill,bills=bills,groupbill=groupbill,creator=creator)
    return redirect('/')

@app.route('/billstatus', methods=['GET','POST'])
@login_required
def billstatus():
     if request.method=='GET':
            userspaid=[]
            users_not_paid=[]
            groupbill_id=int(escape(request.args.get('groupbill_id')))
            groupbill=GroupBill.query.filter_by(id=groupbill_id).first()
            groupbill_name=groupbill.name
            bill=Bill.query.filter_by(groupbill_id=groupbill_id).first()
            group=Group.query.filter_by(id=bill.group_id).first()
            users=group.followers
            for i in users:
                if Bill.query.filter_by(groupbill_id=groupbill_id,user_id=i.id).first().isPaid==True:
                    userspaid.append(i)
                else:
                    users_not_paid.append(i)
            return render_template("billstatus.html",users=users,users_not_paid=users_not_paid,userspaid=userspaid,groupbill_name=groupbill_name)
        
@app.route('/groups', methods=['GET','POST'])
@login_required
def groups():
    if  request.method=='GET':
        user=User.query.filter_by(id=current_user.id).first()
        groups=user.following
    return render_template("showgroups.html",groups=groups)

@app.route('/viewgroup', methods=['GET','POST'])
@login_required
def viewgroup():
    if request.method=='GET':
        group_id=escape(request.args.get('group_id'))
        group=Group.query.filter_by(id=group_id).first()
        users=group.followers
        return render_template("showgroup.html", group=group,users=users)
    return redirect('/')
        
@app.route('/addgroup', methods=['GET','POST'])
@login_required
def addgroup():
    if request.method=='POST':
        name=escape(request.form['name'])
        newgroup=Group(name=name)
        exists=Group.query.filter_by(name=name).first()
        if exists is None:
            db.session.add(newgroup)
            db.session.commit()
            group=Group.query.filter_by(name=name).first()
            user=User.query.filter_by(id=current_user.id).first()
            user.following.append(group)
            db.session.commit()
            return str(group.id)
        return "Group name already exist. Try new one!"
    if request.method=='GET':
        friends=Friend.query.filter_by(user_id=current_user.id).all()
        return render_template("addgroup.html",friends=friends)

@app.route('/addgroup_members', methods=['GET','POST'])
@login_required
def addgroup_members():
    if request.method=='POST':
        group_id=escape(request.form['group_id'])
        friend_email=escape(request.form['user_email'])
        user=User.query.filter_by(email=friend_email).first()
        group=Group.query.filter_by(id=group_id).first()
        user.following.append(group)
        db.session.commit()
        return "User Added Successfully!" 
           
@app.route('/remove_members', methods=['GET','POST'])
@login_required
def remove_members():
    if request.method=='POST':
        group_id=escape(request.form['group_id'])
        friend_email=escape(request.form['user_email'])
        user=User.query.filter_by(email=friend_email).first()
        group=Group.query.filter_by(id=group_id).first()
        user.following.remove(group)
        db.session.commit()
        return "User Removed Successfully!"

