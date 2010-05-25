#!/usr/bin/env python

from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages


setup(
    name='Wikkid',
    version='0.1',
    description="A wiki that is backed by Bazaar that allows local branching of the wiki for later merging. Also doesn't have any page locks and uses Bazaar's three way merging.",
    author='Wikkid Committers',
    author_email='wikkid-dev@lists.launchpad.net',
    url='https://launchpad.net/wikkid',
    scripts=['wikkid-serve'],
    packages=find_packages(),
    package_dir={'bzrlib.plugins.wikkid':'plugin'},
    package_data={'wikkid/skin':['default/*.html',
                                 'default/favicon.ico',
                                 'default/static/*']},
    test_suite='wikkid.tests',
    )
