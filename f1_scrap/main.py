from time import sleep
from pathlib import Path

from playwright.sync_api import sync_playwright, Playwright, Page, Browser, FrameLocator
import msgspec
from loguru import logger

from f1_scrap.circuits.circuit import get_circuits
from f1_scrap.drivers.drivers import get_drivers
from f1_scrap.teams.teams import get_teams
from f1_scrap.results.results import get_results


class Main:
    def __init__(self, playwright: Playwright):
        self.browser: Browser = playwright.chromium.launch(headless=True)
        self.page: Page = self.browser.new_page()

        self.page.goto("https://www.formula1.com")
        self._handle_gdpr()

    def _handle_gdpr(self):
        self.page.wait_for_selector('iframe[id^="sp_message_iframe"]', timeout=1000)

        while self.page.query_selector('iframe[id^="sp_message_iframe"]') is not None:
            gdpr_frame: FrameLocator = self.page.frame_locator('iframe[id^="sp_message_iframe"]')
            gdpr_frame.locator('button[title="REJECT ALL"]').click()
            sleep(1)

    @staticmethod
    def save_data(path: Path, data: msgspec.Struct):
        with path.open("wb") as f:
            f.write(msgspec.json.encode(data))

    def save_circuits(self, output_path: Path):
        logger.info("getting circuits")
        circuits = get_circuits(self.page)
        self.save_data(output_path, circuits)
        logger.info("> done")

    def save_drivers(self, output_path: Path):
        logger.info("getting drivers")
        drivers = get_drivers(self.page)
        self.save_data(output_path, drivers)
        logger.info("> done")

    def save_teams(self, output_path: Path):
        logger.info("getting teams")
        teams = get_teams(self.page)
        self.save_data(output_path, teams)
        logger.info("> done")

    def save_results(self, output_path: Path):
        logger.info("getting results")
        results = get_results(self.page)
        self.save_data(output_path, results)
        logger.info("> done")


if __name__ == "__main__":
    logger.info("start")

    circuits_save_path: Path = Path("output/circuits.json")
    drivers_save_path: Path = Path("output/drivers.json")
    teams_save_path: Path = Path("output/teams.json")
    results_save_path: Path = Path("output/results.json")

    circuits_save_path.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as pw:
        main = Main(pw)
        main.save_circuits(circuits_save_path)
        main.save_drivers(drivers_save_path)
        main.save_teams(teams_save_path)
        main.save_results(results_save_path)

    logger.info("end")
