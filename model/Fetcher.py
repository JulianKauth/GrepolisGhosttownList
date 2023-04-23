import requests
import zlib


def get_content_from_url(url: str) -> list[tuple[str]]:
    """load the plain text content from the server and split it into rows and columns"""
    response = requests.get(url)  # crash on error
    text = zlib.decompress(response.content, wbits=zlib.MAX_WBITS | 32).decode("UTF-8")  # https://stackoverflow.com/a/22310760
    return [tuple(row.split(",")) for row in text.split("\n") if row]


def get_players(world: str) -> list[tuple[int, str, int, int, int, int]]:
    """returns $id, $name, $alliance_id, $points, $rank, $towns"""
    return get_content_from_url(f"https://{world}.grepolis.com/data/players.txt.gz")


def get_alliances(world: str) -> list[tuple[int, str, int, int, int, int]]:
    """returns $id, $name, $points, $towns, $members, $rank"""
    return get_content_from_url(f"https://{world}.grepolis.com/data/alliances.txt.gz")


def get_towns(world: str) -> list[tuple[int, int, str, int, int, int, int]]:
    """returns $id, $player_id, $name, $island_x, $island_y, $slot_number_on_island, $points"""
    return get_content_from_url(f"https://{world}.grepolis.com/data/towns.txt.gz")


def get_islands(world: str) -> list[tuple[int, int, int, int, int, str, str]]:
    """$id, $island_x, $island_y, $island_type_number, $available_towns, $resources_advantage, $resources_disadvantage"""
    return get_content_from_url(f"https://{world}.grepolis.com/data/islands.txt.gz")


def get_player_kills_all(world: str):
    return get_content_from_url(f"https://{world}.grepolis.com/data/player_kills_all.txt.gz")


def get_player_kills_att(world: str):
    return get_content_from_url(f"https://{world}.grepolis.com/data/player_kills_att.txt.gz")


def get_player_kills_def(world: str):
    return get_content_from_url(f"https://{world}.grepolis.com/data/player_kills_def.txt.gz")


def get_alliance_kills_all(world: str):
    return get_content_from_url(f"https://{world}.grepolis.com/data/alliance_kills_all.txt.gz")


def get_alliance_kills_att(world: str):
    return get_content_from_url(f"https://{world}.grepolis.com/data/alliance_kills_att.txt.gz")


def get_alliance_kills_def(world: str):
    return get_content_from_url(f"https://{world}.grepolis.com/data/alliance_kills_def.txt.gz")
