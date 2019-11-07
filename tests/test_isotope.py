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

from rates.isotope import Isotope


class TestIsotope:

    ppn_outputs = ["PROT ", "NEUT ", "MG 28", "O  16", "TAg80", "HF*80"]
    isotopes = [(1, 1), (0, 1), (12, 28), (8, 16), (73, 180), (72, 180)]
    isomers = [False, False, False, False, True, True]

    names = ["c12", "C12", "p", "P", "n", "N", "t"]
    names_out = ["C12", "C12", "p", "p", "n", "n", "t"]

    def test_init(self):
        with pytest.raises(ValueError):
            assert Isotope(119, 350)
        with pytest.raises(ValueError):
            assert Isotope(118, 351)

    def test_init_to_ppn(self):
        for iso, isomer, out in zip(self.isotopes, self.isomers, self.ppn_outputs):
            assert Isotope(iso[0], iso[1], isomer).ppn_name == out

    def test_ppn_to_numbers(self):
        for iso, isomer, out in zip(self.isotopes, self.isomers, self.ppn_outputs):
            assert Isotope.ppn_name_factory(out).numbers(force_isomer=True) == (
                iso[0],
                iso[1],
                isomer,
            )

    def test_name(self):
        for n, n_out in zip(self.names, self.names_out):
            isotope = Isotope.name(n)
            assert str(isotope) == n_out

    def test_class_re_input_to_name(self):
        assert str(Isotope.name(Isotope(7, 14))) == "N14"

    def test_str(self):
        assert str(Isotope(7, 14)) == "N14"
        assert str(Isotope(4, 9)) == "Be9"

        assert str(Isotope(1, 0)) == "weak"

    def test_eq(self):
        assert Isotope.name("Ne20") == "Ne20" and "ne20" and "20Ne"

        assert Isotope.name("O12") != "NE20"

    def test_numbers(self):

        assert Isotope(7, 14).numbers() == (7, 14)

        assert Isotope(6, 12, True).numbers() == (6, 12, True)

        assert Isotope(6, 12, False).numbers(force_isomer=True) == (6, 12, False)

    def test_decay(self):
        assert Isotope(9, 26).decay().numbers() == (12, 26)

        assert Isotope(4, 8).decay().numbers() == (2, 4)

        assert Isotope(14, 26).decay().numbers() == (12, 26)

        assert Isotope(2, 4).decay().numbers() == (2, 4)

        # This asserts the code is not working physically but as intended
        assert Isotope(20, 36).decay().numbers() == (16, 36)

    def test_is_stable(self):
        for s, j in Isotope.stable_isotopes:
            assert Isotope(s, j).is_stable

    def test_is_primordial(self):
        for s, j in Isotope.primordial:
            assert Isotope(s, j).is_primordial

    def test_number_to_ppn_name(self):
        assert Isotope.number_to_ppn_name(10, 10, 1) == 'NE 10'

        assert Isotope.number_to_ppn_name(10, 10, 2) == 'NE*10'

    def test_number_to_ppn_name_error(self):
        with pytest.raises(ValueError):
            Isotope.number_to_ppn_name(10, 10, 3)

    def test_ppn_name_to_numbers(self):
        assert Isotope.ppn_name_to_numbers('NE 10') == (10, 10)

    def test_decay_isotope(self):
        assert Isotope.decay_isotope(10, 10) == (5, 10, False)
