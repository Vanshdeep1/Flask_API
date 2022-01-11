Library
{
pip install flask
pip install flask_sqlalchemy
pip install werkzeug.security
pip install pandas
}

SETUP DATABASE

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="postgresql://postgres:password@localhost/sampledb"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'thisissecret'
db=SQLAlchemy(app)

DATABASE 1
class User(db.Model):
    __tablename__='user'
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(40))
    password=db.Column(db.String(200))

DATABASE 2
class Data(db.Model):
    __tablename__='data'
    id=db.Column(db.Integer,primary_key=True)
    firstname=db.Column(db.String(40), nullable=True)
    lastname=db.Column(db.String(40), nullable=True)


API TESTING:

Register API:

            link: http://127.0.0.1:5000/register

            Syntax: 
                    {
                "username":"xxxxxxxxxxxx@gmail.com",
                "password":"xxxxxxx"
                }


Login API:

        Link: http://127.0.0.1:5000/login

        Syntax: API TESTING
                {
            "username":"xxxxxxxxxxxx@gmail.com",
            "password":"xxxxxxx"
            }


Logout:

        Link: http://127.0.0.1:5000/logout


Upload file:

        Link: http://127.0.0.1:5000/uploadfile

        Syntax:
            {
                "file": file location
        }