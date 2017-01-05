from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import TextField
from wtforms.validators import InputRequired
from alchemy import db
from alchemy import Package
import time
app = Flask(__name__)
app.secret_key = 'random string'

class FieldForm(FlaskForm):#All the form in this class with FlaskForm as constructor
   fnms = TextField('fnms', validators=[InputRequired('Provide Sender Name')])
   fnmr = TextField('fnmr', validators=[InputRequired('Provide Receiver Name')])
   address = TextField('address', validators=[InputRequired('Address is Required')])
   city = TextField('city', validators=[InputRequired('City Required')])
   pc = TextField('pc', validators=[InputRequired('Postal code Required')])
class idForm(FlaskForm):
   id = TextField('id', validators=[InputRequired('Id Required')])
class RadioForm(FlaskForm):
   radioform = TextField('radioform', validators=[InputRequired('Field Is Required')])


@app.route('/',methods = ['POST', 'GET'])
def home():	
	return render_template('Home.html')
   
@app.route('/NewPackage',methods = ['POST', 'GET'])
def newpackage():
	form = FieldForm()#form variable 
	msg=None

	if request.method=='POST':
		if form.validate_on_submit():
			new_package=Package(sender_name=request.form['fnms'],rec_name=request.form['fnmr'],city=request.form['city'],address=request.form['address'],tk=request.form['pc'],rdate=time.strftime('%d/%m/%Y'))
			db.session.add(new_package)
			db.session.commit()
			msg='You successfully added a new entry'
	return render_template('NewPackage.html',msg=msg, form=form)#define form
	
@app.route('/PackageSend',methods = ['POST', 'GET'])
def packagesend():
	form = idForm()#form variable 
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
	return render_template('PackageSend.html',msg=msg, form=form)#define form

@app.route('/Inventory',methods = ['POST', 'GET'])
def inventory():
	form = RadioForm()#form variable 
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
			if len(list)<1 and len(form.radioform.errors)<1:
				form.radioform.errors.append("No entry")		
		else:
			for f in request.form.getlist('row'):
				Package.query.filter_by(id=f).delete()
				db.session.commit()
				list=Package.query.all()
	return render_template('Inventory.html',list=list,form=form)#define form	

	
if __name__ == '__main__':
   app.run(debug = True)
 
