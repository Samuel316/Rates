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

from rates.isotope import Isotope


class TestIsotope:

    ppn_outputs = ["PROT ", "NEUT ", "MG 28", "O  16", "TAg80", "HF*80"]
    isotopes = [(1, 1), (0, 1), (12, 28), (8, 16), (73, 180), (72, 180)]
    isomers = [False, False, False, False, True, True]

    names = ["c12", "C12", "p", "P", "n", "N"]
    names_out = ["C12", "C12", "p", "p", "n", "n"]

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

    def test_class_reinput_to_name(self):
        assert str(Isotope.name(Isotope(7, 14))) == "N14"


if __name__ == "__main__":
    pass
