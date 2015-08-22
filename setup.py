# -*- coding: utf-8 -*-

"""setup.py: setuptools control."""


import re
from setuptools import setup, find_packages

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('svyn/svyn.py').read(),
    re.M
    ).group(1)

with open("README.rst", "rb") as f:
    long_descr = f.read().decode("utf-8")

setup(
    name="svyn",
    packages=find_packages(exclude=['tests*']),
    entry_points={
        "console_scripts": ['svyn = svyn.svyn:main']
    },
    version=version,
    description="Wrapper for pysvn, over the command-line.",
    long_description=long_descr,
    author="Lance T. Erickson",
    author_email="lancetarn@gmail.com",
    license="BSD 2-Clause",
)
