-- Create a keyspace
CREATE KEYSPACE IF NOT EXISTS highscoredata WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : '1' };


-- Create a table highScores
CREATE TABLE IF NOT EXISTS highscoredata.highScores(
    highScores_username text,
    highScores_score int,
    PRIMARY KEY (highScores_username, highScores_score)
);