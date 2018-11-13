# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


setup(
    name='python-allegro',
    # version='0.0.1',       # currently no version
    description='Simple wrapper (client) for Allegro.pl REST API written in Python (using requests)',
    url='https://github.com/chawel/python-allegro.git',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
)