#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""Tests for the wikkid bzr user."""

from breezy.tests import TestCaseWithTransport
from webob import Request, Response

from wikkid.interface.user import IUser
from wikkid.tests import ProvidesMixin
from wikkid.user.bzr import LocalBazaarUserMiddleware


class TestLocalUserMiddleware(TestCaseWithTransport, ProvidesMixin):

    def setUp(self):
        super(TestLocalUserMiddleware, self).setUp()
        self.user = None

    def app_func(self, environment, start_response):
        self.user = environment['wikkid.user']
        return Response('done')(environment, start_response)

    def test_user_is_set(self):
        branch = self.make_branch_and_tree('.').branch
        req = Request.blank('/')
        app = LocalBazaarUserMiddleware(self.app_func, branch)
        req.get_response(app)
        self.assertIsNot(None, self.user)
        self.assertProvides(self.user, IUser)

    def test_user_attributes(self):
        branch = self.make_branch_and_tree('.').branch
        branch.get_config().set_user_option(
            'email', 'Test User <test@example.com>')
        req = Request.blank('/')
        app = LocalBazaarUserMiddleware(self.app_func, branch)
        req.get_response(app)
        self.assertEqual(
            'Test User <test@example.com>', self.user.committer_id)
        self.assertEqual('Test User', self.user.display_name)
        self.assertEqual('test@example.com', self.user.email)
