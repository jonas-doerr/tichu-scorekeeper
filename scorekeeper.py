class TichuGame:
    def __init__(self, teamlist):
        self.rounds = []
        self.score1 = 0
        self.score2 = 0
        self.team1 = teamlist[:2]
        self.team2 = teamlist[2:4]
        self.calls = {}

    
    def add_round(self, round):

        #Check for 1-2
        onetwo = self.check_onetwo(round.finish_order, self.team1, self.team2)
        if onetwo == "Team 1":
            self.score1 += 200
        elif onetwo == "Team 2":
            self.score2 += 200
        else:
            #Add base score
            self.score1 += round.score1
            self.score2 += round.score2

        #Check for Tichus
        self.check_tichus(round.calls, round.finish_order)

        self.rounds.append({
            "team1": round.score1,
            "team2": round.score2,
            "one_two": onetwo,
            "finish_order": round.finish_order,
            "calls": round.calls
        })

        #add stats
        for place, player in enumerate(round.finish_order, start=1):
            player.placements[place] += 1

    def check_tichus(self, calls, finish_order):
        winner = finish_order[0]
        for player, value in calls.items():
            if player == winner:
                points = value 
                if points == 100:
                    player.tichus_won += 1 
                else:
                    player.grand_tichus_won += 1
            else:
                points = -value
                if points == 100:
                    player.tichus_lost += 1 
                else:
                    player.grand_tichus_lost += 1

            if player in self.team1:
                self.score1 += points
            elif player in self.team2:
                self.score2 += points

    def check_onetwo(self, finish_order, team1, team2):
        if finish_order[0] in team1 and finish_order[1] in team1:
            return "Team 1"
        elif finish_order[0] in team2 and finish_order[1] in team2:
            return "Team 2"
        return None  

    def winner(self):
        if self.score1 >= 1000 and self.score1 > self.score2:
            for player in self.team1: 
                player.games_won += 1
            return "Team 1"
        elif self.score2 >= 1000 and self.score2 > self.score1:
            for player in self.team2: 
                player.games_won += 1
            return "Team 2"
        return None

class Player:
    def __init__(self, name):
        self.name = name

        # Games
        self.games_played = 0
        self.games_won = 0

        # Rounds
        self.rounds_played = 0

        # Placements
        self.placements = {
            1: 0,
            2: 0,
            3: 0,
            4: 0
        }

        # Tichus
        self.tichus_called = 0
        self.tichus_won = 0
        self.tichus_lost = 0

        self.grand_tichus_called = 0
        self.grand_tichus_won = 0
        self.grand_tichus_lost = 0

class Round:
    def __init__(self, team1_points, team2_points, finish_order, calls):
        self.score1 = team1_points
        self.score2 = team2_points
        self.finish_order = finish_order      # list of Player objects
        self.calls = calls                    # {Player: "tichu"}

        self.one_two = None
        self.tichu_results = {}

class Database:
    pass