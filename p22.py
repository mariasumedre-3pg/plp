""" Python script to implement P2 of Phase 2 of Python Learning Program
    This is the Poker game with classes and stuff """
from __future__ import unicode_literals
from random import shuffle

COLORS = ["heart",
          "spade",
          "club",
          "star"]

class Suite(object):
    """ enum like thing for the suites in a  deck """
    HEARTS = 'Heart'
    SPADE = 'Spade'
    CLUB = 'Club'
    DIAMOND = 'Diamond'
    # HEARTS = '\N{Black Heart Suit}'
    # SPADE = '\N{Black Spade Suit}'
    # CLUB = '\N{Black Club Suit}'
    # DIAMOND = '\N{Black Diamond Suit}'

class Card(object):
    """ Card class models a card from the 52 card deck (used for e.g. in Poker)
        Each card has a color (or shape) and a value - a number """
    def __init__(self, value=10, color=None):
        """ constructor for the Card class
            expects a value for the Card and a type/color """
        self._value = value
        self._color = color or Suite.HEARTS

    def color(self):
        """ getter for the color/shape/type of the card """
        return self._color

    def value(self):
        """ getter for the value of the card """
        return self._value

    def __repr__(self):
        """ override representation as this is used in displaying players' cards """
        return "Card(value={value}, color='{color}')".format(
            value=self._value,
            color=self._color
        )

    def __str__(self):
        """ value gets printed as is, but over 10 we have ace, jack, queen, king """
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
            # order by color, so all colors stick together
            # and then by number, though here, ace will be less than jack or queen or king
            if self._color == obj.color():
                result = self._value - obj.value()
            else:
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

    def __iter__(self):
        return iter(self._cards)

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

    def __repr__(self):
        return repr(self._cards)

    def print_cards(self):
        """ print/show cards in deck """
        for card in self._cards:
            print card


class PokerPlayer(object):
    """ PokerPlayer class models the Poker players, who expect cards from PokerDealer """
    def __init__(self, name="Ion Popescu", money=1000):
        self._name = name
        self._cards = []
        self._money = money

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

    def collect_money(self, total):
        """ collect money in case of winning, add to total player's money"""
        self._money += total

    def action(self, pot):
        """ return check, call, raise or fold
            some algorithm to bet/play """
        result = ("call", pot)
        if pot > self._money:
            result = ("check", 0)
        return result

    def __repr__(self):
        return self._name


class PokerDealer(object):
    """ Dealer class that handles a Deck, and gives cards to the players """
    def __init__(self):
        self._deck = Deck(full=True)
        self._players = []
        self._game_on = False

    def add_player(self, player):
        """ method to add players to the game, before the game starts """
        if not self._game_on:
            self._players.append(player)
        else:
            print "Players cannot join while a game is ongoing"

    def deal_hole(self):
        """ method to deal the initial 2 cards """
        for player in self._players:
            print "Dealing 3 cards to Player", player.name()
            player.receive_card(self._deck.remove_card())
            player.receive_card(self._deck.remove_card())
            player.receive_card(self._deck.remove_card())

    def deal_turn(self):
        """ method to deal the fourth card to players """
        for player in self._players:
            print "Dealing the turn card to Player", player
            player.receive_card(self._deck.remove_card())

    def deal_river(self):
        """ method to deal the fifth card to players """
        for player in self._players:
            print "Dealing the river card to Player", player
            player.receive_card(self._deck.remove_card())

    def reveal_players(self):
        """ ask players to reveal their hand """
        for player in self._players:
            print "Player {0} reveals their cards:".format(player)
            player.reveal()

    def _bet_round(self, pot=5, total=0):
        """ a betting round in which players call, raise, check of fold """
        for player in self._players[:]:
            result, amount = player.action(pot)
            print "Player {0} has {1}ed".format(player, result)
            if result == "call":
                total += 5
            elif result == "fold":
                self._players.remove(player)
            elif result == "raise":
                if amount > pot:
                    total += amount
                    pot = amount
                else:
                    print "Cannot raise less than the pot"
        return (total, pot)

    def _check_if_game_on(self, total):
        """ check if game is over and we have a winner """
        result = True
        if len(self._players) == 1:
            winner = self._players[0]
            print "We have a winner:", winner
            winner.collect_money(total)
            result = False
        elif not self._players:
            print "All folded, game over without a winner"
            result = False
        return result

    def start_game(self):
        """ method to start a game of Poker
            it starts when there are enough Players and the game was not already started """
        if len(self._players) > 2 and (not self._game_on):
            self._game_on = True
            pot = 5
            total = 0
            for player in self._players:
                player.start_game()
            self.deal_hole()
            # there are some bets
            total, pot = self._bet_round(pot=pot, total=total)
            print

            self._game_on = self._check_if_game_on(total)
            if self._game_on:
                self.deal_turn()
                total, pot = self._bet_round(pot=pot, total=total)
                print "Total is now", total
                print
                self._game_on = self._check_if_game_on(total)
                if self._game_on:
                    self.deal_river()
                    total, pot = self._bet_round(pot=pot, total=total)
                    print "Total is now", total
                    print
                    self._game_on = self._check_if_game_on(total)
                    if self._game_on:
                        self.reveal_players()
                        print "Total is now", total
                        # then decide who wins
                        print "Who won?"
                else:
                    total = 0
                    print
            else:
                total = 0
                print

    def reset(self):
        """ method to reset the game of Poker """
        self._players = []
        self._deck.collect_cards()
        #self._deck.shuffle()
        self._deck.sort()
        self._deck.print_cards()

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
