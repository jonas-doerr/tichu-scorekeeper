class TichuGame:
    def __init__(self):
        self.rounds = []
        self.score1 = 0
        self.score2 = 0

    def add_round(self, score1, score2):
        self.score1 += score1
        self.score2 += score2

        self.rounds.append({
            "team1": score1,
            "team2": score2
        })

    def winner(self):
        if self.score1 >= 1000 and self.score1 > self.score2:
            return "Team 1"
        elif self.score2 >= 1000 and self.score2 > self.score1:
            return "Team 2"
        return None

class Player:
    pass

class Database:
    pass