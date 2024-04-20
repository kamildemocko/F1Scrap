from pydantic import BaseModel


class Result(BaseModel):
    position: str
    driver_number: int
    driver_name: str
    team_name: str
    time: str
    points: str


class Results(BaseModel):
    sprint: dict[str, list[Result]] = dict[str, list[Result]]
    race: dict[str, list[Result]] = dict[str, list[Result]]
