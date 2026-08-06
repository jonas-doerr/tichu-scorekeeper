from scorekeeper import TichuGame, Player, Round
from database import *
import random
from datetime import date

#Random player nanmes for testing
player1 = Player("Simon")
player2 = Player("Jonas")
player3 = Player("Micah")
player4 = Player("Mom")
playerlist = [player1, player2, player3, player4]

game = TichuGame(playerlist)

def make_random_finish(playerlist):
    #Randomly select a finish order (for testing)
    rand_finish = random.sample(playerlist, len(playerlist))
    print([player.name for player in rand_finish])
    return rand_finish

def make_random_calls(players):
    calls = {}

    # 50% chance nobody calls tichu
    if random.choice([True, False]):
        return calls

    # Pick one random player
    caller = random.choice(players)
    caller.tichus_called += 1

    # Add their call
    calls[caller] = 100
    print(f"{caller.name} called a Tichu!")

    return calls

#Print the teams
print(f"{playerlist[0].name} and {playerlist[1].name} vs {playerlist[2].name} and {playerlist[3].name}")

#play full game
def simulate_game():
    while game.winner() not in ["Team 1", "Team 2"]:
        score = random.randint(-5, 20) * 5
        round = Round(score, 100 - score, make_random_finish(playerlist), make_random_calls(playerlist), playerlist[:2], playerlist[2:4])
        game.add_round(round)
        print(f"{game.score1} to {game.score2}")

    print(game)

    print("\nPlayer Stats")
    print("============")

    for player in playerlist:
        print(player)
        print()
        save_player(player)

    current_date = date.today()
    save_game(current_date, game.winner(), game.score1, game.score2)

simulate_game()
view_games()