-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;

CREATE TABLE players
(
	player_id	SERIAL PRIMARY KEY NOT NULL,
	full_name	VARCHAR(255) NOT NULL
);

CREATE TABLE matches
(
	match_id	INT NOT NULL,
	result      INT NOT NULL,
	FOREIGN KEY (match_id) REFERENCES players(player_id)
);

CREATE VIEW standings AS
SELECT 	players.player_id, 
	players.full_name, 
	COUNT(CASE result WHEN 1 THEN 1 END) AS wins,
	COUNT(matches.match_id) AS rounds
FROM players
LEFT OUTER JOIN matches
ON players.player_id = matches.match_id
GROUP BY players.player_id;
