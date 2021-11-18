import os

from record import Record
from person import Person, get_people

from espn_api.football import League
# I'm worried that python-fire isn't really being super actively maintained by Google anymore
# but goddamn is it convenient for making CLIs (see https://github.com/google/python-fire)
import fire

class LeagueCalculator(object):
    """Does stuff with ESPN fantasy football leagues"""

    def __init__(self):
        # One day...
        pass

    def alternate_schedule_record(self, target_person: Person, other_person: Person, up_to_week: int) -> Record:
        """
        Calculates what the target person's record would be if they played the other person's schedule
        :param target_person: Person to calculate the record for
        :param other_person: Person whose schedule we'll use
        :returns: Record
        """
        record = Record()
        for i in range(0, up_to_week - 1):
            if target_person.team_id == other_person.opponents[i].team_id:
                continue

            if target_person.scores[i] > other_person.opponents[i].scores[i]:
                record.wins += 1
            elif target_person.scores[i] < other_person.opponents[i].scores[i]:
                record.losses += 1
            else:
                record.ties += 1

        return record

    def print_all_alternate_records_for_person(self, league_id: int, year: int, person_name: str) -> None:
        league = League(
            league_id=league_id,
            year=year,
            espn_s2=os.getenv("ESPN_S2", "").strip(),
            swid=os.getenv("SWID", "").strip()
        )
        people = get_people(league)

        target_person = None
        for person in people:
            if person.name == person_name:
                target_person = person

        if not target_person:
            assert(False, "Couldn't find person")

        for person in people:
            if person.name == target_person.name:
                pass

            latest_week = league.nfl_week
            # temporary hack
            latest_week = len(league.teams[0].schedule) + 1
            alternate_record = self.alternate_schedule_record(target_person, person, latest_week - 1)
            print(f"{target_person.name} would be {alternate_record} with {person.name}'s schedule.")

    def print_true_records(self, league_id: int, year: int) -> None:
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
        print("True Record")
        print("If your total all play wins > all play losses in a week, that's a true win. "
            "This is roughly equivalent to saying 'weeks you were in the top half of scorers'. "
            "Your luck is the differential between your wins and your true wins.")
        for person in people:
            luck = person.actual_record.wins - person.true_record.wins
            luck_sign = '+' if luck > 0 else ''
            print(f"{person.name}: {person.true_record} (Luck: {luck_sign}{luck})")



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
        # Duplicatively makes another league
        self.print_true_records(league_id, year)

        print("")
        print("Head to Head Every Week")
        for person in people:
            print(person.name)
            person.print_h2h()
            print("")


if __name__ == "__main__":
    fire.Fire(LeagueCalculator)
