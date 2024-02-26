import msgspec


class TeamMember(msgspec.Struct):
    name: str
    number: int


class Team(msgspec.Struct):
    name: str
    full_name: str
    base: str
    team_chief: str
    tech_chief: str
    chassis: str
    power_unit: str
    first_team_entry: str
    world_championships: str
    highest_race_finish: str
    pole_positions: str
    fastest_laps: str
    member1: TeamMember
    member2: TeamMember


class Teams(msgspec.Struct):
    data: list[Team]
