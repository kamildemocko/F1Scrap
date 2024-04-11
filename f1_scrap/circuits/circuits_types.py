from pydantic import BaseModel


class CircuitWeekendStructure(BaseModel):
    name: str
    day: str
    month: str
    time: str


class Circuit(BaseModel):
    title: str
    date_span: str
    circuit_name: str
    weekend_structure: list[CircuitWeekendStructure]


class Circuits(BaseModel):
    data: list[Circuit]
