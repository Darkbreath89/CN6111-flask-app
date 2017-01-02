from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///erg.db'
db=SQLAlchemy(app)

class Package(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	sender_name=db.Column(db.String(30))
	rec_name=db.Column(db.String(30))
	city=db.Column(db.String(20))
	address=db.Column(db.String(20))
	tk=db.Column(db.String(10))
	rdate=db.Column(db.String(10))
	sdate=db.Column(db.String(10))