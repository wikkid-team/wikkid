#
# Copyright (C) 2010 Wikkid Developers
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""View classes to control the rendering of wiki pages."""

from webob.exc import HTTPTemporaryRedirect

from wikkid.formatter.registry import get_wiki_formatter
from wikkid.interface.resource import IWikiTextFile
from wikkid.view.base import BaseView


def format_content(bytes, base_name):
    """ Format the content with the right formatter.

    Check the first line of the content to see if it specifies a
    formatter. The default is currently ReST, but we should have it
    configurable shortly.
    """
    content, formatter = get_wiki_formatter(bytes, 'rest')
    return formatter.format(base_name, content)


class WikiPage(BaseView):
    """A wiki page is a page that is going to be rendered for viewing."""

    for_interface = IWikiTextFile
    name = 'view'
    is_default = True
    template = 'view_page'

    @property
    def content(self):
        bytes = self.context.get_bytes()
        return format_content(bytes, self.context.base_name)

    def _render(self, skin):
        """If the page is not being viewed with the preferred path, redirect.

        For example, /FrontPage.txt will redirect to /FrontPage
        """
        preferred = self.context.preferred_path
        if self.context.path != preferred:
            raise HTTPTemporaryRedirect(location=preferred)
        else:
            return super(WikiPage, self)._render(skin)
