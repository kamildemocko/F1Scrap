import urllib.parse

from playwright.sync_api import Page, Locator, TimeoutError, Browser
import arrow

from .drivrer_types import Drivers, Driver


def _get_driver_info(browser: Browser, base_url: str, driver: Locator) -> Driver | None:
    team = driver.locator("> div > div > div > p").text_content().strip()
    names = driver.locator("h4.f1-inner-wrapper > div > p").all()
    firstname = names[0].text_content().strip()
    lastname = names[1].text_content().strip()

    driver_data = {"firstname": firstname,
                   "lastname": lastname,
                   "name": " ".join([firstname, lastname]),
                   "short": lastname[:3].upper(),
                   "team": team,
                   }

    temp_page = browser.new_page()
    try:
        temp_page.goto(urllib.parse.urljoin(base_url, driver.get_attribute("href")))

        try:
            temp_page.locator(".f1-driver-position > div > p").wait_for(timeout=10000)
            driver_number = temp_page.locator(".f1-driver-position > div > p").text_content().strip()

        except TimeoutError:
            driver_number = 0

        stat_table_values_loc: list[Locator] = temp_page.locator("div.f1-dl > dl > dd").all()
        stat_table_values = [v.text_content().strip() for v in stat_table_values_loc]

        if len(stat_table_values) != 10:
            return Driver(**driver_data)

        driver_data["number"] = int(driver_number)
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

    finally:
        temp_page.close()


def get_drivers(browser: Browser, base_url: str, page: Page) -> Drivers:
    page.goto("https://www.formula1.com/en/drivers.html")

    drivers: list[Locator] = page.locator('div.f1-inner-wrapper > div > a').all()
    result: list[Driver] = []

    for driver in drivers:
        driver = _get_driver_info(browser, base_url, driver)
        if driver is not None:
            result.append(driver)

    if len(result) < 20:
        raise AssertionError(f"Wrong driver count, should be more drivers. is: {len(result)}")

    return Drivers(data=result)
