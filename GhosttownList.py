import sys

from model.Database import Database

from urllib.parse import unquote

class Town:
    def __init__(self, id, name, x, y, points):
        self.id = id
        self.name = unquote(name)
        self.x = x
        self.y = y
        self.points = points
        self.sea = f"M{int(self.x/100)}{int(self.y/100)}"

    def __repr__(self):
        return f"[town]{self.id}[/town] {self.points} {self.x}/{self.y}"

if __name__ == "__main__":
    db = Database()
    db.fill_database("de99")

    gt = db.cur.execute('SELECT town_id, name, island_x, island_y, points FROM towns WHERE player_id=""').fetchall()
    gt = [Town(*t) for t in gt]

    # filter by distance if a distance argument is given
    if len(sys.argv) > 1:
        len_before = len(gt)
        # called as `python GhosttownList.py 100` the number will be interpreted as a max distance from 500/500
        # sys.argv would be ["Ghsottownlist.py", "100"] in that case
        distance = int(sys.argv[1])
        gt = [t for t in gt if ((t.x-500)**2 + (t.y-500)**2) < distance**2]
        len_after = len(gt)
        print(f"Filtered by distance {distance}: {len_before} Cities -> {len_after} Cities")

    # print sorted by sea
    print("\nSorted by Sea:")
    gt = sorted(gt, key=lambda t: t.sea)
    print("\n".join([str(t) for t in gt]))

    # print sorted by points
    print("\nSorted by Points:")
    gt = sorted(gt, key=lambda t: t.points)
    print("\n".join([str(t) for t in gt]))

