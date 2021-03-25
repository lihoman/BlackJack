from Player import *
import time


class GameRound:

    def __init__(self, player_name):
        self.player = Player(player_name, 100)
        self.dealer = Player('Dealer')
        self.player_result = 0
        self.dealer_result = 0

    def one_more_card(self, player_name, answer):
        if player_name == self.dealer.name:
            player_name = self.dealer
        elif player_name == self.player.name:
            player_name = self.player
        player_name.plus_one_card(answer)
        result = player_name.finish_result()
        print(player_name.my_cards, f"{player_name.name} result: {result}".capitalize(), sep='\n')
        return result

    def player_game(self):
        # Player's start cards
        print(f'Your count: {self.player.count}')
        self.player_rate = int(input("Please, make your bet: "))
        self.player_result = self.player.finish_result()
        print(self.player.my_cards, f'{self.player.name} result: {self.player_result}', sep='\n')

        # Player's game
        answer = input('Do you want to take one more card? (y/n): ').upper()

        while answer == 'Y':
            self.player_result = self.one_more_card(self.player.name, answer)
            answer = input('Do you want to take one more card? (y/n): ').upper()
        return self.player_result

    def dealer_game(self):
        # Dealer's game
        print("It's a dealer's time now")
        time.sleep(1)
        self.dealer_result = self.dealer.finish_result()
        print(self.dealer.my_cards, f'Dealer result: {self.dealer_result}', sep='\n')
        time.sleep(1)
        while self.dealer_result <= 17:
            time.sleep(1)
            self.dealer_result = self.one_more_card(self.dealer.name, 'Y')
        return self.dealer_result

    # To compare results and determination a winner
    def compare_results(self, player_result, dealer_result):
        if player_result > dealer_result:
            return f'Winner: {self.player.name}'
        elif player_result == dealer_result:
            return "It's a draw!"
        else:
            return f'Winner: {self.dealer.name}'

    def find_winner(self):
        if self.player_result <= 21 and self.dealer_result <= 21:
            game_result = self.compare_results(self.player_result, self.dealer_result)
            print(game_result)
            self.player.get_rate(self.player_rate, game_result)
            print(f'Your count: {self.player.count}')
        else:
            game_result = self.compare_results(self.dealer_result, self.player_result)
            print(game_result)
            self.player.get_rate(self.player_rate, game_result)
            print(f'Your count: {self.player.count}')
