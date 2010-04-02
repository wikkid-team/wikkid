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

from wikkid.formatter.rest import RestructuredTextFormatter
from wikkid.views.base import BaseView


class MissingPage(BaseView):
    """A wiki page that does not exist."""

    template = 'missing'

    @property
    def content(self):
        '%s Not found' % self.path


class WikiPage(BaseView):
    """A wiki page is a page that is going to be rendered for viewing."""

    template = 'view_page'

    @property
    def content(self):
        # Format the content.  Right not this is hard coded to ReST, although
        # I want to offer multiple ways to do this.
        formatter = RestructuredTextFormatter()
        return formatter.format(self.resource.get_content())


class OtherTextPage(BaseView):
    """Any other non-binary file is considered other text.

    Will be rendered using pygments.
    """

    template = 'view_page'

    @property
    def content(self):
        return self.resource.get_content()


class EditWikiPage(BaseView):
    """The page shows the wiki content in a large edit field."""

    template = 'edit_page'

    @property
    def rev_id(self):
        if self.resource is None:
            return None
        else:
            return self.resource.last_modified_in_revision

    @property
    def content(self):
        if self.resouce is None:
            return ''
        else:
            return self.resource.get_content()


class DirectoryListingPage(BaseView):
    """The directory listing shows the content in the directory.

    This view is shown if there is no matching wiki apge the same name as the
    directory (i.e. with '.txt' on the end).
    """

    # template = 'view_directory'
    template = 'view_page'

    @property
    def content(self):
        return 'Directory listing for %s' % self.path
