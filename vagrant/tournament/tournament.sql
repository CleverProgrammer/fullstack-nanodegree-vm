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
	id	SERIAL PRIMARY KEY NOT NULL,
	full_name	VARCHAR(255) NOT NULL
);

insert into players values
  (1, 'Tenzin'),
  (2, 'Qazi');

CREATE TABLE matches
(
	id	        SERIAL PRIMARY KEY NOT NULL,
	winner      INT NOT NULL,
	loser       INT NOT NULL,
	FOREIGN KEY (winner) REFERENCES players(id),
	FOREIGN KEY (loser) REFERENCES players(id)
);

insert into matches values
  (1, 1, 2);

select * from matches;

/*
CREATE VIEW standings AS
SELECT 	players.player_id, 
	players.full_name, 
	COUNT(CASE result WHEN 1 THEN 1 END) AS wins,
	COUNT(matches.match_id) AS rounds
FROM players
LEFT OUTER JOIN matches
ON players.player_id = matches.match_id
GROUP BY players.player_id;

select * from standings;
*/
