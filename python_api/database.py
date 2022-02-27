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

@app.route('/HighScores/GetPosition', methods =['POST'])
def callHighScorePosition():
	score = request.json['score']
	position = getHighScorePosition(score)
	if position == -1:
		return 'Error', 500
	return str(position)

# JSON { "user" : string, "score" : int}
@app.route('/HighScores/Add', methods = ['POST'])
def calladdHighScoreUser():
	username = request.json['username']
	score = request.json['score']
	result = addHighScoreUser(username, score)
	if result[0] == True:
		return result[1], 200
	else:
		return result[1], 400

@app.route('/HighScores/CheckUser', methods = ['POST'])
def callCheckUserExists():
	username = request.json['username']
	if checkUserExists(username):
		return 'User Exists', 200
	
	return 'User Does not Exist', 404

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


def getHighScorePosition (score: str) -> int:
	position = -1
	try:
		cnxn = pyodbc.connect(connecion_string)
		cursor = cnxn.cursor()
		cursor.execute('SELECT COUNT(highScores_score) FROM highScoredata WHERE highScores_score >=' + str(score))
		result = cursor.fetchall()
		# Increments score to account for top record being 0
		position = result[0][0] + 1
	except pyodbc.Error as e:
		print(e)
	finally:
		cursor.close()
		cnxn.close()
	return position

# Need to refactor this
def addHighScoreUser (username: str, score: int) -> set():
	inserted, msg = False, ""
	valid = True
	# Check if username already has a high score assoicated in the db
	if checkUserExists(username):
		try:
			cnxn = pyodbc.connect(connecion_string)
			cursor = cnxn.cursor()
			cursor.execute('SELECT * FROM highscoredata WHERE highscores_username = ? ', (username))
			row = cursor.fetchone()
			if row[1] > score:
				valid = False
		except pyodbc.Error as e:
			print(e)
			valid = False
			inserted = False
		finally:
			cursor.close()
			cnxn.close()
	# If not, insert it into the database 
	if not valid:
		msg = "This username already has a higher score"
	else:
		try:
			cnxn = pyodbc.connect(connecion_string)
			cursor = cnxn.cursor()
			if checkUserExists(username) == False:
				result = cursor.execute("""INSERT INTO highscoredata (highScores_username, highScores_score) VALUES (?, ?)""", username, score)
			else:
				result = cursor.execute("""UPDATE highscoredata SET highScores_score = (?) WHERE highScores_username = (?)""", score, username)
			cnxn.commit()
			inserted, msg = True, "Score Inserted Successfully"
		except pyodbc.Error as e:
			print(e)
			inserted = False
		finally:
			cursor.close()
			cnxn.close()
	return (inserted, msg)

def checkUserExists(username: str) -> bool:
	exists = False
	try:
		cnxn = pyodbc.connect(connecion_string)
		cursor = cnxn.cursor()
		cursor.execute('SELECT * FROM highscoredata WHERE highscores_username = ? ', (username))
		row = cursor.fetchone()
		if row != None:
			exists = True
	except pyodbc.Error as e:
		print(e)
	finally:
		cursor.close()
		cnxn.close()
	
	return exists

if __name__ == '__main__':
	app.run(host='0.0.0.0')

