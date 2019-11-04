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

from pathlib import Path

from rates.kadonis_file import Kadonis

kadonis_file = Path(__file__).parent / "kadonis_mock"


def test_test_file_exists():
    assert kadonis_file.is_file()


class TestKadonis:
    def test_read_file(self):
        k = Kadonis.read_file(kadonis_file)
        assert list(k.df.columns[0:5]) == ["Z", "A", "Isomer", "Sym", "RR(5keV)"]

        assert list(k.df.Z) == [1, 1, 2, 3]
        assert list(k.df.A) == [1, 2, 3, 6]

        assert list(k.df["RR(5keV)"]) == [4.04e4, 2.17e2, 5.05e2, 7.54e3]

        assert list(k.df.Sym) == ["H", "H", "He", "Li"]

    def test_reaction(self):
        k = Kadonis.read_file(kadonis_file)

        assert str(k.df.Reaction.iloc[0]) == "n+p -> d"
        assert str(k.df.Reaction.iloc[3]) == "n+Li6 -> Li7"

    def test_getitem(self):
        k = Kadonis.read_file(kadonis_file)

        assert str(k["Li6"]) == "n+Li6 -> Li7"
