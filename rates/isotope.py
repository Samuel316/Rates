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

from typing import Tuple, Union, Optional, Any

import numpy as np

real = Union[float, int]


class Isotope:
    """Representation of an isotope.

        Attributes
        ----------
        charge_number : int
            Proton number of the Isotope.
        mass_number : int
            Mass number of the Isotope
        isomer : bool
            True if the Isotope is an Isomer.

    """

    charge_numbers = {
        "n": 0,
        "H": 1,
        "He": 2,
        "Li": 3,
        "Be": 4,
        "B": 5,
        "C": 6,
        "N": 7,
        "O": 8,
        "F": 9,
        "Ne": 10,
        "Na": 11,
        "Mg": 12,
        "Al": 13,
        "Si": 14,
        "P": 15,
        "S": 16,
        "Cl": 17,
        "Ar": 18,
        "K": 19,
        "Ca": 20,
        "Sc": 21,
        "Ti": 22,
        "V": 23,
        "Cr": 24,
        "Mn": 25,
        "Fe": 26,
        "Co": 27,
        "Ni": 28,
        "Cu": 29,
        "Zn": 30,
        "Ga": 31,
        "Ge": 32,
        "As": 33,
        "Se": 34,
        "Br": 35,
        "Kr": 36,
        "Rb": 37,
        "Sr": 38,
        "Y": 39,
        "Zr": 40,
        "Nb": 41,
        "Mo": 42,
        "Tc": 43,
        "Ru": 44,
        "Rh": 45,
        "Pd": 46,
        "Ag": 47,
        "Cd": 48,
        "In": 49,
        "Sn": 50,
        "Sb": 51,
        "Te": 52,
        "I": 53,
        "Xe": 54,
        "Cs": 55,
        "Ba": 56,
        "La": 57,
        "Ce": 58,
        "Pr": 59,
        "Nd": 60,
        "Pm": 61,
        "Sm": 62,
        "Eu": 63,
        "Gd": 64,
        "Tb": 65,
        "Dy": 66,
        "Ho": 67,
        "Er": 68,
        "Tm": 69,
        "Yb": 70,
        "Lu": 71,
        "Hf": 72,
        "Ta": 73,
        "W": 74,
        "Re": 75,
        "Os": 76,
        "Ir": 77,
        "Pt": 78,
        "Au": 79,
        "Hg": 80,
        "Tl": 81,
        "Pb": 82,
        "Bi": 83,
        "Po": 84,
        "At": 85,
        "Rn": 86,
        "Fr": 87,
        "Ra": 88,
        "Ac": 89,
        "Th": 90,
        "Pa": 91,
        "U": 92,
        "Np": 93,
        "Pu": 94,
        "Am": 95,
        "Cm": 96,
        "Bk": 97,
        "Cf": 98,
        "Es": 99,
        "Fm": 100,
        "Md": 101,
        "No": 102,
        "Lr": 103,
        "Rf": 104,
        "Db": 105,
        "Sg": 106,
        "Bh": 107,
        "Hs": 108,
        "Mt": 109,
        "Ds": 110,
        "Rg": 111,
        "Cn": 112,
        "Nh": 113,
        "Fl": 114,
        "Mc": 115,
        "Lv": 116,
        "Ts": 117,
        "Og": 118,
    }

    symbol = dict((v, k) for k, v in charge_numbers.items())

    _full_name = {
        "H": "Hydrogen",
        "He": "Helium",
        "Li": "Lithium",
        "Be": "Beryllium",
        "B": "Boron",
        "C": "Carbon",
        "N": "Nitrogen",
        "O": "Oxygen",
        "F": "Fluorine",
        "Ne": "Neon",
        "Na": "Sodium",
        "Mg": "Magnesium",
        "Al": "Aluminium",
        "Si": "Silicon",
        "P": "Phosphorus",
        "S": "Sulfur",
        "Cl": "Chlorine",
        "Ar": "Argon",
        "K": "Potassium",
        "Ca": "Calcium",
        "Sc": "Scandium",
        "Ti": "Titanium",
        "V": "Vanadium",
        "Cr": "Chromium",
        "Mn": "Manganese",
        "Fe": "Iron",
        "Co": "Cobalt",
        "Ni": "Nickel",
        "Cu": "Copper",
        "Zn": "Zinc",
        "Ga": "Gallium",
        "Ge": "Germanium",
        "As": "Arsenic",
        "Se": "Selenium",
        "Br": "Bromine",
        "Kr": "Krypton",
        "Rb": "Rubidium",
        "Sr": "Strontium",
        "Y": "Yttrium",
        "Zr": "Zirconium",
        "Nb": "Niobium",
        "Mo": "Molybdenum",
        "Tc": "Technetium",
        "Ru": "Ruthenium",
        "Rh": "Rhodium",
        "Pd": "Palladium",
        "Ag": "Silver",
        "Cd": "Cadmium",
        "In": "Indium",
        "Sn": "Tin",
        "Sb": "Antimony",
        "Te": "Tellurium",
        "I": "Iodine",
        "Xe": "Xenon",
        "Cs": "Caesium",
        "Ba": "Barium",
        "La": "Lanthanum",
        "Ce": "Cerium",
        "Pr": "Praseodymium",
        "Nd": "Neodymium",
        "Pm": "Promethium",
        "Sm": "Samarium",
        "Eu": "Europium",
        "Gd": "Gadolinium",
        "Tb": "Terbium",
        "Dy": "Dysprosium",
        "Ho": "Holmium",
        "Er": "Erbium",
        "Tm": "Thulium",
        "Yb": "Ytterbium",
        "Lu": "Lutetium",
        "Hf": "Hafnium",
        "Ta": "Tantalum",
        "W": "Tungsten",
        "Re": "Rhenium",
        "Os": "Osmium",
        "Ir": "Iridium",
        "Pt": "Platinum",
        "Au": "Gold",
        "Hg": "Mercury",
        "Tl": "Thallium",
        "Pb": "Lead",
        "Bi": "Bismuth",
        "Po": "Polonium",
        "At": "Astatine",
        "Rn": "Radon",
        "Fr": "Francium",
        "Ra": "Radium",
        "Ac": "Actinium",
        "Th": "Thorium",
        "Pa": "Protactinium",
        "U": "Uranium",
        "Np": "Neptunium",
        "Pu": "Plutonium",
        "Am": "Americium",
        "Cm": "Curium",
        "Bk": "Berkelium",
        "Cf": "Californium",
        "Es": "Einsteinium",
        "Fm": "Fermium",
        "Md": "Mendelevium",
        "No": "Nobelium",
        "Lr": "Lawrencium",
        "Rf": "Rutherfordium",
        "Db": "Dubnium",
        "Sg": "Seaborgium",
        "Bh": "Bohrium",
        "Hs": "Hassium",
        "Mt": "Meitnerium",
        "Ds": "Darmstadtium",
        "Rg": "Roentgenium",
        "Cn": "Copernicium",
        "Nh": "Nihonium",
        "Fl": "Flerovium",
        "Mc": "Moscovium",
        "Lv": "Livermorium",
        "Ts": "Tennessine",
        "Og": "Oganesson",
    }

    stable_isotopes = (
        (1, 1),
        (1, 2),
        (2, 3),
        (2, 4),
        (3, 6),
        (3, 7),
        (4, 9),
        (5, 10),
        (5, 11),
        (6, 12),
        (6, 13),
        (7, 14),
        (7, 15),
        (8, 16),
        (8, 17),
        (8, 18),
        (9, 19),
        (10, 20),
        (10, 21),
        (10, 22),
        (11, 23),
        (12, 24),
        (12, 25),
        (12, 26),
        (13, 27),
        (14, 28),
        (14, 29),
        (14, 30),
        (15, 31),
        (16, 32),
        (16, 33),
        (16, 34),
        (16, 36),
        (17, 35),
        (17, 37),
        (18, 36),
        (18, 38),
        (18, 40),
        (19, 39),
        (19, 41),
        (20, 40),
        (20, 42),
        (20, 43),
        (20, 44),
        (20, 46),
        (21, 45),
        (22, 46),
        (22, 47),
        (22, 48),
        (22, 49),
        (22, 50),
        (23, 51),
        (24, 50),
        (24, 52),
        (24, 53),
        (24, 54),
        (25, 55),
        (26, 54),
        (26, 56),
        (26, 57),
        (26, 58),
        (27, 59),
        (28, 58),
        (28, 60),
        (28, 61),
        (28, 62),
        (28, 64),
        (29, 63),
        (29, 65),
        (30, 64),
        (30, 66),
        (30, 67),
        (30, 68),
        (30, 70),
        (31, 69),
        (31, 71),
        (32, 70),
        (32, 72),
        (32, 73),
        (32, 74),
        (33, 75),
        (34, 74),
        (34, 76),
        (34, 77),
        (34, 78),
        (34, 80),
        (35, 79),
        (35, 81),
        (36, 80),
        (36, 82),
        (36, 83),
        (36, 84),
        (36, 86),
        (37, 85),
        (38, 84),
        (38, 86),
        (38, 87),
        (38, 88),
        (39, 89),
        (40, 90),
        (40, 91),
        (40, 92),
        (40, 94),
        (41, 93),
        (42, 92),
        (42, 94),
        (42, 95),
        (42, 96),
        (42, 97),
        (42, 98),
        (44, 96),
        (44, 98),
        (44, 99),
        (44, 100),
        (44, 101),
        (44, 102),
        (44, 104),
        (45, 103),
        (46, 102),
        (46, 104),
        (46, 105),
        (46, 106),
        (46, 108),
        (46, 110),
        (47, 107),
        (47, 109),
        (48, 106),
        (48, 108),
        (48, 110),
        (48, 111),
        (48, 112),
        (48, 114),
        (49, 113),
        (50, 112),
        (50, 114),
        (50, 115),
        (50, 116),
        (50, 117),
        (50, 118),
        (50, 119),
        (50, 120),
        (50, 122),
        (50, 124),
        (51, 121),
        (51, 123),
        (52, 120),
        (52, 122),
        (52, 123),
        (52, 124),
        (52, 125),
        (52, 126),
        (53, 127),
        (54, 124),
        (54, 126),
        (54, 128),
        (54, 129),
        (54, 130),
        (54, 131),
        (54, 132),
        (54, 134),
        (55, 133),
        (56, 132),
        (56, 134),
        (56, 135),
        (56, 136),
        (56, 137),
        (56, 138),
        (57, 139),
        (58, 136),
        (58, 138),
        (58, 140),
        (58, 142),
        (59, 141),
        (60, 142),
        (60, 143),
        (60, 145),
        (60, 146),
        (60, 148),
        (62, 144),
        (62, 149),
        (62, 150),
        (62, 152),
        (62, 154),
        (63, 153),
        (64, 154),
        (64, 155),
        (64, 156),
        (64, 157),
        (64, 158),
        (64, 160),
        (65, 159),
        (66, 156),
        (66, 158),
        (66, 160),
        (66, 161),
        (66, 162),
        (66, 163),
        (66, 164),
        (67, 165),
        (68, 162),
        (68, 164),
        (68, 166),
        (68, 167),
        (68, 168),
        (68, 170),
        (69, 169),
        (70, 168),
        (70, 170),
        (70, 171),
        (70, 172),
        (70, 173),
        (70, 174),
        (70, 176),
        (71, 175),
        (72, 176),
        (72, 177),
        (72, 178),
        (72, 179),
        (72, 180),
        (73, 181),
        (74, 182),
        (74, 183),
        (74, 184),
        (74, 186),
        (75, 185),
        (76, 184),
        (76, 187),
        (76, 188),
        (76, 189),
        (76, 190),
        (76, 192),
        (77, 191),
        (77, 193),
        (78, 192),
        (78, 194),
        (78, 195),
        (78, 196),
        (78, 198),
        (79, 197),
        (80, 196),
        (80, 198),
        (80, 199),
        (80, 200),
        (80, 201),
        (80, 202),
        (80, 204),
        (81, 203),
        (81, 205),
        (82, 204),
        (82, 206),
        (82, 207),
        (82, 208),
    )

    primordial = (
        (52, 128),
        (36, 78),
        (54, 136),
        (32, 76),
        (56, 130),
        (34, 82),
        (48, 116),
        (20, 48),
        (40, 96),
        (83, 209),
        (52, 130),
        (60, 150),
        (42, 100),
        (63, 151),
        (73, 180),
        (74, 180),
        (23, 50),
        (48, 113),
        (62, 148),
        (60, 144),
        (76, 186),
        (72, 174),
        (49, 115),
        (64, 152),
        (78, 190),
        (62, 147),
        (57, 138),
        (37, 87),
        (75, 187),
        (71, 176),
        (90, 232),
        (92, 238),
        (19, 40),
        (92, 235),
    )

    def __init__(
        self, charge_number: real, mass_number: real, isomer: bool = False
    ) -> None:
        """
        Parameters
        ----------
        charge_number : [int, float]
        mass_number : [int, float]
        isomer : bool

        Returns
        -------
        self
        """

        if float(charge_number) > 118:
            raise ValueError("Element has no name", charge_number)
        if float(mass_number) > 350:
            raise ValueError("Mass seems a bit high", mass_number)
        self.charge_number = int(float(charge_number))
        self.mass_number = int(float(mass_number))
        self.isomer = isomer

    def __str__(self) -> str:
        """

        Returns
        -------
        str
        """
        if self.mass_number == 0:
            name = "weak"
        elif self.charge_number == 0 and self.mass_number == 1:
            name = "n"
        elif self.charge_number == 1 and self.mass_number == 1:
            name = "p"
        elif self.charge_number == 1 and self.mass_number == 2:
            name = "d"
        elif self.charge_number == 1 and self.mass_number == 3:
            name = "t"
        else:
            name = self.symbol[self.charge_number] + str(self.mass_number)

        return name

    def __eq__(self, other):
        other = Isotope.name(other)
        return (
            other.mass_number == self.mass_number
            and other.charge_number == self.charge_number
            and other.isomer == self.isomer
        )

    @property
    def full_name(self) -> str:

        return f"{self._full_name[self.symbol[self.charge_number]]}-{self.mass_number}"

    @property
    def ppn_name(self) -> str:
        """ Name of isotope in ppn file format.

        Returns
        -------
        str
        """
        iso = "Are you sure this is an isomer???"

        if self.charge_number == 0 and self.mass_number == 1:
            iso = "NEUT "
        elif self.charge_number == 1 and self.mass_number == 1:
            iso = "PROT "
        elif self.isomer is False:
            iso = self.symbol[self.charge_number].upper().ljust(2) + str(
                self.mass_number
            ).rjust(3)
        elif self.isomer is True and self.charge_number != 73:
            iso = (
                self.symbol[self.charge_number].upper()
                + "*"
                + str(self.mass_number)[-2:]
            )
        elif (
            self.isomer is True and self.charge_number == 73 and self.mass_number == 180
        ):
            iso = "TAg80"

        return iso

    def numbers(
        self, force_isomer: bool = False
    ) -> Union[Tuple[int, int], Tuple[int, int, bool]]:
        """

        Parameters
        ----------
        force_isomer : bool
            Forces output to include Isomer value when False.

        Returns
        -------
        Union[Tuple[int, int], Tuple[int, int, bool]]

        """
        num: Any

        if self.isomer or force_isomer:
            num = (self.charge_number, self.mass_number, self.isomer)
        else:
            num = (self.charge_number, self.mass_number)

        return num

    def decay(self, primordial_as_stable: bool = True) -> "Isotope":
        """

        Parameters
        ----------
        primordial_as_stable : bool

        Returns
        -------
        Isotope

        """
        # TODO: This only works from beta decay and beta unstable isotopes
        # Currently the time scale of the decay is assumed to ber a small fraction of the
        # half life of primordial isotopes.
        stable: np.array[Tuple[int]] = self.stable_isotopes + self.primordial
        stable = np.array(stable)
        stable = stable[stable[:, 0].argsort()]
        # TODO: Isomers
        self.isomer = False

        if self.is_stable or self.is_primordial:
            return self
        elif self.mass_number == 8:
            self.mass_number = 4
            self.charge_number = 2
        else:
            product = stable[np.where(stable[:, 1] == self.mass_number)][0]
            self.mass_number = product[1]
            self.charge_number = product[0]
        return self

    @property
    def is_stable(self) -> bool:
        """ Returns True if isotope is stable.

        Returns
        -------
        bool

        """
        if (self.charge_number, self.mass_number) in self.stable_isotopes:
            return True
        return False

    @property
    def is_primordial(self) -> bool:
        """Returns True is isotope is primordial.

        Returns
        -------
        bool

        """
        if (self.charge_number, self.mass_number) in self.primordial:
            return True
        return False

    @classmethod
    def name(cls, name: Union["Isotope", str]) -> "Isotope":
        """ Factory method from string representation.

        Parameters
        ----------
        name : str
            Name of isotope, order and capitalisation don't matter.

        Returns
        -------
        Isotope

        """
        if isinstance(name, cls):
            return name
        else:
            name_str: str = str(name)

        if name_str.lower() == "n":
            iso = cls(0, 1)
        elif name_str.lower() == "p":
            iso = cls(1, 1)
        elif name_str.lower() == "d":
            iso = cls(1, 2)
        elif name_str.lower() == "t":
            iso = cls(1, 3)
        else:
            sym = "".join([c for c in name_str if c.isalpha()]).lower().capitalize()
            num = "".join([c for c in name_str if c.isnumeric()])
            charge_number = Isotope.charge_numbers[sym]
            iso = cls(charge_number, int(num))

        return iso

    @classmethod
    def ppn_name_factory(cls, ppn_name: str) -> "Isotope":
        """Factory method from PPN fixed width file representation.

        Parameters
        ----------
        ppn_name : str

        Returns
        -------
        Isotope
        """
        ppn_name = ppn_name.strip()
        if ppn_name == "NEUT":
            iso = cls(0, 1)
        elif ppn_name == "PROT":
            iso = cls(1, 1)
        elif ppn_name[2] == "*":
            charge_number = Isotope.charge_numbers[
                ppn_name[0:2].strip().lower().capitalize()
            ]
            iso = cls(charge_number, int("1" + ppn_name[3:5].strip()), True)
        elif ppn_name[2] == "g":
            charge_number = Isotope.charge_numbers[
                ppn_name[0:2].strip().lower().capitalize()
            ]
            iso = cls(charge_number, int("1" + ppn_name[3:5].strip()), True)
        else:
            charge_number = Isotope.charge_numbers[
                ppn_name[0:2].strip().lower().capitalize()
            ]
            iso = cls(charge_number, int(ppn_name[2:5].strip()))

        return iso

    @staticmethod
    def number_to_ppn_name(
        charge_number: real, mass_number: real, isomer: int = 1
    ) -> str:
        """Convert charge and mass number to PPN name.

        Parameters
        ----------
        charge_number : [int, float]
        mass_number : [int, float]
        isomer : int {1, 2}
            1 for false, 2 for true.

        Returns
        -------
        str

        """
        if int(isomer) == 1:
            isomer = False
        elif int(isomer) == 2:
            isomer = True
        else:
            raise ValueError(
                "No valid input for isomer, should be 1 for False or 2 for True", isomer
            )

        return Isotope(charge_number, mass_number, isomer).ppn_name

    @staticmethod
    def ppn_name_to_numbers(
        ppn_name: str
    ) -> Union[Tuple[int, int], Tuple[int, int, bool]]:
        """

        Parameters
        ----------
        ppn_name : str
            Name of isotope in PPN format

        Returns
        -------
        [Tuple[int, int], Tuple[int, int, bool]]
            (charge number, mass number, [isomer])

        """
        return Isotope.ppn_name_factory(ppn_name).numbers()

    @staticmethod
    def decay_isotope(
        charge_number: real, mass_number: real, isomer: bool = False
    ) -> Union[Tuple[int, int], Tuple[int, int, bool]]:
        """

        Parameters
        ----------
        charge_number
        mass_number
        isomer

        Returns
        -------
        Tuple[int, int, bool]

        """
        return (
            Isotope(charge_number, mass_number, isomer)
            .decay()
            .numbers(force_isomer=True)
        )
