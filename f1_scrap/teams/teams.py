from playwright.sync_api import Page, Locator

from .teams_types import Team, Teams, TeamMember


def _get_team_info(page: Page) -> Team:
    team_members_names: list[Locator] = page.locator("ul.drivers h1.driver-name").all()
    team_members_nums: list[Locator] = page.locator("ul.drivers div.driver-number").all()

    member1 = TeamMember(
        name=team_members_names[0].text_content().strip(),
        number=int(team_members_nums[0].text_content().strip()),
    )
    member2 = TeamMember(
        name=team_members_names[1].text_content().strip(),
        number=int(team_members_nums[1].text_content().strip()),
    )

    stat_table_values_loc: list[Locator] = page.locator("table.stat-list td").all()
    stat_table_values = [v.text_content().strip() for v in stat_table_values_loc]
    assert len(stat_table_values) == 11

    return Team(
        name=page.locator("h1.headline").text_content().strip(),
        full_name=stat_table_values[0],
        base=stat_table_values[1],
        team_chief=stat_table_values[2],
        tech_chief=stat_table_values[3],
        chassis=stat_table_values[4],
        power_unit=stat_table_values[5],
        first_team_entry=stat_table_values[6],
        world_championships=stat_table_values[7],
        highest_race_finish=stat_table_values[8],
        pole_positions=stat_table_values[9],
        fastest_laps=stat_table_values[10],
        member1=member1,
        member2=member2,
    )


def get_teams(page: Page) -> Teams:
    # page.locator("div.primary-links").get_by_text("Teams", exact=True).click()
    page.goto("https://www.formula1.com/en/teams.html")

    teams: list[Locator] = page.locator('main[pagename="Teams"] a.listing-link').all()
    result: list[Team] = []

    for team in teams:
        team.click()
        page.wait_for_load_state("load")

        driver = _get_team_info(page)
        result.append(driver)

        page.go_back()

    assert len(result) == 10

    return Teams(data=result)
