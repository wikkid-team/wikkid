#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""Tests the edit views."""

from wikkid.dispatcher import get_view
from wikkid.tests.factory import FactoryTestCase
from wikkid.tests.fakes import TestRequest, TestUser


class TestEdit(FactoryTestCase):
    """Test the edit view."""

    def setUp(self):
        super(TestEdit, self).setUp()
        self.user = TestUser('test@example.com', 'Test User')
        self.request = TestRequest()

    def test_title_nexted(self):
        """Test that a nested page returns the expected title"""
        factory = self.make_factory([
                ('SomePage/SubPage/Nested.txt', 'some text')])
        info = factory.get_resource_at_path('/SomePage/SubPage')
        view = get_view(info, 'edit', self.request, self.user)
        self.assertEqual('Editing "Sub Page"', view.title)

