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

"""A base test case for factory tests."""

from wikkid.model.factory import ResourceFactory
from wikkid.filestore.volatile import FileStore
from wikkid.tests import TestCase


class FactoryTestCase(TestCase):

    def make_factory(self, content=None):
        """Make a factory with a volatile filestore."""
        filestore = FileStore(content)
        return ResourceFactory(filestore)
