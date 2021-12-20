# -*- coding: utf-8 -*-
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


def format_content(bytes, base_name, default_format):
    """ Format the content with the right formatter.

    Check the first line of the content to see if it specifies a
    formatter. The default is currently ReST, but we should have it
    configurable shortly.
    """
    content, formatter = get_wiki_formatter(bytes, default_format)
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
        try:
            text = bytes.decode('utf-8')
        except UnicodeDecodeError:
            try:
                text = bytes.decode('latin-1')
            except UnicodeDecodeError:
                text = bytes.decode('ascii', 'replace')

        default_format = self.execution_context.default_format
        return format_content(text, self.context.base_name, default_format)

    def _render(self, skin):
        """If the page is not being viewed with the preferred path, redirect.

        For example, /FrontPage.txt will redirect to /FrontPage
        """
        preferred = self.context.preferred_path
        if self.context.path != preferred:
            location = self.canonical_url(self.context)
            raise HTTPTemporaryRedirect(location=location)
        else:
            return super(WikiPage, self)._render(skin)
