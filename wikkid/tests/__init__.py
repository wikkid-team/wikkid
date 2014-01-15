#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""The wikkid tests and test only code."""

import unittest

import testtools
from zope.interface.verify import verifyObject


class ProvidesMixin(object):

    def assertProvides(self, obj, interface):
        """Assert 'obj' correctly provides 'interface'."""
        self.assertTrue(
            interface.providedBy(obj),
            "%r does not provide %r." % (obj, interface))
        self.assertTrue(
            verifyObject(interface, obj),
            "%r claims to provide %r but does not do so correctly."
            % (obj, interface))


class TestCase(testtools.TestCase, ProvidesMixin):
    """Add some zope interface helpers."""


def test_suite():
    packages = [
        'formatters',
        'views',
        ]
    names = [
        'app',
        'context',
        'model_factory',
        'volatile_filestore',
        'bzr_filestore',
        'bzr_user',
        'git_filestore',
        'view_dispatcher',
        'model',
        ]
    module_names = ['wikkid.tests.test_' + name for name in names]
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromNames(module_names)
    for pkgname in packages:
        pkg = __import__(
            'wikkid.tests.' + pkgname, globals(), locals(), ['test_suite'])
        suite.addTests(pkg.test_suite())
    return suite
