# local representation of the data fetched from the server.
# must hold all the datapoints available in the api endpoints described here:
# https://wiki.de.grepolis.com/wiki/Weltdaten
import sqlite3
from model.Fetcher import *

class Database:
    def __init__(self):
        self.db = sqlite3.connect(":memory:")
        self.cur = self.db.cursor()

        #response = self.cur.execute()
        #response.fetchall()

    def fill_database(self, world: str):
        # create player table
        players = get_players(world)
        self.cur.execute("CREATE TABLE players("
            "player_id INTEGER UNIQUE PRIMARY KEY, "
            "name TEXT UNIQUE, "
            "alliance_id INTEGER, "
            "points INTEGER, "
            "rank INTEGER, "
            "towns INTEGER, "
            "FOREIGN KEY(alliance_id) REFERENCES alliances(alliance_id))"
        )
        self.cur.executemany("INSERT INTO players VALUES(?, ?, ?, ?, ?, ?)", players)

        # create alliance table
        alliances = get_alliances(world)
        self.cur.execute("CREATE TABLE alliances("
            "alliance_id INTEGER UNIQUE PRIMARY KEY, "
            "name TEXT UNIQUE, "
            "points INTEGER, "
            "towns INTEGER, "
            "members INTEGER, "
            "rank INTEGER)"
        )
        self.cur.executemany("INSERT INTO alliances VALUES(?, ?, ?, ?, ?, ?)", alliances)

        # create towns table
        towns = get_towns(world)
        self.cur.execute("CREATE TABLE towns("
            "town_id INTEGER UNIQUE PRIMARY KEY, "
            "player_id INTEGER, "
            "name TEXT, "
            "island_x INTEGER, "
            "island_y INTEGER, "
            "slot_number INTEGER, "
            "points INTEGER, "
            "FOREIGN KEY(player_id) REFERENCES players(player_id))"
        )
        self.cur.executemany("INSERT INTO towns VALUES(?, ?, ?, ?, ?, ?, ?)", towns)

        # create islands table
        islands = get_islands(world)
        self.cur.execute("CREATE TABLE islands("
            "island_id INTEGER UNIQUE PRIMARY KEY, "
            "x INTEGER, "
            "y INTEGER, "
            "type INTEGER, "
            "num_towns INTEGER, "
            "ressource_plus TEXT, "
            "ressource_minus TEXT)"
        )
        self.cur.executemany("INSERT INTO islands VALUES(?, ?, ?, ?, ?, ?, ?)", islands)

        self.db.commit()
