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
from typing import Union, List, Iterable, Sequence
from collections import Counter

import numpy as np
import matplotlib.pyplot as plt

from rates.isotope import Isotope
from rates.temperature import Temperature

real = Union[float, int]
iso_list_type = Iterable[Union[Isotope, str]]


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
    "mpl_plt" : plt.axis axis
    """

    def __init__(self, targets: iso_list_type, products: iso_list_type) -> None:
        self.targets = [Isotope.name(t) for t in targets]
        self.products = [Isotope.name(t) for t in products]

    def __str__(self) -> str:
        return "{0} -> {1}".format(
            "+".join([str(i) for i in self.targets]),
            "+".join([str(i) for i in self.products]),
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Reaction):
            raise NotImplementedError

        return Counter([str(i) for i in self.targets]) == Counter(
            [str(i) for i in other.targets]
        ) and Counter([str(i) for i in self.products]) == Counter(
            [str(i) for i in other.products]
        )

    def mpl_plot(
        self, ax: plt.axis = None, temp_unit: str = "Gk", **kwargs
    ) -> plt.axis:
        """

        Parameters
        ----------
        ax :
        temp_unit :
        kwargs :
        """
        ax = ax or plt.gca()
        ax.set_title("Reaction Rate")
        ax.set_ylabel("Rate ($cm^3\;mol^{-1}\;sec^{-1}$)")

        if temp_unit is "Gk":
            ax.set_xlabel("Temperature ($GK$)")

        return ax


class ReaclibReaction(Reaction):
    """

    Parameters
    ----------
    targets : List of str or Isotope
        List of all the target isotopes including n and p.
    products : List of str or Isotope
        List of all the product isotopes including n and p.

    Attributes
    ----------
    """

    def __init__(
        self,
        targets: iso_list_type,
        products: iso_list_type,
        a_rates: Sequence[real],
        label: str,
    ) -> None:
        super().__init__(targets, products)
        self.a = a_rates
        self.label = label

    def rate(self, temp9: Union[real, np.asarray]):
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

    def mpl_plot(
        self, ax: plt.axis = None, temp_unit: str = "GK", **kwargs
    ) -> plt.axis:
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

        ax = super().mpl_plot(ax=ax, temp_unit=temp_unit)

        return ax

    @classmethod
    def reaclib_factory(
        cls,
        chapter: int,
        ei: Sequence[str],
        a_rates: Sequence[real],
        label: str = "None",
    ) -> "ReaclibReaction":
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
            reaclib_reaction = cls([ei[0]], [ei[1]], a_rates, label)
        elif chapter is 2:
            reaclib_reaction = cls([ei[0]], ei[1:3], a_rates, label)
        elif chapter is 3:
            reaclib_reaction = cls([ei[0]], ei[1:4], a_rates, label)
        elif chapter is 4:
            reaclib_reaction = cls(ei[0:2], [ei[2]], a_rates, label)
        elif chapter is 5:
            reaclib_reaction = cls(ei[0:2], ei[2:4], a_rates, label)
        elif chapter is 6:
            reaclib_reaction = cls(ei[0:2], ei[2:5], a_rates, label)
        elif chapter is 7:
            reaclib_reaction = cls(ei[0:2], ei[2:6], a_rates, label)
        elif chapter is 8:
            reaclib_reaction = cls(ei[0:3], [ei[3]], a_rates, label)
        elif chapter is 9:
            reaclib_reaction = cls(ei[0:3], ei[3:5], a_rates, label)
        elif chapter is 10:
            reaclib_reaction = cls(ei[0:4], ei[4:6], a_rates, label)
        elif chapter is 11:
            reaclib_reaction = cls([ei[0]], ei[1:5], a_rates, label)
        else:
            raise Exception

        return reaclib_reaction


class KadonisReaction(Reaction):
    """

    Parameters
    ----------
    target : Union[str, Isotope]
        Target isotope for n gamma.
    rr:

    Attributes
    ----------

    """

    def __init__(
        self,
        target: Union[str, Isotope],
        rr: Iterable[real],
        err: Iterable[real],
        temp: Iterable[real] = (5, 8, 10, 15, 20, 25, 30, 40, 50, 60, 80, 100),
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

    def mpl_plot(self, ax: plt.axis = None, temp_unit: str = "Gk", **kwargs):
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

        ax = super().mpl_plot(ax, temp_unit=temp_unit)

        return ax
