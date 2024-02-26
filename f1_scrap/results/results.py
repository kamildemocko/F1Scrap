from time import sleep

from playwright.sync_api import Page, Locator

from f1_scrap.results.results_types import Result, Results


def _get_results_info(tr: Locator) -> Result:
    columns: list[Locator] = tr.locator("td").all()
    columns_values = [v.text_content().strip() for v in columns]

    name = " ".join(
        [v.strip() for v in columns_values[3].split("\n")[:2]]
    )

    return Result(
        position=columns_values[1],
        driver_number=columns_values[2],
        driver_name=name,
        team_name=columns_values[4],
        time=columns_values[6],
        points=columns_values[7],
    )


def get_results(page: Page) -> Results:
    page.locator("div.primary-links").get_by_text("Results", exact=True).click()

    page.wait_for_selector("div.resultsarchive-filter-wrap", timeout=30_000)
    filters = page.locator('div.resultsarchive-filter-wrap').all()
    # filters[0].locator("li").first.click()
    filters[0].locator("li").nth(1).click()
    filters[1].locator("li").first.click()

    circuits: list[Locator] = filters[2].locator("li").all()[1:]
    output: list[dict[str, Result]] = []
    temp_h1: str = "THIS IS NOT THE TITLE"

    for circuit in circuits:
        circuit_name = circuit.text_content().strip()
        positions: list[Result] = []

        circuit.click()
        while True:
            temp_h1 == "" and sleep(1)
            sleep(0.2)

            actual_h1 = page.locator("h1.ResultsArchiveTitle").text_content().strip()
            if temp_h1 in actual_h1:
                continue

            temp_h1 = actual_h1
            sleep(1)
            break

        if page.query_selector("div.resultsarchive-content") is None:
            continue

        table_trs = page.locator("div.resultsarchive-content").locator("tr").all()[1:]
        if len(table_trs) == 0:
            output.append({circuit_name: positions})
            continue

        for tr in table_trs:
            results: Result = _get_results_info(tr)
            positions.append(results)

        output.append({circuit_name: positions})

    return Results(data=output)
