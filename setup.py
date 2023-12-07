# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


setup(
    name='allegroapi',
    version='0.0.1',    
    description='Simple wrapper (client) for Allegro.pl REST API written in Python (using requests)',
    url='https://github.com/chawel/python-allegro.git',
    license="MIT",
    packages=find_packages(exclude=('tests', 'docs')),
)
