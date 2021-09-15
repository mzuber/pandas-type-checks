#!/usr/bin/env python

import os

from setuptools import setup, find_packages

with open('requirements.txt') as requirements_file:
    requirements = requirements_file.read().splitlines()

with open(os.path.join(os.path.dirname(__file__), 'version.txt')) as version_file:
    version = version_file.read().strip()

setup(
    name='pandas-type-checks',
    version=version,
    author='Martin Zuber',
    author_email='martin.zuber@@sap.com',
    description='Structural type checking for Pandas data frames.',
    license='BSD',
    keywords=[
        'Pandas', 'type check'
    ],
    url='https://github.com/mzuber/pandas-type-checks',
    project_urls={
        'Source Code': 'https://github.com/mzuber/pandas-type-checks',
    },
    packages=find_packages('src'),
    package_dir={'': 'src'},
    platforms='any',
    install_requires=requirements,
    python_requires='>=3.6',
    include_package_data=True,
    classifiers=[
        # complete classifier list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developer'
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development :: Libraries',
        'Typing :: Typed'
    ]
)
