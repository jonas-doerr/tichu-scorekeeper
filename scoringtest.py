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

def make_random_finish(playerlist, calls):
    remaining = list(playerlist)
    finish_order = []

    # Map each player to their teammate based on indices
    teammate_map = {
        playerlist[0]: playerlist[1],
        playerlist[1]: playerlist[0],
        playerlist[2]: playerlist[3],
        playerlist[3]: playerlist[2],
    }

    while remaining:
        candidates = []
        weights = []

        for player in remaining:
            partner = teammate_map[player]
            player_call = calls.get(player, 0)
            partner_call = calls.get(partner, 0)

            # Check if teammate called Tichu and hasn't gone out yet
            partner_waiting_on_tichu = (
                partner_call > 0 and partner in remaining
            )

            # Block player if their teammate called Tichu and hasn't gone out yet.
            # (Allows both if both called Tichu to avoid deadlocks)
            if partner_waiting_on_tichu and not (
                player_call > 0 and partner_call > 0
            ):
                continue

            # Assign weights for eligible candidates
            if player_call == 200:
                w = 7
            elif player_call == 100:
                w = 5
            else:
                w = 1

            candidates.append(player)
            weights.append(w)

        # Weighted selection from eligible players
        chosen_player = random.choices(candidates, weights=weights, k=1)[0]

        finish_order.append(chosen_player)
        remaining.remove(chosen_player)

    print([player.name for player in finish_order])
    return finish_order

def make_random_calls(players):
    calls = {}
    randcall = random.randint(1, 10)
    # Desperation Grand Tichu calls
    if game.score1 + 600 < game.score2:
        caller = random.choice(players[:2])
        caller.tichus_called += 1
        calls[caller] = 200
        return calls
    if game.score2 + 600 < game.score1:
        caller = random.choice(players[2:4])
        caller.tichus_called += 1
        calls[caller] = 200
        return calls
    # 50% chance nobody calls tichu
    if random.choice([True, False]):
        return calls

    # Pick one random player
    caller = random.choice(players)
    caller.tichus_called += 1
    if random.randint(1, 5) < 5:
        calls[caller] = 100
    else:
        calls[caller] = 200

    if random.choice([True, False]):
        return calls

    if caller in players[:2]:
        caller = random.choice(players[2:4])
        caller.tichus_called += 1
        calls[caller] = 100
    else:
        caller = random.choice(players[:2])
        caller.tichus_called += 1
        calls[caller] = 100
    return calls

#Print the teams
print(f"{playerlist[0].name} and {playerlist[1].name} vs {playerlist[2].name} and {playerlist[3].name}")

#play full game
def simulate_game():
    while game.winner() not in ["Team 1", "Team 2"]:
        score = random.randint(-5, 25) * 5
        calls = make_random_calls(playerlist)
        print(calls)
        round = Round(score, 100 - score, make_random_finish(playerlist, calls), calls, playerlist[:2], playerlist[2:4])
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
    game_id = save_game(current_date, game.score1, game.score2)
    save_teams(game_id, playerlist[:2], playerlist[2:4])

    for round_number, round_data in enumerate(game.rounds, start=1):
        round_id = save_round(game_id, round_number, round_data)

        save_placements(round_id, round_data)
        save_calls(round_id, round_data)

simulate_game()

#print database results
# Options: "players", "games", "rounds", "placements", "calls", ""
checked_data_tables = [
        "players",
        "games"
    ]
for table in checked_data_tables:
    view_table(table)