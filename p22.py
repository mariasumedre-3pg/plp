""" Python script to implement P2 of Phase 2 of Python Learning Program
    This is the Poker game with classes and stuff """
from __future__ import unicode_literals
from random import shuffle

import itertools
from operator import itemgetter

SUITES = [u'\N{Black Heart Suit}',
          u'\N{Black Spade Suit}',
          u'\N{Black Club Suit}',
          u'\N{Black Diamond Suit}']

class Suite(object):
    """ enum like thing for the suites in a  deck """
    #HEARTS = 'Heart'
    #SPADE = 'Spade'
    #CLUB = 'Club'
    #DIAMOND = 'Diamond'
    HEARTS = u'\N{Black Heart Suit}'
    SPADE = u'\N{Black Spade Suit}'
    CLUB = u'\N{Black Club Suit}'
    DIAMOND = u'\N{Black Diamond Suit}'

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
        ).encode("utf-8")

    def __str__(self):
        """ value gets printed as is, but over 10 we have ace, jack, queen, king """
        # there are also unicode characters for the actual cards, starting with U+1F0A
        # that would be fun to try :D
        number = str(self._value)
        if self._value == 1:
            number = "ace"
        elif self._value == 11:
            number = "jack"
        elif self._value == 12:
            number = "queen"
        elif self._value == 13:
            number = "king"
        return u"{0} of {1}".format(number, self._color).encode('utf-8').strip()

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
        self._cards = [Card(value, color) for color in SUITES for value in range(1, 14)]

    def __repr__(self):
        return repr(self._cards)

    def print_cards(self):
        """ print/show cards in deck """
        for card in self._cards:
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
        return u''.join(self.cards)

    def __repr__(self):
        return repr(self.cards)

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

    def compute_a_key(self):
        """ Make a number out of the cards in hand to figure out a player's points
            This must be fine-tuned as for now it just recognizes the big categories
            """
        result = 1 #nothing or high card means 1

        flush = False
        straight = False
        one_pair = False
        three_of_a_kind = False

        sorted_cards = sorted(self.cards, key=lambda x: x.value())
        #sorted_cards = sorted(self.cards, key=lambda x: x.color())

        if len(self.cards) == 5:
            collection = self.group_same_values(sorted_cards)
            more_of_a_kind = [len(x[1]) for x in collection]

            # test for a pair
            if 2 in more_of_a_kind:
                one_pair = True
                result = 2

            # test for two pairs
            if len([x for x in more_of_a_kind if x == 2]) == 2:
                result = 3

            # test for three of a kind
            if 3 in more_of_a_kind:
                three_of_a_kind = True
                result = 4

            # test for straight
            consec = self.consecutive(sorted_cards)
            if consec == 5:
                result = 5
                straight = True

            # test for flush:
            f_heart = sum(itertools.imap(lambda x: x.color() == Suite.HEARTS, self.cards)) == 5
            f_club = sum(itertools.imap(lambda x: x.color() == Suite.CLUB, self.cards)) == 5
            f_diamond = sum(itertools.imap(lambda x: x.color() == Suite.DIAMOND, self.cards)) == 5
            f_spade = sum(itertools.imap(lambda x: x.color() == Suite.SPADE, self.cards)) == 5
            if f_heart or f_club or f_diamond or f_spade:
                result = 6
                flush = True

            # test for full house
            if one_pair and three_of_a_kind:
                result = 7

            #test for four of a kind
            if 4 in more_of_a_kind:
                result = 8

            # test for straight flush
            if straight and flush:
                result = 9

        return result

class PokerPlayer(object):
    """ PokerPlayer class models the Poker players, who expect cards from PokerDealer """
    def __init__(self, name="Ion Popescu", money=1000):
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
            print "I have a", card
        #for card in self._community:
        #    print "Community card I could use:", card

    def points(self):
        """ figure out maximum points that can be obtained """
        sorted_community = sorted(self.community, key=lambda x: x.value())
        community_comb = itertools.combinations(sorted_community, 3)
        max_points = 0
        for possibility in community_comb:
            hand = PokerHand()
            hand.add_cards(self.cards)
            hand.add_cards([card for card in possibility])
            points = hand.compute_a_key()
            if points > max_points:
                max_points = points
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
            print "It's a", card

    def deal_turn(self):
        """ method to deal the fourth card to placommunityyers """
        print "Dealing the turn card to community"
        card = self._deck.remove_card()
        self.community.append(card)
        print "It's a", card

    def deal_river(self):
        """ method to deal the fifth card to community """
        print "Dealing the river card to community"
        card = self._deck.remove_card()
        self.community.append(card)
        print "It's a", card

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
