import datetime

from pydantic import BaseModel


class Driver(BaseModel):
    firstname: str
    lastname: str
    name: str
    short: str
    team: str
    number: int = 0
    country: str = ""
    podiums: str = ""
    points: str = ""
    gp_entered: str = ""
    world_championships: str = ""
    highest_race_finish: str = ""
    highest_grid_position: str = ""
    date_of_birth: datetime.date = datetime.date(1, 1, 1)
    place_of_birth: str = ""


class Drivers(BaseModel):
    data: list[Driver]
