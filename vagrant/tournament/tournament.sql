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
  (2, 'Qazi'),
	(3, 'Bob'),
	(4, 'Martin');

CREATE TABLE matches
(
	id        SERIAL PRIMARY KEY NOT NULL,
	winner_id INT,
	loser_id  INT,
	FOREIGN KEY (winner_id) REFERENCES players(id),
	FOREIGN KEY (loser_id) REFERENCES players(id)
);

insert into matches values
  (1, 1, 2),
	(8, 2, 1),
	(25, 3, 1);

select * from matches;

CREATE VIEW rounds AS
	SELECT players.id, count(winner_id) as matches
	FROM players
		left outer join matches
	on players.id = matches.winner_id or players.id = matches.loser_id
	GROUP BY players.id;

-- select * from rounds;

CREATE VIEW win_standings AS
  SELECT players.id, players.full_name, count(winner_id) as wins
    FROM players
    LEFT OUTER JOIN matches
    ON players.id = matches.winner_id
		GROUP BY players.id;

-- select * from win_standings;

CREATE VIEW standings AS
select win_standings.id, full_name, wins, matches
	from rounds
	left outer join win_standings
		on rounds.id = win_standings.id
	order by wins desc;

select * from standings;

create view final_standings AS
	select win_standings.id, full_name
	from rounds
	left outer join win_standings
		on rounds.id = win_standings.id
	order by wins desc;

select * from final_standings;

\c vagrant;
