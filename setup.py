# -*- coding: utf-8 -*-
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
        
setup(
    name='eurovat',
    version='0.9.0',
    description='Dealing with VAT in the EU',
    author='airG products',
    author_email='hello@airgproducts.com',
    url='https://github.com/airgproducts/eurovat',
    license='MIT License',
    packages=find_packages(exclude=['tests']),
    package_data = {
        'eurovat': ['data/*']
        },
    install_requires=[
        ],
    provides=['eurovat']
    )
