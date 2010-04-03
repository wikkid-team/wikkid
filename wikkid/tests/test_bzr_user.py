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

"""Tests for the wikkid bzr user."""

from bzrlib.tests import TestCaseWithTransport

from wikkid.bzr.user import UserFactory
from wikkid.interfaces import IUser, IUserFactory
from wikkid.tests import ProvidesMixin


class TestBzrUser(TestCaseWithTransport, ProvidesMixin):
    """Tests for the bzr filestore and files."""

    def test_userfactory_provides_IUserFactory(self):
        tree = self.make_branch_and_tree('.')
        factory =  UserFactory(tree.branch)
        self.assertProvides(factory, IUserFactory)

    def test_user_provides_IUser(self):
        tree = self.make_branch_and_tree('.')
        factory =  UserFactory(tree.branch)
        user = factory.create(None)
        self.assertProvides(user, IUser)

    def test_user_attributes(self):
        branch = self.make_branch_and_tree('.').branch
        branch.get_config().set_user_option(
            'email', 'Test User <test@example.com>')
        user = UserFactory(branch).create(None)
        self.assertEqual(
            'Test User <test@example.com>', user.committer_id)
        self.assertEqual('Test User', user.display_name)
        self.assertEqual('test@example.com', user.email)
