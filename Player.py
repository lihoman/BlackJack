from Cards import *


class Player:
    game_deck = Deck(52)  # to create a cards deck for playing

    def __init__(self, name, count=0):
        self.name = name
        self.my_cards = []  # 2 random cards to start the game
        self.count = count

    def get_card(self):
        """Func to add a random card from the deck. """
        random_card = self.game_deck.choice_random_card()
        self.game_deck.deck.remove(random_card)  # removing this card from playing cards deck
        return random_card

    def generate_start_cards(self):
        """Func to generate 2 start cards to start the game and appending this cards (class objects) in a list. """
        my_cards = []
        i = 0
        while i < 2:
            my_cards.append(self.get_card())
            i += 1
        return my_cards

    def plus_one_card(self, answer):
        """Func to add one card for player, if he wants more (answer = 'YES'). """
        if answer == 'Y':
            self.my_cards.append(self.get_card())

    def values_result(self):
        """Func to append natural value of card, because cards is objects of class Card. """
        list_values = []  # if player will has aces ('A'), this list will contain int numbers and tuples (1, 11)
        for i in self.my_cards:
            list_values.append(i.value_int())
        return list_values

    def finish_result(self):
        """Func to calculate sum of cards values and give final result"""
        list_all_values = self.values_result()
        finish_result = []
        ace_values = 0  # amount of aces
        for i in list_all_values:
            if isinstance(i, tuple):
                ace_values += 1  # if player has a ace, rise up common aces amount
                continue
            finish_result.append(i)
        while ace_values > 0:
            self.helper_for_result(finish_result)
            ace_values -= 1
        return sum(finish_result)

    @staticmethod
    def helper_for_result(list_for_appending):
        """Func to append value of ace (1 or 11) depending on sum of player's cards. """
        if sum(list_for_appending) <= 10:
            list_for_appending.append(11)
        else:
            list_for_appending.append(1)

    def get_rate(self, rate, result):
        if rate > self.count:
            return "Sorry, you don't have so much money"
        else:
            if result[8:] == 'Dealer':
                self.count -= rate
            elif result == "It's a draw!":
                pass
            else:
                self.count += rate
            return self.count
