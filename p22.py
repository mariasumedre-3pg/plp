""" Python script to implement P2 of Phase 2 of Python Learning Program
    This is the Poker game with classes and stuff """

from random import shuffle

COLORS = ["heart",
          "spade",
          "club",
          "star"]

class Card(object):
    """ Card class models a card from the 52 card deck (used for e.g. in Poker) """
    def __init__(self, value=10, color=COLORS[0]):
        """ constructor for the Card class
            expects a value for the Card and a type/color """
        self._value = value
        self._color = color

    def color(self):
        """ getter for the color/shape/type of the card """
        return self._color

    def value(self):
        """ getter for the value of the card """
        return self._value

    def __repr__(self):
        """ override representation as this is used in cmp and in displaying players' cards """
        number = str(self._value)
        if self._value == 10:
            number = "ace"
        elif self._value == 11:
            number = "jack"
        elif self._value == 12:
            number = "queen"
        elif self._value == 13:
            number = "king"
        return "{0} of {1}".format(number, self._color)

    def __cmp__(self, obj):
        """ override comparison operator for sorted """
        if isinstance(obj, Card):
            result = self._value - obj.value()
            if result == 0:
                result = self._color < obj.color()
            return result
        return NotImplemented

class Deck(object):
    """ Deck class models the 52 card deck (used for e.g. in Blackjack) """
    def __init__(self, full=True):
        """ constructor for the Deck class
            expects a boolean value to build a full Deck or an empty one """
        self._cards = []
        if full:
            self.collect_cards()
            self.shuffle()

    def shuffle(self):
        """ shuffle the cards, if any """
        if self._cards:
            shuffle(self._cards)

    def sort(self):
        """ sort the cards, if any """
        if self._cards:
            self._cards = sorted(self._cards)

    def remove_card(self):
        """ remove a Card from the Deck and return it (typically to the player) """
        return self._cards.pop()

    def collect_cards(self):
        """ re-stock the deck to the full 52 cards """
        self._cards = [Card(value, color) for color in COLORS for value in range(1, 14)]

    def print_cards(self):
        """ print/show cards in deck """
        for card in self._cards:
            print card


def sort_key(card):
    """ key to give to sorted to sort the Poker Cards """
    return str(card)


class PokerPlayer(object):
    """ PokerPlayer class models the Poker players, who expect cards from PokerDealer """
    def __init__(self, name="Ion Popescu"):
        self._name = name
        self._cards = []
        self._revealed = 0

    def name(self):
        """ getter for the player's name """
        return self._name

    def start_game(self):
        """ reset the cards """
        self._cards = []

    def receive_card(self, card):
        """ save the card from the dealer """
        self._cards.append(card)

    def reveal(self):
        """ Player reveals all cards """
        for card in self._cards:
            print "I have a", card

    def __repr__(self):
        return self._name


class PokerDealer(object):
    """ Dealer class that handles a Deck, and gives cards to the players """
    def __init__(self):
        self._deck = Deck(full=True)
        self._players = []
        self._game_on = False
        self._house = PokerPlayer("House")

    def add_player(self, player):
        """ method to add players to the game, before the game starts """
        if not self._game_on:
            self._players.append(player)
        else:
            print "Players cannot join while a game is ongoing"

    def deal_initial(self):
        """ method to deal the initial 2 cards """
        for player in self._players:
            print "Dealing 2 cards to Player", player.name()
            player.receive_card(self._deck.remove_card())
            player.receive_card(self._deck.remove_card())

    def deal_rest(self):
        """ method to deal the rest of three cards to players """
        for time in range(3):
            for player in self._players:
                print "Dealing the {0}th card to Player {1}".format(str(time + 3), player.name())
                player.receive_card(self._deck.remove_card())

    def deal_house(self):
        """ Dealing cards to House """
        print "Dealing first card to", self._house.name()
        self._house.receive_card(self._deck.remove_card())
        print "Dealing second card to", self._house.name()
        self._house.receive_card(self._deck.remove_card())
        print "Dealing third card to", self._house.name()
        self._house.receive_card(self._deck.remove_card())
        print "Dealing fourth card to", self._house.name()
        self._house.receive_card(self._deck.remove_card())
        print "Dealing fifth card to", self._house.name()
        self._house.receive_card(self._deck.remove_card())

    def reveal_players(self):
        """ ask players to reveal their hand """
        for player in self._players:
            print "Player {0} reveals their cards:".format(player)
            player.reveal()

    def reveal_house(self):
        """ reveal house's hand """
        print "Revealing House's cards:"
        self._house.reveal()

    def start_game(self):
        """ method to start a game of Poker
            it starts when there are enough Players and the game was not already started """
        if len(self._players) > 2 and (not self._game_on):
            self._game_on = True
            for player in self._players:
                player.start_game()
            self.deal_initial()
            print
            self.deal_rest()
            print
            self.deal_house()
            # now players should put forward some cards to be changed
            # then house does the same
            # then everybody reveals their cards
            self.reveal_players()
            self.reveal_house()
            # then decide who wins
            print "Who won?"

    def reset(self):
        """ method to reset the game of Poker """
        self._players = []
        self._house = PokerPlayer("House")
        self._deck.collect_cards()
        self._deck.shuffle()
        #self._deck.sort()
        #self._deck.print_cards()

if __name__ == "__main__":
    # uhh the next are seen as constants, so I had to uppercase them
    LUKE = PokerPlayer("Luke")
    LEIA = PokerPlayer("Leia")
    OBI = PokerPlayer("Obi Wan")
    R2D2 = PokerPlayer("R2D2")

    YODA = PokerDealer()

    YODA.add_player(LUKE)
    YODA.add_player(LEIA)
    YODA.add_player(OBI)
    YODA.add_player(R2D2)

    YODA.start_game()
    #YODA.reset()
