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
import pytest

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
    "d+d -> n+He3",
    "He3+He3 -> p+p+He4",
    "He4+He4+He4 -> C12",
]

n_captures = ["c12", "c13", "n15"]
n_capture_reactions = ["n+C12 -> C13", "n+C13 -> C14", "n+N15 -> N16"]


class TestReaction:
    def test_init(self):
        for r, s in zip(reactions, strings):
            reaction = Reaction(r[0], r[1])

            assert str(reaction) == s


class TestReaclibReaction:
    def test_init(self):
        for r, s in zip(reactions, strings):
            reaction = ReaclibReaction(r[0], r[1], a_rates=[1] * 7, label="Test")

            assert str(reaction) == s
            assert reaction.label == "Test"
            assert reaction.rate(0.3) == 307.0581685280525

    def test_reaclib_factory(self):
        assert (
            ReaclibReaction.reaclib_factory(
                1, ["n", "p"], a_rates=[0, 0, 0, 0, 0]
            ).__str__()
            == "n -> p"
        )

        assert (
            ReaclibReaction.reaclib_factory(
                11, ["fe45", "p", "p", "p", "ti42"], a_rates=[0, 0, 0, 0, 0]
            ).__str__()
            == "Fe45 -> p+p+p+Ti42"
        )


class TestKadonisReaction:
    def test_init(self):
        for n, r in zip(n_captures, n_capture_reactions):
            reaction = KadonisReaction(n, rr=[1.0] * 12, err=[0.0] * 12)

            assert str(reaction) == r

            assert (
                str(KadonisReaction(Isotope(7, 14), rr=[1.0] * 12, err=[0.0] * 12))
                == "n+N14 -> N15"
            )
