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


class Kadonis:
    def __init__(self, file_path: str):
        self.df = pd.read_pickle(file_path)

    def __getitem__(self, key):
        return self.df[key]

    @classmethod
    def read_file(cls, file_path: str):

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
            lambda df: Reaction.reaclib_factory(
                chapter=df.Chapter,
                ei=[df.E0, df.E1, df.E2, df.E3, df.E4, df.E5],
                a_rates=df.Rate,
                label=df.SetLabel,
            ),
            axis=1,
        )
        df.to_pickle(file_path[0:-3])

        return


if __name__ == "__main__":
    pass
