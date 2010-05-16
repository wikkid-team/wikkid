#
# Copyright (C) 2010 Wikkid Developers
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""View classes to control the rendering of wiki pages."""

from twisted.web.util import redirectTo

from wikkid.formatter.registry import get_wiki_formatter
from wikkid.interface.resource import IWikiTextFile
from wikkid.view.base import BaseView


class WikiPage(BaseView):
    """A wiki page is a page that is going to be rendered for viewing."""

    for_interface = IWikiTextFile
    name = 'view'
    is_default = True
    template = 'view_page'

    @property
    def content(self):
        bytes = self.context.get_bytes()
        # Check the first line of the content to see if it specifies a
        # formatter. The default is currently ReST, but we should have it
        # configurable shortly.
        content, formatter = get_wiki_formatter(bytes, 'rest')
        return formatter.format(self.context.base_name, content)

    def _render(self, skin):
        """If the page is not being viewed with the preferred path, redirect.

        For example, /FrontPage.txt will redirect to /FrontPage
        """
        preferred = self.context.preferred_path
        if self.context.path != preferred:
            return redirectTo(preferred, self.request)
        else:
            return super(WikiPage, self)._render(skin)


class ConflictedEditWikiPage(BaseView):
    """The page shows the wiki content in a large edit field."""

    for_interface = ITextFile
    name = 'conflicted'
    template = 'edit_page'

    # TODO: fix this too...

    def __init__(self, skin, resource, path, user, conflict_text,
                 rev_id):
        BaseView.__init__(self, skin, resource, path, user)
        self.content = conflict_text
        self.rev_id = rev_id
