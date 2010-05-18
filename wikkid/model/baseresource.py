#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""The base resource class."""

import bzrlib.urlutils as urlutils

from wikkid.interface.resource import IRootResource


class BaseResource(object):
    """Information about a resource."""

    def __init__(self, server, path, write_filename,
                 file_resource, dir_resource):
        self.server = server
        self.path = path
        self.write_filename = write_filename
        self.file_resource = file_resource
        self.dir_resource = dir_resource

    @property
    def preferred_path(self):
        return self.server.get_preferred_path(self.path)

    @property
    def base_name(self):
        return urlutils.basename(self.path)

    @property
    def dir_name(self):
        return urlutils.dirname(self.path)

    @property
    def parent(self):
        return self.server.get_parent_info(self)

    @property
    def parent_dir(self):
        """Return the directory containing this resource."""
        if IRootResource.providedBy(self):
            return None
        return self.server.get_resource_at_path(self.dir_name)