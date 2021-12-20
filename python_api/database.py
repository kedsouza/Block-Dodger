"""
Rest API that provides calls to the database.
"""

import json 
import logging
import datetime
import time
import sys
from flask import Flask, Response, request
from flask_cors import CORS
from flask.logging import default_handler
from flask_socketio import SocketIO

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from ssl import PROTOCOL_TLSv1_2, SSLContext, CERT_NONE

import threading

# SQL
# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port
import pyodbc 
server = 'tcp:block-dodger.database.windows.net' 
database = 'block-dodger-sql' 
username = 'keegan' 
password = 'Database15!' 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins='*')

# Disable standard flask logging
# log = logging.getLogger('werkzeug')
# log.disabled = True

@socketio.on('message')
def handle_message(data):
	print('recieved message ' + data)

def highscore_broadcast():
	while True:
		time.sleep(1)
		data = getHighScoreUsers()
		socketio.emit('score', data)

@app.route("/test")
def test():
	return 'hello there'

def getHighScoreUsers ():
	json = '{"data": ['

	cursor = cnxn.cursor()
	cursor.execute('SELECT TOP 10 * from highscoredata ORDER BY highScores_score desc')

	for i in cursor:
		json += '{ "username" : "' + i[0] + '" , "score" : ' + str(i[1]) + '},'
	
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
	session.execute('INSERT INTO highscoresorder (highScores_username, highScores_score) VALUES (%s, %s)', (username, score))

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
	cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
	cursor = cnxn.cursor()	

	score = request.json['score']
	cursor.execute('SELECT COUNT(highScores_score) FROM highScoredata WHERE highScores_score >=' + str(score))
	result = cursor.fetchall()
	return str(result[0][0] + 1)

if __name__ == '__main__':
	try:
		t1 = threading.Thread(target=highscore_broadcast)
		t1.daemon = True
		t1.start()
		socketio.run(app)
	except KeyboardInterrupt:
		print ('Stopping')
		sys.exit(0)


