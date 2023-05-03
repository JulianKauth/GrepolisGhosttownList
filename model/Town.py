from urllib.parse import unquote


class Town:
    def __init__(self, id, name, x, y, points):
        self.id = id
        self.name = unquote(name)
        self.x = x
        self.y = y
        self.points = points
        self.sea = f"M{int(self.x / 100)}{int(self.y / 100)}"

    def __repr__(self):
        return f"[town]{self.id}[/town] {self.points} {self.x}/{self.y}"
