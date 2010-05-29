#!/usr/bin/env python

from distutils.core import setup
from wikkid import version

setup(name='Wikkid',
      version=version,
      description="A wiki that is backed by Bazaar that allows local branching of the wiki for later merging. Also doesn't have any page locks and uses Bazaar's three way merging.",
      author='Wikkid Developers',
      author_email='wikkid-dev@lists.launchpad.net',
      url='https://launchpad.net/wikkid',
      scripts=['bin/wikkid-serve'],
      packages=['wikkid',
      'wikkid/interface',
      'wikkid/contrib',
      'wikkid/contrib/creole_1_1',
      'wikkid/model',
      'wikkid/user',
      'wikkid/tests',
      'wikkid/tests/views',
      'wikkid/tests/formatters',
      'wikkid/view',
      'wikkid/filestore',
      'wikkid/skin',
      'wikkid/formatter',
      'bzrlib.plugins.wikkid'],
      package_dir={'bzrlib.plugins.wikkid':'plugin'},
      package_data={'wikkid/skin':['default/*.html',
                                   'default/favicon.ico',
                                   'default/static/*']},
     )
