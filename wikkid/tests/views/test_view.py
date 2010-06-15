#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""Tests the display views."""

from wikkid.tests.factory import ViewTestCase
from wikkid.tests.fakes import TestUser


class TestView(ViewTestCase):
    """Test the display view."""

    def setUp(self):
        super(TestView, self).setUp()
        self.user = TestUser('test@example.com', 'Test User')

    def test_last_modified_by(self):
        """Test that the last committer is displayed properly"""
        factory = self.make_factory([
                ('SomePage/SubPage/Nested.txt', 'some text')])
        view = self.get_view(factory, '/SomePage/SubPage/Nested', 'view')
        user = view.last_modified_by
        self.assertEqual('First User', user.display_name)
