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
from typing import Union, List, Any, Dict
from pathlib import Path

import pandas as pd

from rates.isotope import Isotope
from rates.reaction import ReaclibReaction, Reaction


class Reaclib:
    """Holds all the information from  the provided reaclib file.

    """

    def __init__(self, file_path: Union[str, Path] = None) -> None:

        if file_path is None:
            file_path = Path(__file__).parent.parent / "data/reaclib_default.temp"

        self.file_path = Path(file_path)
        self.df = pd.read_pickle(file_path)

    def __getitem__(self, reaction: Reaction) -> str:
        return "todo"  # make this return reactions

    def get_n_gamma(self, target: Union[Isotope, str]) -> ReaclibReaction:
        """Gets reaction from target Isotope, matches __getitem__ method in the Kadonis class

        Parameters
        ----------
        target : [Isotope, str]

        Returns
        -------
        ReaclibReaction

        """
        target = Isotope.name(target)
        try:
            return self.df[
                (self.df.Chapter == 4)
                & (self.df.E0 == "n")
                & (self.df.E1 == str(target).lower())
            ].Reaction.iloc[0]
        except IndexError:
            raise Exception(str(target) + " Not found in file")

    @classmethod
    def read_file(cls, file_path: Union[str, Path]):
        """

        Parameters
        ----------
        file_path :

        Returns
        -------

        """
        file_path = Path(file_path)

        reaclib: Dict[str, List[Union[float, int, List[Union[float, int]]]]] = {}

        with open(file_path) as reaclib_file_path:
            reaclib_file: List[str] = reaclib_file_path.readlines()

        reaclib["Chapter"] = [int(i.strip()) for i in reaclib_file[0::4]]

        line3 = tuple(
            list(i)
            for i in zip(
                *[
                    [
                        i[5:10],
                        i[10:15],
                        i[15:20],
                        i[20:25],
                        i[25:30],
                        i[30:35],
                        i[43:47],
                        i[47],
                        i[48],
                        float(i[52:64]),
                    ]
                    for i in reaclib_file[1::4]
                ]
            )
        )

        line3_striped = [[l.strip() for l in line] for line in line3[0:-1]] + [
            line3[-1]
        ]

        (
            reaclib["E0"],
            reaclib["E1"],
            reaclib["E2"],
            reaclib["E3"],
            reaclib["E4"],
            reaclib["E5"],
            reaclib["SetLabel"],
            reaclib["RateType"],
            reaclib["ReverseRate"],
            reaclib["QValue"],
        ) = line3_striped

        rates = [
            [i[0:13], i[13:26], i[26:39], i[39:52]] + [j[0:13], j[13:26], j[26:39]]
            for i, j in zip(reaclib_file[2::4], reaclib_file[3::4])
        ]
        reaclib["Rate"] = [[float(i) for i in rate] for rate in rates]

        df = pd.DataFrame(reaclib)
        df["Reaction"] = df.apply(
            lambda df: ReaclibReaction.reaclib_factory(
                chapter=df.Chapter,
                ei=[df.E0, df.E1, df.E2, df.E3, df.E4, df.E5],
                a_rates=df.Rate,
                label=df.SetLabel,
            ),
            axis=1,
        )
        pickle_path = "{0}.temp".format(str(file_path.parent / file_path.stem))
        df.to_pickle(pickle_path)
        return cls(file_path=pickle_path)
