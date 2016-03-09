from flask import *
import flask, redis, time, json, numpy

app = flask.Flask("President")

#set up redis connections
pool_trump = redis.ConnectionPool(host='localhost', port=6379, db=0)
pool_clinton = redis.ConnectionPool(host='localhost', port=6379, db=1)
conn_trump = redis.Redis(connection_pool=pool_trump)
conn_clinton = redis.Redis(connection_pool=pool_clinton)


def buildHistogram():
	# compute rate for Trump
	keys_trump= conn_trump.keys()
	num_trump = len(keys_trump)
	
	# compute rate for Clinton
	keys_clinton= conn_clinton.keys()
	num_clinton = len(keys_clinton)

	num = num_trump + num_clinton
	p_trump = 0
	p_clinton = 0
	if num != 0:
		p_trump = round(float(num_trump)/num, 2)
		p_clinton = 1 - p_trump
	return {'trump': p_trump, 'clinton': p_clinton, 'rate': num}


@app.route("/")
def histogram():
	h = buildHistogram()
	return json.dumps(h)


@app.route("/rate")
def rate():
	h = buildHistogram()
	return json.dumps({'rate':round(h['rate'],2)})


@app.route("/entropy")
def entropy():
	h = buildHistogram()
	s = - h['trump']*numpy.log(h['trump']) - h['clinton']*numpy.log(h['clinton'])
	return json.dumps({"time": time.strftime("%Y-%m-%d %H:%M:%S"),'entropy': round(s,2)})


@app.route("/probability")
def probability():
	h = buildHistogram()
	return json.dumps({'probability': round(h['clinton'],2)})


@app.route("/index")
def index():
	return render_template('index.html')

app.run(debug = True)