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

from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["pandas", "matplotlib", "numpy"]

setup(
    name="rates",
    version="0.0.1",
    author="Samuel Lloyd",
    author_email="samuel.lloyd@ed.ac.uk",
    description="",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    install_requires=requirements
)
