"""
Rest API that provides calls to the database.
"""

import json 
import logging
import datetime
import time
from flask import Flask, Response, request
from flask_cors import CORS
from flask.logging import default_handler
from flask_socketio import SocketIO

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from ssl import PROTOCOL_TLSv1_2, SSLContext, CERT_NONE

import threading


# Cassandra Database

# Remove SSL operation for now
ssl_opts = {
        'cert_reqs': CERT_NONE
}
auth_provider = PlainTextAuthProvider(username="block-dodger-cass-db", password="StMBPhgiA3qrzwTaVqGy4a1JzW3YNUXEkwyPt3Rns5HyK2gIXKxyD0SvctrR5XWJuCcc6dB8AdVB6X3vUquZKw==")
cluster = Cluster(["block-dodger-cass-db.cassandra.cosmos.azure.com"], port=10350, auth_provider=auth_provider, ssl_options=ssl_opts)
session = cluster.connect('highscoredata')

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins='*')

# Disable standard flask logging
# log = logging.getLogger('werkzeug')
# log.disabled = True

@socketio.on('message')
def handle_message(data):
	print('recieved message ' + data)

def test_broadcast():
	while True:
		print("Calling test broadcast")
		time.sleep(1)
		data = getHighScoreUsers()
		socketio.emit('score', data)

@app.route("/test")
def test():
	return 'hello there'

@app.route('/HighScores/Get', methods = ['GET'])
def getHighScoreUsers ():
	json = '{"data": ['
	rows = session.execute('select * from highScores;')
	for row in rows:
		json += '{ "username" : "' + row.highscores_username + '" , "score" : ' + str(row.highscores_score) + '},'
	json = json[:-1] 
	json += ']}'

	return json
@app.route('/HighScores/Add', methods = ['POST'])
def addHighScoreUser ():
	username = request.json['username']
	score = request.json['score']

	rows = session.execute('SELECT * FROM highScores WHERE highscores_username=%s', (username,))
	for users in rows:
		if (users !=None and users.highscores_score < score):	
			insertIntoHighScore(username, score)
			return 'hello'
		else: 
			return 'Not Added'

	insertIntoHighScore(username, score)
	return 'hello'

def insertIntoHighScore(username,score):
	session.execute('INSERT INTO highScores (highScores_username, highScores_score) VALUES (%s, %s)', (username, score))


@app.route('/HighScores/Find', methods = ['POST'])
def findHighScoreUser ():
	try:
		username = request.json['username']
		rows = session.execute('SELECT * FROM highScores WHERE highscores_username=%s', (username,))
	except:
		return "Not Found"
	return "Found"

@app.route('/HighScores/GetPosition', methods =['POST'])
def getHighScorePosition ():
	count = 0
	score = request.json['score']
	rows = session.execute('SELECT * FROM highScores WHERE highScores_score >= %s ALLOW FILTERING', (score,))
	for row in rows:
		count += 1
	return str(count + 1)

if __name__ == '__main__':
	t1= threading.Thread(target=test_broadcast)
	t1.start()
	socketio.run(app)


