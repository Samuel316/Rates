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
import matplotlib as plt

from isotope import Isotope


class Reaction:
    def __init__(self, targets: iter, products: iter):
        self.targets = targets
        self.products = products

    def __str__(self):
        return "{0} -> {1}".format("+".join(self.targets), "+".join(self.products))


class ReaclibReaction(Reaction):
    def __init__(self, targets: iter, products: iter, a_rates: iter, label: str):
        super().__init__(targets, products)
        self.a = a_rates
        self.label = label

    def rate(self, temp9: [float, np.asarray]):
        return np.exp(
            self.a[0]
            + self.a[1] * temp9 ** ((2.0 * 1 - 5.0) / 3.0)
            + self.a[2] * temp9 ** ((2.0 * 2 - 5.0) / 3.0)
            + self.a[3] * temp9 ** ((2.0 * 3 - 5.0) / 3.0)
            + self.a[4] * temp9 ** ((2.0 * 4 - 5.0) / 3.0)
            + self.a[5] * temp9 ** ((2.0 * 5 - 5.0) / 3.0)
            + self.a[6] * np.log(temp9)
        )

    def mpl_plot(self, ax=None, **kwargs):
        t = np.logspace(-1, 1, 1000)

        ax = ax or plt.gca()
        ax.set_title("Reaction Rate")
        ax.set_ylabel("Rate ($cm^3\;mol^{-1}\;sec^{-1}$)")
        ax.set_xlabel("Temperature ($GK$)")
        ax.loglog(t, self.rate(t), label=self.label + " " + self.__str__(), **kwargs)
        ax.legend()

    @classmethod
    def reaclib_factory(cls, chapter: int, ei: iter, a_rates: iter, label: str = None):
        if chapter is 1:
            return cls([ei[0]], [ei[1]], a_rates, label)
        elif chapter is 2:
            return cls([ei[0]], ei[1:3], a_rates, label)
        elif chapter is 3:
            return cls([ei[0]], [ei[1:4]], a_rates, label)
        elif chapter is 4:
            return cls(ei[0:2], [ei[2]], a_rates, label)
        elif chapter is 5:
            return cls(ei[0:2], ei[2:4], a_rates, label)
        elif chapter is 6:
            return cls(ei[0:2], ei[2:5], a_rates, label)
        elif chapter is 7:
            return cls(ei[0:2], ei[2:6], a_rates, label)
        elif chapter is 8:
            return cls(ei[0:3], [ei[3]], a_rates, label)
        elif chapter is 9:
            return cls(ei[0:3], ei[3:5], a_rates, label)
        elif chapter is 10:
            return cls(ei[0:4], ei[4:6], a_rates, label)
        elif chapter is 11:
            return cls([ei[0]], ei[1:5], a_rates, label)


class KadonisReaction(Reaction):
    def __init__(self, target: str, rr: iter, err: iter, label: str):
        product = Isotope.name(target)
        product.mass_number += 1
        super().__init__(["n", target], [product])

        self.rr = rr
        self.err = err
        self.label = label
        self.temperature = [5, 8, 10, 15, 20, 25, 30, 40, 50, 60, 80, 100]

    def rate(self):
        # TODO: interpolation
        return

    def mpl_plot(self, ax=None, **kwargs):

        ax = ax or plt.gca()
        ax.set_title("Reaction Rate")
        ax.set_ylabel("Rate ($cm^3\;mol^{-1}\;sec^{-1}$)")
        ax.set_xlabel("Temperature ($KeV$)")
        ax.loglog(
            self.temperature, self.rr, label=self.label + " " + self.__str__(), **kwargs
        )
        ax.legend()


if __name__ == "__main__":
    pass
