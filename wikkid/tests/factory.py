#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""A base test case for factory tests."""

from webob import Request

from wikkid.dispatcher import get_view
from wikkid.model.factory import ResourceFactory
from wikkid.filestore.volatile import FileStore
from wikkid.tests import TestCase


class FactoryTestCase(TestCase):
    """A test case that can make a factory."""

    def make_factory(self, content=None):
        """Make a factory with a volatile filestore."""
        filestore = FileStore(content)
        return ResourceFactory(filestore)


class ViewTestCase(FactoryTestCase):
    """A factory test case that can create views."""

    def get_view(self, factory, path, name=None, base_url=None):
        info = factory.get_resource_at_path(path)
        request = Request.blank(path, base_url=base_url)
        return get_view(info, name, request)
