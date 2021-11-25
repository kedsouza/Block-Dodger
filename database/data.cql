-- Create a keyspace
CREATE KEYSPACE IF NOT EXISTS highscoredata WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : '1' };


-- Create a table highscoredata
CREATE TABLE IF NOT EXISTS highscoredata.highScores(
    highScores_username text PRIMARY KEY,
    highScores_score int,
);