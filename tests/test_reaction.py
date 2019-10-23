#!/usr/bin/env python3
"""
Copyright Samuel Lloyd
s1887484, 22/10/2019
samueljohnlloyd12@gmail.com

Parameters
----------

Return
------
"""

from rates.reaction import Reaction, ReaclibReaction, KadonisReaction
from rates.isotope import Isotope


reactions = [
    [["n"], ["p"]],
    [["n", "p"], ["d"]],
    [["d", "d"], ["n", "he3"]],
    [["he3", "he3"], ["p", "p", "he4"]],
    [["he4", "he4", "he4"], ["c12"]],
]

strings = [
    "n -> p",
    "n+p -> d",
    "d+d -> n+he3",
    "he3+he3 -> p+p+he4",
    "he4+he4+he4 -> c12",
]

n_captures = ['c12', 'c13', 'n15']
n_capture_reactions = ['n1+C12 -> C13',
'n1+C13 -> C14',
'n1+N15 -> N16']


class TestReaction:
    def test_init(self):
        for r, s in zip(reactions, strings):
            reaction = Reaction(r[0], r[1])

            assert str(reaction) == s


class TestReaclibReaction:
    pass


class TestKadonisReaction:
    def test_init(self):
        for n, r in zip(n_captures, n_capture_reactions):
            reaction = KadonisReaction(n, rr=[1.]*12, err=[.0]*12, label='Test')

            assert str(reaction) == r

