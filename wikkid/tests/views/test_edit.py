#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""Tests the edit views."""

from wikkid.tests.factory import ViewTestCase
from wikkid.tests.fakes import TestUser


class TestEdit(ViewTestCase):
    """Test the edit view."""

    def setUp(self):
        super(TestEdit, self).setUp()
        self.user = TestUser('test@example.com', 'Test User')

    def test_title_nested(self):
        """Test that a nested page returns the expected title"""
        factory = self.make_factory([
                ('SomePage/SubPage/Nested.txt', 'some text')])
        view = self.get_view(factory, '/SomePage/SubPage', 'edit')
        self.assertEqual('Editing "Sub Page"', view.title)

    def test_urls(self):
        """Check the urls for saving and cancel."""
        factory = self.make_factory()
        view = self.get_view(factory, '/NewPage', 'edit')
        self.assertEqual('/NewPage', view.cancel_url)
        self.assertEqual('/NewPage/+save', view.save_url)
