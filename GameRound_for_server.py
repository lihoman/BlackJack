from Player import *


class GameRound:

    def __init__(self, player_name):
        self.player = Player(player_name, 100)  # creating a player with the given name
        self.dealer = Player('Dealer')  # creating a dealer
        self.player_result = 0
        self.dealer_result = 0

    def one_more_card(self, player_name, answer):
        """Func to add one more card to player or dealer depending on given arg: player_name. """
        if player_name == self.dealer.name:
            player_name = self.dealer
        elif player_name == self.player.name:
            player_name = self.player
        player_name.plus_one_card(answer)  # to add one random card depending on answer (Yes or No)
        result = player_name.finish_result()  # result as a integer number
        return result

    def compare_results(self, player_result, dealer_result):
        """Func to find who is winner: player or dealer. """
        if player_result > dealer_result:
            return f'Winner: {self.player.name}'
        elif player_result == dealer_result:
            return "It's a draw!"
        else:
            return f'Winner: {self.dealer.name}'
