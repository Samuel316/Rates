#!/usr/bin/env python3
# coding=utf-8
"""
Copyright Samuel Lloyd
s1887484, 23/10/2019
samueljohnlloyd12@gmail.com

Parameters
----------

Return
------
"""

import pytest

from pathlib import Path

from rates.reaction import Reaction
from rates.reaclib_file import Reaclib

reaclib_mock_file = {
    "Chapter": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    "E0": ["n", "d", "he6", "n", "d", "p", "t", "n", "n", "n", "b17"],
    "E1": ["p", "n", "n", "p", "d", "d", "li7", "n", "p", "n", "n"],
    "E2": ["", "p", "n", "d", "n", "n", "n", "he4", "p", "he4", "n"],
    "E3": ["", "", "he4", "", "he3", "p", "n", "he6", "p", "he4", "n"],
    "E4": ["", "", "", "", "", "p", "he4", "", "d", "t", "c14"],
    "E5": ["", "", "", "", "", "", "he4", "", "", "li7", ""],
    "SetLabel": [
        "wc12",
        "an06",
        "cf88",
        "an06",
        "de04",
        "cf88",
        "mafo",
        "cf88",
        "cf88",
        "mafo",
        "wc12",
    ],
    "RateType": ["w", "n", "r", "n", "n", "n", "n", "r", "n", "n", "w"],
    "ReverseRate": ["", "v", "v", "", "", "v", "", "", "", "v", ""],
    "QValue": [
        0.7823,
        -2.22457,
        -0.975,
        2.22457,
        3.269,
        -2.225,
        8.86442,
        0.975,
        2.225,
        -8.86442,
        16.5362,
    ],
    "Rate": [
        [-6.78161, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [33.0154, -25.815, 0.0, -2.30472, -0.887862, 0.137663, 1.5],
        [22.178, -20.8994, 0.694279, -3.33326, 0.507932, -0.0427342, 2.0],
        [8.84688, 0.0, 0.0, -0.0102082, -0.0893959, 0.00696704, 1.0],
        [19.75, 0.0, -4.2586, 0.733469, 0.171825, -0.0310515, -0.666667],
        [17.3271, -25.82, -3.72, 0.946313, 0.105406, -0.0149431, 0.0],
        [
            27.5043,
            -5.31692e-12,
            -11.333,
            -2.24192e-09,
            2.21773e-10,
            -1.83941e-11,
            -0.666667,
        ],
        [-23.9322, -9.585, 0.694279, -3.33326, 0.507932, -0.0427342, -1.0],
        [-4.24034, 0.0, -3.72, 0.946313, 0.105406, -0.0149431, -1.5],
        [
            -17.4199,
            -102.867,
            -11.333,
            -2.24192e-09,
            2.21773e-10,
            -1.83941e-11,
            -3.66667,
        ],
        [1.56352, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    ],
}

reaclib_path = Path(__file__).parent


class TestReaclib:
    def test_read_file(self):
        reaclib = Reaclib.read_file((reaclib_path / "reaclib_mock"))

        assert isinstance(reaclib, Reaclib)

        for column, data in reaclib_mock_file.items():
            for i, d in enumerate(data):
                assert reaclib.df[column].iloc[i] == d

    def test_default_file(self):
        Reaclib()

    reaclib = Reaclib.read_file((reaclib_path / "reaclib_mock"))

    def test_get_n_gamma(self):

        assert self.reaclib.get_n_gamma("p") == Reaction(["n", "p"], ["d"])

        with pytest.raises(Exception):
            assert self.reaclib.get_n_gamma("HE6")
