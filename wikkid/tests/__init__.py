#
# Copyright (C) 2010 Wikkid Developers
#
# This file is part of Wikkid.
#
# Wikkid is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Foobar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Wikkid.  If not, see <http://www.gnu.org/licenses/>

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
    names = [
        'server',
        'volatile_filestore',
        'bzr_filestore',
        'bzr_user',
        'rest_formatter',
        'view_dispatcher',
        'model',
        ]
    module_names = ['wikkid.tests.test_' + name for name in names]
    loader = unittest.TestLoader()
    return loader.loadTestsFromNames(module_names)
