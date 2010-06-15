#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""Tests the edit views."""

from wikkid.tests.factory import FactoryTestCase
from wikkid.tests.fakes import TestUser
from wikkid.view.base import canonical_url


class TestCanonicalUrl(FactoryTestCase):
    """Test the edit view."""

    def setUp(self):
        super(TestCanonicalUrl, self).setUp()
        self.user = TestUser('test@example.com', 'Test User')

    def test_root(self):
        factory = self.make_factory()
        root = factory.get_resource_at_path('/')
        self.assertEqual('/', canonical_url(root))

    def test_root_listing(self):
        factory = self.make_factory()
        root = factory.get_resource_at_path('/')
        self.assertEqual('/+listing', canonical_url(root, 'listing'))

