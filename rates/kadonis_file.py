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

import numpy as np
import pandas as pd

from pathlib import Path

from rates.isotope import Isotope
from rates.reaction import KadonisReaction


class Kadonis:
    def __init__(self, file_path: [str, Path]):
        self.file_path = Path(file_path)
        self.df = pd.read_pickle(file_path)

    def __getitem__(self, target) -> KadonisReaction:
        target = Isotope.name(target)
        try:
            return self.df[
                (self.df["Z"] == target.charge_number)
                & (self.df["A"] == target.mass_number)
            ].Reaction.iloc[0]
        except IndexError:
            raise Exception(str(target) + " Not found in file")

    @classmethod
    def read_file(cls, file_path: str):
        file_path = Path(file_path)

        df = pd.read_csv(
            file_path,
            index_col=False,
            sep="\t",
            header=0,
            dtype={"Z": np.uint8, "A": np.uint8, "Isomer": str, "Sym": str},
            na_values="-",
        )

        df.drop([" ; reaction rate including SEF in cm3/mole/s"], axis=1, inplace=True)
        df["Version"] = 1.0

        df["Reaction"] = df.apply(
            lambda df: KadonisReaction(
                target=Isotope(df.Z, df.A),
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

        pickle_path = "{0}.temp".format(str(file_path.parent / file_path.stem))
        df.to_pickle(pickle_path)
        return cls(file_path=pickle_path)


if __name__ == "__main__":
    pass
