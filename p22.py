# -*- coding: utf-8 -*-

""" Python script to implement P2 of Phase 2 of Python Learning Program
    This is the Poker game with classes and stuff """
from __future__ import unicode_literals
from random import shuffle

import itertools
from operator import itemgetter

# HEARTS = u'\N{Black Heart Suit}'
# SPADE = u'\N{Black Spade Suit}'
# CLUB = u'\N{Black Club Suit}'
# DIAMOND = u'\N{Black Diamond Suit}'
class Suite(object):
    """ enum like thing for the suites in a  deck """
    HEARTS = 'hearts'
    SPADE = 'spades'
    CLUB = 'clubs'
    DIAMOND = 'diamonds'

    def __init__(self, name):
        self.name = name

    @classmethod
    def elements(cls):
        return [cls.SPADE,
                cls.HEARTS,
                cls.DIAMOND,
                cls.CLUB]

    def __str__(self):
        table = {
            self.HEARTS: '♥',
            self.SPADE: '♠',
            self.CLUB: '♦',
            self.DIAMOND: '♣',
        }
        pretty = table[self.name.lower()]
        return pretty #.encode('utf8')

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
        return self._value if self._value != 1 else 14

    def __repr__(self):
        """ override representation as this is used in displaying players' cards """
        return "Card(value={value}, color='{color}')".format(
            value=self._value,
            color=self._color
        )

    def __str__(self):
        """ value gets printed as is, but over 10 we have ace, jack, queen, king """
        number = str(self._value)
        if self._value == 1:
            number = "A"
        elif self._value == 11:
            number = "J"
        elif self._value == 12:
            number = "Q"
        elif self._value == 13:
            number = "K"
        #return u"{0} of {1}".format(number, self._color).encode('utf-8').strip()
        #color = u'{}'.format(Suite(self._color))
        card = u"{0}{1}".format(number, Suite(self._color))
        return card

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
        self.cards = []
        if full:
            self.collect_cards()
            self.shuffle()

    def __iter__(self):
        return iter(self.cards)

    def shuffle(self):
        """ shuffle the cards, if any """
        if self.cards:
            shuffle(self.cards)

    def sort(self):
        """ sort the cards, if any """
        if self.cards:
            self.cards = sorted(self.cards)

    def remove_card(self):
        """ remove a Card from the Deck and return it (typically to the player) """
        return self.cards.pop()

    def collect_cards(self):
        """ re-stock the deck to the full 52 cards """
        self.cards = [Card(value, color) for color in Suite.elements() for value in range(1, 14)]

    def __repr__(self):
        return repr(self.cards)

    def print_cards(self):
        """ print/show cards in deck """
        for card in self.cards:
            print card

class PokerHand(object):
    """ class to model a Hand in Poker """
    def __init__(self):
        """ initializes a Hand object which has 5 cards and
            can be compared """
        self.cards = []

    def add_card(self, card):
        """ adds a card to the hand, if there are less than 4 cards in Hand """
        if isinstance(card, Card) and len(self.cards) < 5:
            self.cards.append(card)

    def add_cards(self, cards):
        """ adds more than a card to the hand,
            as long as there will be less then 5 cards in total """
        if isinstance(cards, list) and len(self.cards) + len(cards) <= 5:
            self.cards += cards

    def __iter__(self):
        return iter(self.cards)

    def __str__(self):
        return ' '.join(map(unicode, self.cards))

    # def __repr__(self):
    #     return repr(self.cards)

    def consecutive(self, sorted_cards):
        """ How many cards in hand are consecutive - for straight and straight flush
            It doesn't recognize yet when an ace could be a placeholder for 1 (ace, two, three) """
        result = 0
        # we want to group the consecutive items, so we trick groupby with the lambda:
        # lamba will output the same number for consecutive items, because we substract
        # the value from the index (works the other way too)
        # but the value from the lamba is used only for grouping, the actual elements in the
        # grouping are the ones from sorted_cards (in iterable collections things)
        for val_tuple in itertools.groupby(enumerate(sorted_cards), lambda (i, x): x.value() - i):
            # for each val_tuple we have the card value like a key and a collection of suites
            # e.g.:
            # "i have for 2 a spade and a heart, for ace i have a club, a diamond and a spade"
            temp = len(map(itemgetter(1), val_tuple[1]))
            if temp > result:
                result = temp
        return result

    def group_same_values(self, sorted_cards):
        """ Group together cards with same value, to be used checking for pairs,
            checking for full house, and for four of a kind """
        result = []
        temp = [(x.value(), x.color()) for x in sorted_cards]
        for val, colors in itertools.groupby(temp, itemgetter(0)):
            result.append((val, map(itemgetter(1), colors)))
        return result

    def compute_value2(self):
        """ compute a value for the combination of cards in hand
            there must be 5 cards in hand """
        # so a player will order their cards by number,
        # check if cards are sequential for a straight, or they have pairs
        # or if all colors match
        result = None
        sorted_cards = sorted(self.cards, key=lambda x: x.value())
        if len(self.cards) == 5:
            flush = len([x for x in self.cards if x.color() == self.cards[0].color()]) == 5
            if flush:
                result = "6"
            consec = self.consecutive(sorted_cards)
            if consec == 5: #if all 5 cards are sequential
                if flush:
                    # straight flush, starting with first card in sorted list
                    result = "9" + str(sorted_cards[0].value())
                else:
                    # straight, starting with first card in sorted list
                    result = "5" + str(sorted_cards[0].value())
            else: # we might have pairs
                collection = self.group_same_values(sorted_cards)
                pairs = [x for x in collection if len(x[1]) == 2]
                high = max([x for x in collection if len(x[1]) == 1], key=lambda x: x[0])
                three_of_a_kind = [x for x in collection if len(x[1]) == 3]
                four_of_a_kind = [x for x in collection if len(x[1]) == 4]

                # this is the high card in case we have nothing (reuse the variable)
                high = "1" + chr(ord('a') + high[0])
                result = high
                if len(pairs) == 2:
                    result = "3" + chr(ord('a') + pairs[0][0] + pairs[1][0]) + high
                elif len(pairs) == 1:
                    result = "2" + chr(ord('a') + pairs[0][0]) + high
                if len(three_of_a_kind) == 1:
                    if len(pairs) == 1:
                        result = "7" + chr(ord('a') + three_of_a_kind[0][0] + pairs[0][0])
                    else:
                        result = "4" + chr(ord('a') + three_of_a_kind[0][0]) + high
                if len(four_of_a_kind) == 1:
                    result = "8" + chr(ord('a') + four_of_a_kind[0][0]) + high

        return result

class PokerPlayer(object):
    """ PokerPlayer class models the Poker players, who expect cards from PokerDealer """
    def __init__(self, name="Ion Popescu"):
        self.name = name
        self.cards = []
        self.community = []
        self.hand = []

    def start_game(self, community):
        """ reset the cards
            also ... 'pointer' to community cards"""
        self.cards = []
        self.community = community

    def receive_card(self, card):
        """ save the card from the dealer """
        self.cards.append(card)

    def reveal(self):
        """ Player reveals all cards """
        for card in self.cards:
            print u"I have a {}".format(card)
        #for card in self._community:
        #    print "Community card I could use:", card

    def points(self):
        """ figure out maximum points that can be obtained """
        # this is probably optional
        sorted_community = sorted(self.community, key=lambda x: x.value())
        # combinations of 5 cards taken in groups of 3
        # each player has their fixed 2 cards, we need an aditional 3 to make a hand
        community_comb = itertools.combinations(sorted_community, 3)
        max_points = 0
        max_hand = None # just to print it
        # compute points for each combination, we'll return the max points of the combination
        # (which we'll print)
        for possibility in community_comb:
            hand = PokerHand() # create the hand
            hand.add_cards(self.cards)
            hand.add_cards([card for card in possibility])
            #the simple version that just recognizes the different poker hands
            points = hand.compute_value2()
            if points > max_points:
                max_points = points
                max_hand = hand
        print "Player {name} has best hand {hand}".format(name=self.name, hand=max_hand)
        return max_points

    def __repr__(self):
        return self.name


class PokerDealer(object):
    """ Dealer class that handles a Deck, and gives cards to the players """
    def __init__(self):
        self._deck = Deck(full=True)
        self._players = []
        self._game_on = False
        self.community = []

    def add_player(self, player):
        """ method to add players to the game, before the game starts """
        if not self._game_on:
            self._players.append(player)
        else:
            print "Players cannot join while a game is ongoing"

    def deal_hole(self):
        """ method to deal the initial 2 cards """
        for player in self._players:
            print "Dealing 2 cards to Player", player.name
            player.receive_card(self._deck.remove_card())
            player.receive_card(self._deck.remove_card())

    def deal_flop(self):
        """ method to deal the three cards to community """
        print "Dealing the flop cards"
        for idx in range(1, 4):
            print "Dealing the {0} card to community".format(idx)
            card = self._deck.remove_card()
            self.community.append(card)
            print u"It's a {}".format(card)

    def deal_turn(self):
        """ method to deal the fourth card to placommunityyers """
        print "Dealing the turn card to community"
        card = self._deck.remove_card()
        self.community.append(card)
        print u"It's a {}".format(card)

    def deal_river(self):
        """ method to deal the fifth card to community """
        print "Dealing the river card to community"
        card = self._deck.remove_card()
        self.community.append(card)
        print u"It's a {}".format(card)

    def reveal_players(self):
        """ ask players to reveal their hand """
        for player in self._players:
            print "Player {0} reveals their cards:".format(player)
            player.reveal()

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

            for player in self._players:
                player.start_game(self.community)
            self.deal_hole()
            self.deal_flop()
            self.deal_turn()
            self.deal_river()

            self.reveal_players()
            max_points = 0
            winner = None
            for player in self._players:
                points = player.points()
                if points > max_points:
                    max_points = points
                    winner = player
            print "Who won?"
            print winner


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
