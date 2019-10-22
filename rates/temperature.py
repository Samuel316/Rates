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


class Temperature(float):
    def __init__(self, temperature: [int, float], unit: str = 'Gk'):
        super().__init__()
        if unit is "Gk":
            super().__init__(temperature)
            self._kev = None
        elif unit is "KeV":
            super().__init__((temperature * 1.160451e-2))
            self._kev = temperature
            #  https://physics.nist.gov/cuu/Constants/energy.html

        self.unit = 'Gk'

    def __str__(self):
        return str(self) + self.unit

    @property
    def kev(self):
        if self._kev is None:
            return self / 1.160451e-2
        elif self._kev is not None:
            return self._kev


if __name__ == "__main__":
    print(Temperature(30, unit='KeV').kev)