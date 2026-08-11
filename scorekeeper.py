class TichuGame:
    def __init__(self, teamlist):
        self.rounds = []
        self.score1 = 0
        self.score2 = 0
        self.team1 = teamlist[:2]
        self.team2 = teamlist[2:4]
        self.calls = {}

    
    def add_round(self, round):
        round_score1 = self.score1
        round_score2 = self.score2
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

        self.rounds.append(round)

        #add stats
        for place, player in enumerate(round.finish_order, start=1):
            player.placements[place] += 1

        round_score1 = self.score1 - round_score1
        round_score2 = self.score2 - round_score2
        return round_score1, round_score2

    def check_tichus(self, calls, finish_order):
        winner = finish_order[0]
        for player, value in calls.items():
            if player == winner:
                points = value 
                if value == 100:
                    player.tichus_won += 1 
                else:
                    player.grand_tichus_won += 1
            else:
                points = -value
                if value == 100:
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
    
    def __str__(self):
        return (
            f"Tichu Game\n"
            f"----------\n"
            f"Team 1: {self.team1[0].name} & {self.team1[1].name}\n"
            f"Team 2: {self.team2[0].name} & {self.team2[1].name}\n"
            f"Score: {self.score1} - {self.score2}\n"
            f"Rounds Played: {len(self.rounds)}\n"
            f"Winner: {self.winner() or 'None'}"
        )

class Player:
    def __init__(self, name, id = None):
        self.name = name
        self.id = id

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

    def reset_stats(self):
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

    def __str__(self):
        return (
            f"{self.name}\n"
            f"  Placings:\n"
            f"    1st: {self.placements[1]}\n"
            f"    2nd: {self.placements[2]}\n"
            f"    3rd: {self.placements[3]}\n"
            f"    4th: {self.placements[4]}\n"
            f"  Tichus:\n"
            f"    Called: {self.tichus_called}\n"
            f"    Won: {self.tichus_won}\n"
            f"    Lost: {self.tichus_lost}"
        )

class Round:
    def __init__(self, team1_points, team2_points, finish_order, calls, team1, team2):
        self.score1 = team1_points
        self.score2 = team2_points
        self.final_score1 = team1_points
        self.final_score2 = team2_points
        self.finish_order = finish_order      # list of Player objects
        self.calls = calls                    # {Player: "tichu"}

        if finish_order[0] in team1 and finish_order[1] in team1:
            self.one_two = "Team 1"
            self.final_score1 = 200
            self.final_score2 = 0
        elif finish_order[0] in team2 and finish_order[1] in team2:
            self.one_two = "Team 2"
            self.final_score2 = 200
            self.final_score1 = 0
        else:
            self.one_two = None
        
        #define self.tichu_results{}
        self.tichu_results = {}
        for player, call in self.calls.items():
            success = (player == self.finish_order[0])
            if call == 100:
                call_name = "Tichu"
            else:
                call_name = "Grand Tichu"

            if success:
                if player in team1:
                    self.final_score1 += call
                else:
                    self.final_score2 += call
            else:
                if player in team1:
                    self.final_score1 -= call
                else:
                    self.final_score2 -= call

            self.tichu_results[player] = {
                "call": call_name,
                "success": success
            }

    def __str__(self):

        finish = ", ".join(player.name for player in self.finish_order)

        if self.calls:
            calls = ", ".join(
                f"{player.name}: {call}"
                for player, call in self.calls.items()
            )
        else:
            calls = "None"

        return (
            f"Round\n"
            f"-------\n"
            f"Team 1: {self.final_score2}\n"
            f"Team 2: {self.final_score1}\n"
            f"Finish: {finish}\n"
            f"Calls: {calls}\n"
            f"One-Two: {self.one_two}"
        )

class Database:
    pass