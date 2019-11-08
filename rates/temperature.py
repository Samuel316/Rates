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
from numbers import Real
from typing import Union

import numpy


class Temperature:
    """Converts Gk to Kev or the reverse.

    Attributes
    ----------
    gk : [Real, numpy.array]
        Temperature in units of 'Gk'.
    kev : [Real, numpy.array]
        Temperature in units of 'KeV'.

    """

    def __init__(self, temperature: Union[Real, numpy.array], unit: str = "Gk") -> None:
        """

        Parameters
        ----------
        temperature : [Real, numpy.array]
            the temperature(s) to convert.
        unit : str {"Gk", "KeV"}

        """
        if unit == "Gk":
            self.gk = temperature
            self._kev = None
        elif unit == "KeV":
            self.gk = temperature * 1.160451e-2
            self._kev = temperature
            #  https://physics.nist.gov/cuu/Constants/energy.html
        else:
            raise Exception(unit + " is unsupported")
        self.unit = "Gk"

    def __str__(self) -> str:
        return str(self.gk) + self.unit

    @property
    def kev(self) -> Union[Real, numpy.array]:
        """Temperature in Kev.

        Returns
        -------
        [Real, numpy.array]
            Value of temperature in KeV
        """

        if self._kev is None:
            self._kev = self.gk / 1.160451e-2
        elif self._kev is not None:
            pass
        return self._kev
