#!/usr/bin/env python3
# coding=utf-8
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

import numpy as np
import matplotlib.pyplot as plt

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

            assert reaction.targets == r[0]
            assert reaction.products == r[1]

            assert str(reaction) == s

    def test_mpl_plot(self):
        assert (
            str(Reaction(["n"], ["p"]).mpl_plot())
            == "AxesSubplot(0.125,0.11;0.775x0.77)"
        )

    def test_eq(self):
        assert Reaction(["n", "p"], ["d"]) == Reaction(["n", "p"], ["d"])

        assert Reaction(["n", "p"], ["d"]) != Reaction(["p", "p"], ["d"])

    def test_eg_notimplemented(self):
        with pytest.raises(NotImplementedError):
            Reaction(["n", "p"], ["d"]) == "str"


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

    def test_reaclib_factory_exception(self):
        with pytest.raises(Exception):
            ReaclibReaction.reaclib_factory(
                12, ["fe45", "p", "p", "p", "ti42"], a_rates=[0, 0, 0, 0, 0]
            )

    def test_reaclib_mpl_plot(self):
        r = (
            ReaclibReaction.reaclib_factory(
                1, ["n", "p"], a_rates=[1, 1, 1, 1, 1, 1, 1], label="Test"
            )
            .mpl_plot()
            .lines[0]
            .get_xydata()
        )

        assert np.mean(r) == 1.9733072490132147e24
        assert np.max(r) == 1.3063924607895084e27
        assert np.min(r) == 0.1

        plt.clf()

        r = (
            ReaclibReaction.reaclib_factory(
                1, ["n", "p"], a_rates=[1, 1, 1, 1, 1, 1, 1], label="Test"
            )
            .mpl_plot(temp_unit="KeV")
            .lines[0]
            .get_xydata()
        )

        assert np.mean(r) == 1.9733072490132147e24
        assert np.max(r) == 1.3063924607895084e27
        assert np.min(r) == 8.61733929308519

        plt.clf()


class TestKadonisReaction:
    def test_init(self):
        for n, r in zip(n_captures, n_capture_reactions):
            reaction = KadonisReaction(n, rr=[1.0] * 12, err=[0.0] * 12)

            assert str(reaction) == r

            assert (
                str(KadonisReaction(Isotope(7, 14), rr=[1.0] * 12, err=[0.0] * 12))
                == "n+N14 -> N15"
            )

    def test_kadonis_rate(self):
        rk = KadonisReaction("c12", [1] * 12, [1] * 12)
        assert rk.rate(temp=30) == 1

    def test_kadonis_error(self):
        rk = KadonisReaction("c12", [1] * 12, [1] * 12)
        assert rk.error(temp=30) == 1

    def test_kadonis_diff(self):
        rk1 = KadonisReaction("c12", [1] * 12, [1] * 12)
        rk2 = KadonisReaction("c12", [2] * 12, [2] * 12)
        assert rk1.diff(rk2).rr == KadonisReaction("c12", [-1] * 12, [-1] * 12).rr

    def test_kadonis_diff_exception(self):
        with pytest.raises(Exception):
            rk1 = KadonisReaction("c13", [1] * 12, [1] * 12)
            rk2 = KadonisReaction("c12", [2] * 12, [2] * 12)

            rk1.diff(rk2)

    def test_kadonis_mpl_plot(self):
        rk = KadonisReaction("c12", [1] * 12, [1] * 12).mpl_plot().lines[0].get_xydata()

        assert np.mean(rk) == 0.7141999137499999
        assert np.max(rk) == 1.1604510000000001
        assert np.min(rk) == 0.05802255

        plt.clf()

        rk = (
            KadonisReaction("c12", [1] * 12, [1] * 12)
            .mpl_plot(temp_unit="KeV")
            .lines[0]
            .get_xydata()
        )

        assert np.mean(rk) == 18.958333333333332
        assert np.max(rk) == 100.0
        assert np.min(rk) == 1.0

        plt.clf()
