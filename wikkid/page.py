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

"""Classes to control the rendering of the content.

Just by the current feel of what is going in here, I feel that I may well end
up making a 'wikkid.views' package and move the classes in there, as that is
effectively what this is going to be.
"""

import logging

from wikkid.interfaces import FileType


class Page(object):
    """A page is found at a particular location.

    A page may refer to an existing file, or it may render the "couldn't find
    the page you asked for" page.  The page may be a wiki page to render, or
    the page may be an image (ick - change this soon).
    """

    def __init__(self, skin, resource_info):
        self.skin = skin
        self.resource = resource_info.resource
        self.file_type = resource_info.file_type
        self.path = resource_info.path
        self.logger = logging.getLogger('wikkid')

    def render(self):
        """Render the page.

        Return a tuple of content type and content.
        """
        if self.file_type == FileType.BINARY_FILE:
            return self.resource.mimetype, self.resource.get_content()
        elif self.file_type == FileType.MISSING:
            return ('text/plain', '%s Not found' % self.path)
        elif self.file_type == FileType.DIRECTORY:
            return ('text/plain', 'Directory listing for %s' % self.path)
        else:
            rendered = self.skin.page_template.render(
                title=self.path,
                content=self.resource.get_content())
            return ('text/html', rendered)


class WikiPage(Page):
    """A wiki page is a page that is going to be rendered for viewing."""

    template = 'view_page'


class EditWikiPage(Page):
    """The page shows the wiki content in a large edit field."""

    template = 'edit_page'


class DirectoryListingPage(Page):
    """The directory listing shows the content in the directory.

    This view is shown if there is no matching wiki apge the same name as the
    directory (i.e. with '.txt' on the end).
    """

    template = 'view_directory'


class BinaryFile(Page):
    """Renders a binary file with its mimetype."""

