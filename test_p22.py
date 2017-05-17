# -*- coding: utf-8 -*-
""" Add unit-tests for p22, the Poker problem here
    We exercise this way how modules work
    And the p22.py doesn't get any more lines """

import p22

# test the Card class
def test_card_default_values():
    """ test the Card class """
    tested = p22.Card()
    assert unicode(tested) == u"10♥"
    assert repr(tested) == "Card(value=10, color='hearts')"

    #copy = eval(repr(tested))
    #assert copy == tested
    copy = tested
    assert unicode(copy) == u"10♥"
    assert repr(copy) == "Card(value=10, color='hearts')"

    # test when color is set to hearts by default
    tested = p22.Card(value=1)
    assert unicode(tested) == u"A♥"
    tested = p22.Card(value=11)
    assert unicode(tested) == u"J♥"
    tested = p22.Card(value=12)
    assert unicode(tested) == u"Q♥"
    tested = p22.Card(value=13)
    assert unicode(tested) == u"K♥"
    tested = p22.Card(value=7)
    assert unicode(tested) == u"7♥"

    # test when value is put to 10 by default
    tested = p22.Card(color='hearts')
    assert unicode(tested) == u"10♥"
    tested = p22.Card(color='spades')
    assert unicode(tested) == u"10♠"
    tested = p22.Card(color='clubs')
    assert unicode(tested) == u"10♣"
    tested = p22.Card(color='diamonds')
    assert unicode(tested) == u"10♦"

    tested = p22.Card()
    assert tested == p22.Card(color='hearts', value=10)

def test_card2():
    """ test the functionality of Card class """
    # test all possbile correct values
    suites_dict = {'hearts':u'♥', 'spades':u'♠', 'clubs':u'♣', 'diamonds':u'♦'}
    for key in suites_dict:
        val = suites_dict[key]
        tested = p22.Card(value=1, color=key)
        assert unicode(tested) == (u"A" + val)
        tested = p22.Card(value=11, color=key)
        assert unicode(tested) == (u"J" + val)
        tested = p22.Card(value=12, color=key)
        assert unicode(tested) == (u"Q" + val)
        tested = p22.Card(value=13, color=key)
        assert unicode(tested) == (u"K" + val)
    for key in suites_dict:
        val = suites_dict[key]
        for number in range(2, 11):
            tested = p22.Card(value=number, color=key)
            assert unicode(tested) == (unicode(number) + val)
    # test out of bounds value
    tested = p22.Card(value=23)
    exp = p22.Card(value=1)
    assert tested.value() == exp.value()
    tested = p22.Card(value=-12)
    assert tested.value() == exp.value()

def test_player():
    """ test the Player class """
    tested = p22.PokerPlayer()
    # default name
    assert tested.name == "Ion Popescu"
    # change the name
    tested.name = "Vasile"
    assert tested.name == "Vasile"
    # name is also the str
    assert str(tested) == "Vasile"
    # empty cards at start
    assert tested.cards == []
    tested.receive_card(p22.Card())
    assert len(tested.cards) == 1
    assert tested.cards[0] == p22.Card()
    for item in range(1, 5):
        tested.receive_card(p22.Card(value=item))
    assert len(tested.cards) == 5
    assert tested.hand == []
    tested.receive_card(p22.Card(value=12))
    assert len(tested.cards) == 5

def test_deck():
    """ test the Deck class - which will hold one deck of 52 cards for poker """
    tested = p22.Deck(False)
    assert tested.cards == []
    #assert tested.remove_card() is None

    tested = p22.Deck(True)
    same = p22.Deck()
    # there might be a chance in a million for the shuffled decks to be the same
    assert tested != same
    assert tested.sort() == same.sort()

    # 4 colors, each color has 13 cards
    assert len([x for x in tested if x.color() == 'hearts']) == 13
    assert len([x for x in tested if x.color() == 'spades']) == 13
    assert len([x for x in tested if x.color() == 'clubs']) == 13
    assert len([x for x in tested if x.color() == 'diamonds']) == 13

def test_hand_alg_pairs():
    """ test the algorithms of the hand - pairs, one or two"""
    hand1 = p22.PokerHand()
    hand2 = p22.PokerHand()
    assert hand1.cards == []
    assert hand2.cards == []

    # test a pair versus a higher pair
    hand1.add_card(p22.Card(value=4, color='hearts'))
    hand1.add_card(p22.Card(value=4, color='spades'))
    hand1.add_card(p22.Card(value=2, color='spades'))
    hand1.add_card(p22.Card(value=10, color='spades'))
    hand1.add_card(p22.Card(value=12, color='spades'))

    hand2.add_card(p22.Card(value=5, color='hearts'))
    hand2.add_card(p22.Card(value=5, color='spades'))
    hand2.add_card(p22.Card(value=2, color='clubs'))
    hand2.add_card(p22.Card(value=10, color='hearts'))
    hand2.add_card(p22.Card(value=12, color='diamonds'))

    higher = hand2.compute_value2()
    lower = hand1.compute_value2()
    assert higher > lower

    # test same pair, one high card making the difference
    hand1.cards[0]._value = 5
    hand1.cards[1]._value = 5
    hand1.cards[4]._value = 13
    higher = hand1.compute_value2()
    lower = hand2.compute_value2()
    assert higher > lower

    # test 2 pairs vs a pair
    hand2.cards[3]._value = 2
    higher = hand2.compute_value2()
    lower = hand1.compute_value2()
    assert higher > lower

    # test 2 pairs vs 2 pairs, one high card making the difference
    hand1.cards[3]._value = 2
    higher = hand1.compute_value2()
    lower = hand2.compute_value2()
    assert higher > lower

    # test 2 pairs vs 2 pairs
    hand2.cards[3]._value = 3
    hand2.cards[2]._value = 3
    higher = hand2.compute_value2()
    lower = hand1.compute_value2()
    assert higher > lower

def test_hand_alg_three_of_a_kind():
    """ test the algorithms of the hand - three of a kind """
    # test three of a kind, reset tested stuff
    hand1 = p22.PokerHand()
    hand2 = p22.PokerHand()
    hand1.add_card(p22.Card(value=4, color='hearts'))
    hand1.add_card(p22.Card(value=4, color='spades'))
    hand1.add_card(p22.Card(value=4, color='clubs'))
    hand1.add_card(p22.Card(value=10, color='spades'))
    hand1.add_card(p22.Card(value=12, color='spades'))

    hand2.add_card(p22.Card(value=5, color='hearts'))
    hand2.add_card(p22.Card(value=5, color='spades'))
    hand2.add_card(p22.Card(value=5, color='clubs'))
    hand2.add_card(p22.Card(value=10, color='hearts'))
    hand2.add_card(p22.Card(value=11, color='diamonds'))
    higher = hand2.compute_value2()
    lower = hand1.compute_value2()
    assert higher > lower

    # test three of a kind, high card makes the difference
    hand1.cards[0]._value = 5
    hand1.cards[1]._value = 5
    hand1.cards[2]._value = 5
    higher = hand1.compute_value2()
    lower = hand2.compute_value2()
    assert higher > lower

def test_hand_alg_straight():
    """ test the algorithms of the hand - straight """
    # test straight, reset tested stuff
    hand1 = p22.PokerHand()
    hand2 = p22.PokerHand()
    hand1.add_card(p22.Card(value=4, color='hearts'))
    hand1.add_card(p22.Card(value=5, color='spades'))
    hand1.add_card(p22.Card(value=6, color='clubs'))
    hand1.add_card(p22.Card(value=7, color='spades'))
    hand1.add_card(p22.Card(value=8, color='spades'))

    hand2.add_card(p22.Card(value=4, color='spades'))
    hand2.add_card(p22.Card(value=5, color='hearts'))
    hand2.add_card(p22.Card(value=6, color='diamonds'))
    hand2.add_card(p22.Card(value=7, color='clubs'))
    hand2.add_card(p22.Card(value=8, color='diamonds'))
    same1 = hand1.compute_value2()
    same2 = hand2.compute_value2()
    assert same1 == same2

    # different straights
    hand2.cards[0]._value = 9
    higher = hand2.compute_value2()
    lower = hand1.compute_value2()
    assert higher > lower

    # straight beats three of a kind
    hand2 = p22.PokerHand()
    hand2.add_card(p22.Card(value=5, color='hearts'))
    hand2.add_card(p22.Card(value=5, color='spades'))
    hand2.add_card(p22.Card(value=5, color='clubs'))
    hand2.add_card(p22.Card(value=10, color='hearts'))
    hand2.add_card(p22.Card(value=11, color='diamonds'))
    higher = hand1.compute_value2()
    lower = hand2.compute_value2()
    assert higher > lower

def test_hand_alg_flush():
    """ test the algorithms of the hand - flush """
    # test flush
    hand1 = p22.PokerHand()
    hand2 = p22.PokerHand()
    hand1.add_card(p22.Card(value=4, color='hearts'))
    hand1.add_card(p22.Card(value=5, color='hearts'))
    hand1.add_card(p22.Card(value=6, color='hearts'))
    hand1.add_card(p22.Card(value=7, color='hearts'))
    hand1.add_card(p22.Card(value=8, color='hearts'))

    hand2.add_card(p22.Card(value=4, color='spades'))
    hand2.add_card(p22.Card(value=5, color='spades'))
    hand2.add_card(p22.Card(value=6, color='spades'))
    hand2.add_card(p22.Card(value=7, color='spades'))
    hand2.add_card(p22.Card(value=8, color='spades'))
    same1 = hand1.compute_value2()
    same2 = hand2.compute_value2()
    assert same1 == same2

    # flush beats straight
    hand1 = p22.PokerHand()
    hand1.add_card(p22.Card(value=4, color='spades'))
    hand1.add_card(p22.Card(value=5, color='diamonds'))
    hand1.add_card(p22.Card(value=6, color='diamonds'))
    hand1.add_card(p22.Card(value=7, color='clubs'))
    hand1.add_card(p22.Card(value=8, color='diamonds'))
    higher = hand2.compute_value2()
    lower = hand1.compute_value2()
    assert higher > lower

    # flush beats three of a kind
    hand1 = p22.PokerHand()
    hand1.add_card(p22.Card(value=4, color='diamonds'))
    hand1.add_card(p22.Card(value=4, color='spades'))
    hand1.add_card(p22.Card(value=4, color='clubs'))
    hand1.add_card(p22.Card(value=10, color='spades'))
    hand1.add_card(p22.Card(value=12, color='spades'))
    higher = hand2.compute_value2()
    lower = hand1.compute_value2()
    assert higher > lower

def test_hand_alg_full_house():
    """ test the algorithms of the hand - full house """
    # full house
    hand1 = p22.PokerHand()
    hand2 = p22.PokerHand()
    hand2.add_card(p22.Card(value=4, color='hearts'))
    hand2.add_card(p22.Card(value=4, color='spades'))
    hand2.add_card(p22.Card(value=4, color='clubs'))
    hand2.add_card(p22.Card(value=7, color='hearts'))
    hand2.add_card(p22.Card(value=7, color='spades'))

    hand1.add_card(p22.Card(value=5, color='spades'))
    hand1.add_card(p22.Card(value=5, color='hearts'))
    hand1.add_card(p22.Card(value=5, color='clubs'))
    hand1.add_card(p22.Card(value=4, color='spades'))
    hand1.add_card(p22.Card(value=4, color='clubs'))
    higher = hand1.compute_value2()
    lower = hand2.compute_value2()
    assert higher > lower

    # full house with same 3 cards
    hand1 = p22.PokerHand()
    hand2 = p22.PokerHand()
    hand2.add_card(p22.Card(value=5, color='hearts'))
    hand2.add_card(p22.Card(value=5, color='spades'))
    hand2.add_card(p22.Card(value=5, color='clubs'))
    hand2.add_card(p22.Card(value=7, color='hearts'))
    hand2.add_card(p22.Card(value=7, color='spades'))

    hand1.add_card(p22.Card(value=5, color='hearts'))
    hand1.add_card(p22.Card(value=5, color='spades'))
    hand1.add_card(p22.Card(value=5, color='clubs'))
    hand1.add_card(p22.Card(value=6, color='spades'))
    hand1.add_card(p22.Card(value=6, color='clubs'))
    higher = hand2.compute_value2()
    lower = hand1.compute_value2()
    assert higher > lower

def test_hand_alg_four_of_a_kind():
    """ test the algorithms of the hand - four of a kind """
    # four of a kind vs full house
    hand2 = p22.PokerHand()
    hand2.add_card(p22.Card(value=5, color='hearts'))
    hand2.add_card(p22.Card(value=5, color='spades'))
    hand2.add_card(p22.Card(value=5, color='clubs'))
    hand2.add_card(p22.Card(value=7, color='hearts'))
    hand2.add_card(p22.Card(value=7, color='spades'))

    hand1 = p22.PokerHand()
    hand1.add_card(p22.Card(value=5, color='hearts'))
    hand1.add_card(p22.Card(value=5, color='spades'))
    hand1.add_card(p22.Card(value=5, color='clubs'))
    hand1.add_card(p22.Card(value=5, color='diamonds'))
    hand1.add_card(p22.Card(value=6, color='clubs'))
    higher = hand1.compute_value2()
    lower = hand2.compute_value2()
    assert higher > lower

    # two four of a kind
    hand2 = p22.PokerHand()
    hand2.add_card(p22.Card(value=7, color='hearts'))
    hand2.add_card(p22.Card(value=7, color='spades'))
    hand2.add_card(p22.Card(value=7, color='clubs'))
    hand2.add_card(p22.Card(value=7, color='diamonds'))
    hand2.add_card(p22.Card(value=12, color='spades'))
    higher = hand2.compute_value2()
    lower = hand1.compute_value2()
    assert higher > lower

    # two same four of a kind, wins the one with the high card
    hand1 = p22.PokerHand()
    hand1.add_card(p22.Card(value=7, color='hearts'))
    hand1.add_card(p22.Card(value=7, color='spades'))
    hand1.add_card(p22.Card(value=7, color='clubs'))
    hand1.add_card(p22.Card(value=7, color='diamonds'))
    hand1.add_card(p22.Card(value=1, color='clubs'))
    higher = hand1.compute_value2()
    lower = hand2.compute_value2()
    assert higher > lower

def test_hand_alg_straight_flush():
    """ test the algorithms of the hand - straight flush """
    hand1 = p22.PokerHand()
    hand1.add_card(p22.Card(value=7, color='hearts'))
    hand1.add_card(p22.Card(value=8, color='hearts'))
    hand1.add_card(p22.Card(value=9, color='hearts'))
    hand1.add_card(p22.Card(value=10, color='hearts'))
    hand1.add_card(p22.Card(value=11, color='hearts'))

    hand2 = p22.PokerHand()
    hand2.add_card(p22.Card(value=8, color='spades'))
    hand2.add_card(p22.Card(value=9, color='spades'))
    hand2.add_card(p22.Card(value=10, color='spades'))
    hand2.add_card(p22.Card(value=11, color='spades'))
    hand2.add_card(p22.Card(value=12, color='spades'))
    higher = hand2.compute_value2()
    lower = hand1.compute_value2()
    assert higher > lower

    # that which doesn't work: ace does not count as 1
    hand2 = p22.PokerHand()
    hand2.add_card(p22.Card(value=1, color='spades'))
    hand2.add_card(p22.Card(value=2, color='spades'))
    hand2.add_card(p22.Card(value=3, color='spades'))
    hand2.add_card(p22.Card(value=4, color='spades'))
    hand2.add_card(p22.Card(value=5, color='spades'))
    higher = hand1.compute_value2()
    lower = hand2.compute_value2()
    assert higher > lower

    # that which does work: ace does count as 14
    hand2 = p22.PokerHand()
    hand2.add_card(p22.Card(value=13, color='spades'))
    hand2.add_card(p22.Card(value=1, color='spades'))
    hand2.add_card(p22.Card(value=10, color='spades'))
    hand2.add_card(p22.Card(value=11, color='spades'))
    hand2.add_card(p22.Card(value=12, color='spades'))
    higher = hand2.compute_value2()
    lower = hand1.compute_value2()
    assert higher > lower
