from forms import AnalystForm, LogInForm
from flask import Flask, render_template, redirect, url_for, request
from flask_pymongo import PyMongo
from bson.code import Code
from bson.son import SON



import sys
reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)
app._static_folder = "static"

app.config['MONGO_DBNAME'] = 'ccs'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/ccs'
app.config.update(dict(SECRET_KEY="powerful secretkey", WTF_CSRF_SECRET_KEY="a csrf secret key"))

mongo = PyMongo(app)

login_count_u = 0
login_count_a = 0
login_count_b = 0
request_count = 0

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
	global login_count_u
	global login_count_a
	global login_count_b 
	global request_count
	if request.method == 'POST':
		login_count_a += 1
		request_count += 1
		#a very secure set of credentials
		num_users = 3
		#for each user
		num_log_in = [login_count_a, login_count_b, login_count_u] 
		num_request = request_count
		return render_template('admin.html',num_users=num_users, num_log_in=num_log_in,num_request=num_request)

	else:
		return render_template('admin.html',form=form)

	return render_template('admin.html',form=form)

@app.route('/user',methods=['GET','POST'])
def userPage():
	'''
	1. Number of proucts purchased.
	2. Average time between two fill-ups.
	3. Details of last fill-up. (date & location)
	'''
	form = LogInForm()
	global login_count_u
	global request_count

	#ccs = mongo.db.ccs

	if request.method == 'POST':
		login_count_u += 1
		request_count +=3 
		
		annual_consumption = 10 
		pipeline1 = [{"$group":{"_id":"$Product.Description", "nb":{"$sum": 1}}},{"$group":{"_id":"null", "nb":{"$sum": 1}}}]
		annual_consumption = mongo.db.command('aggregate','ccs',pipeline=pipeline1,explain=False)
		annual_consumption = annual_consumption["result"][0]["nb"]

		#frequency = 10  
		
		pipeline3 = [{"$match":{"Customer.ID":"31543"}},
			{"$sort":{"Date":-1,"Time":-1}},
			{"$limit":1},
			{"$project":{"Customer.ID":1,"Date":1,"Time":1,"GasStation.Country":1}}]
		#last_trans = str(ccs.aggregate(pipeline))
		last_trans = (mongo.db.command('aggregate', 'ccs', pipeline=pipeline3,explain=False))

		return render_template('client.html',annual=annual_consumption,last_trans=last_trans['result'][0]['Date'])
	return render_template('client.html',form=form)

@app.route('/analyst',methods=['GET','POST'])
def analystPage():
	'''
	Check the gas station most frequented so far.
	Number of users per gasstation today/ another day.
	'''
	form1 = LogInForm()
	global login_count_b
	global request_count

	if request.method == 'POST':

		login_count_b += 1
		request_count +=2
		return render_template('analyst.html',view="True")

	return render_template('analyst.html',form=form1)

@app.route('/analystAgain',methods=['GET','POST'])
def analystQuery():
	form = AnalystForm()
	# #most_visited = 'X Street'
	pipeline1 =[{"$group":{"_id":"$GasStation.ID","nb":{"$sum":1}}},{"$sort":{"nb":-1}}]
	most_visited = mongo.db.command('aggregate','ccs',pipeline=pipeline1,explain=False)
	most_visited = most_visited['result'][0]['nb']

	if request.method == 'POST':
		#print "Getting..."
		pipeline1 =[{"$group":{"_id":"$GasStation.ID","nb":{"$sum":1}}},{"$sort":{"nb":-1}}]
		most_visit = mongo.db.command('aggregate','ccs',pipeline=pipeline1,explain=False)
		most_visited = most_visit['result'][0]['_id']
		most_visits = most_visit['result'][0]['nb']

		#gs_id = str(request.form['GasStationID'])
		gs_id = 448 

		mapf = Code('''
		function(){
    	Id=this.GasStation.ChainID;
    	emit(Id,{"avg":this.Price,"sum":this.Price,"nb":1});
		};
		''')
		reducef = Code('''
		function(key,values){
		    sum=0;
		    nb=0;
		    for(i=0;i<values.length;i++){
		        sum+=values[i].sum;
		        nb +=values[i].nb;
		    }
		    return {"avg":sum/nb,"sum":sum,"nb":nb};
		};
		''')

		results_id = []
		results_val = []

		resultsf = mongo.db.ccs.map_reduce(map=mapf, reduce=reducef, out=SON([('inline',1)]))
		# for i in range(len(resultsf['results'])):
		# 	results.append(resultsf['results'][i]['_id'])
		# 	results_val.append(resultsf['results'][i]['value']['sum'])
		# 	if i == 10:
		# 		break
		print (resultsf['results'])
		
		pipeline2 = [{"$match":{"GasStation.ID":"448"}}, {"$group":{"_id":"$Customer.ID"}}, {"$group":{"_id":None,"nb":{"$sum":1}}}]
		num_visited = mongo.db.command('aggregate','ccs',pipeline=pipeline2,explain=False)
		num_visited = num_visited['result'][0]['nb']

	 	return render_template('analyst2.html',most_visited=most_visited,most_visits=most_visits, num_visitors=num_visited,gs_id=gs_id)
	return render_template('analyst2.html',form=form,most_visited=most_visited)

if __name__ == '__main__':
   app.run(debug = True)