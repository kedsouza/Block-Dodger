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

# from cassandra.cluster import Cluster
# from cassandra.auth import PlainTextAuthProvider
# from ssl import PROTOCOL_TLSv1_2, SSLContext, CERT_NONE

import threading

print('hello')
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

cursor = cnxn.cursor()
cursor.execute('SELECT TOP 10 * from highscoredata ORDER BY highScores_score desc')

json = '{"data": ['
for i in cursor:
	json += '{ "username" : "' + i[0] + '" , "score" : ' + str(i[1]) + '},'
json = json[:-1] 
json += ']}'

# Returns string in valid json format, will see if we can clean this up
print (json)


