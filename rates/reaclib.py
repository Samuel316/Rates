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
import pandas as pd

from .reaction import Reaction


class Reaclib:
    def __init__(self, file_path: str):
        self.df = pd.read_pickle(file_path)

    def __getitem__(self, key):
        return self.df[key]

    @property
    def reactions(self):
        return self.df.reactions

    @classmethod
    def read_file(cls, file_path: str):

        reaclib = {}

        with open(file_path, "r") as reaclib_file:
            reaclib_file = reaclib_file.readlines()

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

        line3 = [[l.strip() for l in line] for line in line3[0:-1]] + [line3[-1]]

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
        ) = line3

        rates = [
            [i[0:13], i[13:26], i[26:39], i[39:52]] + [j[0:13], j[13:26], j[26:39]]
            for i, j in zip(reaclib_file[2::4], reaclib_file[3::4])
        ]
        reaclib["Rate"] = [[float(i) for i in rate] for rate in rates]

        df = pd.DataFrame(reaclib)
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

        return cls(file_path[0:-3])


if __name__ == "__main__":
    pass
