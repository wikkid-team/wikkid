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

from wikkid.interface.resource import IDirectoryResource
from wikkid.view.base import BaseView


class DirectoryListingPage(BaseView):
    """The directory listing shows the content in the directory.

    This view is shown if there is no matching wiki apge the same name as the
    directory (i.e. with '.txt' on the end).
    """

    for_interface = IDirectoryResource
    name = 'listing'
    is_default = True
    # template = 'view_directory'
    template = 'view_page'

    @property
    def content(self):
        return 'Directory listing for %s' % self.path
