#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 00:51:38 2017

@author: misakawa
"""

from setuptools import setup, find_packages
import os
with open('./README.rst', encoding='utf-8') as f:
    readme = f.read()
setup(  name = 'EBNFParser',
        version = '0.1.2.2',
        keywords='parser, parser framework, parser generator, gramamr, ast, tokenizer, EBNF, BNF',
        description = "very powerful and optional parser framework for python",
        long_description=readme,
        license = 'GPLv3.0 License',
        url = 'https://github.com/thautwarm/EBNFParser',
        author = 'thautwarm',
        author_email = 'twshere@outlook.com',
        include_package_data=True,
        packages=['Misakawa'],
        scripts =  ['parserGenerator.py'],
        platforms='any',
        classifiers=['Programming Language :: Python :: 3.6','Programming Language :: Python :: Implementation :: CPython'],
	zip_safe=False
        )
