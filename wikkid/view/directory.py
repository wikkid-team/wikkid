#
# Copyright (C) 2010 Wikkid Developers
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""View classes to control the rendering of the content."""

from wikkid.interface.resource import IDirectoryResource
from wikkid.view.base import DirectoryBreadcrumbView
from wikkid.view.urls import canonical_url


class ListingItem(object):
    """An item to be shown in the directory listing."""

    def __init__(self, context, request, view, css_class, name=None):
        self.context = context
        self.url = canonical_url(self.context, request, view)
        if name is None:
            name = context.base_name
        self.name = name
        self.css_class = css_class


class DirectoryListingPage(DirectoryBreadcrumbView):
    """The directory listing shows the content in the directory.

    This view is shown if there is no matching wiki apge the same name as the
    directory (i.e. with '.txt' on the end).
    """

    for_interface = IDirectoryResource
    name = 'listing'
    is_default = False
    template = 'view_directory'

    def before_render(self):
        """Get the listing and split it into directories and files."""
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
                ListingItem(parent, self.request, 'listing', 'up', name='..'))
        for item in sorted(directories, key=sort_key):
            items.append(
                ListingItem(item, self.request, 'listing', 'directory'))
        for item in sorted(files, key=sort_key):
            items.append(ListingItem(item, self.request, None, 'file'))
        self.items = items

    @property
    def content(self):
        return 'Directory listing for %s' % self.path

    @property
    def title(self):
        """The title is just the directory path."""
        dir_name = self.context.get_dir_name()
        if dir_name is None:
            return 'Wiki Root'
        else:
            return dir_name
