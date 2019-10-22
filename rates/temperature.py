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
    def __init__(self, temperature: [int, float], unit: str = 'Gk'):
        if unit is "Gk":
            self.gk = temperature
        elif unit is "KeV":
            self.gk = temperature * 1.160451e-2
            #  https://physics.nist.gov/cuu/Constants/energy.html

        self.unit = 'Gk'

    def __str__(self):
        return str(self.gk) + self.unit


if __name__ == "__main__":
    print(Temperature(30, unit='KeV'))