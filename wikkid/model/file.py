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

"""The model class for file resources."""

from zope.interface import implements

from wikkid.model.baseresource import BaseResource
from wikkid.interface.resource import IFileResource, IUpdatableResource


class UpdatableResource(BaseResource):
    """Reflects either a file either missing or actual."""

    implements(IUpdatableResource)

    def put_bytes(self, bytes, committer, rev_id, commit_msg):
        """Update the file resource."""
        self.server.filestore.update_file(
            self.write_filename, bytes, committer, rev_id, commit_msg)


class FileResource(UpdatableResource):
    """Anything that relates to all files."""

    implements(IFileResource)

    @property
    def mimetype(self):
        return self.file_resource.mimetype

    @property
    def last_modified_in_revision(self):
        return self.file_resource.last_modified_in_revision

    def get_bytes(self):
        return self.file_resource.get_content()
