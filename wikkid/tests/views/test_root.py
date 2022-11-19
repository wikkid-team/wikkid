#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""Test views for the root object."""

from bs4 import BeautifulSoup
from testtools.matchers import Equals
from webob.exc import HTTPSeeOther

from wikkid.skin.loader import Skin
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

    def test_home_rendering(self):
        """Render the home page and test the elements."""
        factory = self.make_factory()
        view = self.get_view(factory, '/Home')
        content = view.render(Skin('default'))
        soup = BeautifulSoup(content.text, features="lxml")
        [style] = soup.find_all('link', {'rel': 'stylesheet'})
        self.assertThat(style['href'], Equals('/static/default.css'))

    def test_home_rendering_with_script_name(self):
        """Render the home page and test the elements."""
        factory = self.make_factory()
        view = self.get_view(factory, '/Home', base_url='/p/test')
        content = view.render(Skin('default'))
        soup = BeautifulSoup(content.text, features="lxml")
        [style] = soup.find_all('link', {'rel': 'stylesheet'})
        self.assertThat(style['href'], Equals('/p/test/static/default.css'))
