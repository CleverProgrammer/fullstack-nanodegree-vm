#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM matches;")
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM players;")
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) as num FROM players;")
    results = c.fetchone()[0]
    conn.close()
    return results

# countPlayers()


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO players (full_name) VALUES (%s)", (name,))
    # c.execute("UPDATE matches INNER JOIN players\
               # SET matches.matches_id = players.player_id")
    conn.commit()
    conn.close()

# registerPlayer("Nick Drane")


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT players.player_id, players.full_name,\
        matches.wins, matches.rounds\
        FROM players\
        LEFT OUTER JOIN matches\
        ON players.player_id = matches.match_id\
        ORDER BY matches.wins")
    results = c.fetchall()
    lists = [list(tuple_) for tuple_ in results]
    for index, list_ in enumerate(lists):
        lists[index] = [0 if value == None else value for value in list_]
    tuples = [tuple(list_) for list_ in lists]
    return tuples




def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    c = conn.cursor()
    # c.execute("INSERT INTO matches VALUES (%s)\
              # IF (%s) NOT IN match_id", (winner, winner))

    # c.execute("INSERT INTO matches VALUES (%s)\
               # IF (%s) NOT IN match_id", (loser, loser))

    c.execute("IF NOT EXISTS (SELECT match_id from matches\
               where match_id = (%s)\
               BEGIN INSERT matches(match_id)\
               VALUES (%s)\
               END;", (winner, winner))

    c.execute("IF NOT EXISTS (SELECT match_id from matches\
               where match_id = (%s)\
               BEGIN INSERT matches(match_id)\
               VALUES (%s)\
               END;", (loser, loser))

    c.execute("UPDATE matches SET wins = wins + 1, rounds = rounds + 1\
               WHERE match_id = (%s)", (winner,))

    c.execute("UPDATE matches SET losses = losses + 1, rounds = rounds + 1\
               WHERE match_id = (%s)", (loser,))
    conn.commit()
    conn.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

if __name__ == '__main__':
    # deleteMatches()
    # deletePlayers()
    # registerPlayer("Nick")
    print(playerStandings())
    # reportMatch(2, 1)
