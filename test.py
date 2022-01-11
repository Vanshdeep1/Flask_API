"""
Here is the documentation of this code in which I am Using Flask Framework with Postgresql Database. In
this i am creating seven links as per the task asssign to me, So I demonstrate this as follow! 

How to run :
1) Download all dependent thing
2)run in  cmd  "python file_name"
3)
localhost:5000/
http://127.0.0.1:5000/
"""

"""
Import Library
pip install flask
pip install flask_sqlalchemy
pip install werkzeug.security
pandas

"""
from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd

"""
Create DataBase environment
"""
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="postgresql://postgres:vansh123@localhost/sampledb"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'thisissecret'
db=SQLAlchemy(app)

"""
Create a User Database for Login and Register by creating user table and using three arguments
ID, EMAIL, PASSWORD
"""
class User(db.Model):
    __tablename__='user'
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(40))
    password=db.Column(db.String(200))
    

    def __init__(self,email,password,):
        self.email=email
        self.password=password


"""
Create a Data Database for Saving the csv file by creating data table and using three arguments
ID, Firstname, lastname
"""
class Data(db.Model):
    __tablename__='data'
    id=db.Column(db.Integer,primary_key=True)
    firstname=db.Column(db.String(40), nullable=True)
    lastname=db.Column(db.String(40), nullable=True)

    def __init__(self,firstname,lastname):
        self.firstname=firstname
        self.lastname=lastname

@app.route('/')
def index():
    return { "mess": "Welcome"}

"""
For user registration

link: http://127.0.0.1:5000/register

Syntax: API TESTING
        {
    "username":"xxxxxxxxxxxx@gmail.com",
    "password":"xxxxxxx"
    }
"""

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=='POST':
        _json = request.json
        _username=_json['username']
        _password=_json['password']
        passhash = generate_password_hash(_password)
        user= User(_username,passhash)
        db.session.add(user)
        db.session.commit()
        return f" Register Successfully"
    else:
        return "ERROR"


"""
For Login

Link: http://127.0.0.1:5000/login

Syntax: API TESTING
        {
    "username":"xxxxxxxxxxxx@gmail.com",
    "password":"xxxxxxx"
    }
"""
@app.route('/login', methods=['POST'])
def login():
    if request.method=='POST':
        _json = request.json
        _username = _json['username']
        _password = _json['password']
        # validate the received values
        if _username and _password:
            #check user exists          
            user=User.query.filter_by(email=_username).first()
            if user:
                if check_password_hash(user.password, _password):
                    session['user'] = _username
                    return 'LOGIN Sucessfully'
                else:
                    return 'pass not same'
            else:
                return "user not found"
        else:
            return "NO Username and Password"

"""
For Logout

Link: http://127.0.0.1:5000/logout

"""
@app.route('/logout')
def logout():
    session.pop('user')
    return "SUccessfully logout"

"""
For Upload file

Link: http://127.0.0.1:5000/uploadfile

Syntax: API TESTING
        {
            "file": file location
    }
"""
@app.route('/uploadfile',methods=['POST'])
def upload():
    try:
        if session['user']:
            if request.method=="POST":
                file=request.files['file']
                df=pd.read_csv(file)
                list_=df.values.tolist()
                print(list_)
                s=db.session()
                try:
                    for i in list_:
                        record=Data(**{
                            'firstname': i[0],
                            'lastname':i[1]
                        })
                        s.add(record)
                    s.commit()
                    return "Upload sucessfully"
                except:
                    s.rollback()
                    return "NOT Uploaded"
                finally:
                    s.close()
    except:
        return "Session expired"

"""
A search API  to look through all the CSV data uploaded and return results.

Link: http://127.0.0.1:5000/search

Syntax: API TESTING
  {
    "firstname":"XYZ"
}
"""
@app.route('/search',methods=['POST'])
def search():
    try:
        if session['user']:
            if request.method=="POST":
                _json = request.json
                try:
                    _firstname = _json['firstname']
                except:
                    _lastname = _json['lastname']
                
                if _firstname:
                    user=Data.query.filter_by(firstname=_firstname).first()
                    data={
                        "firstname":user.firstname,
                        "lastname": user.lastname
                    }
                    return {"data":data}
                elif _lastname:
                    user=Data.query.filter_by(lastname=_lastname).first()
                    data={
                        "firstname":user.firstname,
                        "lastname": user.lastname
                    }
                    return {"data":data}
                else:
                    return "No Input found"

            else:
                return "Search Not working"

    except:
        return "Session expired"
    
"""
Show a list of data uploaded categorized by fields

Link: http://127.0.0.1:5000/list_of_data

Syntax: API TESTING
  {
}

"""
@app.route('/list_of_data', methods=['GET'])
def list_of_data():
    try:
        if session['user']:
            if request.method=="GET":
                user=Data.query.all()
                result=[]
                for i in user:
                    data={
                        "firstname":i.firstname,
                        "lastname":i.lastname
                    }
                    result.append(data)
                return {"DATA":result}
    except:
        return "Session expired"

"""
Delete files/data that match specific filter values.

Link: http://127.0.0.1:5000/delete

Syntax: API TESTING
      {
    "firstname":"n"
}


"""
@app.route('/delete', methods=['POST'])
def delete():
    try:
        if session['user']:
            if request.method=="POST":
                _json = request.json
                try:
                    _firstname = _json['firstname']
                except:
                    _lastname = _json['lastname']
                if _firstname:
                    stmt = Data.query.filter_by(firstname = _firstname).delete()
                    db.session.add(stmt)
                    return "Deleted successfully"
                elif _lastname:
                    stmt = Data.query.filter_by(firstname = _firstname).delete()
                    db.session.add(stmt)
                else:
                    return "unexpected input"
    
    except:
        return "Session expired"


if __name__ == "__main__":
    app.run(debug=True)