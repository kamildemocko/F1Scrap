import urllib.parse

import arrow
from playwright.sync_api import Locator, Page

from .circuits_types import CircuitWeekendStructure, Circuit, Circuits


def _get_weekend_structure(page: Page) -> list[CircuitWeekendStructure]:
    weekend_struct: list[CircuitWeekendStructure] = []

    divs_all: list[Locator] = page.locator("div.f1-race-hub--timetable-listings > div.row").all()
    divs: list[Locator] = [d for d in divs_all if "d-none" not in d.get_attribute("class")]

    for div in divs:
        weekend_struct.append(CircuitWeekendStructure(
            name=div.locator(".f1-timetable--title").first.text_content().strip(),
            day=div.locator(".f1-timetable--day").first.text_content().strip(),
            month=div.locator(".f1-timetable--month").first.text_content().strip(),
            time=div.locator(".start-time").first.text_content().strip() if div.locator(".start-time").count() > 0 else "",
        ))

    return weekend_struct


def _get_circuit_info(page: Page) -> tuple[str, str, str]:
    title: str = page.locator(".race-location").all_inner_texts()[0].strip()
    date_span: str = page.locator(".race-weekend-dates").text_content().strip()
    name: str = page.locator("h2.f1--s").text_content().strip()

    return title, date_span, name


def get_circuits(page: Page) -> Circuits:
    page.goto(f"https://www.formula1.com/en/racing/{arrow.now().year}.html")

    circuit_locs: list[Locator] = page.locator("a.event-item-wrapper").all()
    circuit_hrefs: list[str] = [circuit.get_attribute("href") for circuit in circuit_locs]
    result: list[Circuit] = []

    for circuit in circuit_hrefs:
        page.goto(urllib.parse.urljoin(page.url, circuit))

        res_weekend_struct: list[CircuitWeekendStructure] = _get_weekend_structure(page)
        title, date_span, name = _get_circuit_info(page)
        result.append(
            Circuit(title=title, date_span=date_span, circuit_name=name, weekend_structure=res_weekend_struct)
        )

    return Circuits(data=result)
