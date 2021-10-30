#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""The base resource class."""

import breezy.urlutils as urlutils

from wikkid.interface.resource import IRootResource


class BaseResource(object):
    """Information about a resource."""

    def __init__(self, server, path, write_filename,
                 file_resource, dir_resource):
        self.factory = server
        self.path = path
        self.write_filename = write_filename
        self.file_resource = file_resource
        self.dir_resource = dir_resource

    @property
    def preferred_path(self):
        return self.factory.get_preferred_path(self.path)

    @property
    def base_name(self):
        return urlutils.basename(self.path)

    @property
    def dir_name(self):
        return urlutils.dirname(self.path)

    @property
    def parent(self):
        if IRootResource.providedBy(self):
            return None
        return self.factory.get_resource_at_path(self.dir_name)

    @property
    def default_resource(self):
        """Any resource should be able to get to the default resource."""
        return self.factory.get_default_resource()

    @property
    def root_resource(self):
        """Any resource should be able to get to the root resource."""
        return self.factory.get_resource_at_path('/')
