#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""Test views for the root object."""

from webob.exc import HTTPTemporaryRedirect

from wikkid.tests.factory import ViewTestCase


class TestRootViews(ViewTestCase):
    """Test the views on the root object."""

    def test_last_modified_by(self):
        """Test that the last committer is displayed properly"""
        factory = self.make_factory()
        view = self.get_view(factory, '/')
        error = self.assertRaises(
            HTTPTemporaryRedirect,
            view.render,
            None)
        self.assertEqual('/Home', error.headers['Location'])
