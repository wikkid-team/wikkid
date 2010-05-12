#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""Tests for the wikkid bzr user."""

from bzrlib.tests import TestCaseWithTransport

from wikkid.interface.user import IUser, IUserFactory
from wikkid.tests import ProvidesMixin
from wikkid.user.bzr import UserFactory


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
