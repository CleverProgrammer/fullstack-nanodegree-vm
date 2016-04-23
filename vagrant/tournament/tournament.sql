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
	full_name	VARCHAR(255)
);

CREATE TABLE matches
(
	match_id	SERIAL PRIMARY KEY,
	rounds		INT,
	wins		INT,
	losses		INT
);

ALTER TABLE matches
ADD CONSTRAINT match_players FOREIGN KEY (match_id) REFERENCES players(player_id);
