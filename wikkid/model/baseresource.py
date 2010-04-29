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

"""The base resource class."""

import bzrlib.urlutils as urlutils


class BaseResource(object):
    """Information about a resource."""

    def __init__(self, server, path, title, write_filename,
                 file_resource, dir_resource):
        self.server = server
        self.path = path
        self.title = title
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
    def parent(self):
        return self.server.get_parent_info(self)
