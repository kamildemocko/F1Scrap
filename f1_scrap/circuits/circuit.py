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
    page.locator("div.primary-links").get_by_text("Schedule", exact=True).click()

    # circuits: list[Locator] = page.locator("div.event-below-hero > div").all()
    circuits: list[Locator] = page.locator("a.event-item-wrapper").all()
    result: list[Circuit] = []

    for circuit in circuits:
        circuit.click()

        res_weekend_struct: list[CircuitWeekendStructure] = _get_weekend_structure(page)
        title, date_span, name = _get_circuit_info(page)
        result.append(
            Circuit(title=title, date_span=date_span, circuit_name=name, weekend_structure=res_weekend_struct)
        )

        page.go_back()

    return Circuits(data=result)
