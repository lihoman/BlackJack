from GameRound import *

player_name = input('Welcome in BlackJack. What is your name?: ')
game = GameRound(player_name)
print(game.player.count)

while game.player.count > 0:
    game.player_game()
    game.dealer_game()
    game.find_winner()
