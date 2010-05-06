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

from wikkid.interface.resource import IDirectoryResource, IRootResource
from wikkid.view.base import BaseView, Breadcrumb


class ListingItem(object):
    """An item to be shown in the directory listing."""

    def __init__(self, context, url, name=None):
        self.context = context
        self.url = url
        if name is None:
            name = context.base_name
        self.name = name


class DirectoryListingPage(BaseView):
    """The directory listing shows the content in the directory.

    This view is shown if there is no matching wiki apge the same name as the
    directory (i.e. with '.txt' on the end).
    """

    for_interface = IDirectoryResource
    name = 'listing'
    is_default = False
    template = 'view_directory'

    def _create_breadcrumbs(self):
        crumbs = []
        current = self.context
        while not IRootResource.providedBy(current):
            crumbs.append(Breadcrumb(
                    current, suffix='?view=listing', title=current.base_name))
            current = current.parent_dir
        # Add in the root dir.
        crumbs.append(Breadcrumb(
                current, url='/?view=listing', title='wiki root'))
        # And add in the default page.
        crumbs.append(Breadcrumb(current.default_resource))
        return reversed(crumbs)

    def before_render(self):
        """Ghet the listing and split it into directories and files."""
        directories = []
        files = []
        for item in self.context.get_listing():
            if IDirectoryResource.providedBy(item):
                directories.append(item)
            else:
                files.append(item)

        def sort_key(item):
            return item.base_name.lower()

        items = []
        # If we are looking at / don't add a parent dir.
        if self.context.path != '/':
            parent = self.context.parent
            items.append(
                ListingItem(
                    parent, '%s?view=listing' % parent.path, name='..'))
        for item in sorted(directories, key=sort_key):
            items.append(ListingItem(item, '%s?view=listing' % item.path))
        for item in sorted(files, key=sort_key):
            items.append(ListingItem(item, item.path))
        self.items = items

    @property
    def content(self):
        return 'Directory listing for %s' % self.path

    @property
    def title(self):
        """The title is just the directory path."""
        dir_name = self.context.get_dir_name()
        if dir_name is None:
            return self.context.title
        else:
            return dir_name
