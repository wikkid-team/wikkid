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

"""View classes to control the rendering of the content."""

from wikkid.formatter.rest import RestructuredTextFormatter
from wikkid.interface.resource import (
    IDirectoryResource,
    IMissingResource,
    ISourceTextFile,
    ITextFile,
    IWikiTextFile,
    )
from wikkid.view.base import BaseView


class MissingPage(BaseView):
    """A wiki page that does not exist."""

    for_interface = IMissingResource
    name = 'view'
    is_default = True
    template = 'missing'

    @property
    def content(self):
        '%s Not found' % self.path


class WikiPage(BaseView):
    """A wiki page is a page that is going to be rendered for viewing."""

    for_interface = IWikiTextFile
    name = 'view'
    is_default = True
    template = 'view_page'

    @property
    def content(self):
        # Format the content.  Right not this is hard coded to ReST, although
        # I want to offer multiple ways to do this.
        formatter = RestructuredTextFormatter()
        return formatter.format(self.resource.text)


class OtherTextPage(BaseView):
    """Any other non-binary file is considered other text.

    Will be rendered using pygments.
    """

    for_interface = ISourceTextFile
    name = 'view'
    is_default = True
    template = 'view_page'

    @property
    def content(self):
        return self.resource.text


class EditWikiPage(BaseView):
    """The page shows the wiki content in a large edit field."""

    for_interface = ITextFile
    name = 'edit'
    template = 'edit_page'

    @property
    def rev_id(self):
        if self.resource is None:
            return None
        else:
            return self.resource.last_modified_in_revision

    @property
    def content(self):
        if self.resource is None:
            return ''
        else:
            return self.resource.get_content()


class ConflictedEditWikiPage(BaseView):
    """The page shows the wiki content in a large edit field."""

    for_interface = ITextFile
    name = 'conflicted'
    template = 'edit_page'

    def __init__(self, skin, resource, path, user, conflict_text,
                 rev_id):
        BaseView.__init__(self, skin, resource, path, user)
        self.content = conflict_text
        self.rev_id = rev_id


class DirectoryListingPage(BaseView):
    """The directory listing shows the content in the directory.

    This view is shown if there is no matching wiki apge the same name as the
    directory (i.e. with '.txt' on the end).
    """

    for_interface = IDirectoryResource
    name = 'view'
    is_default = True
    # template = 'view_directory'
    template = 'view_page'

    @property
    def content(self):
        return 'Directory listing for %s' % self.path
