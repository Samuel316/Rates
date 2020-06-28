#!/usr/bin/env python3
# coding=utf-8
"""
Copyright Samuel Lloyd
s1887484, 17/01/2020
samueljohnlloyd12@gmail.com

Parameters
----------

Return
------
"""

from requests import get
from contextlib import closing
from bs4 import BeautifulSoup


class MACS:
    def __init__(self, source, macs, uncertainty):
        self.source = source
        self.macs = macs
        self.uncertainty = uncertainty

    def __str__(self):
        return "{} ± {} from {}".format(self.macs, self.uncertainty, self.source)

    @staticmethod
    def _kadonis(m_web):
        m = m_web[1].replace(" ", "").split("±")
        return MACS("KADoNIS " + str(m_web[0]), m[0], m[1])

    @staticmethod
    def kadonis(m_web):
        m = []
        for i in range(int(len(m_web) / 4)):
            m.append(MACS._kadonis(m_web[0 + 4 * i : 3 + 4 * i]))

        return m


def html(url):
    with closing(get(url, stream=True, verify=False)) as resp:
        return resp.content


def macs(isotope, version=1.0):
    if float(version) == 1.0:
        page = html("http://www.kadonis.org/selementquery.php?isotope=" + isotope)
    elif version == 0.3:
        page = html(
            "http://exp-astro.de/kadonis1.0/selementquery.php?isotope=" + isotope
        )
    else:
        raise Exception("Not a compatible version of Kadonis")

    page = BeautifulSoup(page, "html.parser")

    print(page.prettify())

    table = page.find("table", {"class": "tbody"})

    print(table)
    # table = table.findAll("td")

    # macs = [t.get_text() for t in table]

    # return macs


if __name__ == "__main__":
    print(macs("o16", version=1))
    # print(macs("o16", version=0.3))
