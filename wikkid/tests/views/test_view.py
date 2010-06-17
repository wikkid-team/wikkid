#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""Tests the display views."""

from wikkid.tests.factory import ViewTestCase


class TestView(ViewTestCase):
    """Test the display view."""

    def test_wiki_last_modified_by(self):
        """Test that the last committer is displayed properly"""
        factory = self.make_factory([
                ('SomePage/SubPage/Nested.txt', 'some text')])
        view = self.get_view(factory, '/SomePage/SubPage/Nested', 'view')
        user = view.last_modified_by
        self.assertEqual('First User', user.display_name)

    def test_other_last_modified_by(self):
        """Test that the last committer is displayed properly"""
        factory = self.make_factory([
                ('test.py', 'some text')])
        view = self.get_view(factory, '/test.py')
        user = view.last_modified_by
        self.assertEqual('First User', user.display_name)
