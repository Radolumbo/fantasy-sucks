from record import Record

from espn_api.football import Team
from espn_api.football import League

# This class is similar to thea "Team" class in the espn-api module
# but twisted to do what I WANT IT TO DO MUAHAHAHA
# Eventually should probably just hit the API directly instead of using this
# really poorly made espn-api module
class Person():
    def __init__(self, team: Team):
        # It's a little fucked up that I'm keeping a reference to the espn-api's concept
        # of team in here, but it makes some things easier for now. Eventually I'd like to replace the
        # espn-api entirely with my own direct API calls
        self.team = team
        self.team_id = self.team.team_id
        self.name = team.owner
        self.scores = team.scores
        self.actual_record = Record(wins=team.wins, losses=team.losses, ties=team.ties)
        self.all_record = Record()
        self.true_record = Record()
        # This should eventually be matchups instead of just opponents but I'm having trouble
        # reasoning about how I want to handle matchups atm
        self.opponents = []
        self.h2h = {} # should have this be a default dict with Record()
                      # actually this probably just shouldn't be in Person at all

    # Sorts by all play record
    def __lt__(self, other):
        return self.all_record.wins < other.all_record.wins

    def __eq__(self, other):
        return self.all_record.wins == other.all_record.wins

    # Print utility functions are stupid but I'm lazy for now
    def print_all_record(self):
         print(f"{self.all_record}")

    def print_true_record(self):
         print(f"{self.true_record}")

    def print_h2h(self):
        for opponent, record in self.h2h.items():
            print(f"Against {opponent}: {record}")

# This function smells bad and is ugly, and does a lot of hacky shit
# There's definitely a better way to initialize all the records
def get_people(league: League) -> list[Person]:
    """
    Gets all the people in your league and populates their various records
    :param league: An espn_api League object
    :returns: list[Person]
    """
    latest_week = league.nfl_week
    person_map = {}

    # Initialize People from teams
    for team in league.teams:
        owner = team.owner
        person_map[owner] = Person(
            team
        )

    # Make opponents in Person actual references to other People
    # Super duplicative to Person.team.schedule but hey I'm lazy
    for person in person_map.values():
        for opponent in person.team.schedule:
            person.opponents.append(person_map[opponent.owner])

    # Calculate various records
    for i in range(0, latest_week - 1):
        for name1, person1 in person_map.items():
            score1 = person1.scores
            wins_this_week = 0
            losses_this_week = 0
            for name2, person2 in person_map.items():
                score2 = person2.scores
                if person1.team_id == person2.team_id:
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
