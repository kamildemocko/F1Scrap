import msgspec


class CircuitWeekendStructure(msgspec.Struct):
    name: str
    day: str
    month: str
    time: str


class Circuit(msgspec.Struct):
    title: str
    date_span: str
    weekend_structure: list[CircuitWeekendStructure]


class Circuits(msgspec.Struct):
    data: list[Circuit]
