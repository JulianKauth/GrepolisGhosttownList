# local representation of the data fetched from the server.
# must hold all the datapoints available in the api endpoints described here:
# https://wiki.de.grepolis.com/wiki/Weltdaten
import sqlite3
import time
from typing import Optional

from model.Fetcher import *
from model.Town import Town


class Database:
    def __init__(self):
        self.db = sqlite3.connect(":memory:")
        self.cur = self.db.cursor()
        self.world = None
        self.last_update = None

    def get_ghosts(self, distance: Optional[int], reference: Optional[tuple[int, int]]) -> list[Town]:
        gt = self.cur.execute('SELECT town_id, name, island_x, island_y, points FROM towns WHERE player_id=""').fetchall()
        gt = [Town(*t) for t in gt]
        if reference is None:
            ref_x, ref_y = 500, 500
        else:
            ref_x, ref_y = reference
        if distance:
            gt = [t for t in gt if ((t.x - ref_x) ** 2 + (t.y - ref_y) ** 2) < distance ** 2]
        # print(f"Database.get_ghosts(): Fount {len(gt)} Ghosts")
        return gt

    def fill_database(self, world: str):
        # print(f"Database.fill_database({world})")

        """
        Based on some boolean logic we decide if we need to refresh the database or not
        world None / same as old world / up to date
        not / not / not  -> clean, then fetch
        not / not / yes  -> clean, then fetch
        not / yes / not  -> clean, then fetch
        not / yes / yes  -> we are already done
        yes / not / ___  -> just fetch the data
        yes / yes / ___  -> impossible state
        """
        world_is_not_none = self.world is not None
        world_is_same = self.world == world
        up_to_date = self.last_update is not None and self.last_update + 600 < time.time()  # last refresh less than ten minutes ago

        if world_is_not_none and world_is_same and up_to_date:
            return  # nothing to do
        elif world_is_not_none:
            # reset DB, we got a different world this time or need to refresh the data
            self.cur.execute("DROP TABLE players")
            self.cur.execute("DROP TABLE alliances")
            self.cur.execute("DROP TABLE towns")
            self.cur.execute("DROP TABLE islands")

        # update the values for next time
        self.last_update = time.time()
        self.world = world

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
