#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""Test views for the root object."""

from webob.exc import HTTPSeeOther

from wikkid.tests.factory import ViewTestCase


class TestRootViews(ViewTestCase):
    """Test the views on the root object."""

    def test_root_redirects(self):
        """Going to / redirects to the Home page."""
        factory = self.make_factory()
        view = self.get_view(factory, '/')
        error = self.assertRaises(
            HTTPSeeOther,
            view.render,
            None)
        self.assertEqual('/Home', error.headers['Location'])

    def test_root_redirects_with_script_name(self):
        """Redirection works and respects the script name"""
        factory = self.make_factory()
        view = self.get_view(factory, '/', base_url='/p/test')
        error = self.assertRaises(
            HTTPSeeOther,
            view.render,
            None)
        self.assertEqual('/p/test/Home', error.headers['Location'])
