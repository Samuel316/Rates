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

import numpy as np
import pandas as pd

from pathlib import Path
from typing import Union

from rates.isotope import Isotope
from rates.reaction import KadonisReaction


class Kadonis:
    """ Holds all the information from a Kadonis file

    Parameters
    ----------
    file_path : Union[str, Path] = None
        Path to reaction rate fiole in the Kadonis format, if None then
        version must be specified.
    version : float = {1, 0.3}
        specifying a version loads a file from within the code.

    """

    def __init__(
        self, file_path: Union[str, Path] = None, version: float = None
    ) -> None:

        if (file_path is None) and (version == 1):
            file_path = Path(__file__).parent.parent / "Data/kadonis_rrates_1.0.txt"
        elif (file_path is None) and (version == 0.3):
            file_path = Path(__file__).parent.parent / "Data/kadonis_rrates_0.3.txt"
        else:
            raise Exception("File not specified")

        self.file_path = Path(file_path.parent / file_path.stem)
        try:
            self.df = pd.read_pickle(str(self.file_path) + ".temp")
        except:
            self.df = self.read_file(file_path)

    def __str__(self) -> str:
        return self.file_path.stem

    def __getitem__(self, target: Union[str, "Isotope"]) -> KadonisReaction:
        target = Isotope.name(target)
        try:
            return self.df[
                (self.df["Z"] == target.charge_number)
                & (self.df["A"] == target.mass_number)
            ].Reaction.iloc[0]
        except IndexError:
            raise Exception(str(target) + " Not found in file")

    def in_file(self, target: Union[str, "Isotope"]):
        target = Isotope.name(target)
        try:
            self.__getitem__(target)
            return True
        except Exception:
            return False

    @staticmethod
    def read_file(file_path: Union[str, Path]) -> pd.DataFrame:
        """

        Parameters
        ----------
        file_path :

        Returns
        -------

        """
        file_path = Path(file_path)

        df = pd.read_csv(
            file_path,
            index_col=False,
            sep="\t",
            header=0,
            dtype={"Z": np.uint8, "A": np.uint8, "Isomer": str, "Sym": str},
            na_values="-",
        )

        try:
            df.drop(
                [" ; reaction rate including SEF in cm3/mole/s"], axis=1, inplace=True
            )
            version = 1.0
        except KeyError:
            df.rename(
                {"100(keV); reaction rate including SEF in cm3/mole/s": "100"},
                axis=1,
                inplace=True,
            )
            version = 0.3
            print("Warning Loading Kadonis in 0.3 format")
        except:
            raise Exception

        if version == 1.0:
            df["Reaction"] = df.apply(
                lambda df: KadonisReaction(
                    target=Isotope(df.Z, df.A),
                    label="Kadonis 1.0",
                    rr=[
                        df["RR(5keV)"],
                        df["RR(8keV)"],
                        df["RR(10keV)"],
                        df["RR(15keV)"],
                        df["RR(20keV)"],
                        df["RR(25keV)"],
                        df["RR(30keV)"],
                        df["RR(40keV)"],
                        df["RR(50keV)"],
                        df["RR(60keV)"],
                        df["RR(80keV)"],
                        df["RR(100keV)"],
                    ],
                    err=[
                        df["Err(5keV)"],
                        df["Err(8keV)"],
                        df["Err(10keV)"],
                        df["Err(15keV)"],
                        df["Err(20keV)"],
                        df["Err(25keV)"],
                        df["Err(30keV)"],
                        df["Err(40keV)"],
                        df["Err(50keV)"],
                        df["Err(60keV)"],
                        df["Err(80keV)"],
                        df["Err(100keV)"],
                    ],
                ),
                axis=1,
            )

        elif version == 0.3:
            df["Reaction"] = df.apply(
                lambda df: KadonisReaction(
                    target=Isotope(df.Z, df.A),
                    label="Kadonis 0.3",
                    rr=[
                        df["5"],
                        df["8"],
                        df["10"],
                        df["15"],
                        df["20"],
                        df["25"],
                        df["30"],
                        df["40"],
                        df["50"],
                        df["60"],
                        df["80"],
                        df["100"],
                    ],
                    err=[0.0] * 12,
                ),
                axis=1,
            )

        pickle_path = "{0}.temp".format(str(file_path.parent / file_path.stem))
        df.to_pickle(pickle_path)
        return df
