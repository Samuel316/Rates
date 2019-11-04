#!/usr/bin/env python3
# coding=utf-8
"""
Copyright Samuel Lloyd
s1887484, 21/10/2019
samueljohnlloyd12@gmail.com

Parameters
----------

Return
------
"""
import pytest
import numpy as np

from rates.temperature import Temperature


class TestTemperature:
    def test_gk_input(self):
        temp = Temperature(0.3)

        assert temp.gk == 0.3
        assert temp.unit == "Gk"
        assert temp.kev == 25.852017879255563

    def test_kev_input(self):
        temp = Temperature(30, "KeV")

        assert temp.kev == 30
        assert temp.gk == 0.3481353

    def test_false_unit(self):
        with pytest.raises(Exception):
            Temperature(10, "k")
        with pytest.raises(Exception):
            Temperature(10, "z")

    def test_array_input(self):
        temp = np.logspace(-1, 1, 10)
        assert list(Temperature(temp).kev) == [
            8.61733929308519,
            14.374588304030578,
            23.978258471983086,
            39.998145838236844,
            66.72092855976918,
            111.29721677303773,
            185.65494708797556,
            309.69111697130046,
            516.5959185859126,
            861.7339293085188,
        ]
