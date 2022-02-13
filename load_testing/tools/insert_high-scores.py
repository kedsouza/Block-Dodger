# Inserts random values to populate data

import random
import uuid

# SQL
import pyodbc 
# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port
server = 'tcp:block-dodger.database.windows.net' 
database = 'block-dodger-sql' 
username = 'keegan' 
password = 'Database15!' 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()



def insertIntoHighScore(username,score):
    #Sample insert query
    count = cursor.execute("""INSERT INTO highscoredata (highScores_username, highScores_score) VALUES (?,?)""", username, score)
    cnxn.commit()
    print('Rows inserted: ' + str(count))

for  i in range(100):
    user = str(uuid.uuid4())
    score = random.randint(0, 500)
    insertIntoHighScore ( user, score)

