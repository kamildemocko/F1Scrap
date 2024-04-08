from playwright.sync_api import Page, Locator
import arrow

from f1_scrap.drivers.drivrer_types import Drivers, Driver


def _get_driver_info(page: Page, driver: Locator) -> Driver | None:
    rank = driver.locator(".rank").text_content().strip()
    team = driver.locator(".listing-item--team").text_content().strip()

    names = driver.locator(".listing-item--name > span").all()
    firstname = names[0].text_content().strip()
    lastname = names[1].text_content().strip()

    driver_data = {"firstname": firstname,
                   "lastname": lastname,
                   "name": " ".join([firstname, lastname]),
                   "short": lastname[:3].upper(),
                   "number": int(rank),
                   "team": team,
                   }

    driver.click()
    page.wait_for_load_state("load")

    stat_table_values_loc: list[Locator] = page.locator("table.stat-list td").all()
    stat_table_values = [v.text_content().strip() for v in stat_table_values_loc]

    page.go_back()

    if len(stat_table_values) != 10:
        return Driver(**driver_data)

    driver_data["country"] = stat_table_values[1]
    driver_data["podiums"] = stat_table_values[2]
    driver_data["points"] = stat_table_values[3]
    driver_data["gp_entered"] = stat_table_values[4]
    driver_data["world_championships"] = stat_table_values[5]
    driver_data["highest_race_finish"] = stat_table_values[6]
    driver_data["highest_grid_position"] = stat_table_values[7]
    driver_data["date_of_birth"] = arrow.get(stat_table_values[8], "D/M/YYYY").date()
    driver_data["place_of_birth"] = stat_table_values[9]

    return Driver(**driver_data)


def get_drivers(page: Page) -> Drivers:
    page.locator("div.primary-links").get_by_text("Drivers", exact=True).click()

    drivers: list[Locator] = page.locator('main[pagename="Drivers"] a.listing-item--link').all()
    result: list[Driver] = []

    for driver in drivers:
        driver = _get_driver_info(page, driver)
        if driver is not None:
            result.append(driver)

    assert len(result) >= 20

    return Drivers(data=result)
