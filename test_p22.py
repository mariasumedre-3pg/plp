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

