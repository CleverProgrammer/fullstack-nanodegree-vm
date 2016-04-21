-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

CREATE TABLE players
(
	player_id	SERIAL PRIMARY KEY NOT NULL,
	LastName	VARCHAR(255),
	FirstName	VARCHAR(255)
);

INSERT INTO players (LastName, FirstName) VALUES
	('Qazi', 'Rafeh'),
	('Phuljung', 'Tenzin');

CREATE TABLE matches
(
	match_id	SERIAL PRIMARY KEY,
	rounds		INT,
	score		NUMERIC
);

ALTER TABLE matches
ADD CONSTRAINT match_players FOREIGN KEY (match_id) REFERENCES players(player_id);

INSERT INTO matches (match_id, rounds, score) VALUES
	(1, 2, 2),
	(2, 1, 0.5);

\d

SELECT players.FirstName
FROM players
INNER JOIN matches
ON players.player_id = matches.match_id
WHERE matches.score = 2;

SELECT * FROM matches;