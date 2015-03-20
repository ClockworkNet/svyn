# -*- coding: utf-8 -*-

"""setup.py: setuptools control."""


import re
from setuptools import setup

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('svyn/svyn.py').read(),
    re.M
    ).group(1)

with open("README.rst", "rb") as f:
    long_descr = f.read().decode("utf-8")

setup(
    name="svyn",
    packages=["svyn"],
    entry_points={
        "console_scripts": ['svyn = svyn.svyn:main']
    },
    version=version,
    description="Wrapper for pysvn, over the command-line.",
    long_description=long_descr,
    author="Lance T. Erickson",
    author_email="lancetarn@gmail.com",
)
