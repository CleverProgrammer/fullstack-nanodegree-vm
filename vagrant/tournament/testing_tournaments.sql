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

INSERT INTO players (full_name) VALUES
	('Rafeh Qazi'),
	('Tenzin Phuljung');

CREATE TABLE matches
(
	match_id	SERIAL REFERENCES players(player_id),
	rounds		INT,
	wins		INT,
	losses		INT
	-- FOREIGN KEY (match_id) REFERENCES players(player_id)
);

ALTER TABLE matches
ADD CONSTRAINT match_players FOREIGN KEY (match_id) REFERENCES players(player_id);

INSERT INTO matches (match_id, rounds, wins, losses) VALUES
	(1, 2, 2, 0),
	(2, 3, 1, 2);

\d

SELECT * FROM players;
SELECT * FROM matches;


-- Return the player with the max wins.
SELECT players.full_name
FROM players
INNER JOIN matches
ON players.player_id = matches.match_id
WHERE matches.wins IN
		(SELECT MAX(wins)
			FROM matches as most_wins);

SELECT MAX(wins)
FROM matches;

SELECT players.player_id, players.full_name,
        matches.wins, matches.rounds
        FROM players
        INNER JOIN matches
        ON players.player_id = matches.match_id
        ORDER BY matches.wins;

\c vagrant;
