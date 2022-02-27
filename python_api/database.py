"""
Rest API that provides calls to the database.
"""
import os
import json 
import logging
import datetime
import time
import sys
from flask import Flask, Response, request
from flask_cors import CORS
from flask.logging import default_handler
from flask_socketio import SocketIO
from flask import jsonify

import threading

# Load environment variables from .env file.
# On Azure we execude .env file and set them as app settings.
from dotenv import load_dotenv
load_dotenv()

# SQL
import pyodbc 
server = os.getenv('BD_SERVER') #'tcp:block-dodger.database.windows.net' 
database = os.getenv('BD_DATABASE') #'block-dodger-sql' 
username = os.getenv('BD_USER')#'keegan' 
password = os.getenv('BD_PASSWORD') #'Database15!' 
connecion_string = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password
cnxn = pyodbc.connect(connecion_string)
cursor = cnxn.cursor()

cursor.execute("SELECT @@version;")
row = cursor.fetchone()
if row:
	print("Succesfully estiablished DB connection: " + row[0])
else:
	print("Failed to connect to db")
	sys.exit(0)
cursor.close()


app = Flask(__name__)
CORS(app)


# Health endpoint to verify the flask api is running
@app.route("/health")
def health():
	return 'Healthy!'

@app.route("/HighScores/GetTopTen")
def callgetHighScoreUsers():
	data = getHighScoreUsers()
	if data == None:
		return 'Error', 500
	return jsonify(data)

# JSON { "score" : int }
@app.route('/HighScores/GetPosition', methods =['POST'])
def callHighScorePosition():
	score = request.json['score']
	return getHighScorePosition(score)

# JSON { "user" : string, "score" : int}
@app.route('/HighScores/Add', methods = ['POST'])
def calladdHighScoreUser():
	username = request.json['username']
	score = request.json['score']
	return addHighScoreUser(username, score)

# Returns the top ten users and scores.
def getHighScoreUsers ():
	data = []
	try:
		cnxn = pyodbc.connect(connecion_string)
		cursor = cnxn.cursor()	
		cursor.execute('SELECT TOP 10 * from highscoredata ORDER BY highScores_score desc')
		for row in cursor:
			user, score = row[0], row[1]
			data.append((user,  score))
	except pyodbc.Error as e:
		print(e)
	finally:
		cursor.close()
		cnxn.close()
	return data

# Queries the SQL Database to get the position based on score. 
# inputs:
# 	score: int
def getHighScorePosition (score):
	cursor = cnxn.cursor()	
	cursor.execute('SELECT COUNT(highScores_score) FROM highScoredata WHERE highScores_score >=' + str(score))
	result = cursor.fetchall()
	# Increments position to account for top record being 0 
	return str(result[0][0] + 1)

# Adds inputs into the database, need to revist logic of user names
# inputs:
# 	username: text
# 	score : int 
def addHighScoreUser (username, score):
	cursor = cnxn.cursor()
	cursor.execute('SELECT * FROM highscoredata WHERE CONVERT(VARCHAR, highscores_username) = ? ', (username,))
	for user in cursor:
		print (user)
		if (score > user[1]):	
			cursor.execute("""INSERT INTO highscoredata (highScores_username, highScores_score) VALUES (?, ?)""", username, score)
			return 'hello'
		else: 
			return 'Not Added'

	cursor.execute("""INSERT INTO highscoredata (highScores_username, highScores_score) VALUES (?, ?)""", username, score)
	return 'hello'

if __name__ == '__main__':
	app.run(host='0.0.0.0')


