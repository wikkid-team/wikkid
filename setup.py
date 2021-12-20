#!/usr/bin/env python3

from setuptools import setup, find_packages
from wikkid import version


setup(
    name='Wikkid',
    version=version,
    description="VCS-backed wiki",
    long_description="""\
A wiki that is backed by Gitr or Bazaar that allows local branching of the wiki
for later merging. Also doesn't have any page locks and uses three way merging.
""",
    author='Wikkid Developers',
    author_email='wikkid-dev@lists.launchpad.net',
    url='https://launchpad.net/wikkid',
    scripts=['bin/wikkid-serve'],
    data_files=[('share/man/man1', ['wikkid-serve.1']), ],
    packages=find_packages(),
    package_dir={'breezy.plugins.wikkid': 'plugin'},
    package_data={'wikkid/skin': ['default/*.html',
                                  'default/favicon.ico',
                                  'default/static/*']},
    include_package_data=True,
    install_requires=[
        'breezy',
        'docutils',
        'dulwich',
        'jinja2',
        'pygments',
        'twisted',
        'webob',
        'zope.interface',
        ],
    test_requires=[
        'bs4',
        'breezy.tests',
        'testtools',
        ],
    test_suite='wikkid.tests',
    )
