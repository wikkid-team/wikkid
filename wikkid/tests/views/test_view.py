#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""Tests the display views."""

from wikkid.dispatcher import get_view
from wikkid.tests.factory import FactoryTestCase
from wikkid.tests.fakes import TestRequest, TestUser

#XXX: This test fails, it seems to not actually commit, may need more faking
class DisabledTestView(FactoryTestCase):
    """Test the display view."""

    def setUp(self):
        super(TestView, self).setUp()
        self.user = TestUser('test@example.com', 'Test User')
        self.request = TestRequest()

    def test_last_modified_by(self):
        """Test that the last committer is displayed properly"""
        factory = self.make_factory([
                ('SomePage/SubPage/Nested.txt', 'some text')])
        info = factory.get_resource_at_path('/SomePage/SubPage/Nested.txt')
        view = get_view(info, 'view', self.request, self.user)
        self.assertEqual('Test User', view.last_modified_by)

