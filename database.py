"""
Rest API that provides calls to the database.
"""

import json 
from flask import Flask, Response, request
from flask_cors import CORS
from cassandra.cluster import Cluster


cluster = Cluster()
session = cluster.connect('highscoredata')



app = Flask(__name__)
CORS(app)

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

@app.errorhandler(ValueError)
def exceptionHandler (error):
	return "Do not exists"

if __name__ == '__main__':
   app.run()