import random


class Card:
    """Class for creating a view of one card. """

    cards_suits = {
        'spade': "♠",
        'heart': "♥",
        'diamond': "♦",
        'club': "♣",
    }
    cards_values = (2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A')

    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def value_int(self):
        """Func to create equivalent value for string card symbol (J, Q, K, A). """
        if isinstance(self.value, str):
            if self.value == 'A':
                return 1, 11
            else:
                return 10
        else:
            return self.value

    def __repr__(self):
        """Overload standard method in order to view more beautiful interface for user"""
        if self.value in self.cards_values:
            return f'{self.value}{self.cards_suits[self.suit]}'
        else:
            return "There is no such card"


class Deck:
    """Class to create card deck depending on what user selects (36 or 52 cards in deck)"""

    def __init__(self, length_of_deck):
        self.length_of_deck = length_of_deck
        self.deck = self.generate_deck()

    def generate_deck(self):
        if self.length_of_deck == 36:
            return self.generate_deck_36()
        elif self.length_of_deck == 52:
            return self.generate_deck_52()

    @staticmethod
    def generate_deck_36():
        return [Card(suit, value) for value in Card.cards_values[4:] for suit in Card.cards_suits]

    @staticmethod
    def generate_deck_52():
        return [Card(suit, value) for value in Card.cards_values for suit in Card.cards_suits]

    def shuffle_deck(self):
        random.shuffle(self.deck)
        return self.deck

    def choice_random_card(self):
        return random.choice(self.deck)
