-- Create a keyspace
CREATE KEYSPACE IF NOT EXISTS highscoredata WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : '1' };


-- Create a table highScores
CREATE TABLE IF NOT EXISTS highscoredata.highScores(
    highScores_username text,
    highScores_score int,
    PRIMARY KEY (highScores_username, highScores_score)
);

CREATE TABLE IF NOT EXISTS highscoredata.highScoresOrder(
    highScores_username text,
    highScores_score int,
    PRIMARY KEY (highScores_score, highScores_username)
);

CREATE TABLE IF NOT EXISTS highscoredata.highScoresOrder(
    highScores_username text,
    highScores_score int,
    PRIMARY KEY (highScores_username, highScores_score)
)
WITH CLUSTERING ORDER BY (highScores_score DESC)