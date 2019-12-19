"""Minimal setup file for audatar project."""

import sys
import os

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

readme = open('README.md').read()

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    'pytest'
    # TODO : put test requirements here
]

setup(
    name='audatar',
    version='0.1.0',
    license='HomeAway Inc',
    description='a data validation framework for creating and running data validation checks',
    long_description=readme + '\n\n',
    author='Anil Pai',
    author_email='apai@homeaway.com',
    url='https://github.homeawaycorp.com/AnalyticsEngineering/ae-audatar',
    packages=find_packages(where='audatar'),
    package_dir={'': 'audatar'},
    install_requires=requirements,
    zipsafe=False,
    keywords='audatar, celery, data validation',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: HomeAway License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
