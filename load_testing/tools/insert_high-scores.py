# Inserts random values to populate data

import random
import uuid

# Cassandra
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from ssl import PROTOCOL_TLSv1_2, SSLContext, CERT_NONE

# Remove SSL operation for now
ssl_opts = {
        'cert_reqs': CERT_NONE
}
auth_provider = PlainTextAuthProvider(username="block-dodger-cass-db", password="StMBPhgiA3qrzwTaVqGy4a1JzW3YNUXEkwyPt3Rns5HyK2gIXKxyD0SvctrR5XWJuCcc6dB8AdVB6X3vUquZKw==")
cluster = Cluster(["block-dodger-cass-db.cassandra.cosmos.azure.com"], port=10350, auth_provider=auth_provider, ssl_options=ssl_opts)
session = cluster.connect('highscoredata')

def insertIntoHighScore(username,score):
	session.execute('INSERT INTO highscoresorder (highScores_username, highScores_score) VALUES (%s, %s)', (username, score))

for  i in range(100):
    user = str(uuid.uuid4())
    score = random.randint(0, 500)
    insertIntoHighScore ( user, score)

