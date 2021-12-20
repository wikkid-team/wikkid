#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""The root resource class.

The root resource represents the object at the root of the wiki path.

Currently this just refers to '/', but it is expected that at some stage in
the not too distant future the server will support a wiki root where it is not
the root path.
"""

from zope.interface import implementer

from wikkid.model.directory import DirectoryResource
from wikkid.interface.resource import IRootResource


@implementer(IRootResource)
class RootResource(DirectoryResource):
    """The root of the wiki.

    Some special wiki views hang off the root resource and not others.  A root
    resource is also a directory resource where the directory is the root of
    the filesystem.
    """

    def get_dir_name(self):
        return None

    @property
    def has_home_page(self):
        return self.file_resource is not None

    def __repr__(self):
        return "<RootResource '/'>"

    @property
    def preferred_path(self):
        return '/'
