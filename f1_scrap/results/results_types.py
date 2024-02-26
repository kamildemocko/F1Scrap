import msgspec


class Result(msgspec.Struct):
    position: int
    driver_number: int
    driver_name: str
    team_name: str
    time: str
    points: int


class Results(msgspec.Struct):
    data: dict[str, list[Result]]
