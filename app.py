from forms import AnalystForm, LogInForm
from flask import Flask, render_template, redirect, url_for, request
from flask_pymongo import PyMongo


import sys
reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)
app._static_folder = "static"

app.config['MONGO_DBNAME'] = 'ccs'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/ccs'
app.config.update(dict(SECRET_KEY="powerful secretkey", WTF_CSRF_SECRET_KEY="a csrf secret key"))

mongo = PyMongo(app)

@app.route('/')
def index():
	'''
	log in page
	'''
	return render_template('index.html')

@app.route('/admin',methods=['GET','POST'])
def adminPage():
	'''
	1. Number of logins/ users. 
	2. Number of requests.
	3. Data spread across clusters.
	'''
	form = LogInForm()

	if request.method == 'POST':
		#a very secure set of credentials
		num_users = 10
		#for each user
		num_log_in = [10, 10, 10] 
		num_request = 10
		num_clusters = 2
		return render_template('admin.html',num_users=num_users, num_log_in=num_log_in,num_request=num_request,num_clusters=num_clusters)

	else:
		return render_template('admin.html',form=form)

	return render_template('admin.html',form=form)

@app.route('/user',methods=['GET','POST'])
def userPage():
	'''
	1. Annual consumption.
	2. Average time between two fill-ups.
	3. Details of last fill-up. (date & location)
	'''
	form = LogInForm()

	if request.method == 'POST':
		annual_consumption = 10 
		frequency = 10  
		last_trans = 10
		return render_template('client.html',annual=annual_consumption,frequency=frequency,last_trans=last_trans)
	return render_template('client.html',form=form)

@app.route('/analyst',methods=['GET','POST'])
def analystPage():
	'''
	Check the gas station most frequented so far.
	Number of users per gasstation today/ another day.
	'''
	form1 = LogInForm()

	if request.method == 'POST':
		form2 = AnalystForm()
		most_visited = 'X Street'
		num_visitors = 10 
		return render_template('analyst.html',most_visited=most_visited, num_visitors=num_visitors)
	return render_template('analyst.html',form=form1)

if __name__ == '__main__':
   app.run(debug = True)