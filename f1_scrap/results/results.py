from time import sleep
import urllib.parse

import arrow
from playwright.sync_api import Page, Locator

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


def get_results(base_url: str, page: Page) -> Results:
    page.goto(f"https://www.formula1.com/en/results.html/{arrow.now().year}/races.html")

    circuits: list[Locator] = (page
                               .locator("ul.resultsarchive-filter")
                               .nth(2)
                               .locator("li.resultsarchive-filter-item > a")
                               .all())
    output: dict[str, list[Result]] = {}

    for circuit in circuits:
        if circuit.text_content().strip() == "All":
            continue

        page.goto(urllib.parse.urljoin(base_url, circuit.get_attribute("href")))

        circuit_name = circuit.text_content().strip()
        positions: list[Result] = []

        if page.query_selector("div.resultsarchive-content") is None:
            continue

        table_trs = page.locator("div.resultsarchive-content").locator("tr").all()[1:]
        if len(table_trs) == 0:
            output[circuit_name] = positions
            continue

        for tr in table_trs:
            results: Result = _get_results_info(tr)
            positions.append(results)

        output[circuit_name] = positions

    return Results(results=output)
