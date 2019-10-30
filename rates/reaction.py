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
import copy
import numpy as np
import matplotlib.pyplot as plt

from rates.isotope import Isotope
from rates.temperature import Temperature


class Reaction:
    """The default reaction class.

    Parameters
    ----------
    targets : List of str or Isotope
        List of all the target isotopes including n and p.
    products : List of str or Isotope
        List of all the product isotopes including n and p.

    Attributes
    ----------
    mpl_plt : matplotlib axis


    
    """

    def __init__(self, targets: iter, products: iter):
        self.targets = [Isotope.name(t) for t in targets]
        self.products = [Isotope.name(t) for t in products]

    def __str__(self):
        return "{0} -> {1}".format(
            "+".join([str(i) for i in self.targets]),
            "+".join([str(i) for i in self.products]),
        )

    def mpl_plt(self, ax=None, temp_units="Gk", **kwargs):
        """

        Parameters
        ----------
        ax :
        temp_units :
        kwargs :
        """
        ax = ax or plt.gca()
        ax.set_title("Reaction Rate")
        ax.set_ylabel("Rate ($cm^3\;mol^{-1}\;sec^{-1}$)")

        if temp_units is "Gk":
            ax.set_xlabel("Temperature ($GK$)")

        return ax


class ReaclibReaction(Reaction):
    """

    """

    def __init__(self, targets: iter, products: iter, a_rates: iter, label: str):
        super().__init__(targets, products)
        self.a = a_rates
        self.label = label

    def rate(self, temp9: [float, np.asarray]):
        """

        Parameters
        ----------
        temp9 :

        Returns
        -------

        """
        return np.exp(
            self.a[0]
            + self.a[1] * temp9 ** ((2.0 * 1 - 5.0) / 3.0)
            + self.a[2] * temp9 ** ((2.0 * 2 - 5.0) / 3.0)
            + self.a[3] * temp9 ** ((2.0 * 3 - 5.0) / 3.0)
            + self.a[4] * temp9 ** ((2.0 * 4 - 5.0) / 3.0)
            + self.a[5] * temp9 ** ((2.0 * 5 - 5.0) / 3.0)
            + self.a[6] * np.log(temp9)
        )

    def mpl_plot(self, ax=None, temp_unit="GK", **kwargs):
        """

        Parameters
        ----------
        ax :
        temp_unit :
        kwargs :

        Returns
        -------

        """
        ax = ax or plt.gca()

        t = np.logspace(-1, 1, 1000)
        if temp_unit is "GK":
            ax.loglog(
                t, self.rate(t), label=self.label + " " + self.__str__(), **kwargs
            )
        elif temp_unit is "KeV":
            ax.loglog(
                Temperature(t).kev,
                self.rate(t),
                label=self.label + " " + self.__str__(),
                **kwargs
            )

        ax = super().mpl_plt(ax=ax, temp_unit=temp_unit)

        return ax

    @classmethod
    def reaclib_factory(cls, chapter: int, ei: iter, a_rates: iter, label: str = None):
        """

        Parameters
        ----------
        chapter :
        ei :
        a_rates :
        label :

        Returns
        -------

        """
        if chapter is 1:
            return cls([ei[0]], [ei[1]], a_rates, label)
        elif chapter is 2:
            return cls([ei[0]], ei[1:3], a_rates, label)
        elif chapter is 3:
            return cls([ei[0]], ei[1:4], a_rates, label)
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
    """

    """

    def __init__(
        self,
        target: [str, Isotope],
        rr: iter,
        err: iter,
        temp: iter = (5, 8, 10, 15, 20, 25, 30, 40, 50, 60, 80, 100),
        temp_units: str = "KeV",
        label: str = "Kadonis",
    ):
        product = copy.deepcopy(Isotope.name(target))
        product.mass_number += 1
        super().__init__(["n", target], [product])

        self.rr = rr
        self.err = err
        self.temperature = temp
        self.temp_unit = temp_units
        self.label = label

    def mpl_plot(self, ax=None, temp_unit="Gk", **kwargs):
        """

        Parameters
        ----------
        ax :
        temp_unit :
        kwargs :

        Returns
        -------

        """
        ax = ax or plt.gca()

        if temp_unit is "Gk":
            ax.errorbar(
                Temperature(np.array(self.temperature), unit=self.temp_unit).gk,
                self.rr,
                yerr=self.err,
                label="{0} {1}".format(self.label, self.__str__()),
                **kwargs
            )
        elif temp_unit is "KeV":
            ax.errorbar(
                Temperature(np.array(self.temperature), unit=self.temp_unit).kev,
                self.rr,
                yerr=self.err,
                label="{0} {1}".format(self.label, self.__str__()),
                **kwargs
            )

        ax.set_yscale("log")

        ax = super().mpl_plt(ax, temp_units=temp_unit)

        return ax
