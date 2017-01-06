#importing needed modules
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired, Length
from alchemy import db
from alchemy import Package
import time

app = Flask(__name__) #Flask constructor takes the name app (__name__) as argument
app.secret_key = 'random string' #Secret key is needed in order to keep the client-side sessions secured

#The classes beneath contain the definition of textfields for each page of the app 
#Validators are imported from the wtf module and used in each textfield in order to set specific rules for each input
class FieldForm(FlaskForm):# Custom class inheritance FlaskForm as her constructor
   fnms = StringField('fnms', validators=[InputRequired('Provide Sender Name'),Length(min=3, max=30, message=None)])
   fnmr = StringField('fnmr', validators=[InputRequired('Provide Receiver Name'),Length(min=3, max=30, message=None)])
   address = StringField('address', validators=[InputRequired('Address is Required'),Length(min=3, max=20, message=None)])
   city = StringField('city', validators=[InputRequired('City Required'),Length(min=3, max=20, message=None)])
   pc = StringField('pc', validators=[InputRequired('Postal code Required'),Length(min=3, max=10, message=None)])
class idForm(FlaskForm):
   id = StringField('id', validators=[InputRequired('Id Required'),Length(min=1, max=5, message=None)])
class RadioForm(FlaskForm):
   radioform = StringField('radioform', validators=[InputRequired('Field Is Required'),Length(min=1, max=30, message=None)])



#Four fuctions for each page of the app
@app.route('/',methods = ['POST', 'GET'])#Route is a decorator in Flask and is used to bind a URL to a function
def home():	#Defining fuction with her name
	return render_template('Home.html')#The return tells jinja2 to render a certain html file

#POST method used to take the data from the forms of the URL
#Get method is used to send a request to server
@app.route('/NewPackage',methods = ['POST', 'GET'])
def newpackage():
	form = FieldForm()
	msg=None

	if request.method=='POST':
		if form.validate_on_submit():
			new_package=Package(sender_name=request.form['fnms'],rec_name=request.form['fnmr'],city=request.form['city'],address=request.form['address'],tk=request.form['pc'],rdate=time.strftime('%d/%m/%Y'))
			db.session.add(new_package)
			db.session.commit()
			msg='You successfully added a new entry'
	return render_template('NewPackage.html',msg=msg, form=form)#Rendering the scecified html file with jinja2 and defining its arguments
	
@app.route('/PackageSend',methods = ['POST', 'GET'])
def packagesend():
	form = idForm() 
	msg=None
	if request.method=='POST':
		if form.validate_on_submit():
			update_this=Package.query.filter_by(id=request.form['id']).first()
			if update_this:
				if update_this.sdate==None:
					update_this.sdate=time.strftime('%d/%m/%Y')
					db.session.commit()
					msg='Sent Date added to entry'
				else:
					msg='Package already sent'
			else:
				msg='Entry does not exist'
	return render_template('PackageSend.html',msg=msg, form=form)

@app.route('/Inventory',methods = ['POST', 'GET'])
def inventory():
	form = RadioForm()
	list=[]
	if request.method=='POST':
		if request.form["action"]=="Submit":
			if request.form['radio']=="0":
				list+=Package.query.all()
			elif request.form['radio']=="1":
				if form.validate_on_submit():
					list+=Package.query.filter_by(sender_name=request.form['radioform'])
			elif request.form['radio']=="2":
				if form.validate_on_submit():
					list+=Package.query.filter_by(rec_name=request.form['radioform'])
			elif request.form['radio']=="3":
				if form.validate_on_submit():
					list+=Package.query.filter_by(id=request.form['radioform'])
			if len(list)<1 and len(form.radioform.errors)<1:# Condition check if query returned empty and also there were no validator check fails
				form.radioform.errors=["No Entries"] #Force form.radioform.errors to be a list		
		else:
			for f in request.form.getlist('row'):
				Package.query.filter_by(id=f).delete()
				db.session.commit()
				list=Package.query.all()
	return render_template('Inventory.html',list=list,form=form)

	
if __name__ == '__main__':
   app.run(debug = True)
 
