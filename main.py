from flask import Flask, render_template, request
from alchemy import db
from alchemy import Package
import time
app = Flask(__name__)
app.secret_key = 'random string'

@app.route('/',methods = ['POST', 'GET'])
def home():	
	return render_template('Home.html')
   
@app.route('/NewPackage',methods = ['POST', 'GET'])
def newpackage():
	msg=None
	if request.method=='POST':
		new_package=Package(sender_name=request.form['fnms'],rec_name=request.form['fnmr'],city=request.form['city'],address=request.form['address'],tk=request.form['pc'],rdate=time.strftime('%d/%m/%Y'))
		db.session.add(new_package)
		db.session.commit()
		msg='You successfully added a new entry'
	return render_template('NewPackage.html',msg=msg)
	
@app.route('/PackageSend',methods = ['POST', 'GET'])
def packagesend():
	msg=None
	if request.method=='POST':
		update_this=Package.query.filter_by(id=request.form['id']).first()
		if update_this:
			update_this.sdate=time.strftime('%d/%m/%Y')
			db.session.commit()
			msg='Sent Date added to entry'
		else:
			msg='Entry does not exist'
	return render_template('PackageSend.html',msg=msg)

@app.route('/Inventory',methods = ['POST', 'GET'])
def inventory():
	list=None
	if request.method=='POST':		
		if request.form['radio']=="0":
			list=Package.query.all()
		elif request.form['radio']=="1":
			list=Package.query.filter_by(sender_name=request.form['radioform'])
		elif request.form['radio']=="2":
			list=Package.query.filter_by(rec_name=request.form['radioform'])
		elif request.form['radio']=="3":
			list=Package.query.filter_by(id=request.form['radioform'])		
	return render_template('Inventory.html',list=list)	

	
if __name__ == '__main__':
   app.run(debug = True)
 