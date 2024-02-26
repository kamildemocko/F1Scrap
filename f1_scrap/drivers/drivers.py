from playwright.sync_api import Page, Locator
import arrow

from f1_scrap.drivers.drivrer_types import Drivers, Driver


def _get_driver_info(page: Page) -> Driver:
    stat_table_values_loc: list[Locator] = page.locator("table.stat-list td").all()
    stat_table_values = [v.text_content().strip() for v in stat_table_values_loc]
    assert len(stat_table_values) == 10

    return Driver(
        name=page.locator(".driver-name").text_content().strip(),
        short=page.locator(".driver-name").text_content().strip()[:3].upper(),
        number=int(page.locator(".driver-number").text_content().strip()),
        team=stat_table_values[0],
        country=stat_table_values[1],
        podiums=stat_table_values[2],
        points=stat_table_values[3],
        gp_entered=stat_table_values[4],
        world_championships=stat_table_values[5],
        highest_race_finish=stat_table_values[6],
        highest_grid_position=stat_table_values[7],
        date_of_birth=arrow.get(stat_table_values[8], "D/M/YYYY").date(),
        place_of_birth=stat_table_values[9],
    )


def get_drivers(page: Page) -> Drivers:
    page.locator("div.primary-links").get_by_text("Drivers", exact=True).click()

    drivers: list[Locator] = page.locator('main[pagename="Drivers"] a.listing-item--link').all()
    result: list[Driver] = []

    for driver in drivers:
        driver.click()
        page.wait_for_load_state("load")

        driver = _get_driver_info(page)
        result.append(driver)

        page.go_back()

    assert len(result) == 20

    return Drivers(data=result)
