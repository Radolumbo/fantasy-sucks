from record import Record

class Person():
    def __init__(self, name, actual_record=Record()):
        self.name = name
        self.actual_record = actual_record
        self.all_record = Record()
        self.true_record = Record()
        self.wins = 0
        self.h2h = {} # should have this be a default dict with Record()

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
