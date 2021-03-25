from GameRound import *


start = GameRound('Nikita')

while start.player.count > 0:
    start.player_game()
    start.dealer_game()
    start.find_winner()
