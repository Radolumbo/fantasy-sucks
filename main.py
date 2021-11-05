import os
from typing import List

from record import Record
from person import Person

from espn_api.football import League
# I'm worried that python-fire isn't really being super actively maintained by Google anymore
# but goddamn is it convenient for making CLIs (see https://github.com/google/python-fire)
import fire

# This function smells bad and is ugly
# There's definitely a better way to initialize all the records without having it
# straight up just be a function in main.py
def get_people(league: League) -> List[Person]:
    """
    Gets all the people in your league and populates their various records
    :param league: An espn_api League object
    :returns: list[Person]
    """
    score_map = {}
    person_map = {}
    for team in league.teams:
        score_map[team.owner] = team.scores
        person_map[team.owner] = Person(
            team.owner,
            actual_record=Record(wins=team.wins, losses=team.losses, ties=team.ties)
        )

    for i in range(0, league.nfl_week - 1):
        for name1, score1 in score_map.items():
            wins_this_week = 0
            losses_this_week = 0
            for name2, score2 in score_map.items():
                if name1 == name2:
                    continue
                if score1[i] == score2[i]:
                    person_map[name1].all_record.ties += 1
                    person_map[name1].h2h.setdefault(name2, Record()).ties += 1
                elif score1[i] > score2[i]:
                    wins_this_week += 1
                    person_map[name1].all_record.wins += 1
                    person_map[name1].h2h.setdefault(name2, Record()).wins += 1
                else:
                    losses_this_week += 1
                    person_map[name1].all_record.losses += 1
                    person_map[name1].h2h.setdefault(name2, Record()).losses += 1

            if wins_this_week == losses_this_week:
                person_map[name1].true_record.ties += 1
            elif wins_this_week > losses_this_week:
                person_map[name1].true_record.wins += 1
            else:
                person_map[name1].true_record.losses += 1

    return [person for person in person_map.values()]


class LeagueCalculator(object):
    """Does stuff with ESPN fantasy football leagues"""

    def __init__(self):
        # One day...
        pass

    def print_records(self, league_id: int, year: int) -> None:
        """
        Print All Play record, True record, and Head to Head Every Week records for every team
        :param league_id: The ID of the ESPN league; get it from the URL of your league
        :param year: The year during which to calculate records
        :returns: None
        """

        league = League(
            league_id=league_id,
            year=year,
            espn_s2=os.getenv("ESPN_S2", "").strip(),
            swid=os.getenv("SWID", "").strip()
        )
        people = get_people(league)
        people.sort(reverse=True)

        print("All Play Every Week")
        for person in people:
            print(f"{person.name}: {person.all_record}")

        print("")
        print("True Record")
        print("If your total all play wins > all play losses in a week, that's a true win. "
            "This is roughly equivalent to saying 'weeks you were in the top half of scorers'. "
            "Your luck is the differential between your wins and your true wins.")
        for person in people:
            luck = person.actual_record.wins - person.true_record.wins
            luck_sign = '+' if luck > 0 else ''
            print(f"{person.name}: {person.true_record} (Luck: {luck_sign}{luck})")

        print("")
        print("Head to Head Every Week")
        for person in people:
            print(person.name)
            person.print_h2h()
            print("")


if __name__ == "__main__":
    fire.Fire(LeagueCalculator)
