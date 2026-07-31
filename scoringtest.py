from scorekeeper import TichuGame

game = TichuGame()

game.add_round(75, 25)
game.add_round(35, 65)

print(game.score1)
print(game.score2)