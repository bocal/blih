"""Blih installation script

https://github.com/bocal/blih
"""

from setuptools import setup, find_packages
from codecs import open as copen
import os


MODULE_NAME = 'blih'


def get_long_description():
    """ Retrieve the long description from README.rst """
    here = os.path.abspath(os.path.dirname(__file__))

    with copen(os.path.join(here, 'README.rst'), encoding='utf-8') as description:
        return description.read()

def get_version():
    """ Retrieve version information from the package """
    return __import__('blih').__version__


setup(
    name=MODULE_NAME,
    version=get_version(),
    description="BLIH - Bocal Lightweight Interface for Humans",
    long_description=get_long_description(),

    url="https://github.com/bocal/blih",

    author="Emmanuel Vadot",
    author_email="elbarto@bocal.org",

    license="BSD",

    install_requires=['requests'],

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',

        'Intended Audience :: End Users/Desktop',
        'Topic :: Utilities',

        'License :: OSI Approved :: BSD License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],

    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),

    keywords="blih bocal api",

    entry_points={
        'console_scripts': [
            'blih=blih:main',
        ],
    },
)
