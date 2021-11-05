class Record():
    def __init__(self, wins=0, losses=0, ties=0):
        self.wins = wins
        self.losses = losses
        self.ties = ties

    def __str__(self):
        return f"{self.wins}-{self.losses}-{self.ties}"
