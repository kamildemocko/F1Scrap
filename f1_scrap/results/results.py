from typing import Literal
from urllib.parse import urljoin
from time import sleep

import arrow
from playwright.sync_api import Page, Locator, ElementHandle

from .results_types import Result, Results


def _get_results_info(tr: Locator) -> Result:
    columns: list[Locator] = tr.locator("td").all()
    columns_values = [v.text_content().strip() for v in columns]

    name = " ".join(
        [v.strip() for v in columns_values[3].split("\n")[:2]]
    )

    return Result(
        position=columns_values[1],
        driver_number=int(columns_values[2]),
        driver_name=name,
        team_name=columns_values[4],
        time=columns_values[6],
        points=columns_values[7],
    )


def _get_event_data(page: Page, event_type: Literal["race", "sprint"]) -> list[Result] | None:
    positions: list[Result] = []

    # no data on page whatsoever
    if page.query_selector("div.resultsarchive-content") is None:
        return None

    # click button sprint or race
    loc: ElementHandle | None = None
    title_expect: str = "RACE RESULT" if event_type == "race" else "SPRINT"

    if event_type == "race":
        loc = page.query_selector('a[data-value="race-result"]')
    elif event_type == "sprint":
        loc = page.query_selector('a[data-value="sprint-results"]')

    if loc is None:
        return positions

    loc.click()

    # wait until title loads == loaded
    for _ in range(10):
        sleep(.2)
        title = page.locator("h1.ResultsArchiveTitle").text_content()

        if title_expect in title:
            break
    else:
        return positions

    table_trs = page.locator("div.resultsarchive-content").locator("tr").all()[1:]
    if len(table_trs) == 0:
        return positions

    for tr in table_trs:
        results: Result = _get_results_info(tr)
        positions.append(results)

    return positions


def get_results(base_url: str, page: Page) -> Results:
    page.goto(f"https://www.formula1.com/en/results.html/{arrow.now().year}/races.html")

    circuits: list[Locator] = (page
                               .locator("ul.resultsarchive-filter")
                               .nth(2)
                               .locator("li.resultsarchive-filter-item > a")
                               .all())
    output_sprint: dict[str, list[Result]] = {}
    output_race: dict[str, list[Result]] = {}

    for circuit in circuits:
        if circuit.text_content().strip() == "All":
            continue

        circuit_name = circuit.text_content().strip()
        href_url = urljoin(base_url, circuit.get_attribute("href"))
        page.goto(href_url)

        output_sprint[circuit_name] = _get_event_data(page, "sprint")
        output_race[circuit_name] = _get_event_data(page, "race")

    return Results(sprint=output_sprint, race=output_race)
