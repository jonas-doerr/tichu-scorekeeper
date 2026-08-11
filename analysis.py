from database import get_players, get_player_placements, view_games, get_player_calls

players = get_players()

player_dict = {
    name: player_id
    for player_id, name in players
}

# Create list of placements
def placement_list(player_id):
    placements = get_player_placements(player_id)

    placement_counts = {
        1: placements.count(1),
        2: placements.count(2),
        3: placements.count(3),
        4: placements.count(4)
    }

    total_placements = len(placements)
    placement_value = 0
    for value in placements:
        placement_value += value
    average_placement = placement_value / total_placements

    return placement_counts, average_placement

def games_played(player_id):
    games = view_games()
    total_games = enumerate(games)

def call_stats(player_id):
    calls = get_player_calls(player_id)
    tichus = [call for call, success in calls if call == "Tichu"]
    grand_tichus = [call for call, success in calls if call == "Grand Tichu"]

    successful_tichus = [
        call for call, success in calls
        if call == "Tichu" and success
    ]

    successful_grand_tichus = [
        call for call, success in calls
        if call == "Grand Tichu" and success
    ]

    return tichus, grand_tichus, successful_tichus, successful_grand_tichus

# def count_one_two(player_id):
#     one_twos = get_one_two(player_id)
#     total_one_twos = len([one_two for one_two in one_twos if one_two != None])
#     return total_one_twos