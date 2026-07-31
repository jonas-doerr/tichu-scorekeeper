class TichuGame:
    def __init__(self):
        self.rounds = []
        self.score1 = 0
        self.score2 = 0
        self.team1 = []
        self.team2 = []
        self.calls = {}

    
    def add_round(self, score1, score2, finish_order, calls):

        #Check for 1-2
        onetwo = self.check_onetwo(finish_order, self.team1, self.team2)
        if onetwo == "Team 1":
            self.score1 += 200
        elif onetwo == "Team 2":
            self.score2 += 200
        else:
            #Add base score
            self.score1 += score1
            self.score2 += score2

        #Check for Tichus
        self.check_tichus(calls, finish_order)

        self.rounds.append({
            "team1": score1,
            "team2": score2,
            "one_two": onetwo,
            "finish_order": finish_order,
            "calls": calls
        })

    def check_tichus(self, calls, finish_order):
        winner = finish_order[0]
        for player, value in calls.items:
            points = value if player == winner else -value

            if player in self.team1:
                self.score1 += points
            elif player in self.team2:
                self.score2 += points

    def check_onetwo(self, finish_order, team1, team2):
        if team1[0] and team1[1] in finish_order[:1]:
            return "Team 1"
        elif team2[0] and team2[1] in finish_order[:1]:
            return "Team 2"
        return None  

    def winner(self):
        if self.score1 >= 1000 and self.score1 > self.score2:
            return "Team 1"
        elif self.score2 >= 1000 and self.score2 > self.score1:
            return "Team 2"
        return None

class Player:
    def __init__(self, name):
        self.name = name
        self.small_tichu_wins = 0
        self.small_tichu_losses = 0
        self.grand_tichu_wins = 0
        self.grand_tichu_losses = 0

class Database:
    pass