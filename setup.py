#!/usr/bin/env python

from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages
from wikkid import version


setup(
    name='Wikkid',
    version=version,
    description="A wiki that is backed by Bazaar that allows local branching of the wiki for later merging. Also doesn't have any page locks and uses Bazaar's three way merging.",
    author='Wikkid Developers',
    author_email='wikkid-dev@lists.launchpad.net',
    url='https://launchpad.net/wikkid',
    scripts=['wikkid-serve'],
    packages=find_packages(),
    package_dir={'bzrlib.plugins.wikkid':'plugin'},
    package_data={'wikkid/skin':['default/*.html',
                                 'default/favicon.ico',
                                 'default/static/*']},
    install_requires=[
        'zope.interface',
        'twisted',
        'jinja2',
        'docutils',
        'testtools',
        'beautifulsoup',
        'pygments',
        ],
    test_suite='wikkid.tests',
    )
