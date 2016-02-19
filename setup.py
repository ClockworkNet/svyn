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
    description="Convenience functions for svn",
    long_description=long_descr,
    author="Lance T. Erickson",
    author_email="lancetarn@gmail.com",
    license="MIT",
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Natural Language :: English",
        "Topic :: Software Development :: Version Control"
    ]
)
