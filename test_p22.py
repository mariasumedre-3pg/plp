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

def test_deck():
    """ test the Deck class - which will hold one deck of 52 cards for poker """
    tested = p22.Deck(False)
    assert tested.cards == []
    #assert tested.remove_card() is None

    tested = p22.Deck(True)
    same = p22.Deck()
    assert tested != same
    assert tested.sort() == same.sort()

    # 4 colors, each color has 13 cards
    assert len([x for x in tested if x.color() == 'hearts']) == 13
    assert len([x for x in tested if x.color() == 'spades']) == 13
    assert len([x for x in tested if x.color() == 'clubs']) == 13
    assert len([x for x in tested if x.color() == 'diamonds']) == 13

