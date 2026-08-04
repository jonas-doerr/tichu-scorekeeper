from scorekeeper import TichuGame, Player, Round
import random

#Random player nanmes for testing
player1 = Player("Simon")
player2 = Player("Jonas")
player3 = Player("Dad")
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

# #Round 1
# game.add_round(75, 25, make_random_finish(playerlist), make_random_calls(playerlist))
# print(f"{game.score1} to {game.score2}")
# #Round 2
# game.add_round(35, 65, make_random_finish(playerlist), make_random_calls(playerlist))
# print(f"{game.score1} to {game.score2}")

#Option to play full game
while game.winner() not in ["Team 1", "Team 2"]:
    score = random.randint(-5, 20) * 5
    round = Round(score, 100 - score, make_random_finish(playerlist), make_random_calls(playerlist))
    game.add_round(round)
    print(f"{game.score1} to {game.score2}")

# print(game.rounds)
print("\nFinal Player Stats")

for player in playerlist:
    print(f"\n{player.name}")
    print(f"1st: {player.placements[1]}")
    print(f"2nd: {player.placements[2]}")
    print(f"3rd: {player.placements[3]}")
    print(f"4th: {player.placements[4]}")

    print(f"Tichus Called: {player.tichus_called}")
    print(f"Tichus Won: {player.tichus_won}")
    print(f"Tichus Lost: {player.tichus_lost}")

called = sum(p.tichus_called for p in playerlist)
won = sum(p.tichus_won for p in playerlist)
lost = sum(p.tichus_lost for p in playerlist)

print(called, won, lost)

#should all equal number of rounds
print(sum(p.placements[1] for p in playerlist))
print(sum(p.placements[2] for p in playerlist))
print(sum(p.placements[3] for p in playerlist))
print(sum(p.placements[4] for p in playerlist))