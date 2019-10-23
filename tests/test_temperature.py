#!/usr/bin/env python3
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

from rates.temperature import Temperature


class TestTemperature:

    def test_gk_input(self):
        temp = Temperature(0.3)

        assert temp.gk == 0.3
        assert temp.unit == 'Gk'
        assert temp.kev == 25.852017879255563

    def test_kev_input(self):
        temp = Temperature(30, 'KeV')

        assert temp.kev == 30
        assert temp.gk == 0.3481353

    def test_false_unit(self):
        with pytest.raises(Exception):
            Temperature(10, 'k')

            Temperature(10, 'z')


if __name__ == "__main__":
    print(Temperature(0.3).kev)
