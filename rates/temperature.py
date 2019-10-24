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


class Temperature:
    def __init__(self, temperature: [int, float], unit: str = "Gk"):
        if unit is "Gk":
            self.gk = temperature
            self._kev = None
        elif unit is "KeV":
            self.gk = temperature * 1.160451e-2
            self._kev = temperature
            #  https://physics.nist.gov/cuu/Constants/energy.html
        else:
            raise Exception("Unsupported unit")
        self.unit = "Gk"

    def __str__(self):
        return str(self) + self.unit

    @property
    def kev(self):
        if self._kev is None:
            self._kev = self.gk / 1.160451e-2
            return self._kev
        elif self._kev is not None:
            return self._kev
